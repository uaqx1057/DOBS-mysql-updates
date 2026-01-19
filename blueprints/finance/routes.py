import os
import re
from datetime import datetime, date, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Message
from sqlalchemy import exists
from extensions import db, mail
from models import Driver, User, Offboarding
from utils.email_utils import send_password_change_email

finance_bp = Blueprint("finance", __name__)

# -------------------------
# Config
# -------------------------
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def make_safe_filename(driver, prefix, filename):
    """Sanitize uploaded filenames."""
    ext = filename.rsplit(".", 1)[1].lower()
    safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", driver.name.strip())
    safe_iqama = re.sub(r"[^0-9]", "", driver.iqaama_number or "")
    return f"{prefix}_{safe_name}_{safe_iqama}.{ext}"

# -------------------------
# Helper functions
# -------------------------
def driver_to_dict(driver):
    return {
        "id": driver.id,
        "name": driver.name,
        "iqaama_number": driver.iqaama_number,
        "iqaama_expiry": driver.iqaama_expiry.isoformat() if driver.iqaama_expiry else None,
        "onboarding_stage": driver.onboarding_stage,
        "absher_number": driver.absher_number,
        "nationality": driver.nationality,
        "previous_sponsor_number": driver.previous_sponsor_number,
        "iqama_card_upload": driver.iqama_card_upload,
        "qiwa_transfer_approved": driver.qiwa_transfer_approved,
        "ops_manager_approved_at": driver.ops_manager_approved_at,
        "hr_approved_at": driver.hr_approved_at,
        "ops_supervisor_approved_at": driver.ops_supervisor_approved_at,
        "fleet_manager_approved_at": driver.fleet_manager_approved_at,
        "saudi_driving_license": driver.saudi_driving_license,
        "issued_mobile_number": driver.issued_mobile_number,
        "issued_device_id": driver.issued_device_id,
        "mobile_issued": driver.mobile_issued,
        "assignment_date": driver.assignment_date,
        "transfer_fee_paid": driver.transfer_fee_paid,
        "transfer_fee_amount": driver.transfer_fee_amount,
        "transfer_fee_paid_at": driver.transfer_fee_paid_at,
        "car_details": driver.car_details,
        "finance_approved_at": driver.finance_approved_at,
        "transfer_fee_paid": driver.transfer_fee_paid,
        "transfer_fee_amount": driver.transfer_fee_amount,
        "transfer_fee_receipt": driver.transfer_fee_receipt,
        "tamm_authorization_ss": driver.tamm_authorization_ss,
        "sponsorship_transfer_proof": driver.sponsorship_transfer_proof,
        "driver_type_id": driver.driver_type_id,

    }
 
def offboarding_to_dict(off):
    return {
        "id": off.id,
        "driver_name": off.driver.name,
        "driver_iqama": off.driver.iqaama_number,
        "status": off.status,
        "requested_at": off.requested_at.strftime("%Y-%m-%d %H:%M") if off.requested_at else None,
    }

# -------------------------
# Finance Dashboard
# -------------------------
# -------------------------
# Finance Dashboard
# -------------------------
@finance_bp.route("/dashboard")
@login_required
def dashboard_finance():
    if current_user.role != "FinanceManager":
        flash("Access denied. Finance Manager role required.", "danger")
        return redirect(url_for("auth.login"))

    from flask import session
    lang = session.get("lang", "en")

    # -------------------------
    # Fetch data
    # -------------------------
    pending_drivers = Driver.query.filter_by(onboarding_stage="Finance").all()
    completed_drivers = Driver.query.filter(
        Driver.onboarding_stage == "Completed",
        ~exists().where(Offboarding.driver_id == Driver.id)
    ).all()

    offboarding_requests = Offboarding.query.join(Offboarding.driver).filter(
        Offboarding.status == "Finance"
    ).order_by(Offboarding.requested_at.desc()).all()

    total_drivers = len(pending_drivers)
    total_users = len(offboarding_requests)

    # Choose template based on language
    template = "rtl_dashboard_finance.html" if lang == "ar" else "dashboard_finance.html"

    return render_template(
        template,
        pending_drivers=pending_drivers,
        completed_drivers=completed_drivers,
        offboarding_requests=offboarding_requests,
        datetime=datetime,
        total_drivers=total_drivers,
        total_users=total_users,
        user=current_user,
        lang=lang
    )

