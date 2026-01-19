from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, session
from flask_login import login_required, current_user
from extensions import db, mail
from flask_mail import Message
from datetime import datetime, date
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import joinedload
from models import Offboarding, Driver, User
from utils.email_utils import send_password_change_email
import os

fleet_bp = Blueprint("fleet", __name__)

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

    lang = session.get("lang", "en")
    template = "rtl_dashboard_fleet.html" if lang == "ar" else "dashboard_fleet.html"

    return render_template(
        template,
        onboarding_drivers=onboarding_drivers,
        offboarding_requests=offboarding_requests,
        total_drivers=total_drivers,
        total_users=offboarding_fleet,
        total_tamm=offboarding_pending_tamm,
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

    driver = Driver.query.get_or_404(driver_id)

    # Gather form data
    vehicle_plate = request.form.get("vehicle_plate", "").strip()
    vehicle_details = request.form.get("vehicle_details", "").strip()
    assignment_date = request.form.get("assignment_date", "").strip()
    tamm_authorized = request.form.get("tamm_authorized")
    tamm_file = request.files.get("tamm_authorization_ss")

    # Validate required fields
    if not all([vehicle_plate, vehicle_details, assignment_date, tamm_authorized]):
        return jsonify({
            "success": False,
            "message": "All fields, including TAMM Authorization, must be filled before approval."
        }), 400

    if not tamm_file or not tamm_file.filename:
        return jsonify({
            "success": False,
            "message": "TAMM Authorization Screenshot is required before approval."
        }), 400

    try:
        # Validate and parse date
        parsed_date = datetime.strptime(assignment_date, "%Y-%m-%d").date()
        if parsed_date > date.today():
            return jsonify({"success": False, "message": "Assignment date cannot be in the future."}), 400

        # Generate safe filename
        ext = os.path.splitext(tamm_file.filename)[1].lower()
        safe_name = secure_filename(
            f"{driver.name}_{driver.iqaama_number}_{vehicle_plate}_TAMM_Authorisation{ext}"
        )
        upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], safe_name)
        tamm_file.save(upload_path)

        # Update driver record
        driver.car_details = f"{vehicle_plate} - {vehicle_details}"
        driver.assignment_date = parsed_date
        driver.tamm_authorized = True
        driver.tamm_authorization_ss = safe_name
        driver.mark_fleet_manager_approved()

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

        # Send notification email
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

            mail.send(msg)

            current_app.logger.info(f"[FLEET] {next_stage} notification email sent successfully.")
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
@login_required
def offboarding_action(offboarding_id):
    if current_user.role != "FleetManager":
        return jsonify({"success": False, "message": "Access denied"}), 403

    record = Offboarding.query.get_or_404(offboarding_id)
    data = request.get_json()

    try:
        # --- Fleet Clearance ---
        record.fleet_cleared = True
        record.fleet_cleared_at = datetime.utcnow()
        record.fleet_damage_report = data.get("fleet_damage_report")
        record.fleet_damage_cost = float(data.get("fleet_damage_cost") or 0)

        # --- TAMM Revocation ---
        if data.get("tamm_revoked"):
            record.tamm_revoked = True
            record.tamm_revoked_at = datetime.utcnow()

        # --- Determine next stage ---
        if data.get("finalize") and data.get("finance_cleared"):
            # Finance has cleared → Completed
            record.status = "Finance"
            db.session.commit()

            # Notify HR/Admin
            recipients = [u.email for u in User.query.filter(User.role.in_(["HR", "Admin"])).all() if u.email]
            if recipients:
                msg = Message(
                    subject=f"Driver Fully Offboarded | اكتمال خروج السائق: {record.driver.name}",
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
                            <p>Driver <strong>{record.driver.name}</strong> (Iqama: <strong>{record.driver.iqaama_number or "N/A"}</strong>) has been fully offboarded.</p>
                            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>Offboarding Completed At</strong></td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{datetime.utcnow().strftime('%Y-%m-%d %H:%M')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>TAMM Revoked At</strong></td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{record.tamm_revoked_at.strftime('%Y-%m-%d %H:%M') if record.tamm_revoked_at else 'N/A'}</td>
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
                            <p>تم إتمام خروج السائق <strong>{record.driver.name}</strong> (رقم الإقامة: <strong>{record.driver.iqaama_number or "N/A"}</strong>).</p>
                            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;">تاريخ إتمام الخروج</td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{datetime.utcnow().strftime('%Y-%m-%d %H:%M')}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;">تاريخ إلغاء صلاحية TAMM</td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{record.tamm_revoked_at.strftime('%Y-%m-%d %H:%M') if record.tamm_revoked_at else 'N/A'}</td>
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

                mail.send(msg)



            return jsonify({"success": True, "message": f"Driver {record.driver.name} fully offboarded."})

        else:
            # Send to FinanceManager
            record.status = "Finance"
            db.session.commit()

            # Notify Finance
            finance_users = User.query.filter(User.role.in_(["FinanceManager", "Finance"])).all()
            emails = [f.email for f in finance_users if f.email]
            if emails:
                msg = Message(
                    subject=f"Driver Sent to Finance Manager | تحويل السائق إلى المالية: {record.driver.name}",
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
                            <p>Driver <strong>{record.driver.name}</strong> (Iqama: <strong>{record.driver.iqaama_number or "N/A"}</strong>) has been cleared by the Fleet Manager.</p>
                            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>Fleet Damage Report</strong></td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{record.fleet_damage_report or "N/A"}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>Damage Cost</strong></td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{record.fleet_damage_cost or 0} SAR</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>TAMM Revoked</strong></td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{"Yes" if record.tamm_revoked else "No"}</td>
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
                            <p>تمت الموافقة على السائق <strong>{record.driver.name}</strong> (رقم الإقامة: <strong>{record.driver.iqaama_number or "N/A"}</strong>) من قبل مدير الأسطول.</p>
                            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;">تقرير أضرار الأسطول</td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{record.fleet_damage_report or "N/A"}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;">تكلفة الأضرار</td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{record.fleet_damage_cost or 0} ريال سعودي</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;">إلغاء صلاحية TAMM</td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{"نعم" if record.tamm_revoked else "لا"}</td>
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

                mail.send(msg)



            return jsonify({
                "success": True,
                "message": f"Driver {record.driver.name} cleared by Fleet and sent to Finance Manager.",
                "cleared_at": record.fleet_cleared_at.strftime("%Y-%m-%d %H:%M"),
                "damage_cost": record.fleet_damage_cost,
                "damage_report": record.fleet_damage_report,
                "tamm_revoked_at": record.tamm_revoked_at.strftime("%Y-%m-%d %H:%M") if record.tamm_revoked else None
            })

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"[FLEET OFFBOARDING ERROR] {e}")
        return jsonify({"success": False, "message": str(e)}), 500


# -------------------------
# Change Password
# -------------------------
@fleet_bp.route("/change_password", methods=["POST"])
@login_required
def change_password():
    if current_user.role != "FleetManager":
        flash("Access denied. Fleet Manager role required.", "danger")
        return redirect(url_for("auth.login"))

    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not current_password or not new_password or not confirm_password:
        flash("Please fill all password fields.", "danger")
        return redirect(url_for("fleet.dashboard_fleet"))

    if not check_password_hash(current_user.password, current_password):
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
