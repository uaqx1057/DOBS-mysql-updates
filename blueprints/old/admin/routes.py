from flask import Blueprint, render_template, request, redirect, url_for, flash, session , current_app
from flask_login import login_required, current_user
from models import Offboarding, User, Driver
from extensions import db, mail
from flask_mail import Mail,Message
from datetime import datetime
import os
from utils.email_utils import send_password_change_email 
from werkzeug.security import check_password_hash, generate_password_hash


# âœ… Blueprint for SuperAdmin/Admin
admin_bp = Blueprint("admin", __name__)

UPLOAD_FOLDER = "static/uploads"

# -------------------------
# Language Helper
# -------------------------
def set_lang():
    """
    Determine current language:
    - URL parameter 'lang' (priority)
    - session (fallback)
    Defaults to 'en'
    Returns: lang_code, is_rtl
    """
    lang = request.args.get("lang") or session.get("lang") or "en"
    session["lang"] = lang
    rtl = True if lang == "ar" else False
    return lang, rtl


def safe_date(value):
    """Return formatted date if value is datetime/date, else return value or None."""
    if not value:
        return None
    try:
        return value.strftime("%Y-%m-%d")
    except Exception:
        return value  # already a string

def safe_datetime(value):
    """Return formatted datetime if value is datetime, else return value or None."""
    if not value:
        return None
    try:
        return value.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return value

# -------------------------
# SuperAdmin Dashboard
# -------------------------
@admin_bp.route("/")
@login_required
def dashboard():
    if current_user.role != "SuperAdmin":
        return "Forbidden", 403

    # --------------------------
    # Users
    # --------------------------
    users = User.query.filter(User.id != current_user.id).all()
    users_dicts = [
        {
            "id": u.id,
            "username": u.username,
            "name": u.name,
            "designation": u.designation,
            "branch_city": u.branch_city,
            "email": u.email,
            "role": u.role,
        }
        for u in users
    ]

    lang, rtl = set_lang()
    template = "rtl_dashboard.html" if rtl else "dashboard.html"
    # --------------------------
    # Drivers & Offboarding
    # --------------------------
    drivers = Driver.query.all()
    offboarding_records = Offboarding.query.all()

    total_drivers = int(len(drivers) or 0)
    total_users = int(len(users) or 0)

    # Separate offboarding by status
    pending_offboarding_records = [o for o in offboarding_records if o.status != "Completed"]
    completed_offboarding_records = [o for o in offboarding_records if o.status == "Completed"]

    pending_offboarding_drivers = [o.driver for o in pending_offboarding_records]
    completed_offboarding_drivers = [o.driver for o in completed_offboarding_records]

    # --------------------------
    # Counts logic
    # --------------------------
    offboarded_ids = {o.driver_id for o in offboarding_records}

    # Pending onboarding = not yet completed
    total_pending_onboarded = int(sum(1 for d in drivers if d.onboarding_stage != "Completed") or 0)

    # Completed onboarding = completed but NOT offboarded
    total_completed_onboarded = int(
        sum(1 for d in drivers if d.onboarding_stage == "Completed" and d.id not in offboarded_ids)
    )

    # Offboarding counts
    total_pending_offboarded = int(len(pending_offboarding_drivers) or 0)
    total_completed_offboarded = int(len(completed_offboarding_drivers) or 0)

    # --------------------------
    # Helpers
    # --------------------------
    def safe_date(value):
        if not value:
            return None
        try:
            return value.strftime("%Y-%m-%d")
        except Exception:
            return value

    def safe_datetime(value):
        if not value:
            return None
        try:
            return value.strftime("%Y-%m-%d %H:%M")
        except Exception:
            return value

    # Get all offboarding driver IDs
    offboarded_ids = {o.driver_id for o in offboarding_records}

    # Update the function to accept optional offboarding record
    def serialize_driver(d, offboarding_record=None):
        return {
            "id": d.id,
            "full_name": d.full_name,
            "iqama_number": d.iqama_number,
            "iqama_expiry_date": safe_date(d.iqama_expiry_date),
            "saudi_driving_license": d.saudi_driving_license,
            "nationality": d.nationality,
            "mobile_number": d.mobile_number,
            "previous_sponsor_number": d.previous_sponsor_number,
            "iqama_card_upload": d.iqama_card_upload,
            "platform": [p.platform_name for p in d.platforms],
            "platform_id": d.platforms[0].id if d.platforms else None,
            "city": d.city,
            "car_details": d.car_details,
            "assignment_date": safe_date(d.assignment_date),
            "onboarding_stage": d.onboarding_stage,
            "offboarding_stage": offboarding_record.status if offboarding_record else "",
            "qiwa_contract_created": d.qiwa_contract_created,
            "sponsorship_transfer_status": d.sponsorship_transfer_status,
            "ops_manager_approved_at": safe_datetime(d.ops_manager_approved_at),
            "hr_approved_at": safe_datetime(d.hr_approved_at),
            "ops_supervisor_approved_at": safe_datetime(d.ops_supervisor_approved_at),
            "fleet_manager_approved_at": safe_datetime(d.fleet_manager_approved_at),
            "finance_approved_at": safe_datetime(d.finance_approved_at),
            "ops_manager_approved": d.ops_manager_approved,
            "hr_approved_by": d.hr_approved_by,
            "mobile_issued": bool(d.mobile_issued),
            "tamm_authorized": bool(d.tamm_authorized),
            "transfer_fee_paid": bool(d.transfer_fee_paid),
            "transfer_fee_amount": d.transfer_fee_amount,
            "transfer_fee_paid_at": safe_datetime(d.transfer_fee_paid_at),
            "transfer_fee_receipt": d.transfer_fee_receipt,
            "issued_mobile_number": d.issued_mobile_number,
            "issued_device_id": d.issued_device_id,
            "tamm_authorization_ss": d.tamm_authorization_ss,
            "sponsorship_transfer_proof": d.sponsorship_transfer_proof,
            "company_contract_file": d.company_contract_file, 
            "promissory_note_file": d.promissory_note_file, 
            "qiwa_contract_file": d.qiwa_contract_file,
            "fully_onboarded": d.onboarding_stage == "Completed",
            "in_offboarding": d.id in offboarded_ids
        }




    driver_dicts = [serialize_driver(d) for d in drivers]
    pending_offboarding_driver_dicts = [
        serialize_driver(o.driver, offboarding_record=o) for o in pending_offboarding_records
    ]
    completed_offboarding_driver_dicts = [
        serialize_driver(o.driver, offboarding_record=o) for o in completed_offboarding_records
    ]
    # âœ… Filter fully onboarded drivers who are NOT in offboarding
    fully_onboarded_only = [d for d in driver_dicts if d["fully_onboarded"] and not d["in_offboarding"]]

    # --------------------------
    # Render Dashboard
    # --------------------------
    return render_template(
        template,
        users=users_dicts,
        drivers=driver_dicts,
        fully_onboarded_drivers=fully_onboarded_only,  # âœ… new variable for tab
        total_users=total_users,
        total_drivers=total_drivers,
        total_pending_onboarded=total_pending_onboarded,
        total_completed_onboarded=total_completed_onboarded,
        total_pending_offboarded=total_pending_offboarded,
        total_completed_offboarded=total_completed_offboarded,
        pending_offboarding_drivers=pending_offboarding_driver_dicts,
        completed_offboarding_drivers=completed_offboarding_driver_dicts,
        lang=lang,
        rtl=rtl
    )

