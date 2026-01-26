from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, session
from flask_login import login_required, current_user
from extensions import db, mail
from extensions import db, mail, limiter
from flask_mail import Message
from datetime import datetime, date
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import joinedload
from models import Offboarding, Driver, User, Vehicle, AssignDriver, AssignDriverReport
from utils.email_utils import send_password_change_email
import os
from flask_wtf.csrf import validate_csrf, CSRFError
from forms.common import CSRFOnlyForm, ChangePasswordForm, FleetAssignForm, FleetOffboardingForm

fleet_bp = Blueprint("fleet", __name__)


def _validate_csrf():
    """Validate CSRF token from form or X-CSRFToken header."""
    header_token = request.headers.get("X-CSRFToken")
    if header_token:
        try:
            validate_csrf(header_token)
            return True
        except CSRFError as exc:
            current_app.logger.warning("[FLEET] Header CSRF failed: %s", exc)
            return False

    form = CSRFOnlyForm()
    return form.validate_on_submit()

# -------------------------
# Fleet Manager Dashboard
# -------------------------
@fleet_bp.route("/dashboard")
@login_required
def dashboard_fleet():
    if current_user.role != "FleetManager":
        flash("Access denied", "danger")
        return redirect(url_for("auth.login"))

    total_drivers = Driver.query.filter_by(onboarding_stage="Fleet Manager").count()
    offboarding_fleet = Offboarding.query.filter_by(status="Fleet").count()
    offboarding_pending_tamm = Offboarding.query.filter_by(status="pending_tamm").count()

    onboarding_drivers = (
        Driver.query
        #.options(joinedload(Driver.platforms))
        .filter_by(onboarding_stage="Fleet Manager")
        .all()
    )

    # Latest offboarding per driver
    latest_requests_subq = (
        db.session.query(
            Offboarding.driver_id,
            db.func.max(Offboarding.requested_at).label("latest_request")
        )
        .filter(Offboarding.status.in_(["Fleet",  "FinanceManager"]))
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
        .options(joinedload(Offboarding.driver))
        .order_by(Offboarding.requested_at.desc())
        .all()
    )

    # Available vehicles (not assigned and marked available)
    assigned_vehicle_ids = (
        db.session.query(AssignDriver.vehicle_id)
        .filter(AssignDriver.status == "active")
        .subquery()
    )

    available_vehicles = (
        Vehicle.query
        .filter(
            Vehicle.status == "available",
            ~Vehicle.id.in_(assigned_vehicle_ids.select())
        )
        .order_by(Vehicle.registration_number)
        .all()
    )

    lang = session.get("lang", "en")
    template = "rtl_dashboard_fleet.html" if lang == "ar" else "dashboard_fleet.html"

    return render_template(
        template,
        onboarding_drivers=onboarding_drivers,
        offboarding_requests=offboarding_requests,
        total_drivers=total_drivers,
        total_users=offboarding_fleet,
        total_tamm=offboarding_pending_tamm,
        available_vehicles=available_vehicles,
    )


