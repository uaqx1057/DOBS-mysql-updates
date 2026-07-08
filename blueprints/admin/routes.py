from flask import Flask, render_template, request, redirect, url_for, flash, session , current_app, jsonify
from flask_login import login_required, current_user
from models import (
    Business, DriverBusinessIDS, Offboarding, db, Driver, User, BusinessID, BusinessDriver,
    DriverType, OnboardingStageTemplate, DriverTypeSettings, ContractTemplate, Branch,
)
from extensions import db, mail, limiter
from flask_mail import Message
from datetime import datetime
import os
from utils.email_utils import send_password_change_email
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from services.admin_service import (
    update_driver_from_form,
    delete_driver_and_offboarding,
    create_user_from_form,
    update_user_from_form,
    delete_user as delete_user_service,
    change_user_password,
)
from forms.common import (
    CSRFOnlyForm, AddUserForm, AddDriverForm, ChangePasswordForm, EditUserForm,
    OnboardingStageTemplateForm, DriverTypeSettingsForm, ContractTemplateForm, RoleForm,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from utils.auth import require_roles_or_owner
from utils.cache import ttl_cache
from models import Role, Permission, UserRole, UserPermission
from services.rbac import (
    grant_role, revoke_role, set_permission_override, clear_permission_override,
    role_permission_codes, set_role_permissions,
)
from . import admin_bp

UPLOAD_FOLDER = "static/uploads"


@ttl_cache(ttl_seconds=120, maxsize=1)
def _cached_businesses():
    return Business.query.order_by(Business.name).all()

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


def _pagination_params():
    try:
        page = max(1, int(request.args.get("page", 1)))
    except ValueError:
        page = 1
    try:
        per_page = int(request.args.get("per_page", 50))
    except ValueError:
        per_page = 50
    per_page = max(1, min(per_page, 200))
    return page, per_page

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


def normalize_onboarding_stage(value):
    if value in (None, ""):
        return value
    text = str(value).strip()
    key = text.lower().replace(" ", "")
    if key in {"fleet", "fleetmanager"}:
        return "Fleet Manager"
    return text

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
    page, per_page = _pagination_params()
    search_q = (request.args.get("q") or "").strip()

    # Paginate pending onboarding drivers only, so pages refill correctly
    # after a driver moves to Completed and leaves the pending pool.
    filtered_drivers_query = Driver.query.filter(Driver.onboarding_stage != "Completed")
    if search_q:
        pattern = f"%{search_q}%"
        filtered_drivers_query = filtered_drivers_query.filter(
            or_(
                Driver.name.ilike(pattern),
                Driver.iqaama_number.ilike(pattern),
                Driver.driver_id.ilike(pattern),
            )
        )

    paged_total_drivers = filtered_drivers_query.count()
    total_pages = max(1, (paged_total_drivers + per_page - 1) // per_page)
    page = min(page, total_pages)

    drivers_query = filtered_drivers_query.order_by(Driver.id.desc())
    drivers_total = Driver.query.count()
    drivers_completed_total = Driver.query.filter(Driver.onboarding_stage == "Completed").count()
    drivers_pending_total = max(0, drivers_total - drivers_completed_total)
    drivers = drivers_query.offset((page - 1) * per_page).limit(per_page).all()

    status_pairs = Offboarding.query.with_entities(Offboarding.driver_id, Offboarding.status).all()
    offboarded_ids = {driver_id for driver_id, status in status_pairs if status == "Completed"}
    in_offboarding_ids = {driver_id for driver_id, status in status_pairs if status != "Completed"}

    pending_q = (
        Offboarding.query.filter(Offboarding.status != "Completed")
        .order_by(Offboarding.updated_at.desc())
    )
    completed_q = (
        Offboarding.query.filter(Offboarding.status == "Completed")
        .order_by(Offboarding.updated_at.desc())
    )
    pending_total = pending_q.count()
    completed_total = completed_q.count()
    pending_offboarding_records = pending_q.offset((page - 1) * per_page).limit(per_page).all()
    completed_offboarding_records = completed_q.offset((page - 1) * per_page).limit(per_page).all()

    # -------------------------
    # Helper: serialize drivers
    # -------------------------
    def serialize_driver(d, offboarding_record=None):
        normalized_stage = normalize_onboarding_stage(d.onboarding_stage)
        data = {
            "id": d.id,
            "name": d.name,
            "branch_id": d.branch_id,
            "iqaama_number": d.iqaama_number,
            "iqaama_expiry": d.iqaama_expiry.isoformat() if d.iqaama_expiry else None,
            "nationality": d.nationality,
            "absher_number": d.absher_number,
            "previous_sponsor_number": d.previous_sponsor_number,
            "iqama_card_upload": d.iqama_card_upload,
            "iqama_card_upload_url": url_for("static", filename=f"uploads/{d.iqama_card_upload}") if d.iqama_card_upload else "",
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
            "onboarding_stage": normalized_stage,
            "company_contract_file": d.company_contract_file,
            "promissory_note_file": d.promissory_note_file,
            "qiwa_contract_file": d.qiwa_contract_file,
            "company_contract_file_url": url_for("static", filename=f"uploads/{d.company_contract_file}") if d.company_contract_file else "",
            "promissory_note_file_url": url_for("static", filename=f"uploads/{d.promissory_note_file}") if d.promissory_note_file else "",
            "qiwa_contract_file_url": url_for("static", filename=f"uploads/{d.qiwa_contract_file}") if d.qiwa_contract_file else "",
            "transfer_fee_receipt_url": url_for("static", filename=f"uploads/{d.transfer_fee_receipt}") if d.transfer_fee_receipt else "",
            "sponsorship_transfer_proof_url": url_for("static", filename=f"uploads/{d.sponsorship_transfer_proof}") if d.sponsorship_transfer_proof else "",
            "tamm_authorization_ss_url": url_for("static", filename=f"uploads/{d.tamm_authorization_ss}") if d.tamm_authorization_ss else "",
            "offboarding_stage": d.offboarding_stage or (offboarding_record.status if offboarding_record else None),
            "fully_onboarded": normalized_stage == "Completed",
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
    # Skip any offboarding records without an attached driver to avoid AttributeError
    pending_offboarding_driver_dicts = [
        serialize_driver(o.driver, offboarding_record=o)
        for o in pending_offboarding_records
        if o.driver is not None
    ]
    completed_offboarding_driver_dicts = [
        serialize_driver(o.driver, offboarding_record=o)
        for o in completed_offboarding_records
        if o.driver is not None
    ]
    # Build the fully-onboarded list from all drivers (not just the current page)
    completed_drivers = Driver.query.filter(Driver.onboarding_stage == "Completed").order_by(Driver.id.desc()).all()
    fully_onboarded_only = [
        serialize_driver(d)
        for d in completed_drivers
        if d.id not in in_offboarding_ids
    ]

    # -------------------------
    # Businesses and available IDs
    # -------------------------
    businesses = _cached_businesses()
    assigned_ids_subq = (
        db.session.query(DriverBusinessIDS.business_id_id)
        .filter(DriverBusinessIDS.transferred_at.is_(None))
        .subquery()
    )
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
    # Render template
    # -------------------------
    return render_template(
        "dashboard.html",
        users=users_dicts,
        drivers=driver_dicts,
        fully_onboarded_drivers=fully_onboarded_only,
        pending_offboarding_drivers=pending_offboarding_driver_dicts,
        completed_offboarding_drivers=completed_offboarding_driver_dicts,
        total_users=len(users),
        total_drivers=drivers_total,
        paged_total_drivers=paged_total_drivers,
        total_pending_onboarded=drivers_pending_total,
        total_completed_onboarded=drivers_completed_total,
        total_pending_offboarded=pending_total,
        total_completed_offboarded=completed_total,
        page=page,
        total_pages=total_pages,
        per_page=per_page,
        q=search_q,
        all_businesses=all_businesses,
        branches=Branch.query.filter(Branch.deleted_at.is_(None)).order_by(Branch.name).all(),
    )

# -------------------------
# Get Driver JSON       
# -------------------------
@admin_bp.route("/driver/<int:driver_id>/json")
@login_required
def driver_json(driver_id):
    if current_user.role not in ["Admin", "SuperAdmin"]:
        return {"error": "Access denied"}, 403

    driver = Driver.query.get_or_404(driver_id)

    assigned = []
    active_ids = (
        DriverBusinessIDS.query
        .filter_by(driver_id=driver.id, transferred_at=None)
        .all()
    )
    if active_ids:
        business_id_ids = [link.business_id_id for link in active_ids]
        business_ids = BusinessID.query.filter(BusinessID.id.in_(business_id_ids)).all()
        for bid in business_ids:
            assigned.append({
                "business_id": bid.business_id,
                "platform_id": bid.id,
                "platform_value": bid.value,
            })

    driver_data = {
        "id": driver.id,
        "name": driver.name,
        "iqaama_number": driver.iqaama_number,
        "iqaama_expiry": driver.iqaama_expiry.isoformat() if driver.iqaama_expiry else None,
        "nationality": driver.nationality,
        "absher_number": driver.absher_number,
        "previous_sponsor_number": driver.previous_sponsor_number,
        "iqama_card_upload": driver.iqama_card_upload,
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
        "onboarding_stage": normalize_onboarding_stage(driver.onboarding_stage),
        # file URLs
        "iqama_card_upload_url": url_for("static", filename=f"uploads/{driver.iqama_card_upload}") if driver.iqama_card_upload else "",
        "tamm_authorization_ss_url": getattr(driver, "tamm_authorization_ss_url", ""),
        "transfer_fee_receipt_url": getattr(driver, "transfer_fee_receipt_url", ""),
        "sponsorship_transfer_proof_url": getattr(driver, "sponsorship_transfer_proof_url", ""),
        "company_contract_file_url": getattr(driver, "company_contract_file_url", ""),
        "promissory_note_file_url": getattr(driver, "promissory_note_file_url", ""),
        "qiwa_contract_file_url": getattr(driver, "qiwa_contract_file_url", "")
    }

    return driver_data


# -------------------------
# Add Driver
# -------------------------
@admin_bp.route("/driver/add", methods=["POST"])
@login_required
def add_driver():
    if current_user.role not in ["Admin", "SuperAdmin"]:
        flash("Access denied", "danger")
        return redirect(url_for("auth.login"))

    form = AddDriverForm()
    if not form.validate_on_submit():
        # Surface field-level errors to the UI
        for field, errors in form.errors.items():
            for err in errors:
                flash(f"{field}: {err}", "danger")
        current_app.logger.warning("[ADMIN] Add driver validation failed", extra={"errors": form.errors})
        return redirect(url_for("admin.dashboard"))

    transfer_paid_at_raw = form.transfer_fee_paid_at.data
    transfer_paid_at = None
    if transfer_paid_at_raw:
        try:
            transfer_paid_at = datetime.fromisoformat(transfer_paid_at_raw)
        except ValueError:
            transfer_paid_at = None
    driver = Driver(
        name=form.name.data,
        iqaama_number=form.iqaama_number.data,
        iqaama_expiry=form.iqaama_expiry.data,
        saudi_driving_license=form.saudi_driving_license.data == "true",
        nationality=form.nationality.data,
        city=form.city.data,
        absher_number=form.absher_number.data,
        previous_sponsor_number=form.previous_sponsor_number.data,
        issued_mobile_number=form.issued_mobile_number.data,
        issued_device_id=form.issued_device_id.data,
        mobile_issued=form.mobile_issued.data == "true",
        car_details=form.car_details.data,
        assignment_date=form.assignment_date.data,
        tamm_authorized=form.tamm_authorized.data == "true",
        transfer_fee_paid=form.transfer_fee_paid.data == "true",
        transfer_fee_amount=float(form.transfer_fee_amount.data) if form.transfer_fee_amount.data else None,
        transfer_fee_paid_at=transfer_paid_at,
        qiwa_contract_status=form.qiwa_contract_status.data or "Pending",
        onboarding_stage=form.onboarding_stage.data or "Ops Manager",
    )

    db.session.add(driver)
    try:
        db.session.flush()
    except IntegrityError as e:
        db.session.rollback()
        msg = str(getattr(e, "orig", e))
        flash(f"Failed to create driver: {msg}", "danger")
        current_app.logger.exception("[ADMIN] IntegrityError creating driver")
        return redirect(url_for("admin.dashboard"))

    business_ids = request.form.getlist("business_id[]")
    platform_ids = request.form.getlist("platform_id[]")
    try:
        if platform_ids:
            update_driver_from_form(driver, request.form, business_ids, platform_ids)
        else:
            db.session.commit()
        flash(f"✅ Driver {driver.name} created successfully.", "success")
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("[ADMIN] Error creating driver")
        flash(f"❌ Error creating driver: {str(e)}", "danger")

    return redirect(url_for("admin.dashboard"))

# -------------------------
# Update Existing Driver
# -------------------------
@admin_bp.route("/driver/<int:driver_id>/update", methods=["POST"])
@login_required
def update_driver(driver_id):
    if current_user.role not in ["Admin", "SuperAdmin"]:
        flash("Access denied", "danger")
        return redirect(url_for("auth.login"))

    form = AddDriverForm()
    if not form.validate_on_submit():
        flash("Please correct the driver form.", "danger")
        return redirect(url_for("admin.dashboard"))

    driver = Driver.query.get_or_404(driver_id)
    try:
        business_ids = request.form.getlist("business_id[]")
        platform_ids = request.form.getlist("platform_id[]")
        update_driver_from_form(driver, request.form, business_ids, platform_ids)
        flash(f"✅ Driver {driver.name} updated successfully.", "success")
        return redirect(url_for("admin.dashboard"))
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("Error updating driver")
        flash(f"❌ Error updating driver: {str(e)}", "danger")
        return redirect(url_for("admin.dashboard"))


# -------------------------
# Delete Driver
# -------------------------
@admin_bp.route("/dashboard/driver/<int:driver_id>/delete", methods=["POST"])
@login_required
def delete_driver(driver_id):
    from app import db

    is_ajax = request.headers.get("X-Requested-With") == "XMLHttpRequest"

    form = CSRFOnlyForm()
    if not form.validate_on_submit():
        if is_ajax:
            return jsonify({"ok": False, "message": "Invalid request."}), 400
        flash("Invalid request.", "danger")
        return redirect(url_for("admin.dashboard"))

    try:
        delete_driver_and_offboarding(driver_id)
        if is_ajax:
            return jsonify({"ok": True, "message": "Driver deleted successfully."}), 200
        flash("Driver and related offboarding records deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        if is_ajax:
            return jsonify({"ok": False, "message": f"Error deleting driver: {str(e)}"}), 500
        flash(f"Error deleting driver: {str(e)}", "danger")

    return redirect(url_for("admin.dashboard"))

# -------------------------
# Add/Edit/Delete Users (unchanged)
# -------------------------
@admin_bp.route("/add_user", methods=["POST"])
@login_required
def add_user():
    if current_user.role != "SuperAdmin":
        return "Access Denied", 403

    form = AddUserForm()
    if not form.validate_on_submit():
        flash("Please correct the user form.", "danger")
        return redirect(url_for("admin.dashboard"))

    username = form.username.data
    raw_password = form.password.data
    role = form.role.data
    name = form.name.data
    designation = form.designation.data
    branch_city = form.branch_city.data
    email = form.email.data

    try:
        new_user = create_user_from_form(
            username=username,
            raw_password=raw_password,
            role=role,
            name=name,
            designation=designation,
            branch_city=branch_city,
            email=email,
        )
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to create user: {e}", "danger")
        return redirect(url_for("admin.dashboard"))

    # Send email notification
    sender = current_app.config.get("MAIL_DEFAULT_SENDER")
    email_sent = False

    try:
        msg = Message(
            "Your Account Has Been Created | تم إنشاء حسابك",
            recipients=[email],
            sender=sender,
        )
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
        email_sent = True
    except Exception as e:
        current_app.logger.exception(
            "Welcome email failed for new user id=%s email=%s: %s",
            new_user.id,
            email,
            e,
        )
        flash(f"User created, but the welcome email failed: {e}", "warning")

    if email_sent:
        current_app.logger.info(
            "Welcome email accepted by mail server for new user id=%s email=%s",
            new_user.id,
            email,
        )
        flash("User created successfully and welcome email was accepted by the mail server.", "success")
    return redirect(url_for("admin.dashboard"))

# -------------------------
# Edit User
# -------------------------
@admin_bp.route("/edit_user/<int:user_id>", methods=["POST"])
@login_required
@require_roles_or_owner("SuperAdmin", owner_loader=lambda user_id: User.query.get(user_id), owner_attr="id")
def edit_user(user_id):
    form = EditUserForm()
    if not form.validate_on_submit():
        flash("Invalid or incomplete user data.", "danger")
        return redirect(url_for("admin.dashboard"))

    user = User.query.get_or_404(user_id)
    try:
        if current_user.role == "SuperAdmin":
            update_user_from_form(
                user,
                username=form.username.data or user.username,
                name=form.name.data or user.name,
                designation=form.designation.data or user.designation,
                branch_city=form.branch_city.data or user.branch_city,
                email=form.email.data or user.email,
                role=form.role.data or user.role,
            )
            flash(f"User {user.username} updated successfully.", "success")
        else:
            # Allow self-service updates for non-privileged users without role/username changes
            user.name = form.name.data or user.name
            user.designation = form.designation.data or user.designation
            user.branch_city = form.branch_city.data or user.branch_city
            user.email = form.email.data or user.email
            db.session.commit()
            flash("Profile updated successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to update user: {e}", "danger")
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

    form = CSRFOnlyForm()
    if not form.validate_on_submit():
        flash("Invalid request.", "danger")
        return redirect(url_for("admin.dashboard"))

    user = User.query.get_or_404(user_id)
    try:
        delete_user_service(user, acting_user_id=current_user.id)
        flash(f"User {user.username} deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to delete user: {e}", "danger")
    return redirect(url_for("admin.dashboard"))

# -------------------------
# Change Password (for SuperAdmin)
# -------------------------
@admin_bp.route("/change_password", methods=["POST"])
@limiter.limit("5 per minute")
@login_required
def change_password():
    """Allow SuperAdmin to change their password securely and send email notification."""
    if current_user.role != "SuperAdmin":
        flash("Access Denied", "danger")
        return redirect(url_for("admin.dashboard"))

    form = ChangePasswordForm()
    if not form.validate_on_submit():
        flash("Please correct the password form.", "danger")
        return redirect(url_for("admin.dashboard"))

    current_password = form.current_password.data
    new_password = form.new_password.data

    if not check_password_hash(current_user.password, current_password):
        flash("Current password is incorrect.", "danger")
        return redirect(url_for("admin.dashboard"))

    try:
        # Update password in database
        change_user_password(current_user, new_password)

        # Send email notification using helper
        if send_password_change_email(current_user, new_password):
            flash("Password updated and email notification sent.", "success")
        else:
            flash("Password updated, but email could not be sent.", "warning")

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(f"[ADMIN] Failed to change password: {e}")
        flash("Could not update password right now. Try again later.", "danger")

    return redirect(url_for("admin.dashboard"))


# -------------------------
# Onboarding Workflow Builder + Contract Template Manager
#
# Admin-editable data driving services/onboarding_workflow.py and
# services/contracts.py - adding a driver type's stage sequence or a
# platform's contract template happens here, not in code.
# -------------------------
@admin_bp.route("/workflow-config", methods=["GET"])
@login_required
def workflow_config():
    if current_user.role != "SuperAdmin":
        return "Forbidden", 403

    driver_types = DriverType.query.filter(DriverType.deleted_at.is_(None)).order_by(DriverType.name).all()
    stage_templates = OnboardingStageTemplate.query.order_by(
        OnboardingStageTemplate.driver_type_id, OnboardingStageTemplate.sequence_order
    ).all()
    type_settings = {row.driver_type_id: row for row in DriverTypeSettings.query.all()}
    contract_templates = ContractTemplate.query.order_by(ContractTemplate.name).all()
    businesses = _cached_businesses()

    stages_by_type = {}
    for row in stage_templates:
        stages_by_type.setdefault(row.driver_type_id, []).append(row)

    return render_template(
        "admin_workflow_config.html",
        driver_types=driver_types,
        stages_by_type=stages_by_type,
        type_settings=type_settings,
        contract_templates=contract_templates,
        businesses=businesses,
        stage_form=OnboardingStageTemplateForm(),
        settings_form=DriverTypeSettingsForm(),
        contract_form=ContractTemplateForm(),
    )


@admin_bp.route("/workflow-config/stage-template/add", methods=["POST"])
@login_required
def add_stage_template():
    if current_user.role != "SuperAdmin":
        return "Forbidden", 403

    form = OnboardingStageTemplateForm()
    if not form.validate_on_submit():
        for field, errors in form.errors.items():
            for err in errors:
                flash(f"{field}: {err}", "danger")
        return redirect(url_for("admin.workflow_config"))

    row = OnboardingStageTemplate(
        driver_type_id=form.driver_type_id.data,
        sequence_order=form.sequence_order.data,
        stage_name=form.stage_name.data,
        skip_condition_field=form.skip_condition_field.data or None,
        skip_condition_value=form.skip_condition_value.data or None,
    )
    db.session.add(row)
    try:
        db.session.commit()
        flash("Stage added to the onboarding sequence.", "success")
    except IntegrityError:
        db.session.rollback()
        flash("That driver type already has a stage at this order position.", "danger")
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("[ADMIN] Failed to add stage template")
        flash(f"Failed to add stage: {e}", "danger")

    return redirect(url_for("admin.workflow_config"))


@admin_bp.route("/workflow-config/stage-template/<int:row_id>/delete", methods=["POST"])
@login_required
def delete_stage_template(row_id):
    if current_user.role != "SuperAdmin":
        return "Forbidden", 403

    form = CSRFOnlyForm()
    if not form.validate_on_submit():
        flash("Invalid request.", "danger")
        return redirect(url_for("admin.workflow_config"))

    row = OnboardingStageTemplate.query.get_or_404(row_id)
    db.session.delete(row)
    db.session.commit()
    flash("Stage removed from the onboarding sequence.", "success")
    return redirect(url_for("admin.workflow_config"))


@admin_bp.route("/workflow-config/driver-type-settings/save", methods=["POST"])
@login_required
def save_driver_type_settings():
    if current_user.role != "SuperAdmin":
        return "Forbidden", 403

    form = DriverTypeSettingsForm()
    if not form.validate_on_submit():
        flash("Please choose a driver type and contract mode.", "danger")
        return redirect(url_for("admin.workflow_config"))

    settings = DriverTypeSettings.query.get(form.driver_type_id.data)
    if settings:
        settings.contract_mode = form.contract_mode.data
    else:
        settings = DriverTypeSettings(
            driver_type_id=form.driver_type_id.data,
            contract_mode=form.contract_mode.data,
        )
        db.session.add(settings)

    db.session.commit()
    flash("Driver type contract mode saved.", "success")
    return redirect(url_for("admin.workflow_config"))


@admin_bp.route("/workflow-config/contract-template/add", methods=["POST"])
@login_required
def add_contract_template():
    if current_user.role != "SuperAdmin":
        return "Forbidden", 403

    form = ContractTemplateForm()
    if not form.validate_on_submit():
        for field, errors in form.errors.items():
            for err in errors:
                flash(f"{field}: {err}", "danger")
        return redirect(url_for("admin.workflow_config"))

    template = ContractTemplate(
        name=form.name.data,
        business_id=form.business_id.data or None,
        driver_type_id=form.driver_type_id.data or None,
        body_content=form.body_content.data,
        is_active=form.is_active.data,
    )
    db.session.add(template)
    db.session.commit()
    flash(f"Contract template '{template.name}' created.", "success")
    return redirect(url_for("admin.workflow_config"))


@admin_bp.route("/workflow-config/contract-template/<int:template_id>/toggle-active", methods=["POST"])
@login_required
def toggle_contract_template(template_id):
    if current_user.role != "SuperAdmin":
        return "Forbidden", 403

    form = CSRFOnlyForm()
    if not form.validate_on_submit():
        flash("Invalid request.", "danger")
        return redirect(url_for("admin.workflow_config"))

    template = ContractTemplate.query.get_or_404(template_id)
    template.is_active = not template.is_active
    db.session.commit()
    flash(f"Contract template '{template.name}' is now {'active' if template.is_active else 'inactive'}.", "success")
    return redirect(url_for("admin.workflow_config"))


@admin_bp.route("/workflow-config/contract-template/<int:template_id>/delete", methods=["POST"])
@login_required
def delete_contract_template(template_id):
    if current_user.role != "SuperAdmin":
        return "Forbidden", 403

    form = CSRFOnlyForm()
    if not form.validate_on_submit():
        flash("Invalid request.", "danger")
        return redirect(url_for("admin.workflow_config"))

    template = ContractTemplate.query.get_or_404(template_id)
    db.session.delete(template)
    db.session.commit()
    flash("Contract template deleted.", "success")
    return redirect(url_for("admin.workflow_config"))


# -------------------------
# Per-user access: multi-role grants + standalone permission overrides
#
# This is what makes "give this Ops Manager extra Fleet access" or "let
# this specific employee request offboarding regardless of role" an
# admin-dashboard action instead of a code change.
# -------------------------
@admin_bp.route("/user/<int:user_id>/access", methods=["GET"])
@login_required
def user_access(user_id):
    if current_user.role != "SuperAdmin":
        return "Forbidden", 403

    user = User.query.get_or_404(user_id)
    all_roles = Role.query.order_by(Role.name).all()
    all_permissions = Permission.query.order_by(Permission.code).all()
    granted_role_ids = {row.role_id for row in UserRole.query.filter_by(user_id=user.id).all()}
    overrides = {row.permission_id: row.granted for row in UserPermission.query.filter_by(user_id=user.id).all()}

    return render_template(
        "admin_user_access.html",
        user=user,
        all_roles=all_roles,
        all_permissions=all_permissions,
        granted_role_ids=granted_role_ids,
        overrides=overrides,
    )


@admin_bp.route("/user/<int:user_id>/access/roles", methods=["POST"])
@login_required
def save_user_roles(user_id):
    if current_user.role != "SuperAdmin":
        return "Forbidden", 403

    form = CSRFOnlyForm()
    if not form.validate_on_submit():
        flash("Invalid request.", "danger")
        return redirect(url_for("admin.user_access", user_id=user_id))

    user = User.query.get_or_404(user_id)
    selected_role_ids = {int(v) for v in request.form.getlist("role_ids")}
    all_roles = Role.query.all()

    for role in all_roles:
        if role.id in selected_role_ids:
            grant_role(user, role.name)
        else:
            revoke_role(user, role.name)

    db.session.commit()
    flash(f"Roles updated for {user.username}.", "success")
    return redirect(url_for("admin.user_access", user_id=user_id))


@admin_bp.route("/user/<int:user_id>/access/permissions", methods=["POST"])
@login_required
def save_user_permissions(user_id):
    if current_user.role != "SuperAdmin":
        return "Forbidden", 403

    form = CSRFOnlyForm()
    if not form.validate_on_submit():
        flash("Invalid request.", "danger")
        return redirect(url_for("admin.user_access", user_id=user_id))

    user = User.query.get_or_404(user_id)
    # Radio group per permission: "grant" | "revoke" | "inherit" (no override)
    for perm in Permission.query.all():
        choice = request.form.get(f"perm_{perm.id}", "inherit")
        if choice == "grant":
            set_permission_override(user, perm.code, True)
        elif choice == "revoke":
            set_permission_override(user, perm.code, False)
        else:
            clear_permission_override(user, perm.code)

    db.session.commit()
    flash(f"Permission overrides updated for {user.username}.", "success")
    return redirect(url_for("admin.user_access", user_id=user_id))


# ------------------------
# Role management (create roles, define their default permissions)
# ------------------------

# Seeded by migrations/versions/20260707_rbac_workflow_config.py - these
# names are still matched by raw-string role checks elsewhere in the app
# (dobs_user.role, base.html's nav, ROLE_DASHBOARD_ENDPOINTS), so renaming
# or deleting them here would silently desync those. Protected, not just by
# convention - enforced in delete_role below.
LEGACY_ROLE_NAMES = {
    "SuperAdmin", "HR", "HRManager", "OpsManager", "OpsSupervisor",
    "OpsCoordinator", "FleetManager", "Finance", "FinanceManager", "Admin",
}


@admin_bp.route("/roles", methods=["GET"])
@login_required
def roles():
    if current_user.role != "SuperAdmin":
        return "Forbidden", 403

    all_roles = Role.query.order_by(Role.name).all()
    user_counts = {
        row[0]: row[1]
        for row in db.session.query(UserRole.role_id, db.func.count(UserRole.user_id))
        .group_by(UserRole.role_id).all()
    }
    return render_template(
        "admin_roles.html",
        roles=all_roles,
        legacy_role_names=LEGACY_ROLE_NAMES,
        user_counts=user_counts,
        role_form=RoleForm(),
    )


@admin_bp.route("/roles/add", methods=["POST"])
@login_required
def add_role():
    if current_user.role != "SuperAdmin":
        return "Forbidden", 403

    form = RoleForm()
    if not form.validate_on_submit():
        for field, errors in form.errors.items():
            for err in errors:
                flash(f"{field}: {err}", "danger")
        return redirect(url_for("admin.roles"))

    if Role.query.filter_by(name=form.name.data).first():
        flash("A role with that name already exists.", "danger")
        return redirect(url_for("admin.roles"))

    db.session.add(Role(name=form.name.data.strip(), description=form.description.data or None))
    db.session.commit()
    flash(f"Role '{form.name.data}' created.", "success")
    return redirect(url_for("admin.roles"))


@admin_bp.route("/roles/<int:role_id>/delete", methods=["POST"])
@login_required
def delete_role(role_id):
    if current_user.role != "SuperAdmin":
        return "Forbidden", 403

    form = CSRFOnlyForm()
    if not form.validate_on_submit():
        flash("Invalid request.", "danger")
        return redirect(url_for("admin.roles"))

    role = Role.query.get_or_404(role_id)
    if role.name in LEGACY_ROLE_NAMES:
        flash(f"'{role.name}' is a built-in role and cannot be deleted.", "danger")
        return redirect(url_for("admin.roles"))

    in_use = (
        UserRole.query.filter_by(role_id=role.id).first()
        or User.query.filter_by(role=role.name).first()
    )
    if in_use:
        flash(f"'{role.name}' is still assigned to at least one user and cannot be deleted.", "danger")
        return redirect(url_for("admin.roles"))

    db.session.delete(role)
    db.session.commit()
    flash(f"Role '{role.name}' deleted.", "success")
    return redirect(url_for("admin.roles"))


@admin_bp.route("/roles/<int:role_id>/permissions", methods=["GET"])
@login_required
def role_permissions(role_id):
    if current_user.role != "SuperAdmin":
        return "Forbidden", 403

    role = Role.query.get_or_404(role_id)
    all_permissions = Permission.query.order_by(Permission.code).all()
    granted_codes = role_permission_codes(role)

    grouped = {}
    for perm in all_permissions:
        category = perm.code.split(".")[0]
        grouped.setdefault(category, []).append(perm)

    return render_template(
        "admin_role_permissions.html",
        role=role,
        grouped_permissions=grouped,
        granted_codes=granted_codes,
    )


@admin_bp.route("/roles/<int:role_id>/permissions", methods=["POST"])
@login_required
def save_role_permissions(role_id):
    if current_user.role != "SuperAdmin":
        return "Forbidden", 403

    form = CSRFOnlyForm()
    if not form.validate_on_submit():
        flash("Invalid request.", "danger")
        return redirect(url_for("admin.role_permissions", role_id=role_id))

    role = Role.query.get_or_404(role_id)
    selected_codes = set(request.form.getlist("permission_codes"))
    set_role_permissions(role, selected_codes)
    db.session.commit()
    flash(f"Permissions updated for role '{role.name}'.", "success")
    return redirect(url_for("admin.role_permissions", role_id=role_id))