# -------------------------
# Add Driver (NEW)
# -------------------------
@admin_bp.route("/driver/add", methods=["POST"])
@login_required
def add_driver():
    if current_user.role != "SuperAdmin":
        flash("Access Denied", "danger")
        return redirect(url_for("admin.dashboard"))

    # Collect form data
    full_name = request.form.get("full_name")
    iqama_number = request.form.get("iqama_number")
    iqama_expiry_date = request.form.get("iqama_expiry_date")
    nationality = request.form.get("nationality")
    mobile_number = request.form.get("mobile_number")
    platform = request.form.get("platform")
    platform_id = request.form.get("platform_id")
    car_details = request.form.get("car_details")
    assignment_date = request.form.get("assignment_date")

    # Handle uploads safely
    iqama_card_upload = None
    if "iqama_card_upload" in request.files:
        file = request.files["iqama_card_upload"]
        if file.filename:
            filename = secure_filename(f"iqama_{datetime.utcnow().timestamp()}_{file.filename}")
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            iqama_card_upload = filename

    tamm_authorization_ss = None
    if "tamm_authorization_ss" in request.files:
        file = request.files["tamm_authorization_ss"]
        if file.filename:
            filename = secure_filename(f"tamm_{datetime.utcnow().timestamp()}_{file.filename}")
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            tamm_authorization_ss = filename

    new_driver = Driver(
        full_name=full_name,
        iqama_number=iqama_number,
        iqama_expiry_date=datetime.strptime(iqama_expiry_date, "%Y-%m-%d").date() if iqama_expiry_date else None,
        nationality=nationality,
        mobile_number=mobile_number,
        platform=platform,
        platform_id=platform_id,
        car_details=car_details,
        assignment_date=datetime.strptime(assignment_date, "%Y-%m-%d").date() if assignment_date else None,
        iqama_card_upload=iqama_card_upload,
        tamm_authorization_ss=tamm_authorization_ss,
    )

    db.session.add(new_driver)
    db.session.commit()

    flash(f"Driver {new_driver.full_name} added successfully.", "success")
    return redirect(url_for("admin.dashboard"))

