from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, session , current_app
from flask_login import login_required, current_user
from models import Business, DriverBusinessIDS, Offboarding, db, Driver, User, BusinessID, BusinessDriver
from extensions import db, mail
from flask_mail import Message
from datetime import datetime
import os
from utils.email_utils import send_password_change_email 
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

# âœ… Blueprint for SuperAdmin/Admin
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

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

# -------------------------
# Date helpers
# -------------------------
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

# -------------------------
# SuperAdmin Dashboard
# -------------------------
@admin_bp.route("/", methods=["GET"])
@login_required
def dashboard():
    # Only SuperAdmin can access this
    if current_user.role != "SuperAdmin":
        return "Forbidden", 403

    # -------------------------
    # Users
    # -------------------------
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

    # -------------------------
    # Drivers and Offboarding
    # -------------------------
    drivers = Driver.query.all()
    offboarding_records = Offboarding.query.all()
    
    offboarded_ids = {o.driver_id for o in offboarding_records if o.status == "Completed"}
    in_offboarding_ids = {o.driver_id for o in offboarding_records if o.status != "Completed"}

    pending_offboarding_records = [o for o in offboarding_records if o.status != "Completed"]
    completed_offboarding_records = [o for o in offboarding_records if o.status == "Completed"]

    # -------------------------
    # Helper: serialize drivers
    # -------------------------
    def serialize_driver(d, offboarding_record=None):
        data = {
            "id": d.id,
            "name": d.name,
            "iqaama_number": d.iqaama_number,
            "iqaama_expiry": d.iqaama_expiry.isoformat() if d.iqaama_expiry else None,
            "nationality": d.nationality,
            "absher_number": d.absher_number,
            "previous_sponsor_number": d.previous_sponsor_number,
            "saudi_driving_license": bool(d.saudi_driving_license),
            "city": d.city,
            "car_details": d.car_details,
            "assignment_date": d.assignment_date.isoformat() if d.assignment_date else None,
            "issued_mobile_number": d.issued_mobile_number,
            "issued_device_id": d.issued_device_id,
            "mobile_issued": bool(d.mobile_issued),
            "qiwa_contract_created": bool(d.qiwa_contract_created),
            "company_contract_created": bool(d.company_contract_created),
            "qiwa_contract_status": d.qiwa_contract_status,
            "ops_manager_approved_at": d.ops_manager_approved_at.isoformat() if d.ops_manager_approved_at else None,
            "ops_supervisor_approved_at": d.ops_supervisor_approved_at.isoformat() if d.ops_supervisor_approved_at else None,
            "fleet_manager_approved_at": d.fleet_manager_approved_at.isoformat() if d.fleet_manager_approved_at else None,
            "finance_approved_at": d.finance_approved_at.isoformat() if d.finance_approved_at else None,
            "hr_approved_at": d.hr_approved_at.isoformat() if d.hr_approved_at else None,
            "transfer_fee_paid": bool(d.transfer_fee_paid),
            "transfer_fee_amount": float(d.transfer_fee_amount) if d.transfer_fee_amount else None,
            "transfer_fee_paid_at": d.transfer_fee_paid_at.isoformat() if d.transfer_fee_paid_at else None,
            "transfer_fee_receipt": d.transfer_fee_receipt,
            "sponsorship_transfer_proof": d.sponsorship_transfer_proof,
            "tamm_authorization_ss": d.tamm_authorization_ss,
            "tamm_authorized": bool(d.tamm_authorized),
            "sponsorship_transfer_status": d.sponsorship_transfer_status,
            "onboarding_stage": d.onboarding_stage,
            "company_contract_file": d.company_contract_file,
            "promissory_note_file": d.promissory_note_file,
            "qiwa_contract_file": d.qiwa_contract_file,
            "offboarding_stage": d.offboarding_stage or (offboarding_record.status if offboarding_record else None),
            "fully_onboarded": d.onboarding_stage == "Completed",
            "in_offboarding": d.id in in_offboarding_ids,
            "offboard_requested_by":d.offboard_requested_by if offboarding_record else None,
            "offboard_reason": d.offboard_reason if offboarding_record else None,
            "offboard_requested_at": safe_datetime(offboarding_record.requested_at) if offboarding_record else None,
        }

        # Include offboarding record(s) as a list
        records = []
        if offboarding_record:
            records.append({
                "id": offboarding_record.id,
                "driver_id": offboarding_record.driver_id,
                "requested_by_id": offboarding_record.requested_by_id,
                "offboarding_requested_at": offboarding_record.requested_at.isoformat() if offboarding_record.requested_at else None,
                "status": offboarding_record.status,
                "ops_supervisor_cleared": offboarding_record.ops_supervisor_cleared,
                "ops_supervisor_cleared_at": offboarding_record.ops_supervisor_cleared_at.isoformat() if offboarding_record.ops_supervisor_cleared_at else None,
                "ops_supervisor_note": offboarding_record.ops_supervisor_note or "",
                "fleet_cleared": offboarding_record.fleet_cleared,
                "fleet_cleared_at": offboarding_record.fleet_cleared_at.isoformat() if offboarding_record.fleet_cleared_at else None,
                "fleet_damage_report": offboarding_record.fleet_damage_report or "",
                "fleet_damage_cost": offboarding_record.fleet_damage_cost or 0.0,
                "finance_cleared": offboarding_record.finance_cleared,
                "finance_cleared_at": offboarding_record.finance_cleared_at.isoformat() if offboarding_record.finance_cleared_at else None,
                "finance_note": offboarding_record.finance_note or "",
                "hr_cleared": offboarding_record.hr_cleared,
                "hr_cleared_at": offboarding_record.hr_cleared_at.isoformat() if offboarding_record.hr_cleared_at else None,
                "hr_note": offboarding_record.hr_note or "",
                "tamm_revoked": offboarding_record.tamm_revoked,
                "tamm_revoked_at": offboarding_record.tamm_revoked_at.isoformat() if offboarding_record.tamm_revoked_at else None,
                "company_contract_cancelled": offboarding_record.company_contract_cancelled,
                "qiwa_contract_cancelled": offboarding_record.qiwa_contract_cancelled,
                "salary_paid": offboarding_record.salary_paid,
                "updated_at": offboarding_record.updated_at.isoformat() if offboarding_record.updated_at else None,
            })
        data["records"] = records
        return data


    # -------------------------
    # Serialize drivers
    # -------------------------
    driver_dicts = [serialize_driver(d) for d in drivers]
    pending_offboarding_driver_dicts = [serialize_driver(o.driver, offboarding_record=o) for o in pending_offboarding_records]
    completed_offboarding_driver_dicts = [serialize_driver(o.driver, offboarding_record=o) for o in completed_offboarding_records]
    fully_onboarded_only = [
        serialize_driver(d) 
        for d in drivers 
        if d.onboarding_stage == "Completed" and d.id not in in_offboarding_ids
    ]

    # -------------------------
    # Businesses and available IDs
    # -------------------------
    businesses = Business.query.order_by(Business.name).all()
    assigned_ids_subq = db.session.query(BusinessDriver.business_id).subquery()
    all_businesses = []
    for b in businesses:
        available_ids = (
            db.session.query(BusinessID)
            .filter(
                BusinessID.business_id == b.id,
                BusinessID.is_active == True,
                ~BusinessID.id.in_(assigned_ids_subq.select())
            ).all()
        )
        all_businesses.append({
            "id": b.id,
            "name": b.name,
            "available_ids": [{"id": bid.id, "value": bid.value} for bid in available_ids]
        })

    # -------------------------
    # Language / RTL
    # -------------------------
    lang = request.args.get("lang") or session.get("lang") or "en"
    session["lang"] = lang
    rtl = True if lang == "ar" else False
    template = "rtl_dashboard.html" if rtl else "dashboard.html"

    # -------------------------
    # Render template
    # -------------------------
    return render_template(
        template,
        users=users_dicts,
        drivers=driver_dicts,
        fully_onboarded_drivers=fully_onboarded_only,
        pending_offboarding_drivers=pending_offboarding_driver_dicts,
        completed_offboarding_drivers=completed_offboarding_driver_dicts,
        total_users=len(users),
        total_drivers=len(drivers),
        total_pending_onboarded=sum(1 for d in drivers if d.onboarding_stage != "Completed"),
        total_completed_onboarded=sum(1 for d in drivers if d.onboarding_stage == "Completed" and d.id not in offboarded_ids),
        total_pending_offboarded=len(pending_offboarding_driver_dicts),
        total_completed_offboarded=len(completed_offboarding_driver_dicts),
        lang=lang,
        rtl=rtl,
        all_businesses=all_businesses
    )

