from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models import Driver, Offboarding, User
from extensions import db, mail
from flask_mail import Message
from datetime import datetime
from werkzeug.exceptions import BadRequest
from utils.email_utils import send_password_change_email 
from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify


 
ops_manager_bp = Blueprint("ops_manager", __name__)

@ops_manager_bp.route("/dashboard")
@login_required
def dashboard_ops():
    if current_user.role != "OpsManager":
        flash("Access denied. Ops Manager role required.", "danger")
        return redirect(url_for("auth.login"))

    from flask import session
    lang = session.get("lang", "en")

    # --- Fetch data ---
    drivers = Driver.query.filter_by(onboarding_stage="Ops Manager").all()
    fully_onboarded_drivers = Driver.query.filter(Driver.onboarding_stage == "Completed").all()
    rejected = Driver.query.filter_by(onboarding_stage="Rejected").order_by(Driver.name.asc()).all()

    # --- Fetch offboarding drivers and convert to dicts for JSON ---
    raw_offboarding_drivers = Driver.query.filter_by(offboard_request=True).order_by(Driver.name.asc()).all()
    offboarding_drivers = []

    for d in raw_offboarding_drivers:
        records_list = [
            {
                "id": r.id,
                "status": r.status,
                "ops_supervisor_cleared": r.ops_supervisor_cleared,
                "ops_supervisor_cleared_at": r.ops_supervisor_cleared_at.strftime("%Y-%m-%d %H:%M") if r.ops_supervisor_cleared_at else None,
                "ops_supervisor_note": r.ops_supervisor_note,
                "fleet_cleared": r.fleet_cleared,
                "fleet_cleared_at": r.fleet_cleared_at.strftime("%Y-%m-%d %H:%M") if r.fleet_cleared_at else None,
                "fleet_damage_report": r.fleet_damage_report,
                "fleet_damage_cost": r.fleet_damage_cost,
                "finance_cleared": r.finance_cleared,
                "finance_cleared_at": r.finance_cleared_at.strftime("%Y-%m-%d %H:%M") if r.finance_cleared_at else None,
                "finance_note": r.finance_note,
                "hr_cleared": r.hr_cleared,
                "hr_cleared_at": r.hr_cleared_at.strftime("%Y-%m-%d %H:%M") if r.hr_cleared_at else None,
                "hr_note": r.hr_note,
                "tamm_revoked": r.tamm_revoked,
                "tamm_revoked_at": r.tamm_revoked_at.strftime("%Y-%m-%d %H:%M") if r.tamm_revoked_at else None,
                "company_contract_cancelled": r.company_contract_cancelled,
                "qiwa_contract_cancelled": r.qiwa_contract_cancelled,
                "salary_paid": r.salary_paid
            } for r in d.offboarding_records
        ]

        # Determine current stage dynamically
        current_stage = records_list[-1]["status"] if records_list else d.onboarding_stage

        offboarding_drivers.append({
            "id": d.id,
            "name": d.name,
            "iqama_number": d.iqaama_number,
            "city": d.city,
            "offboard_requested_by": d.offboard_requested_by,
            "offboard_reason": d.offboard_reason,
            "offboard_requested_at": d.offboard_requested_at.strftime("%Y-%m-%d") if d.offboard_requested_at else None,
            "records": records_list,
            "current_stage": current_stage
        })

    # --- Select template based on language ---
    template = "rtl_dashboard_ops.html" if lang == "ar" else "dashboard_ops.html"

    return render_template(
        template,
        drivers=drivers,
        rejected_drivers=rejected,
        offboarding_drivers=offboarding_drivers,
        fully_onboarded_drivers=fully_onboarded_drivers,
        count_onboarding_ops=len(drivers),
        count_offboarding_requested=len(offboarding_drivers)
    )

