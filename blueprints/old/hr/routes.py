# blueprints/hr/routes.py
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Driver, User, Offboarding
from extensions import db, mail
from flask_mail import Message
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

hr_bp = Blueprint("hr", __name__, url_prefix='/hr')

UPLOAD_FOLDER = os.path.join(os.getcwd(), "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXT = {'.jpg', '.jpeg', '.png', '.pdf'}

def _allowed_filename(fn):
    _, ext = os.path.splitext(fn.lower())
    return ext in ALLOWED_EXT

def _serialize_driver(d):
    return {
        "id": d.id,
        "full_name": d.full_name,
        "iqama_number": d.iqama_number,
        "iqama_expiry_date": d.iqama_expiry_date.isoformat() if d.iqama_expiry_date else None,
        "nationality": d.nationality,
        "mobile_number": d.mobile_number,
        "previous_sponsor_number": d.previous_sponsor_number,
        "saudi_driving_license": bool(d.saudi_driving_license),
        "city": d.city,
        "platforms": [
            {"id": p.id, "platform_name": p.platform_name, "platform_user_id": p.platform_user_id}
            for p in d.platforms
        ],
        "car_details": d.car_details,
        "assignment_date": d.assignment_date.isoformat() if d.assignment_date else None,
        "issued_mobile_number": d.issued_mobile_number,
        "issued_device_id": d.issued_device_id,
        "mobile_issued": bool(d.mobile_issued),
        "iqama_card_upload": d.iqama_card_upload,
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
        "qiwa_contract_file": d.qiwa_contract_file
    }

def _serialize_offboarding(o):
    return {
        "offboarding_id": o.id,
        "driver_id": o.driver.id if o.driver else None,
        "full_name": o.driver.full_name if o.driver else "",
        "iqama_number": o.driver.iqama_number if o.driver else "",
        "status": o.status or "",
        "hr_note": o.hr_note or "",
        "tamm_revoked": bool(o.tamm_revoked),
        "company_contract_cancelled": bool(o.company_contract_cancelled),
        "qiwa_contract_cancelled": bool(o.qiwa_contract_cancelled),
        "pending_salary": float(getattr(o, "finance_adjustments", 0) or 0),
        "finance_note": getattr(o, "finance_note", "") or "",
        "fleet_damage_report": getattr(o, "fleet_damage_report", "") or "",
        "fleet_damage_cost": float(getattr(o, "fleet_damage_cost", 0) or 0),
        "salary_paid": bool(o.salary_paid),
    }

 
# -------------------------
# HR Dashboard
# -------------------------
@hr_bp.route("/dashboard")
@login_required
def dashboard_hr():
    if current_user.role != "HR":
        flash("Access denied. HR role required.", "danger")
        return redirect(url_for("auth.login"))

    all_drivers = Driver.query.filter(
        Driver.onboarding_stage.in_(["HR", "HR Final", "Completed"])
    ).all()

    offboarding_driver_ids = {o.driver_id for o in Offboarding.query.all()}

    hr_stage_drivers = Driver.query.filter_by(onboarding_stage="HR").all()
    total_drivers = len([d for d in hr_stage_drivers if d.id not in offboarding_driver_ids])

    hr_final_drivers = Driver.query.filter_by(onboarding_stage="HR Final").all()
    total_users = len([d for d in hr_final_drivers if d.id not in offboarding_driver_ids])

    completed_onboarded = Driver.query.filter_by(onboarding_stage="Completed").all()
    total_completed_onboarded = len([d for d in completed_onboarded if d.id not in offboarding_driver_ids])

    offboarding_hr = Offboarding.query.filter(Offboarding.status == "HR").all()
    total_pending_onboarded = len(offboarding_hr)

    completed_offboarded = Offboarding.query.filter(Offboarding.status == "Completed").all()
    total_completed_offboarded = len(completed_offboarded)

    drivers_data = [_serialize_driver(d) for d in all_drivers if d.id not in offboarding_driver_ids]
    offboardings = Offboarding.query.filter(Offboarding.status.in_(["HR", "Completed"])).all()
    offboarding_data = [_serialize_offboarding(o) for o in offboardings]

    from flask import session
    lang = session.get("lang", "en")
    template = "rtl_dashboard_hr.html" if lang == "ar" else "dashboard_hr.html"
    return render_template(
        template,
        drivers=drivers_data,
        offboarding_drivers=offboarding_data,
        total_drivers=total_drivers,
        total_users=total_users,
        total_completed_onboarded=total_completed_onboarded,
        total_pending_onboarded=total_pending_onboarded,
        total_completed_offboarded=total_completed_offboarded
    )

 

# -------------------------
# Approve Driver & Upload Contracts
# -------------------------
@hr_bp.route("/approve_driver/<int:driver_id>", methods=["POST"])
@login_required
def approve_driver(driver_id):
    if current_user.role != "HR":
        flash("Access denied. HR role required.", "danger")
        return redirect(url_for("auth.login"))

    driver = Driver.query.get_or_404(driver_id)

    # Mapping: DB field → form file input name
    file_fields = {
        "company_contract_file": "company_contract",
        "promissory_note_file": "promissory_note",
        "qiwa_contract_file": "qiwa_contract",
    }

    for db_field, form_name in file_fields.items():
        uploaded_file = request.files.get(form_name)
        if uploaded_file and uploaded_file.filename:
            # Check allowed extension
            _, ext = os.path.splitext(uploaded_file.filename)
            if ext.lower() not in ALLOWED_EXT:
                flash(f"Invalid file type for {db_field}. Only JPG, PNG, PDF allowed.", "danger")
                return redirect(url_for("hr.dashboard_hr"))

            # Safe filename
            safe_name = f"{driver.full_name.replace(' ', '_')}_{driver.iqama_number}_{db_field}{ext.lower()}"
            dest = os.path.join(UPLOAD_FOLDER, safe_name)
            uploaded_file.save(dest)

            # ✅ Save filename to DB column
            setattr(driver, db_field, safe_name)

    # Save Qiwa / company contract statuses
    driver.qiwa_contract_created = bool(request.form.get("qiwa_contract_created"))
    driver.company_contract_created = bool(request.form.get("company_contract_created"))
    driver.qiwa_contract_status = request.form.get("qiwa_contract_status", "Pending")
    driver.sponsorship_transfer_status = request.form.get("sponsorship_transfer_status", "Pending")

    # Mark HR approval & move to next stage
    driver.hr_approved_at = datetime.utcnow()
    driver.onboarding_stage = "Ops Supervisor"

    # Commit everything
    db.session.commit()

    # Notify Ops Supervisors
    try:
        ops_supervisors = User.query.filter_by(role="OpsSupervisor").all()
        recipients = [op.email for op in ops_supervisors if op.email]
        if recipients:
            msg = Message(
                subject=f"Driver Ready for Ops Supervisor Stage: {driver.full_name}",
                recipients=recipients,
                body=f"""
            Hello Ops Supervisor Team,
            
            Driver {driver.full_name} (Iqama: {driver.iqama_number or "N/A"}) has been moved to your stage for processing.
            
            Please review and complete the necessary actions.
            
            ------------------------------------------------------
            
            السادة فريق مشرف العمليات،
            
            تم نقل السائق {driver.full_name} (رقم الإقامة: {driver.iqama_number or "N/A"}) إلى مرحلتكم لمتابعة الإجراءات.
            
            يرجى مراجعة البيانات واستكمال الإجراءات المطلوبة.
            
            Regards / مع التحية,
            Operations Team / فريق العمليات
            """
            )
            mail.send(msg)

    except Exception as e:
        print("[EMAIL ERROR]", e)

    flash(f"Driver {driver.full_name} approved and sent to Ops Supervisor stage.", "success")
    return redirect(url_for("hr.dashboard_hr"))



@hr_bp.route("/reject_driver/<int:driver_id>", methods=["POST"])
@login_required
def reject_driver(driver_id):
    # Only HR can perform this action
    if current_user.role != "HR":
        flash("Access denied. HR role required.", "danger")
        return redirect(url_for("auth.login"))

    driver = Driver.query.get_or_404(driver_id)
    reason = request.form.get("rejection_reason", "").strip()

    if not reason:
        flash("Please provide a rejection reason.", "warning")
        return redirect(url_for("hr.dashboard_hr"))

    driver_name = driver.full_name
    iqama_number = driver.iqama_number
    nationality = driver.nationality

    try:
        # Delete driver permanently
        db.session.delete(driver)
        db.session.commit()

        # Collect recipients (Ops, HR, Admin)
        recipients = []
        ops_managers = User.query.filter_by(role="OpsManager").all()
        hr_users = User.query.filter_by(role="HR").all()
        admins = User.query.filter_by(role="Admin").all()

        for group in (ops_managers, hr_users, admins):
            recipients.extend([u.email for u in group if u.email])

        # Send email notification
        if recipients:
            msg = Message(
                subject=f"Driver Rejected by HR: {driver_name}",
                recipients=recipients,
                body=f"""
            Hello Team,

            Driver {driver_name} (Iqama: {iqama_number or "N/A"}, Nationality: {nationality})
            has been REJECTED by the HR department and permanently removed from the system.

            Reason for rejection:
            {reason}

            Rejected by: {current_user.name}
            Date: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC

            Please review this information and take note of the rejection decision.

            ------------------------------------------------------

            السادة فريق الإدارة والعمليات والموارد البشرية،

            تم رفض السائق {driver_name} (رقم الإقامة: {iqama_number or "N/A"}، الجنسية: {nationality})
            من قبل قسم الموارد البشرية وتم حذفه نهائيًا من النظام.

            سبب الرفض:
            {reason}

            تم الرفض بواسطة: {current_user.name}
            التاريخ: {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC

            يرجى مراجعة هذه المعلومات وأخذ العلم بقرار الرفض.

            Regards / مع التحية,  
            HR Department / قسم الموارد البشرية
            """
            )
            mail.send(msg)


        flash(f"Driver {driver_name} rejected and deleted. Notifications sent.", "success")

    except Exception as e:
        db.session.rollback()
        print("[HR REJECT DRIVER ERROR]", e)
        flash("❌ Error rejecting driver. Please try again.", "danger")

    return redirect(url_for("hr.dashboard_hr"))


# -------------------------
# HR Final Stage: Complete Sponsorship Transfer (handles Qiwa / non-Qiwa cases)
# -------------------------
@hr_bp.route("/complete_transfer/<int:driver_id>", methods=["POST"])
@login_required
def complete_sponsorship_transfer(driver_id):
    if current_user.role != "HR":
        flash("Access denied", "danger")
        return redirect(url_for("auth.login"))

    driver = Driver.query.get_or_404(driver_id)

    try:
        # Determine current case
        if not driver.qiwa_contract_created:
            # 🔹 Case 1: Driver has NO Qiwa contract
            driver.onboarding_stage = "Completed"
            driver.sponsorship_transfer_status = "Not Required"
            driver.sponsorship_transfer_proof = None
            driver.sponsorship_transfer_completed_at = datetime.utcnow()
            db.session.commit()

            flash(f"✅ Driver {driver.full_name} marked as completed (no Qiwa contract).", "success")

        else:
            # 🔹 Case 2: Driver HAS a Qiwa contract — must upload proof + status
            transfer_status = request.form.get("sponsorship_transfer_status")
            file = request.files.get("sponsorship_transfer_proof")

            if transfer_status != "Transferred" or not file or not file.filename:
                flash("⚠️ Please select 'Transferred' and upload proof before marking complete.", "warning")
                return redirect(url_for("hr.dashboard_hr"))

            if not _allowed_filename(file.filename):
                flash("Invalid file type. Only JPG, PNG, and PDF are allowed.", "danger")
                return redirect(url_for("hr.dashboard_hr"))

            ext = os.path.splitext(file.filename)[1].lower()
            driver_name = driver.full_name.replace(" ", "_") if driver.full_name else "driver"
            iqama = driver.iqama_number or "unknown"
            filename = f"{driver_name}_{iqama}_transfer_proof{ext}"
            dest = os.path.join(UPLOAD_FOLDER, filename)
            file.save(dest)

            driver.sponsorship_transfer_status = transfer_status
            driver.sponsorship_transfer_proof = filename
            driver.sponsorship_transfer_completed_at = datetime.utcnow()
            driver.onboarding_stage = "Completed"
            db.session.commit()

            flash(f"✅ Sponsorship transfer completed for {driver.full_name}.", "success")

        # 📧 Notify SuperAdmins after completion
        superadmins = User.query.filter_by(role="SuperAdmin").all()
        recipients = [sa.email for sa in superadmins if sa.email]
        if recipients:
            msg = Message(
                subject=f"Driver Onboarding Completed: {driver.full_name}",
                recipients=recipients,
                body=f"""
            Hello Team,
            
            Driver {driver.full_name} has successfully completed the onboarding process.
            
            Details:
            - Iqama: {driver.iqama_number or "N/A"}
            - Qiwa Contract Created: {'✅ Yes' if driver.qiwa_contract_created else '❌ No'}
            - Sponsorship Transfer Completed At: {driver.sponsorship_transfer_completed_at.strftime('%Y-%m-%d %H:%M') if driver.sponsorship_transfer_completed_at else 'N/A'}
            
            Please update your records accordingly.
            
            ------------------------------------------------------
            
            السادة الفريق،
            
            لقد أكمل السائق {driver.full_name} عملية الانضمام بنجاح.
            
            التفاصيل:
            - رقم الإقامة: {driver.iqama_number or "N/A"}
            - إنشاء عقد قوى: {'✅ نعم' if driver.qiwa_contract_created else '❌ لا'}
            - تاريخ إكمال نقل الكفالة: {driver.sponsorship_transfer_completed_at.strftime('%Y-%m-%d %H:%M') if driver.sponsorship_transfer_completed_at else 'N/A'}
            
            يرجى تحديث سجلاتكم وفقاً لذلك.
            
            Regards / مع التحية,
            HR / فريق الموارد البشرية
            """
            )
            mail.send(msg)


    except Exception as e:
        db.session.rollback()
        print("[HR COMPLETE TRANSFER ERROR]", e)
        flash(f"❌ Error completing sponsorship transfer: {str(e)}", "danger")

    return redirect(url_for("hr.dashboard_hr"))

@hr_bp.route('/complete_driver/<int:driver_id>', methods=['POST'])
@login_required
def complete_driver(driver_id):
    if current_user.role != "HR":
        flash("Access denied", "danger")
        return redirect(url_for("auth.login"))

    driver = Driver.query.get_or_404(driver_id)

    # Only for drivers without a Qiwa contract
    if not driver.qiwa_contract_created:
        driver.onboarding_stage = "Completed"
        driver.sponsorship_transfer_status = "Not Required"
        driver.sponsorship_transfer_proof = None
        driver.sponsorship_transfer_completed_at = datetime.utcnow()
        db.session.commit()
        flash(f"✅ Driver {driver.full_name} marked as completed (no Qiwa contract).", "success")
    else:
        flash(f"⚠️ Driver {driver.full_name} has a Qiwa contract. Use normal transfer workflow.", "warning")

    return redirect(request.referrer or url_for("hr.dashboard_hr"))

# -------------------------
# Change HR Password
# -------------------------
@hr_bp.route("/change_password", methods=["POST"])
@login_required
def change_password():
    if current_user.role != "HR":
        flash("Access denied. HR role required.", "danger")
        return redirect(url_for("auth.login"))

    current_password = request.form["current_password"]
    new_password = request.form["new_password"]
    confirm_password = request.form["confirm_password"]

    if not check_password_hash(current_user.password, current_password):
        flash("Current password is incorrect.", "danger")
        return redirect(url_for("hr.dashboard_hr"))

    if new_password != confirm_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for("hr.dashboard_hr"))

    current_user.password = generate_password_hash(new_password)
    db.session.commit()

    flash("Password updated successfully.", "success")
    return redirect(url_for("hr.dashboard_hr"))