# -------------------------
# Assign Vehicle & Send to Next Stage
# -------------------------
@fleet_bp.route("/assign_vehicle/<int:driver_id>", methods=["POST"])
@login_required
def assign_vehicle(driver_id):
    """Fleet Manager assigns vehicle and sends driver to next stage."""
    if current_user.role != "FleetManager":
        return jsonify({"success": False, "message": "Access denied. Fleet Manager role required."}), 403

    form = FleetAssignForm()
    if not form.validate_on_submit():
        return jsonify({"success": False, "message": "Invalid CSRF token."}), 400

    driver = Driver.query.get_or_404(driver_id)

    # Gather form data
    vehicle_id = form.vehicle_id.data
    assignment_date = form.assignment_date.data
    tamm_authorized = bool(form.tamm_authorized.data)
    tamm_file = request.files.get("tamm_authorization_ss")

    # Validate required fields
    if not (vehicle_id and assignment_date and tamm_authorized):
        return jsonify({
            "success": False,
            "message": "Vehicle selection, assignment date, and TAMM Authorization are required."
        }), 400

    if not tamm_file or not tamm_file.filename:
        return jsonify({
            "success": False,
            "message": "TAMM Authorization Screenshot is required before approval."
        }), 400

    try:
        # Validate date
        if assignment_date > date.today():
            return jsonify({"success": False, "message": "Assignment date cannot be in the future."}), 400

        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return jsonify({"success": False, "message": "Selected vehicle not found."}), 404

        if vehicle.status != "available":
            return jsonify({"success": False, "message": "Vehicle is not available."}), 400

        vehicle_plate = vehicle.registration_number
        vehicle_details = f"{vehicle.make} {vehicle.model}" if vehicle.make and vehicle.model else "N/A"

        # Ensure driver and vehicle are not already actively assigned
        existing_driver_assignment = AssignDriver.query.filter_by(driver_id=driver.id, status="active").first()
        if existing_driver_assignment:
            return jsonify({"success": False, "message": "Driver is already assigned to a vehicle."}), 400

        existing_vehicle_assignment = AssignDriver.query.filter_by(vehicle_id=vehicle.id, status="active").first()
        if existing_vehicle_assignment:
            return jsonify({"success": False, "message": "Vehicle is already assigned to another driver."}), 400

        # Generate safe filename
        ext = os.path.splitext(tamm_file.filename)[1].lower()
        safe_name = secure_filename(
            f"{driver.name}_{driver.iqaama_number}_{vehicle.registration_number}_TAMM_Authorisation{ext}"
        )
        upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], safe_name)
        tamm_file.save(upload_path)

        # Update driver record and assignment tables
        driver.car_details = f"{vehicle.registration_number} - {vehicle.make}/{vehicle.model}"
        driver.assignment_date = assignment_date
        driver.tamm_authorized = True
        driver.tamm_authorization_ss = safe_name
        driver.mark_fleet_manager_approved()

        assignment_link = AssignDriver(
            vehicle_id=vehicle.id,
            driver_id=driver.id,
            assign_date=assignment_date,
            status="active",
            tam_authorization=True
        )
        db.session.add(assignment_link)

        assignment_report = AssignDriverReport(
            vehicle_id=vehicle.id,
            driver_id=driver.id,
            add_date=datetime.utcnow(),
            status="assign"
        )
        db.session.add(assignment_report)

        vehicle.status = "assigned"

        # Determine next stage and recipients
        if not driver.qiwa_contract_created:
            next_stage = "HR Final"
            recipients = [
                u.email for u in User.query.filter(User.role.in_(["HR", "HRManager"])).all() if u.email
            ]
        else:
            next_stage = "Finance"
            recipients = [
                u.email for u in User.query.filter(User.role.in_(["Finance", "FinanceManager"])).all() if u.email
            ]

        driver.onboarding_stage = next_stage
        db.session.commit()

        # Send notification email; swallow network failures so assignment succeeds even if email fails.
        if recipients:
            msg = Message(
                subject=f"Driver Assigned Vehicle & Ready for next Stage | تم تعيين مركبة للسائق وجاهز لمرحلة  {driver.name}",
                recipients=recipients
            )

            msg.html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">

                    <!-- English -->
                    <div style="text-align: left;">
                        <h2 style="color: #713183;">Driver Vehicle Assignment</h2>
                        <p>Hello {next_stage} Team,</p>
                        <p>Driver <strong>{driver.name}</strong> has been assigned a vehicle by the Fleet Manager.</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Plate</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{vehicle_plate or "N/A"}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Details</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{vehicle_details or "N/A"}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Assignment Date</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.assignment_date.strftime('%Y-%m-%d') if driver.assignment_date else "N/A"}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>TAMM Authorized</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">✅ Yes (Screenshot uploaded)</td>
                            </tr>
                        </table>
                        <p>Please log in and complete your next stage: <a href="https://dobs.dobs.cloud/login</" target="_blank">Login Here</a></p>
                    </div>

                    <hr style="margin: 30px 0;">

                    <!-- Arabic -->
                    <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                        <h2 style="color: #713183;">تعيين مركبة للسائق</h2>
                        <p>فريق {next_stage} المحترم،</p>
                        <p>تم تعيين مركبة للسائق <strong>{driver.name}</strong> بواسطة مدير الأسطول.</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">اللوحة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{vehicle_plate or "N/A"}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">التفاصيل</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{vehicle_details or "N/A"}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">تاريخ التعيين</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.assignment_date.strftime('%Y-%m-%d') if driver.assignment_date else "N/A"}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">TAMM مصرح</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">✅ نعم (تم رفع لقطة الشاشة)</td>
                            </tr>
                        </table>
                        <p>يرجى تسجيل الدخول وإتمام المرحلة التالية: <a href="https://dobs.dobs.cloud/login</" target="_blank">Login هنا</a></p>
                    </div>

                    <hr style="margin: 30px 0;">

                    <p style="text-align:center;">Regards / مع التحية,<br>Fleet Team / فريق الأسطول</p>

                </div>
            </body>
            </html>
            """

            try:
                mail.send(msg)
                current_app.logger.info(f"[FLEET] {next_stage} notification email sent successfully.")
            except Exception as mail_err:
                current_app.logger.error(f"[FLEET] Notification email failed: {mail_err}")
        else:
            current_app.logger.warning(f"[FLEET] No {next_stage} users with email found. Skipping notification.")

        return jsonify({
            "success": True,
            "message": f"✅ Vehicle assigned to {driver.name} and driver moved to {next_stage} stage."
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"[FLEET] Error assigning vehicle: {e}")
        return jsonify({"success": False, "message": f"❌ Error assigning vehicle: {str(e)}"}), 500


# -------------------------
# Fleet Manager Offboarding / TAMM Revocation (Unified)
# -------------------------
@fleet_bp.route("/api/offboarding_action/<int:offboarding_id>", methods=["POST"])
@limiter.limit("30 per minute")
@login_required
def offboarding_action(offboarding_id):
    if current_user.role != "FleetManager":
        return jsonify({"success": False, "message": "Access denied"}), 403

    if not _validate_csrf():
        return jsonify({"success": False, "message": "Invalid CSRF token."}), 400

    record = Offboarding.query.get_or_404(offboarding_id)
    data = request.get_json(silent=True) or {}
    driver_name = record.driver.name if record.driver else "Driver"

    try:
        now = datetime.utcnow()
        fleet_damage_report = data.get("fleet_damage_report")
        fleet_damage_cost = float(data.get("fleet_damage_cost") or 0)
        tamm_revoked = bool(data.get("tamm_revoked")) or bool(record.tamm_revoked)
        tamm_revoked_at = now if data.get("tamm_revoked") else record.tamm_revoked_at

        base_updates = {
            "fleet_cleared": True,
            "fleet_cleared_at": now,
            "fleet_damage_report": fleet_damage_report,
            "fleet_damage_cost": fleet_damage_cost,
            "tamm_revoked": tamm_revoked,
            "tamm_revoked_at": tamm_revoked_at,
        }

        # --- Determine next stage ---
        if data.get("finalize") and data.get("finance_cleared"):
            # Finance has cleared → Completed
            status = "Finance"
            Offboarding.query.filter_by(id=record.id).update(
                {**base_updates, "status": status},
                synchronize_session=False,
            )
            db.session.commit()

            # Notify HR/Admin
            recipients = [u.email for u in User.query.filter(User.role.in_(["HR", "Admin"])).all() if u.email]
            if recipients and record.driver:
                msg = Message(
                    subject=f"Driver Fully Offboarded | اكتمال خروج السائق: {driver_name}",
                    recipients=recipients
                )

                msg.html = f"""
                <html>
                <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">

                        <!-- English -->
                        <div style="text-align: left;">
                            <h2 style="color: #713183;">Driver Fully Offboarded</h2>
                            <p>Dear HR / Admin Team,</p>
                            <p>Driver <strong>{driver_name}</strong> (Iqama: <strong>{record.driver.iqaama_number or "N/A"}</strong>) has been fully offboarded.</p>
                            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>Offboarding Completed At</strong></td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{datetime.utcnow().strftime('%Y-%m-%d %H:%M')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>TAMM Revoked At</strong></td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{tamm_revoked_at.strftime('%Y-%m-%d %H:%M') if tamm_revoked_at else 'N/A'}</td>
                                </tr>
                            </table>
                            <p>Please update your records accordingly.</p>
                            <p>Login here to review: <a href="https://dobs.dobs.cloud/login</" target="_blank">HR Dashboard</a></p>
                        </div>

                        <hr style="margin: 30px 0;">

                        <!-- Arabic -->
                        <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                            <h2 style="color: #713183;">اكتمال خروج السائق</h2>
                            <p>السادة فريق الموارد البشرية / الإدارة،</p>
                            <p>تم إتمام خروج السائق <strong>{driver_name}</strong> (رقم الإقامة: <strong>{record.driver.iqaama_number or "N/A"}</strong>).</p>
                            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;">تاريخ إتمام الخروج</td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{datetime.utcnow().strftime('%Y-%m-%d %H:%M')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;">تاريخ إلغاء صلاحية TAMM</td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{tamm_revoked_at.strftime('%Y-%m-%d %H:%M') if tamm_revoked_at else 'N/A'}</td>
                                </tr>
                            </table>
                            <p>يرجى تحديث سجلاتكم حسب ذلك.</p>
                            <p>Login هنا لمراجعة: <a href="https://dobs.dobs.cloud/login</r" target="_blank">لوحة الموارد البشرية</a></p>
                        </div>

                        <hr style="margin: 30px 0;">

                        <p style="text-align:center;">Regards / مع التحية,<br>Fleet Team / فريق الأسطول</p>

                    </div>
                </body>
                </html>
                """

                try:
                    mail.send(msg)
                except Exception as mail_err:
                    current_app.logger.error(f"[FLEET] HR/Admin notification email failed: {mail_err}")



            return jsonify({"success": True, "message": f"Driver {driver_name} fully offboarded."})

        else:
            # Send to FinanceManager
            status = "Finance"
            Offboarding.query.filter_by(id=record.id).update(
                {**base_updates, "status": status},
                synchronize_session=False,
            )
            db.session.commit()

            # Notify Finance
            finance_users = User.query.filter(User.role.in_(["FinanceManager", "Finance"])).all()
            emails = [f.email for f in finance_users if f.email]
            if emails and record.driver:
                msg = Message(
                    subject=f"Driver Sent to Finance Manager | تحويل السائق إلى المالية: {driver_name}",
                    recipients=emails
                )

                msg.html = f"""
                <html>
                <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">

                        <!-- English -->
                        <div style="text-align: left;">
                            <h2 style="color: #713183;">Driver Sent to Finance Manager</h2>
                            <p>Dear Finance Team,</p>
                            <p>Driver <strong>{driver_name}</strong> (Iqama: <strong>{record.driver.iqaama_number or "N/A"}</strong>) has been cleared by the Fleet Manager.</p>
                            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>Fleet Damage Report</strong></td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{fleet_damage_report or "N/A"}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>Damage Cost</strong></td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{fleet_damage_cost or 0} SAR</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>TAMM Revoked</strong></td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{"Yes" if tamm_revoked else "No"}</td>
                                </tr>
                            </table>
                            <p>Please proceed with the settlement.</p>
                            <p>Login here to review: <a href="https://dobs.dobs.cloud/login</" target="_blank">Finance Dashboard</a></p>
                        </div>

                        <hr style="margin: 30px 0;">

                        <!-- Arabic -->
                        <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                            <h2 style="color: #713183;">تم تحويل السائق إلى المالية</h2>
                            <p>السادة فريق المالية،</p>
                            <p>تمت الموافقة على السائق <strong>{driver_name}</strong> (رقم الإقامة: <strong>{record.driver.iqaama_number or "N/A"}</strong>) من قبل مدير الأسطول.</p>
                            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;">تقرير أضرار الأسطول</td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{fleet_damage_report or "N/A"}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;">تكلفة الأضرار</td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{fleet_damage_cost or 0} ريال سعودي</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;">إلغاء صلاحية TAMM</td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{"نعم" if tamm_revoked else "لا"}</td>
                                </tr>
                            </table>
                            <p>يرجى متابعة التسوية حسب الإجراءات.</p>
                            <p>Login هنا لمراجعة: <a href="https://dobs.dobs.cloud/login</e" target="_blank">لوحة المالية</a></p>
                        </div>

                        <hr style="margin: 30px 0;">

                        <p style="text-align:center;">Regards / مع التحية,<br>Fleet Team / فريق الأسطول</p>

                    </div>
                </body>
                </html>
                """

                try:
                    mail.send(msg)
                except Exception as mail_err:
                    current_app.logger.error(f"[FLEET] Finance notification email failed: {mail_err}")



            return jsonify({
                "success": True,
                "message": f"Driver {driver_name} cleared by Fleet and sent to Finance Manager.",
                "cleared_at": now.strftime("%Y-%m-%d %H:%M"),
                "damage_cost": fleet_damage_cost,
                "damage_report": fleet_damage_report,
                "tamm_revoked_at": tamm_revoked_at.strftime("%Y-%m-%d %H:%M") if tamm_revoked_at else None
            })

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"[FLEET OFFBOARDING ERROR] {e}")
        return jsonify({"success": False, "message": str(e)}), 500


# -------------------------
# Change Password
# -------------------------
@fleet_bp.route("/change_password", methods=["POST"])
@limiter.limit("5 per minute")
@login_required
def change_password():
    if current_user.role != "FleetManager":
        flash("Access denied. Fleet Manager role required.", "danger")
        return redirect(url_for("auth.login"))

    form = ChangePasswordForm()
    if not form.validate_on_submit():
        flash("Invalid or missing CSRF token. Please try again.", "danger")
        return redirect(url_for("fleet.dashboard_fleet"))

    new_password = form.new_password.data
    confirm_password = form.confirm_password.data

    if not check_password_hash(current_user.password, form.current_password.data):
        flash("Current password is incorrect.", "danger")
        return redirect(url_for("fleet.dashboard_fleet"))

    if new_password != confirm_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for("fleet.dashboard_fleet"))

    try:
        current_user.password = generate_password_hash(new_password)
        db.session.commit()

        if send_password_change_email(current_user, new_password):
            flash("✅ Password updated and email notification sent.", "success")
        else:
            flash("✅ Password updated, but email could not be sent.", "warning")

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(f"[FLEET] Failed to change password: {e}")
        flash("Could not update password right now. Try again later.", "danger")

    return redirect(url_for("fleet.dashboard_fleet"))
