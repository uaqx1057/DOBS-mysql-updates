from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models import Driver, Offboarding, User
from extensions import db, mail 
from flask_mail import Message
from datetime import datetime
from werkzeug.exceptions import BadRequest
from utils.email_utils import send_password_change_email 
from werkzeug.security import check_password_hash, generate_password_hash

ops_manager_bp = Blueprint("ops_manager", __name__)

@ops_manager_bp.route("/dashboard")
@login_required
def dashboard_ops():
    if current_user.role != "OpsManager":
        flash("Access denied. Ops Manager role required.", "danger")
        return redirect(url_for("auth.login"))

    # --- Language handling ---
    from flask import session
    lang = session.get("lang", "en")

    # --- Fetch data ---
    drivers = Driver.query.filter_by(onboarding_stage="Ops Manager").all()
    fully_onboarded_drivers = Driver.query.filter(Driver.onboarding_stage == "Completed").all()

    # Drivers with offboarding requested by Ops Coordinator

    offboarding_drivers = (
        Driver.query
        .filter_by(offboard_request=True)
        .order_by(Driver.full_name.asc())
        .all()
    )

    # --- Select template based on language ---
    template = "rtl_dashboard_ops.html" if lang == "ar" else "dashboard_ops.html"

    rejected = Driver.query.filter_by(onboarding_stage="Rejected").order_by(Driver.full_name.asc()).all()


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
            driver_iqama = driver.iqama_number or "N/A"
            driver_iqama_expiry = driver.iqama_expiry_date.strftime("%Y-%m-%d") if driver.iqama_expiry_date else "N/A"
            driver_city = driver.city or "N/A"
            driver_mobile = driver.mobile_number or "N/A"
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
                        <h2 style="color: #004aad;">Driver Onboarding System</h2>
                        <p>Dear HR Team,</p>
                        <p>A driver has been approved by the Operations Manager and is ready for HR processing:</p>
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
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Iqama Expiry</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_iqama_expiry}</td>
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
                        <p>Please log in to the HR dashboard to continue processing.</p>
                    </div>
        
                    <hr style="margin: 30px 0;">
        
                    <!-- Arabic RTL -->
                    <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                        <h2 style="color: #004aad;">نظام إدخال السائقين</h2>
                        <p>عزيزي فريق الموارد البشرية،</p>
                        <p>تمت الموافقة على السائق من قبل مدير العمليات وهو جاهز للمعالجة من قبل الموارد البشرية:</p>
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
                                <td style="padding: 8px; border: 1px solid #ddd;">تاريخ انتهاء الإقامة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver_iqama_expiry}</td>
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
                        <p>يرجى تسجيل الدخول إلى لوحة الموارد البشرية لمتابعة المعالجة.</p>
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

    flash(f"✅ {driver.full_name} approved and forwarded to HR.", "success")
    return redirect(url_for("ops_manager.dashboard_ops"))