# -------------------------
# Get Driver JSON       
# -------------------------
@admin_bp.route("/driver/<int:driver_id>/json")
@login_required
def driver_json(driver_id):
    if current_user.role != "Admin":
        return {"error": "Access denied"}, 403

    driver = Driver.query.get_or_404(driver_id)

    assigned = []
    for bd in driver.business_drivers:
        assigned.append({
            "business_id": bd.business_id,
            "platform_id": getattr(bd, "platform_id", None)
        })

    driver_data = {
        "id": driver.id,
        "name": driver.name,
        "iqaama_number": driver.iqaama_number,
        "iqaama_expiry": driver.iqaama_expiry.isoformat() if driver.iqaama_expiry else None,
        "nationality": driver.nationality,
        "absher_number": driver.absher_number,
        "previous_sponsor_number": driver.previous_sponsor_number,
        "saudi_driving_license": driver.saudi_driving_license,
        "assigned_businesses": assigned,
        "issued_mobile_number": driver.issued_mobile_number,
        "issued_device_id": driver.issued_device_id,
        "mobile_issued": driver.mobile_issued,
        "car_details": driver.car_details,
        "assignment_date": driver.assignment_date.isoformat() if driver.assignment_date else None,
        "tamm_authorized": driver.tamm_authorized,
        "transfer_fee_paid": driver.transfer_fee_paid,
        "transfer_fee_amount": driver.transfer_fee_amount,
        "transfer_fee_paid_at": driver.transfer_fee_paid_at.isoformat() if driver.transfer_fee_paid_at else None,
        "qiwa_contract_status": driver.qiwa_contract_status,
        "onboarding_stage": driver.onboarding_stage,
        # file URLs
        "tamm_authorization_ss_url": getattr(driver, "tamm_authorization_ss_url", ""),
        "transfer_fee_receipt_url": getattr(driver, "transfer_fee_receipt_url", ""),
        "sponsorship_transfer_proof_url": getattr(driver, "sponsorship_transfer_proof_url", ""),
        "company_contract_file_url": getattr(driver, "company_contract_file_url", ""),
        "promissory_note_file_url": getattr(driver, "promissory_note_file_url", ""),
        "qiwa_contract_file_url": getattr(driver, "qiwa_contract_file_url", "")
    }

    return driver_data
