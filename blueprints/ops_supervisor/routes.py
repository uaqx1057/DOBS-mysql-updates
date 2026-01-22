from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from flask_login import login_required, current_user
from models import Driver, User, BusinessDriver, Business, BusinessID, Offboarding, DriverBusinessIDS
from extensions import db, mail, limiter
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from utils.email_utils import send_password_change_email
from sqlalchemy import func
from flask_wtf.csrf import validate_csrf, CSRFError
from forms.common import CSRFOnlyForm, ChangePasswordForm, OpsSupervisorApproveForm

ops_supervisor_bp = Blueprint("ops_supervisor", __name__)


def _validate_csrf():
    """Validate CSRF token from form or X-CSRFToken header."""
    header_token = request.headers.get("X-CSRFToken")
    if header_token:
        try:
            validate_csrf(header_token)
            return True
        except CSRFError as exc:
            current_app.logger.warning("[OPS_SUPERVISOR] Header CSRF failed: %s", exc)
            return False

    form = CSRFOnlyForm()
    return form.validate_on_submit()


# -------------------------
# Dashboard
# -------------------------
@ops_supervisor_bp.route("/dashboard")
@login_required
def dashboard_ops_supervisor():
    if current_user.role != "OpsSupervisor":
        flash("Access denied", "danger")
        return redirect(url_for("auth.login"))

    onboarding_drivers = Driver.query.filter_by(onboarding_stage="Ops Supervisor").all()

    # Latest offboarding requests
    latest_requests_subq = (
        db.session.query(
            Offboarding.driver_id,
            func.max(Offboarding.requested_at).label("latest_request")
        )
        .filter(Offboarding.status.in_(["Requested", "OpsSupervisor"]))
        .group_by(Offboarding.driver_id)
        .subquery()
    )

    offboarding_requests = (
        db.session.query(Offboarding)
        .join(
            latest_requests_subq,
            (Offboarding.driver_id == latest_requests_subq.c.driver_id) &
            (Offboarding.requested_at == latest_requests_subq.c.latest_request)
        )
        .order_by(Offboarding.requested_at.desc())
        .all()
    )

    total_drivers = len(onboarding_drivers)
    total_offboardings = len(offboarding_requests)

    lang = session.get("lang", "en")
    template = "rtl_dashboard_ops_supervisor.html" if lang == "ar" else "dashboard_ops_supervisor.html"

    # Prepare all businesses + only active & unassigned IDs
    businesses = Business.query.order_by(Business.name).all()
    all_businesses = []

    # Get all assigned business IDs
    assigned_ids_subq = db.session.query(BusinessDriver.business_id).subquery()

    for b in businesses:
        available_ids = (
            db.session.query(BusinessID)
            .filter(
                BusinessID.business_id == b.id,
                BusinessID.is_active == True,
                ~BusinessID.id.in_(assigned_ids_subq)
            )
            .all()
        )
        available_ids_list = [{"id": bid.id, "value": bid.value} for bid in available_ids]

        all_businesses.append({
            "id": b.id,
            "name": b.name,
            "available_ids": available_ids_list
        })

    return render_template(
        template,
        total_drivers=total_drivers,
        total_offboardings=total_offboardings,
        onboarding_drivers=onboarding_drivers,
        offboarding_requests=offboarding_requests,
        all_businesses=all_businesses,
        bool=bool
    )



