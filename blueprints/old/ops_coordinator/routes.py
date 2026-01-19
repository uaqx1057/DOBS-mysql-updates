from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from flask_login import login_required, current_user
from datetime import datetime
from models import Driver, User , Offboarding
from extensions import db, mail
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash
from utils.email_utils import send_password_change_email
from sqlalchemy.orm import aliased



ops_coordinator_bp = Blueprint("ops_coordinator", __name__)

# -------------------------
# Dashboard - Ops Coordinator
# -------------------------
@ops_coordinator_bp.route("/dashboard")
@login_required
def dashboard_ops_coordinator():
    if current_user.role != "OpsCoordinator":
        flash("Access denied. Ops Coordinator role required.", "danger")
        return redirect(url_for("auth.login"))

    lang = session.get("lang", "en")

    # Coordinator sees only completed (onboarded) drivers
    # Fetch drivers with completed onboarding but not in Offboarding
    completed_drivers = (
        Driver.query
        .filter(Driver.onboarding_stage == "Completed")
        .filter(~Driver.offboarding_records.any())  # Exclude drivers present in Offboarding
        .order_by(Driver.full_name.asc())
        .all()
    )

    template = "rtl_dashboard_ops_coordinator.html" if lang == "ar" else "dashboard_ops_coordinator.html"

    return render_template(
        template,
        completed_drivers=completed_drivers,
        count_completed=len(completed_drivers)
    )


# -------------------------
# Initiate Offboarding Request
# -------------------------
@ops_coordinator_bp.route("/initiate_offboarding/<int:driver_id>", methods=["POST"])
@login_required
def initiate_offboarding(driver_id):
    if current_user.role != "OpsCoordinator":
        flash("Access denied. Ops Coordinator role required.", "danger")
        return redirect(url_for("auth.login"))

    driver = Driver.query.get_or_404(driver_id)

    if driver.onboarding_stage != "Completed":
        flash("Only completed drivers can be requested for offboarding.", "warning")
        return redirect(url_for("ops_coordinator.dashboard_ops_coordinator"))

    if driver.offboard_request:
        flash(f"Offboarding already requested for {driver.full_name}.", "info")
        return redirect(url_for("ops_coordinator.dashboard_ops_coordinator"))

    reason = request.form.get("reason", "").strip()

    # Update driver record
    driver.offboard_request = True
    driver.offboard_requested_by = current_user.name or current_user.username
    driver.offboard_reason = reason or "No reason provided"
    driver.offboard_requested_at = datetime.utcnow()

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("Failed to save offboarding request.")
        flash("An error occurred. Try again.", "danger")
        return redirect(url_for("ops_coordinator.dashboard_ops_coordinator"))

    # Notify Ops Manager via email
    try:
        managers = User.query.filter_by(role="OpsManager").all()
        recipients = [m.email for m in managers if m.email]

        if recipients:
            driver_iqama = driver.iqama_number or "N/A"
            coordinator_name = current_user.name or current_user.username
            reason_text = reason or "No reason provided."
            driver_city = driver.city or "N/A"
        
            msg = Message(
                subject="Offboarding Request Submitted | تم تقديم طلب الخروج",
                recipients=recipients
            )
        
            msg.html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
        
                    <!-- English LTR -->
                    <div style="text-align: left;">
                        <h2 style="color: #004aad;">Driver Onboarding System</h2>
                        <p>Dear Ops Manager,</p>
                        <p>Ops Coordinator <strong>{coordinator_name}</strong> has requested offboarding for the following driver:</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Driver Name</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.full_name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Iqama Number</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_iqama}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>City / Branch</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_city}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Requested By</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{coordinator_name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Reason</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{reason_text}</td>
                            </tr>
                        </table>
                        <p>Please log in to your dashboard to review and proceed.</p>
                    </div>
        
                    <hr style="margin: 30px 0;">
        
                    <!-- Arabic RTL -->
                    <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                        <h2 style="color: #004aad;">نظام إدخال السائقين</h2>
                        <p>عزيزي مدير العمليات،</p>
                        <p>قام منسق العمليات <strong>{coordinator_name}</strong> بطلب خروج للسائق التالي:</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">اسم السائق</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.full_name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">رقم الإقامة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_iqama}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">المدينة / الفرع</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_city}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">تم الطلب بواسطة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{coordinator_name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">السبب</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{reason_text}</td>
                            </tr>
                        </table>
                        <p>يرجى تسجيل الدخول إلى لوحة التحكم لمراجعة الطلب والمضي قدمًا.</p>
                    </div>
        
                </div>
            </body>
            </html>
            """
            mail.send(msg)
    except Exception as e:
        current_app.logger.exception("Email notification failed.")
        flash("Offboarding request saved but email could not be sent.", "warning")

    flash(f"✅ Offboarding request submitted for {driver.full_name}.", "success")
    return redirect(url_for("ops_coordinator.dashboard_ops_coordinator"))


# ------------------------- 
# Change Password
# -------------------------
@ops_coordinator_bp.route("/change_password", methods=["POST"])
@login_required
def change_password():
    if current_user.role != "OpsCoordinator":
        flash("Access denied. Ops Coordinator role required.", "danger")
        return redirect(url_for("auth.login"))

    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not current_password or not new_password or not confirm_password:
        flash("Please fill all password fields.", "danger")
        return redirect(url_for("ops_coordinator.dashboard_ops_coordinator"))

    if not check_password_hash(current_user.password, current_password):
        flash("Current password is incorrect.", "danger")
        return redirect(url_for("ops_coordinator.dashboard_ops_coordinator"))

    if new_password != confirm_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for("ops_coordinator.dashboard_ops_coordinator"))

    try:
        current_user.password = generate_password_hash(new_password)
        db.session.commit()

        if send_password_change_email(current_user, new_password):
            flash("✅ Password updated and email notification sent.", "success")
        else:
            flash("✅ Password updated, but email could not be sent.", "warning")

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(f"[ops_coordinator] Failed to change password: {e}")
        flash("Could not update password right now. Try again later.", "danger")

    return redirect(url_for("ops_coordinator.dashboard_ops_coordinator"))