# -------------------------
# Reject Driver
# -------------------------
@ops_manager_bp.route("/reject_driver/<int:driver_id>", methods=["POST"])
@login_required
def reject_driver(driver_id):
    """
    Reject driver at Ops Manager stage and notify Ops Coordinators via email.
    """
    if current_user.role != "OpsManager":
        flash("Access denied. Ops Manager role required.", "danger")
        return redirect(url_for("auth.login"))

    driver = Driver.query.get_or_404(driver_id)

    # Validate stage
    if driver.onboarding_stage != "Ops Manager":
        flash(f"Driver is not in Ops Manager stage (current: {driver.onboarding_stage}).", "warning")
        return redirect(url_for("ops_manager.dashboard_ops"))

    # Get rejection reason
    reject_reason = request.form.get("reject_reason", "").strip() or "No reason provided"

    # Update driver record
    driver.onboarding_stage = "Rejected"
    driver.ops_manager_approved = False
    driver.ops_manager_rejected = True
    driver.ops_manager_rejected_at = datetime.utcnow()
    driver.ops_manager_reject_reason = reject_reason

    # Save changes
    try:
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        current_app.logger.exception("Failed to reject driver in Ops Manager")
        flash("An internal error occurred while rejecting the driver. Please try again.", "danger")
        return redirect(url_for("ops_manager.dashboard_ops"))

    # ----------------------------
    # Send email to all Ops Coordinators
    # ----------------------------
    try:
        coordinators = User.query.filter_by(role="OpsCoordinator").all()
        recipients = [c.email for c in coordinators if c.email]

        if recipients:
            msg = Message(
                subject=f"Driver Rejected: {driver.full_name} | تم رفض السائق",
                recipients=recipients,
                sender=current_app.config.get("MAIL_DEFAULT_SENDER")
            )

            driver_name = driver.full_name
            msg.html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333; padding: 20px; background: #f8f9fa;">
                <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px;">
                    <!-- English -->
                    <div style="text-align: left;">
                        <h2>Driver Onboarding System</h2>
                        <p>Dear Ops Coordinator,</p>
                        <p>The driver <strong>{driver_name}</strong> has been rejected by the Ops Manager.</p>
                        <p><strong>Reason:</strong> {reject_reason}</p>
                    </div>
                    <hr>
                    <!-- Arabic -->
                    <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma;">
                        <h2>نظام إدخال السائقين</h2>
                        <p>عزيزي منسق العمليات،</p>
                        <p>تم رفض السائق <strong>{driver_name}</strong> من قبل مدير العمليات.</p>
                        <p><strong>السبب:</strong> {reject_reason}</p>
                    </div>
                </div>
            </body>
            </html>
            """
            mail.send(msg)
            flash(f"❌ {driver_name} has been rejected and email notification sent.", "success")
        else:
            flash(f"❌ {driver_name} has been rejected, but no coordinator emails found.", "warning")

    except Exception as e:
        current_app.logger.exception("Failed to send rejection email")
        flash(f"❌ {driver_name} has been rejected, but email could not be sent.", "warning")

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
        flash(f"Offboarding already requested for {driver.full_name}.", "info")
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
            driver_iqama = driver.iqama_number or "N/A"
            driver_city = driver.city or "N/A"
            driver_mobile = driver.mobile_number or "N/A"
            
            msg = Message(
                subject=f"Offboarding Requested: {driver.full_name} | تم طلب إنهاء خدمات السائق",
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
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.full_name}</td>
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
                        <p>Please log in to the dashboard to start the clearance process.</p>
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
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.full_name}</td>
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
                        <p>يرجى تسجيل الدخول إلى لوحة التحكم لبدء عملية إنهاء الخدمة.</p>
                    </div>
        
                </div>
            </body>
            </html>
            """
        
            mail.send(msg)
    except Exception as e:
        print("[EMAIL ERROR]", e)

    flash(f"Offboarding requested for {driver.full_name}.", "success")
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
            driver_iqama = driver.iqama_number or "N/A"
            driver_city = driver.city or "N/A"
            driver_mobile = driver.mobile_number or "N/A"
        
            msg = Message(
                subject=f"Offboarding Requested: {driver.full_name} | تم طلب إنهاء خدمات السائق",
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
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.full_name}</td>
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
                        <p>Please log in to the dashboard to start the clearance process.</p>
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
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.full_name}</td>
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
                        <p>يرجى تسجيل الدخول إلى لوحة التحكم لبدء عملية إنهاء الخدمة.</p>
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

    # Get optional reason from form
    reason = request.form.get("reason", "").strip()

    # Reset offboarding fields
    driver.offboard_request = False
    driver.offboard_requested_by = None
    driver.offboard_reason = None
    driver.offboard_requested_at = None

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("Failed to reject offboarding request.")
        flash("An error occurred. Try again.", "danger")
        return redirect(url_for("ops_manager.dashboard_ops"))

    # Notify Ops Coordinator who requested it
    try:
        from models import User
        if driver.offboard_requested_by:
            coordinator = User.query.filter_by(username=driver.offboard_requested_by).first()
            if coordinator and coordinator.email:
                driver_iqama = driver.iqama_number or "N/A"
                driver_city = driver.city or "N/A"
            
                msg = Message(
                    subject=f"Offboarding Request Rejected: {driver.full_name} | تم رفض طلب إنهاء الخدمة",
                    recipients=[coordinator.email]
                )
            
                msg.html = f"""
                <html>
                <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
            
                        <!-- English LTR -->
                        <div style="text-align: left;">
                            <h2 style="color: #004aad;">Driver Onboarding System</h2>
                            <p>Dear {coordinator.name or coordinator.username},</p>
                            <p>The offboarding request for the following driver has been <strong>rejected</strong> by the Ops Manager:</p>
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
                                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>City</strong></td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{driver_city}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>Reason</strong></td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{reason or 'No reason provided.'}</td>
                                </tr>
                            </table>
                            <p>Please log in to review other drivers.</p>
                        </div>
            
                        <hr style="margin: 30px 0;">
            
                        <!-- Arabic RTL -->
                        <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                            <h2 style="color: #004aad;">نظام إدخال السائقين</h2>
                            <p>عزيزي {coordinator.name or coordinator.username}،</p>
                            <p>تم <strong>رفض</strong> طلب إنهاء الخدمة للسائق التالي من قبل مدير العمليات:</p>
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
                                    <td style="padding: 8px; border: 1px solid #ddd;">المدينة</td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{driver_city}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;">السبب</td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{reason or 'لا يوجد سبب محدد'}</td>
                                </tr>
                            </table>
                            <p>يرجى تسجيل الدخول لمراجعة السائقين الآخرين.</p>
                        </div>
            
                    </div>
                </body>
                </html>
                """
            
                mail.send(msg)

    except Exception as e:
        current_app.logger.exception("Failed to send rejection email to coordinator.")
        flash("Offboarding request rejected, but notification email failed.", "warning")

    flash(f"❌ Offboarding request for {driver.full_name} has been rejected.", "success")
    return redirect(url_for("ops_manager.dashboard_ops"))