# -------------------------
# Update Existing Driver
# -------------------------
@admin_bp.route("/driver/<int:driver_id>/update", methods=["POST"])
@login_required
def update_driver(driver_id):
    if current_user.role != "Admin":
        flash("Access denied", "danger")
        return redirect(url_for("auth.login"))

    driver = Driver.query.get_or_404(driver_id)

    # Get all form data
    form = request.form

    try:
        # -------------------------
        # Update basic fields
        # -------------------------
        bool_fields = ["saudi_driving_license", "mobile_issued", "tamm_authorized", "transfer_fee_paid"]
        date_fields = ["iqaama_expiry", "assignment_date", "transfer_fee_paid_at"]

        for field in form.keys():
            value = form.get(field)
            if field in bool_fields:
                setattr(driver, field, value == "true")
            elif field in date_fields:
                setattr(driver, field, value or None)
            else:
                setattr(driver, field, value)

        # -------------------------
        # Update Business assignments
        # -------------------------
        business_ids = request.form.getlist("business_id[]")
        platform_ids = request.form.getlist("platform_id[]")

        # Mark old history links as transferred
        old_links = DriverBusinessIDS.query.filter_by(driver_id=driver.id, transferred_at=None).all()
        for old in old_links:
            old.transferred_at = datetime.utcnow()

        # Remove old active links
        BusinessDriver.query.filter_by(driver_id=driver.id).delete()

        # Add new assignments
        for b_id, p_id in zip(business_ids, platform_ids):
            db.session.add(DriverBusinessIDS(
                driver_id=driver.id,
                business_id_id=int(b_id),
                assigned_at=datetime.utcnow(),
                transferred_at=None
            ))
            db.session.add(BusinessDriver(
                driver_id=driver.id,
                business_id=int(b_id),
                platform_id=int(p_id)
            ))

        db.session.commit()
        flash(f"✅ Driver {driver.name} updated successfully.", "success")
        return redirect(url_for("admin.dashboard_admin"))

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("Error updating driver")
        flash(f"❌ Error updating driver: {str(e)}", "danger")
        return redirect(url_for("admin.dashboard_admin"))


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