# -------------------------
# Approve Driver (POST only)
# -------------------------
@ops_supervisor_bp.route("/approve_driver/<int:driver_id>", methods=["POST"])
@limiter.limit("30 per minute")
@login_required
def approve_driver(driver_id):
    if current_user.role != "OpsSupervisor":
        flash("Access denied. Ops Supervisor role required.", "danger")
        return redirect(url_for("auth.login"))

    form = OpsSupervisorApproveForm()
    if not form.validate_on_submit():
        flash("Invalid or missing CSRF token. Please try again.", "danger")
        return redirect(url_for("ops_supervisor.dashboard_ops_supervisor"))

    driver = Driver.query.get_or_404(driver_id)
    current_app.logger.info(f"[OPS_SUPERVISOR][START] driver_id={driver_id} form={dict(request.form)}")

    platform_ids = [pid for pid in (form.platform_ids_csv.data or "").split(",") if pid]
    issued_mobile_number = (form.issued_mobile_number.data or "").strip() or None
    issued_device_id = (form.issued_device_id.data or "").strip() or None
    mobile_issued = bool(form.mobile_issued.data)

    if not platform_ids:
        flash("Please choose at least one business ID.", "danger")
        return redirect(url_for("ops_supervisor.dashboard_ops_supervisor"))

    try:
        # -------------------------
        # Update DriverBusinessIDS (history table)
        # -------------------------
        old_links = DriverBusinessIDS.query.filter_by(driver_id=driver.id, transferred_at=None).all()
        for old in old_links:
            old.transferred_at = datetime.utcnow()

        # Insert new DriverBusinessIDS records
        for bid in platform_ids:
            new_link = DriverBusinessIDS(
                driver_id=driver.id,
                business_id_id=int(bid),  # FK to BusinessID
                previous_driver_id=None,
                assigned_at=datetime.utcnow(),
                transferred_at=None
            )
            db.session.add(new_link)

            # -------------------------
            # Update BusinessDriver table (simple link)
            # -------------------------
            business_driver = BusinessDriver(
                driver_id=driver.id,
                business_id=int(bid)
            )
            db.session.add(business_driver)

        # -------------------------
        # Update driver info
        # -------------------------
        driver.issued_mobile_number = issued_mobile_number
        driver.issued_device_id = issued_device_id
        driver.mobile_issued = mobile_issued
        driver.ops_supervisor_approved_at = datetime.utcnow()
        driver.onboarding_stage = "Fleet Manager"

        db.session.commit()
        current_app.logger.info(f"[OPS_SUPERVISOR][SAVED] driver_id={driver.id} assigned_ids={platform_ids}")
        flash(f"✅ Driver {driver.name} processed and sent to Fleet Manager.", "success")

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("[OPS_SUPERVISOR][ERROR] saving driver:")
        flash(f"❌ Error saving driver data: {str(e)}", "danger")
        return redirect(url_for("ops_supervisor.dashboard_ops_supervisor"))

    # -------------------------
    # Notify Fleet Managers
    # -------------------------
    try:
        fleet_users = User.query.filter_by(role="FleetManager").all()
        recipients = [u.email for u in fleet_users if u.email]
        if recipients:
            msg = Message(
                subject=f"Driver Ready for Fleet Assignment | السائق جاهز لمرحلة الأسطول: {driver.name}",
                recipients=recipients
            )

            msg.html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">

                    <!-- English -->
                    <div style="text-align: left;">
                        <h2 style="color: #713183;">Driver Ready for Fleet Assignment</h2>
                        <p>Hello Fleet Team,</p>
                        <p>Driver <strong>{driver.name}</strong> has been processed by the Ops Supervisor and is ready for Fleet stage processing.</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Assigned Business IDs</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{', '.join(platform_ids)}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Issued Mobile</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.issued_mobile_number or 'N/A'}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Issued Device</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.issued_device_id or 'N/A'}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Mobile & SIM Issued</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{'✅ Yes' if mobile_issued else '❌ No'}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Approved At (UTC)</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.ops_supervisor_approved_at.strftime('%Y-%m-%d %H:%M')}</td>
                            </tr>
                        </table>
                        <p>Please assign a vehicle and complete the Fleet stage processing.</p>
                        <p>Login to your dashboard: <a href="https://dobs.dobs.cloud/login" target="_blank">https://dobs.dobs.cloud/login</a></p>
                    </div>

                    <hr style="margin: 30px 0;">

                    <!-- Arabic -->
                    <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                        <h2 style="color: #713183;">السائق جاهز لمرحلة الأسطول</h2>
                        <p>السادة فريق الأسطول،</p>
                        <p>تمت معالجة السائق <strong>{driver.name}</strong> من قبل مشرف العمليات وهو جاهز لمتابعة إجراءات مرحلة الأسطول.</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">أرقام الأعمال المخصصة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{', '.join(platform_ids)}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">الهاتف الصادر</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.issued_mobile_number or 'N/A'}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">الجهاز الصادر</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.issued_device_id or 'N/A'}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">الهاتف والـ SIM صادر</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{'✅ نعم' if mobile_issued else '❌ لا'}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">تاريخ الموافقة (UTC)</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.ops_supervisor_approved_at.strftime('%Y-%m-%d %H:%M')}</td>
                            </tr>
                        </table>
                        <p>يرجى تخصيص المركبة واستكمال إجراءات مرحلة الأسطول.</p>
                        <p>تسجيل الدخول إلى لوحة القيادة: <a href="https://dobs.dobs.cloud/login" target="_blank">https://dobs.dobs.cloud/login</a></p>
                    </div>

                </div>
            </body>
            </html>
            """
            mail.send(msg)

    except Exception as e:
        current_app.logger.warning("[OPS_SUPERVISOR] fleet email error: %s", e)

    return redirect(url_for("ops_supervisor.dashboard_ops_supervisor"))

# -------------------------
# Change Password
# -------------------------
@ops_supervisor_bp.route("/change_password", methods=["POST"])
@limiter.limit("5 per minute")
@login_required
def change_password():
    if current_user.role != "OpsSupervisor":
        flash("Access denied. Ops Supervisor role required.", "danger")
        return redirect(url_for("auth.login"))

    form = ChangePasswordForm()
    if not form.validate_on_submit():
        flash("Invalid or missing CSRF token. Please try again.", "danger")
        return redirect(url_for("ops_supervisor.dashboard_ops_supervisor"))

    new_password = form.new_password.data
    confirm_password = form.confirm_password.data

    if not check_password_hash(current_user.password, form.current_password.data):
        flash("❌ Current password is incorrect.", "danger")
        return redirect(url_for("ops_supervisor.dashboard_ops_supervisor"))

    if new_password != confirm_password:
        flash("❌ New passwords do not match.", "danger")
        return redirect(url_for("ops_supervisor.dashboard_ops_supervisor"))

    try:
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        if send_password_change_email(current_user, new_password):
            flash("✅ Password updated and email notification sent.", "success")
        else:
            flash("✅ Password updated, but email could not be sent.", "warning")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"[OPS_SUPERVISOR] Password update failed: {e}")
        flash("❌ Could not update password. Please try again.", "danger")

    return redirect(url_for("ops_supervisor.dashboard_ops_supervisor"))


# -------------------------
# Offboarding Dashboard
# -------------------------
@ops_supervisor_bp.route("/offboarding")
@login_required
def offboarding_dashboard():
    if current_user.role != "OpsSupervisor":
        flash("Access denied", "danger")
        return redirect(url_for("auth.login"))

    latest_requests_subq = (
        db.session.query(
            Offboarding.driver_id,
            func.max(Offboarding.requested_at).label("latest_request")
        )
        .filter(Offboarding.status.in_(["Requested", "OpsSupervisor"]))
        .group_by(Offboarding.driver_id)
        .subquery()
    )

    offboarding_requests = (
        db.session.query(Offboarding)
        .join(
            latest_requests_subq,
            (Offboarding.driver_id == latest_requests_subq.c.driver_id) &
            (Offboarding.requested_at == latest_requests_subq.c.latest_request)
        )
        .order_by(Offboarding.requested_at.desc())
        .all()
    )

    return render_template("dashboard_ops_supervisor.html", offboarding_requests=offboarding_requests)


# -------------------------
# Handle Ops Supervisor Clearance (API)
# -------------------------
# -------------------------
# Handle Ops Supervisor Clearance (API)
# -------------------------
@ops_supervisor_bp.route("/api/clear_offboarding/<int:offboarding_id>", methods=["POST"])
@login_required
def api_clear_offboarding(offboarding_id):
    if current_user.role != "OpsSupervisor":
        return {"success": False, "message": "Access denied"}, 403

    if not _validate_csrf():
        return {"success": False, "message": "Invalid CSRF token"}, 400

    record = Offboarding.query.get_or_404(offboarding_id)

    try:
        data = request.get_json(force=True)

        # Mark offboarding as cleared
        record.ops_supervisor_cleared = True
        record.ops_supervisor_cleared_at = datetime.utcnow()
        record.company_mobile_returned = bool(data.get("company_mobile_returned"))
        record.company_sim_returned = bool(data.get("company_sim_returned"))
        record.platform_returned = bool(data.get("platform_returned"))
        record.ops_supervisor_note = data.get("ops_supervisor_note", "")
        record.ops_supervisor_id = current_user.id
        record.status = "Fleet"

        # -------------------------
        # Update driver_business_ids to mark IDs as transferred
        # -------------------------
        driver_ids_links = DriverBusinessIDS.query.filter_by(
            driver_id=record.driver_id,
            transferred_at=None
        ).all()
        for link in driver_ids_links:
            link.transferred_at = datetime.utcnow()

        db.session.commit()

        # Notify Fleet Managers
        try:
            fleet_managers = User.query.filter_by(role="FleetManager").all()
            emails = [u.email for u in fleet_managers if u.email]
            if emails:
                msg = Message(
                    subject=f"Driver Offboarding Ready for Fleet Clearance | السائق جاهز لإجراءات الأسطول: {record.driver.name}",
                    recipients=emails
                )
                msg.html = f"""
                <html>
                <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">

                        <!-- English -->
                        <div style="text-align: left;">
                            <h2 style="color: #713183;">Driver Offboarding Ready for Fleet Clearance</h2>
                            <p>Dear Fleet Manager,</p>
                            <p>Driver <strong>{record.driver.name}</strong> has been cleared by the Ops Supervisor and is ready for Fleet clearance processing.</p>
                            <p>Please log in to your dashboard to continue processing: <a href="https://dobs.dobs.cloud/login" target="_blank">https://dobs.dobs.cloud/login</a></p>
                        </div>

                        <hr style="margin: 30px 0;">

                        <!-- Arabic -->
                        <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                            <h2 style="color: #713183;">السائق جاهز لإجراءات الأسطول</h2>
                            <p>السادة مديرو الأسطول،</p>
                            <p>تمت الموافقة على السائق <strong>{record.driver.name}</strong> من قبل مشرف العمليات وهو جاهز لإجراءات مرحلة الأسطول.</p>
                            <p>يرجى تسجيل الدخول إلى لوحة القيادة لمتابعة الإجراءات: <a href="https://dobs.dobs.cloud/login" target="_blank">https://dobs.dobs.cloud/login</a></p>
                        </div>

                    </div>
                </body>
                </html>
                """
                mail.send(msg)

        except Exception as e:
            current_app.logger.warning("[OPS_SUPERVISOR] Fleet email error: %s", e)

        return {
            "success": True,
            "driver_name": record.driver.name,
            "cleared_at": record.ops_supervisor_cleared_at.strftime("%Y-%m-%d %H:%M"),
            "status": record.status
        }

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("[OPS_SUPERVISOR][API CLEAR ERROR]")
        return {"success": False, "message": str(e)}, 500