# -------------------------
# Start Offboarding (contract cancellation)
# -------------------------
@hr_bp.route("/start_offboarding/<int:driver_id>", methods=["POST"])
@login_required
def start_offboarding(driver_id):
    if current_user.role != "HR":
        flash("Access denied", "danger")
        return redirect(url_for("auth.login"))

    driver = Driver.query.get_or_404(driver_id)
    driver.offboarding_stage = "HR"
    driver.offboarding_reason = request.form.get("offboarding_reason", "Not specified")
    driver.offboarding_requested_at = datetime.utcnow()

    db.session.commit()
    flash(f"Offboarding process started for {driver.full_name}.", "info")
    return redirect(url_for("hr.offboarding_hr"))


# -------------------------
# Complete Offboarding
# -------------------------

@hr_bp.route("/complete_offboarding/<int:offboarding_id>", methods=["POST"])
@login_required
def complete_offboarding(offboarding_id):
    if current_user.role != "HR":
        flash("Access denied", "danger")
        return redirect(url_for("auth.login"))

    offboarding = Offboarding.query.get_or_404(offboarding_id)
    note = request.form.get("hr_note")
    offboarding.mark_hr_cleared(note=note)

    db.session.commit()
    flash(f"HR clearance completed for {offboarding.driver.full_name}.", "success")
    return redirect(url_for("hr.dashboard_hr"))