# -------------------------
# Update Driver (Enhanced)
# -------------------------
@admin_bp.route("/driver/<int:driver_id>/update", methods=["POST"])
@login_required
def update_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)

    # Update fields
    driver.full_name = request.form.get("full_name", driver.full_name)
    driver.iqama_number = request.form.get("iqama_number", driver.iqama_number)
    driver.nationality = request.form.get("nationality", driver.nationality)
    driver.mobile_number = request.form.get("mobile_number", driver.mobile_number)
    driver.previous_sponsor_number = request.form.get("previous_sponsor_number", driver.previous_sponsor_number)
    driver.platform = request.form.get("platform", driver.platform)
    driver.platform_id = request.form.get("platform_id", driver.platform_id)
    driver.issued_mobile_number = request.form.get("issued_mobile_number", driver.issued_mobile_number)
    driver.issued_device_id = request.form.get("issued_device_id", driver.issued_device_id)
    driver.mobile_issued = request.form.get("mobile_issued") == "true"
    driver.car_details = request.form.get("car_details", driver.car_details)
    driver.tamm_authorized = request.form.get("tamm_authorized") == "true"
    driver.transfer_fee_paid = request.form.get("transfer_fee_paid") == "true"

    # Dates
    iqama_expiry_date = request.form.get("iqama_expiry_date")
    if iqama_expiry_date:
        driver.iqama_expiry_date = datetime.strptime(iqama_expiry_date, "%Y-%m-%d").date()

    assignment_date = request.form.get("assignment_date")
    if assignment_date:
        driver.assignment_date = datetime.strptime(assignment_date, "%Y-%m-%d").date()

    transfer_fee_paid_at = request.form.get("transfer_fee_paid_at")
    if transfer_fee_paid_at:
        driver.transfer_fee_paid_at = datetime.strptime(transfer_fee_paid_at, "%Y-%m-%dT%H:%M")

    driver.transfer_fee_amount = request.form.get("transfer_fee_amount") or None

    # File uploads
    if "tamm_authorization_ss" in request.files:
        file = request.files["tamm_authorization_ss"]
        if file.filename:
            filename = f"tamm_{datetime.utcnow().timestamp()}_{file.filename}"
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            driver.tamm_authorization_ss = filename

    if "transfer_fee_receipt" in request.files:
        file = request.files["transfer_fee_receipt"]
        if file.filename:
            filename = f"receipt_{datetime.utcnow().timestamp()}_{file.filename}"
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            driver.transfer_fee_receipt = filename

    db.session.commit()
    flash("Driver details updated successfully.", "success")
    return redirect(url_for("admin.dashboard"))

# -------------------------
# Delete Driver
# -------------------------
@admin_bp.route("/dashboard/driver/<int:driver_id>/delete", methods=["POST"])
@login_required
def delete_driver(driver_id):
    from app import db
    from models import Driver, Offboarding

    # Get the driver or 404 if not found
    driver = Driver.query.get_or_404(driver_id)

    try:
        # ðŸ§¹ First, delete all related offboarding records
        Offboarding.query.filter_by(driver_id=driver.id).delete()

        # ðŸ§¹ Now delete the driver
        db.session.delete(driver)
        db.session.commit()

        flash("Driver and related offboarding records deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting driver: {str(e)}", "danger")

    # Redirect back to admin dashboard
    return redirect(url_for("admin.dashboard"))