# -------------------------
# Approve Driver
# -------------------------
@finance_bp.route("/approve_driver/<int:driver_id>", methods=["POST"])
@login_required
def approve_driver(driver_id):
    if current_user.role != "FinanceManager":
        flash("Access denied. Finance Manager role required.", "danger")
        return redirect(url_for("auth.login"))

    driver = Driver.query.get_or_404(driver_id)

    # Collect form data
    driver.transfer_fee_paid = bool(request.form.get("transfer_fee_paid"))
    amount = request.form.get("transfer_fee_amount")
    driver.transfer_fee_amount = float(amount) if amount else None

    # Validate payment date
    paid_at_str = request.form.get("transfer_fee_paid_at")
    if paid_at_str:
        try:
            if "T" in paid_at_str:
                paid_at = datetime.strptime(paid_at_str, "%Y-%m-%dT%H:%M")
            else:
                paid_at = datetime.strptime(paid_at_str, "%Y-%m-%d")

            if paid_at.date() > date.today():
                flash("❌ Transfer fee payment date cannot be in the future.", "danger")
                return redirect(url_for("finance.dashboard_finance"))

            driver.transfer_fee_paid_at = paid_at
        except ValueError:
            flash("❌ Invalid date format for transfer fee payment.", "danger")
            return redirect(url_for("finance.dashboard_finance"))

    # Handle file upload
    file = request.files.get("transfer_fee_receipt")
    if file and file.filename:
        if not allowed_file(file.filename):
            flash("❌ Invalid file type. Allowed: JPG, JPEG, PNG, PDF.", "danger")
            return redirect(url_for("finance.dashboard_finance"))

        upload_folder = current_app.config.get("UPLOAD_FOLDER") or UPLOAD_FOLDER
        os.makedirs(upload_folder, exist_ok=True)

        filename = make_safe_filename(driver, "transfer_receipt", file.filename)
        file.save(os.path.join(upload_folder, secure_filename(filename)))
        driver.transfer_fee_receipt = filename

    # Mark driver as finance approved
    driver.transfer_fee_paid = True
    driver.transfer_fee_paid_at = datetime.utcnow()
    driver.finance_approved_at = datetime.utcnow()
    driver.onboarding_stage = "HR Final"

    try:
        db.session.commit()
        flash(f"✅ Driver {driver.name} has been financially cleared.", "success")

        # Send notifications
        recipients = [u.email for u in User.query.filter(User.role.in_(["HR"])).all() if u.email]
        if recipients:
            msg = Message(
                subject=f"Driver Transfer Fees Paid | تم دفع رسوم تحويل السائق: {driver.name}",
                recipients=recipients
            )

            msg.html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">

                    <!-- English -->
                    <div style="text-align: left;">
                        <h2 style="color: #713183;">Driver Onboarding System</h2>
                        <p>Dear HR Team,</p>
                        <p>The transfer fees for the following driver have been paid and the driver is now ready for HR processing:</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Driver Name</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Iqaama Number</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.iqaama_number}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Iqaama Expiry</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.iqaama_expiry}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>City</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.city}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Personal Mobile</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.absher_number}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Approved At (UTC)</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.finance_approved_at}</td>
                            </tr>
                        </table>
                        <p>Please log in to the HR dashboard to continue processing: 
                        <a href="https://dobs.dobs.cloud/login" target="_blank">HR Dashboard</a></p>
                    </div>

                    <hr style="margin: 30px 0;">

                    <!-- Arabic -->
                    <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                        <h2 style="color: #713183;">نظام إدخال السائقين</h2>
                        <p>عزيزي فريق الموارد البشرية،</p>
                        <p>تمت دفع رسوم تحويل السائق التالي وهو الآن جاهز للمعالجة من قبل الموارد البشرية:</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">اسم السائق</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">رقم الإقامة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.iqaama_number}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">تاريخ انتهاء الإقامة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.iqaama_expiry}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">المدينة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.city}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">الهاتف الشخصي</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.absher_number}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">تمت الموافقة في (UTC)</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.finance_approved_at}</td>
                            </tr>
                        </table>
                        <p>يرجى تسجيل الدخول إلى لوحة الموارد البشرية لمتابعة المعالجة: 
                        <a href="https://dobs.dobs.cloud/login" target="_blank">لوحة الموارد البشرية</a></p>
                    </div>

                    <hr style="margin: 30px 0;">
                    <p style="text-align:center;">Regards / مع التحية,<br>Finance Team / فريق المالية</p>

                </div>
            </body>
            </html>
            """

            mail.send(msg)



    except Exception as e:
        db.session.rollback()
        flash(f"❌ Error saving finance data: {str(e)}", "danger")

    return redirect(url_for("finance.dashboard_finance"))



# -------------------------
# Change Password
# -------------------------
@finance_bp.route("/change_password", methods=["POST"])
@login_required
def change_password():
    if current_user.role != "FinanceManager":
        flash("Access denied. Finance Manager role required.", "danger")
        return redirect(url_for("auth.login"))

    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not all([current_password, new_password, confirm_password]):
        flash("Please fill all password fields.", "danger")
        return redirect(url_for("finance.dashboard_finance"))

    if not check_password_hash(current_user.password, current_password):
        flash("Current password is incorrect.", "danger")
        return redirect(url_for("finance.dashboard_finance"))

    if new_password != confirm_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for("finance.dashboard_finance"))

    try:
        current_user.password = generate_password_hash(new_password)
        db.session.commit()

        if send_password_change_email(current_user, new_password):
            flash("✅ Password updated and email notification sent.", "success")
        else:
            flash("✅ Password updated, but email could not be sent.", "warning")
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(f"[FINANCE] Failed to change password: {e}")
        flash("Could not update password right now. Try again later.", "danger")

    return redirect(url_for("finance.dashboard_finance"))

# -------------------------
# Clear Offboarding
# -------------------------
@finance_bp.route("/offboarding/clear/<int:offboarding_id>", methods=["POST"])
@login_required
def clear_offboarding(offboarding_id):
    if current_user.role != "FinanceManager":
        flash("Access denied. Finance Manager role required.", "danger")
        return redirect(url_for("finance.dashboard_finance"))

    record = Offboarding.query.get_or_404(offboarding_id)

    try:
        record.finance_cleared = True
        record.finance_cleared_at = datetime.utcnow()
        record.finance_adjustments = float(request.form.get("finance_adjustments") or 0)
        record.finance_note = request.form.get("finance_note", "").strip()

        # Handle invoice upload
        file = request.files.get("finance_invoice_file")
        if file and file.filename:
            if not allowed_file(file.filename):
                flash("❌ Invalid file type.", "danger")
                return redirect(url_for("finance.dashboard_finance"))

            upload_folder = current_app.config.get("UPLOAD_FOLDER") or UPLOAD_FOLDER
            os.makedirs(upload_folder, exist_ok=True)

            filename = make_safe_filename(record.driver, "offboarding_invoice", file.filename)
            file.save(os.path.join(upload_folder, secure_filename(filename)))
            record.finance_invoice_file = filename

        record.status = "HR"
        db.session.commit()

        flash(f"✅ Driver {record.driver.name} has been sent to HR successfully!", "success")

        # Notify HR
        recipients = [u.email for u in User.query.filter_by(role="HR").all() if u.email]
        if recipients:
            msg = Message(
                subject="Driver Approved & Ready for HR | تم الموافقة على السائق وجاهز للموارد البشرية",
                recipients=recipients
            )

            msg.html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">

                    <!-- English -->
                    <div style="text-align: left;">
                        <h2 style="color: #713183;">Driver Offboarding System</h2>
                        <p>Dear HR Team,</p>
                        <p>The following driver has been financially cleared and is ready for HR offboarding processing:</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Driver Name</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{record.driver.name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Finance Notes</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{record.finance_note or 'N/A'}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Adjustments</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{record.finance_adjustments or 'None'}</td>
                            </tr>
                        </table>
                        <p>Please log in to the HR dashboard to continue offboarding: 
                        <a href="https://dobs.dobs.cloud/login" target="_blank">HR Dashboard</a></p>
                    </div>

                    <hr style="margin: 30px 0;">

                    <!-- Arabic -->
                    <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                        <h2 style="color: #713183;">نظام إنهاء خدمات السائقين</h2>
                        <p>عزيزي فريق الموارد البشرية،</p>
                        <p>تمت الموافقة المالية للسائق التالي وهو جاهز للمعالجة من قبل الموارد البشرية:</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">اسم السائق</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{record.driver.name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">ملاحظات المالية</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{record.finance_note or 'N/A'}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">التعديلات</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{record.finance_adjustments or 'None'}</td>
                            </tr>
                        </table>
                        <p>يرجى تسجيل الدخول إلى لوحة الموارد البشرية لمتابعة إنهاء الخدمة: 
                        <a href="https://dobs.dobs.cloud/login" target="_blank">لوحة الموارد البشرية</a></p>
                    </div>

                    <hr style="margin: 30px 0;">
                    <p style="text-align:center;">Regards / مع التحية,<br>Finance Team / فريق المالية</p>

                </div>
            </body>
            </html>
            """

            mail.send(msg)



    except Exception as e:
        db.session.rollback()
        flash(f"❌ Error processing offboarding clearance: {str(e)}", "danger")

    return redirect(url_for("finance.dashboard_finance"))
  