@hr_bp.route("/offboarding/finalize", methods=["POST"])
@login_required
def finalize_offboarding():
    if current_user.role != "HR":
        if request.is_json:
            return jsonify({"success": False, "message": "Access denied"}), 403
        flash("Access denied", "danger")
        return redirect(url_for("auth.login"))

    # Determine if request is JSON or form
    if request.is_json:
        data = request.get_json()
        offboarding_id = data.get("offboarding_id")
        company_cancelled = data.get("company_contract_cancelled") == "yes"
        qiwa_cancelled = data.get("qiwa_contract_cancelled") == "yes"
        salary_paid = data.get("salary_paid") == "yes"
    else:
        offboarding_id = request.form.get("offboarding_id")
        company_cancelled = request.form.get("company_contract_cancelled") == "yes"
        qiwa_cancelled = request.form.get("qiwa_contract_cancelled") == "yes"
        salary_paid = request.form.get("salary_paid") == "yes"

    # Fetch Offboarding record
    offboarding = Offboarding.query.get_or_404(offboarding_id)

    # Update fields
    offboarding.company_contract_cancelled = company_cancelled
    offboarding.qiwa_contract_cancelled = qiwa_cancelled
    offboarding.salary_paid = salary_paid

    # Constraint check
    if not (company_cancelled and qiwa_cancelled and salary_paid):
        message = "Cannot clear: Company & Qiwa contracts must be cancelled and salary must be paid."
        if request.is_json:
            return jsonify({"success": False, "message": message}), 400
        flash(message, "danger")
        return redirect(url_for("hr.dashboard_hr"))

    # Mark HR cleared
    offboarding.hr_cleared = True
    offboarding.hr_cleared_at = datetime.utcnow()
    offboarding.status = "Completed"

    db.session.commit()

    # Send email to Fleet Manager(s)
    try:
        all_users = User.query.all()
        recipients = [u.email for u in all_users if u.email]
        if recipients:
            msg = Message(
                subject=f"Offboarding Completed for {offboarding.driver.full_name}",
                recipients=recipients,
                body=f"""
            Hello Team,
            
            HR has cleared the offboarding process for driver {offboarding.driver.full_name}.
            
            Details:
            - Iqama: {offboarding.driver.iqama_number or "N/A"}
            
            The record is Has been updated and driver is fully Offboarded.
            
            ------------------------------------------------------
            
            مرحبًا بالفريق،
            
            لقد قامت إدارة الموارد البشرية بإنهاء عملية مغادرة السائق{offboarding.driver.full_name}.
            
            التفاصيل:
            - رقم الإقامة: {offboarding.driver.iqama_number or "N/A"}
            
            تم تحديث السجل وتم إلغاء تثبيت برنامج التشغيل بالكامل.
            
            Regards / مع التحية,
            HR / فريق الموارد البشرية
            """
            )
            mail.send(msg)

    except Exception as e:
        print("[EMAIL ERROR]", e)
        if request.is_json:
            return jsonify({"success": False, "message": f"Email send failed: {str(e)}"}), 500
        flash(f"Email send failed: {str(e)}", "danger")
        return redirect(url_for("hr.dashboard_hr"))

    success_message = f"HR clearance completed for {offboarding.driver.full_name} and notified."
    if request.is_json:
        return jsonify({"success": True, "message": success_message})
    flash(success_message, "success")
    return redirect(url_for("hr.dashboard_hr"))