# -------------------------
# Add/Edit/Delete Users (unchanged)
# -------------------------
@admin_bp.route("/add_user", methods=["POST"])
@login_required
def add_user():
    if current_user.role != "SuperAdmin":
        return "Access Denied", 403

    username = request.form["username"]
    raw_password = request.form["password"]
    hashed_password = generate_password_hash(raw_password)
    role = request.form["role"]
    name = request.form["name"]
    designation = request.form["designation"]
    branch_city = request.form["branch_city"]
    email = request.form["email"]

    new_user = User(
        username=username,
        password=hashed_password,
        role=role,
        name=name,
        designation=designation,
        branch_city=branch_city,
        email=email
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to create user: {e}", "danger")
        return redirect(url_for("admin.dashboard"))

    # Send email notification
    # Send email notification
    try:
        msg = Message("Your Account Has Been Created | تم إنشاء حسابك", recipients=[email])
        msg.html = f"""
        <html dir="ltr" lang="en">
        <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                <div style="text-align: center; border-bottom: 3px solid #004aad; padding-bottom: 10px;">
                    <h2 style="color: #004aad;">iLab Information Technology</h2>
                    <p style="font-size: 14px; color: #777;">Account Notification</p>
                </div>

                <div style="margin-top: 20px;">
                    <p>Dear <strong>{name}</strong>,</p>
                    <p>We are pleased to inform you that your account has been successfully created.</p>
                    <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Username</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">{username}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Password</strong></td>
                            <td style="padding: 8px; border: 1px solid #ddd;">{raw_password}</td>
                        </tr>
                    </table>
                    <p>You can now log in to your account using the provided credentials on https://dobs.dobs.cloud/login.</p>

                    <p style="margin-top: 25px;">Best regards,<br><strong>iLab IT Support Team</strong></p>
                </div>

                <hr style="margin: 30px 0;">
                <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                    <p><strong>عزيزي {name}</strong>،</p>
                    <p>نود إعلامك بأنه تم إنشاء حسابك بنجاح.</p>
                    <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;">اسم المستخدم</td>
                            <td style="padding: 8px; border: 1px solid #ddd;">{username}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd;">كلمة المرور</td>
                            <td style="padding: 8px; border: 1px solid #ddd;">{raw_password}</td>
                        </tr>
                    </table>
                    <p>https://dobs.dobs.cloud/login يمكنك الآن تسجيل الدخول باستخدام بيانات الدخول أعلاه.</p>

                    <p style="margin-top: 25px;">مع أطيب التحيات،<br><strong>فريق دعم آي لاب لتقنية المعلومات</strong></p>
                </div>
            </div>
        </body>
        </html>
        """
        mail.send(msg)
    except Exception as e:
        flash(f"User created but email failed: {e}", "warning")

    flash("User created successfully and email sent.", "success")
    return redirect(url_for("admin.dashboard"))

# -------------------------
# Edit User
# -------------------------
@admin_bp.route("/edit_user/<int:user_id>", methods=["POST"])
@login_required
def edit_user(user_id):
    if current_user.role != "SuperAdmin":
        flash("Access Denied", "danger")
        return redirect(url_for("admin.dashboard"))

    user = User.query.get_or_404(user_id)
    user.username = request.form.get("username", user.username)
    user.name = request.form.get("name", user.name)
    user.designation = request.form.get("designation", user.designation)
    user.branch_city = request.form.get("branch_city", user.branch_city)
    user.email = request.form.get("email", user.email)
    user.role = request.form.get("role", user.role)

    db.session.commit()
    flash(f"User {user.username} updated successfully.", "success")
    return redirect(url_for("admin.dashboard"))

# -------------------------
# Delete User
# -------------------------
@admin_bp.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if current_user.role != "SuperAdmin":
        flash("Access Denied", "danger")
        return redirect(url_for("admin.dashboard"))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f"User {user.username} deleted successfully.", "success")
    return redirect(url_for("admin.dashboard"))

# -------------------------
# Change Password (for SuperAdmin)
# -------------------------
@admin_bp.route("/change_password", methods=["POST"])
@login_required
def change_password():
    """Allow SuperAdmin to change their password securely and send email notification."""
    if current_user.role != "SuperAdmin":
        flash("Access Denied", "danger")
        return redirect(url_for("admin.dashboard"))

    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not current_password or not new_password or not confirm_password:
        flash("Please fill all password fields.", "danger")
        return redirect(url_for("admin.dashboard"))

    if not check_password_hash(current_user.password, current_password):
        flash("Current password is incorrect.", "danger")
        return redirect(url_for("admin.dashboard"))

    if new_password != confirm_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for("admin.dashboard"))

    try:
        # Update password in database
        current_user.password = generate_password_hash(new_password)
        db.session.commit()

        # Send email notification using helper
        if send_password_change_email(current_user, new_password):
            flash("âœ… Password updated and email notification sent.", "success")
        else:
            flash("âœ… Password updated, but email could not be sent.", "warning")

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(f"[ADMIN] Failed to change password: {e}")
        flash("Could not update password right now. Try again later.", "danger")

    return redirect(url_for("admin.dashboard"))