# -------------------------
# Approve Driver & Send to HR
# -------------------------
@ops_manager_bp.route("/approve_driver/<int:driver_id>", methods=["POST"])
@login_required
def approve_driver(driver_id):
    """
    Approve driver at Ops Manager stage and forward to HR.
    - Validate that driver is in the correct stage.
    - Set ops_manager_approved flag and timestamp (do not overwrite if already set).
    - Move onboarding_stage to "HR".
    - Notify HR team by email (safely).
    """
    if current_user.role != "OpsManager":
        flash("Access denied. Ops Manager role required.", "danger")
        return redirect(url_for("auth.login"))

    driver = Driver.query.get_or_404(driver_id)

    # Validate stage to avoid re-processing
    if driver.onboarding_stage != "Ops Manager":
        flash(f"Driver is not in Ops Manager stage (current: {driver.onboarding_stage}).", "warning")
        return redirect(url_for("ops_manager.dashboard_ops"))

    # Optional: allow ops manager to add a short note (not required)
    ops_note = request.form.get("ops_note", "").strip()

    # Mark approved only if not already approved
    if not getattr(driver, "ops_manager_approved", False):
        driver.ops_manager_approved = True
        driver.ops_manager_approved_at = datetime.utcnow()
    else:
        # Keep previous timestamp, but still move stage if needed
        if not driver.ops_manager_approved_at:
            driver.ops_manager_approved_at = datetime.utcnow()

    # Move to HR stage
    driver.onboarding_stage = "HR"

    # Save
    try:
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        current_app.logger.exception("Failed to approve driver in Ops Manager")
        flash("An internal error occurred while approving the driver. Please try again.", "danger")
        raise BadRequest("DB commit failed") from exc

    # Notify HR team (only to users with an email)
    try:
        hr_users = User.query.filter_by(role="HR").all()
        recipients = [u.email for u in hr_users if u.email]
        if recipients:
            driver_iqaama = driver.iqaama_number or "N/A"
            driver_iqaama_expiry = driver.iqaama_expiry.strftime("%Y-%m-%d") if driver.iqaama_expiry else "N/A"
            driver_city = driver.city or "N/A"
            driver_mobile = driver.absher_number or "N/A"
            approved_at = driver.ops_manager_approved_at.strftime("%Y-%m-%d %H:%M:%S") if driver.ops_manager_approved_at else "N/A"
        
            msg = Message(
                subject=f"Driver Approved & Ready for HR | تم الموافقة على السائق وجاهز للموارد البشرية",
                recipients=recipients
            )
        
            msg.html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
        
                    <!-- English LTR -->
                    <div style="text-align: left;">
                        <h2 style="color: #713183;">Driver Onboarding System</h2>
                        <p>Dear HR Team,</p>
                        <p>A driver has been approved by the Operations Manager and is ready for HR processing:</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Driver Name</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>iqaama Number</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_iqaama}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>iqaama Expiry</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_iqaama_expiry}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>City</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_city}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Personal Mobile</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_mobile}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Approved At (UTC)</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{approved_at}</td>
                            </tr>
                        </table>
                        <p><a href="https://dobs.dobs.cloud/login">Please Login to the HR dashboard</a> to continue processing.</a></p>
                    </div>
        
                    <hr style="margin: 30px 0;">
        
                    <!-- Arabic RTL -->
                    <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                        <h2 style="color: #713183;">نظام إدخال السائقين</h2>
                        <p>عزيزي فريق الموارد البشرية،</p>
                        <p>تمت الموافقة على السائق من قبل مدير العمليات وهو جاهز للمعالجة من قبل الموارد البشرية:</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">اسم السائق</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">رقم الإقامة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_iqaama}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">تاريخ انتهاء الإقامة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_iqaama_expiry}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">المدينة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_city}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">الهاتف الشخصي</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_mobile}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">تمت الموافقة في (UTC)</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{approved_at}</td>
                            </tr>
                        </table>
                        <p><a href="https://dobs.dobs.cloud/login">يرجى  تسجيل الدخول إلى لوحة الموارد البشرية لمتابعة المعالجة.</a></p>
                    </div>
        
                </div>
            </body>
            </html>
            """
        
            mail.send(msg)
    except Exception as e:
        # Email failure should not block flow; log and inform user gracefully
        current_app.logger.exception("Failed to send HR notification email")
        flash("Driver approved but notification email to HR failed (check mail logs).", "warning")
        return redirect(url_for("ops_manager.dashboard_ops"))

    flash(f"✅ {driver.name} approved and forwarded to HR.", "success")
    return redirect(url_for("ops_manager.dashboard_ops"))


# -------------------------
# Reject Driver
# -------------------------
@ops_manager_bp.route("/reject_driver/<int:driver_id>", methods=["POST"])
@login_required
def reject_driver(driver_id):
    """
    Reject driver at Ops Manager stage.
    - Validate stage
    - Set ops_manager_rejected flag and timestamp
    - Store optional reason
    """
    if current_user.role != "OpsManager":
        flash("Access denied. Ops Manager role required.", "danger")
        return redirect(url_for("auth.login"))

    driver = Driver.query.get_or_404(driver_id)

    # Validate stage
    if driver.onboarding_stage != "Ops Manager":
        flash(f"Driver is not in Ops Manager stage (current: {driver.onboarding_stage}).", "warning")
        return redirect(url_for("ops_manager.dashboard_ops"))

    # Get reason from form
    reject_reason = request.form.get("reject_reason", "").strip()

    # Update driver record
    driver.onboarding_stage = "Rejected"
    driver.ops_manager_approved = False
    driver.ops_manager_rejected = True
    driver.ops_manager_rejected_at = datetime.utcnow()
    driver.ops_manager_reject_reason = reject_reason or "No reason provided"

    # Save to DB
    try:
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        current_app.logger.exception("Failed to reject driver in Ops Manager")
        flash("An internal error occurred while rejecting the driver. Please try again.", "danger")
        raise BadRequest("DB commit failed") from exc

    flash(f"❌ {driver.name} has been rejected.", "success")
    return redirect(url_for("ops_manager.dashboard_ops"))


# ------------------------- 
# Change Password
# -------------------------
@ops_manager_bp.route("/change_password", methods=["POST"])
@login_required
def change_password():
    """Allow Ops Manager to change their own password securely and send email notification."""
    if current_user.role != "OpsManager":
        flash("Access denied. Ops Manager role required.", "danger")
        return redirect(url_for("auth.login"))

    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not current_password or not new_password or not confirm_password:
        flash("Please fill all password fields.", "danger")
        return redirect(url_for("ops_manager.dashboard_ops"))

    if not check_password_hash(current_user.password, current_password):
        flash("Current password is incorrect.", "danger")
        return redirect(url_for("ops_manager.dashboard_ops"))

    if new_password != confirm_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for("ops_manager.dashboard_ops"))

    try:
        # Update password in database
        current_user.password = generate_password_hash(new_password)
        db.session.commit()

        # Send email notification using helper
        if send_password_change_email(current_user, new_password):
            flash("✅ Password updated and email notification sent.", "success")
        else:
            flash("✅ Password updated, but email could not be sent.", "warning")

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(f"[OPS_MANAGER] Failed to change password: {e}")
        flash("Could not update password right now. Try again later.", "danger")

    return redirect(url_for("ops_manager.dashboard_ops"))

# -------------------------
# Request Offboarding (Ops Manager)
# -------------------------
@ops_manager_bp.route("/request_offboarding/<int:driver_id>", methods=["POST"])
@login_required
def request_offboarding(driver_id):
    if current_user.role != "OpsManager":  # ✅ fixed (no space)
        flash("Access denied", "danger")
        return redirect(url_for("ops_manager.dashboard_ops"))

    driver = Driver.query.get_or_404(driver_id)

    if driver.onboarding_stage != "Completed":
        flash("Only completed drivers can be offboarded.", "warning")
        return redirect(url_for("ops_manager.dashboard_ops"))

    # 🔒 Prevent duplicate requests
    existing = Offboarding.query.filter_by(driver_id=driver.id, status="Requested").first()
    if existing:
        flash(f"Offboarding already requested for {driver.name}.", "info")
        return redirect(url_for("ops_manager.dashboard_ops"))

    # ✅ Create a new record
    offboarding = Offboarding(
        driver_id=driver.id,
        requested_by_id=current_user.id,
        requested_at=datetime.utcnow(),
        status="OpsSupervisor"  # 🔑 mark next stage clearly
    )
    db.session.add(offboarding)
    db.session.commit()

    # ✅ Notify Ops Supervisors via email
    try:
        supervisors = User.query.filter_by(role="OpsSupervisor").all()  # ✅ fixed
        emails = [s.email for s in supervisors if s.email]
        if emails:
            driver_iqama = driver.iqaama_number or "N/A"
            driver_city = driver.city or "N/A"
            driver_mobile = driver.absher_number or "N/A"
            
            msg = Message(
                subject=f"Offboarding Requested: {driver.name} | تم طلب إنهاء خدمات السائق",
                recipients=emails
            )
        
            msg.html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
        
                    <!-- English LTR -->
                    <div style="text-align: left;">
                        <h2 style="color: #004aad;">Driver Onboarding System</h2>
                        <p>Dear Ops Supervisor,</p>
                        <p>Ops Manager <strong>{current_user.name or current_user.username}</strong> has requested offboarding for the following driver:</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Driver Name</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Iqama Number</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_iqama}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>City</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_city}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Mobile</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_mobile}</td>
                            </tr>
                        </table>
                        <p>Please log in to the dashboard to start the clearance process. https://dobs.dobs.cloud/login</p>
                    </div>
        
                    <hr style="margin: 30px 0;">
        
                    <!-- Arabic RTL -->
                    <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                        <h2 style="color: #004aad;">نظام إدخال السائقين</h2>
                        <p>عزيزي مشرف العمليات،</p>
                        <p>قام مدير العمليات <strong>{current_user.name or current_user.username}</strong> بطلب إنهاء خدمات السائق التالي:</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">اسم السائق</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">رقم الإقامة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_iqama}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">المدينة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_city}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">الهاتف</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_mobile}</td>
                            </tr>
                        </table>
                        <p>يرجى تسجيل الدخول إلى لوحة التحكم لبدء عملية إنهاء الخدمة.https://dobs.dobs.cloud/login</p>
                    </div>
        
                </div>
            </body>
            </html>
            """
        
            mail.send(msg)
    except Exception as e:
        print("[EMAIL ERROR]", e)

    flash(f"Offboarding requested for {driver.name}.", "success")
    return redirect(url_for("ops_manager.dashboard_ops"))

@ops_manager_bp.route("/api/request_offboarding/<int:driver_id>", methods=["POST"])
@login_required
def api_request_offboarding(driver_id):
    if current_user.role != "OpsManager":
        return {"success": False, "message": "Access denied"}, 403

    driver = Driver.query.get_or_404(driver_id)
    if driver.onboarding_stage != "Completed":
        return {"success": False, "message": "Only completed drivers can be offboarded."}, 400

    existing = Offboarding.query.filter_by(driver_id=driver.id, status="Requested").first()
    if existing:
        return {"success": False, "message": "Offboarding already requested."}, 200

    offboarding = Offboarding(
        driver_id=driver.id,
        requested_by_id=current_user.id,
        status="Requested"
    )
    db.session.add(offboarding)
    db.session.commit()

    # notify supervisors (same as before)
    try:
        supervisors = User.query.filter_by(role="Ops Supervisor").all()
        emails = [s.email for s in supervisors if s.email]
        if emails:
            driver_iqama = driver.iqaama_number or "N/A"
            driver_city = driver.city or "N/A"
            driver_mobile = driver.absher_number or "N/A"
        
            msg = Message(
                subject=f"Offboarding Requested: {driver.name} | تم طلب إنهاء خدمات السائق",
                recipients=emails
            )
        
            msg.html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
        
                    <!-- English LTR -->
                    <div style="text-align: left;">
                        <h2 style="color: #004aad;">Driver Onboarding System</h2>
                        <p>Dear Ops Supervisor,</p>
                        <p>Ops Manager <strong>{current_user.name or current_user.username}</strong> has requested offboarding for the following driver:</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Driver Name</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Iqama Number</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_iqama}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>City</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_city}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Mobile</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_mobile}</td>
                            </tr>
                        </table>
                        <p>Please log in to the dashboard to start the clearance process.https://dobs.dobs.cloud/login</p>
                    </div>
        
                    <hr style="margin: 30px 0;">
        
                    <!-- Arabic RTL -->
                    <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                        <h2 style="color: #004aad;">نظام إدخال السائقين</h2>
                        <p>عزيزي مشرف العمليات،</p>
                        <p>قام مدير العمليات <strong>{current_user.name or current_user.username}</strong> بطلب إنهاء خدمات السائق التالي:</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">اسم السائق</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">رقم الإقامة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_iqama}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">المدينة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_city}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">الهاتف</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_mobile}</td>
                            </tr>
                        </table>
                        <p>يرجى تسجيل الدخول إلى لوحة التحكم لبدء عملية إنهاء الخدمة.https://dobs.dobs.cloud/login</p>
                    </div>
        
                </div>
            </body>
            </html>
            """
        
            mail.send(msg)
    except Exception as e:
        print("[EMAIL ERROR]", e)

    return {
        "success": True,
        "driver_id": driver.id,
        "requested_at": offboarding.requested_at.strftime("%Y-%m-%d"),
    }



@ops_manager_bp.route("/reject_offboarding/<int:driver_id>", methods=["POST"])
@login_required
def reject_offboarding(driver_id):
    if current_user.role != "OpsManager":
        flash("Access denied. Ops Manager role required.", "danger")
        return redirect(url_for("auth.login"))

    driver = Driver.query.get_or_404(driver_id)

    if not driver.offboard_request:
        flash("This driver does not have an offboarding request.", "warning")
        return redirect(url_for("ops_manager.dashboard_ops"))

    # Optional reason
    reason = request.form.get("reason", "").strip()

    # Clear the offboarding fields
    driver.offboard_request = False
    driver.offboard_requested_by = None
    driver.offboard_reason = None
    driver.offboard_requested_at = None

    try:
        db.session.commit()
        flash(f"❌ Offboarding request for {driver.name} has been rejected.", "success")
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(f"Failed to reject offboarding: {e}")
        flash("An error occurred while rejecting the request.", "danger")

    return redirect(url_for("ops_manager.dashboard_ops"))



@ops_manager_bp.route("/dashboard/ops/offboarding_progress/<int:driver_id>")
@login_required
def offboarding_progress(driver_id):
    if current_user.role != "OpsManager":
        return jsonify({"success": False, "message": "Access denied"}), 403

    driver = Driver.query.get_or_404(driver_id)
    
    # Fix: get latest offboarding record
    offboarding = driver.offboarding_records.order_by(Offboarding.id.desc()).first()
    
    if not offboarding:
        return jsonify({"success": False, "message": "No offboarding record available."})

    data = {
        "success": True,
        "driver_name": driver.name,
        "driver_iqama": driver.iqaama_number,
        "requested_by": offboarding.requested_by.name if offboarding.requested_by else "N/A",
        "requested_at": offboarding.requested_at.strftime("%Y-%m-%d %H:%M:%S") if offboarding.requested_at else "N/A",
        "ops_supervisor": {
            "note": offboarding.ops_supervisor_note or "",
            "time": offboarding.ops_supervisor_cleared_at.strftime("%Y-%m-%d %H:%M:%S") if offboarding.ops_supervisor_cleared_at else None
        },
        "fleet": {
            "note": offboarding.fleet_damage_report or "",
            "time": offboarding.fleet_cleared_at.strftime("%Y-%m-%d %H:%M:%S") if offboarding.fleet_cleared_at else None,
            "extra": f"Damage Cost: {offboarding.fleet_damage_cost}" if offboarding.fleet_damage_cost else ""
        },
        "finance": {
            "note": offboarding.finance_note or "",
            "time": offboarding.finance_cleared_at.strftime("%Y-%m-%d %H:%M:%S") if offboarding.finance_cleared_at else None,
            "extra": f"Adjustments: {offboarding.finance_adjustments}" if offboarding.finance_adjustments else ""
        },
        "hr": {
            "note": offboarding.hr_note or "",
            "time": offboarding.hr_cleared_at.strftime("%Y-%m-%d %H:%M:%S") if offboarding.hr_cleared_at else None
        }
    }

    return jsonify(data)

