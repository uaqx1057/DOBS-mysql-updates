# blueprints/hr/routes.py
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models import Driver, User, Offboarding
from extensions import db, mail, csrf
from services.hr_service import process_hr_approval, save_transfer_proof, send_rejection_email
from utils.auth import require_roles
from flask_mail import Message
from datetime import datetime
import os
import sqlalchemy as sa
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from services.hr_service import process_hr_approval, save_transfer_proof, send_rejection_email
from sqlalchemy.exc import IntegrityError

hr_bp = Blueprint("hr", __name__, url_prefix='/hr')

ALLOWED_EXT = {'.jpg', '.jpeg', '.png', '.pdf'}


def _upload_root() -> str:
    path = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(path, exist_ok=True)
    return path

def _allowed_filename(fn):
    _, ext = os.path.splitext(fn.lower())
    return ext in ALLOWED_EXT

def _serialize_driver(d): 
    return {
        "id": d.id,
        "driver_id": d.driver_id,
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


def _next_driver_code():
    """Generate next driver code like D0001 using a locked read to reduce race risk."""
    prefix = "D"
    row = db.session.execute(
        sa.text(
            "SELECT driver_id FROM drivers WHERE driver_id LIKE :pref ORDER BY driver_id DESC LIMIT 1 FOR UPDATE"
        ),
        {"pref": f"{prefix}%"},
    ).first()
    last_val = row[0] if row else None
    try:
        last_num = int(last_val[1:]) if last_val and last_val.startswith(prefix) else 0
    except ValueError:
        last_num = 0
    return f"{prefix}{last_num + 1:04d}"


def _ensure_driver_code(driver: Driver, retries: int = 5):
    if driver.driver_id:
        return
    for attempt in range(1, retries + 1):
        candidate = _next_driver_code()
        driver.driver_id = candidate
        try:
            with db.session.begin_nested():
                db.session.flush()
            return
        except IntegrityError:
            db.session.rollback()
            driver.driver_id = None
            if attempt == retries:
                raise ValueError("Could not assign unique driver code after retries")


def _ensure_driver_password(driver: Driver):
    if driver.password:
        return

    # Create a unique, non-shared password hash for the driver
    random_password = os.urandom(16).hex()
    driver.password = generate_password_hash(random_password)

def _serialize_offboarding(o):
    return {
        "offboarding_id": o.id,
        "driver_id": o.driver.id if o.driver else None,
        "name": o.driver.name if o.driver else "",
        "iqaama_number": o.driver.iqaama_number if o.driver else "",
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
@require_roles("HR")
def dashboard_hr():

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
@require_roles("HR")
def approve_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    files = request.files
    max_bytes = current_app.config.get("MAX_CONTENT_LENGTH", 16 * 1024 * 1024)

    try:
        process_hr_approval(driver, files, request.form, _upload_root(), max_bytes)
        _ensure_driver_password(driver)
        db.session.commit()
        current_app.logger.info(
            "hr_approve_driver",
            extra={"user": current_user.username, "driver_id": driver.id, "iqama": driver.iqaama_number},
        )
    except ValueError as ve:
        db.session.rollback()
        flash(str(ve), "danger")
        return redirect(url_for("hr.dashboard_hr"))
    except Exception as e:
        db.session.rollback()
        flash(f"Error approving driver: {e}", "danger")
        return redirect(url_for("hr.dashboard_hr"))

    # Notify Ops Supervisors
    try:
        ops_supervisors = User.query.filter_by(role="OpsSupervisor").all()
        recipients = [op.email for op in ops_supervisors if op.email]
        if recipients:
            msg = Message(
                subject=f"Driver Ready for Ops Supervisor Stage | السائق جاهز لمرحلة مشرف العمليات: {driver.name}",
                recipients=recipients
            )

            msg.html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">

                    <!-- English LTR -->
                    <div style="text-align: left;">
                        <h2 style="color: #713183;">Driver Processing Notification</h2>
                        <p>Hello Ops Supervisor Team,</p>
                        <p>Driver <strong>{driver.name}</strong> (iqaama: <strong>{driver.iqaama_number or "N/A"}</strong>) has been moved to your stage for processing.</p>
                        <p>Please review and complete the necessary actions.</p>
                        <p>Login to your dashboard: <a href="https://dobs.dobs.cloud/login" target="_blank">https://dobs.dobs.cloud/login</a></p>
                    </div>

                    <hr style="margin: 30px 0;">

                    <!-- Arabic RTL -->
                    <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                        <h2 style="color: #713183;">إشعار متابعة السائق</h2>
                        <p>السادة فريق مشرف العمليات،</p>
                        <p>تم نقل السائق <strong>{driver.name}</strong> (رقم الإقامة: <strong>{driver.iqaama_number or "N/A"}</strong>) إلى مرحلتكم لمتابعة الإجراءات.</p>
                        <p>يرجى مراجعة البيانات واستكمال الإجراءات المطلوبة.</p>
                        <p>تسجيل الدخول إلى لوحة القيادة: <a href="https://dobs.dobs.cloud/login" target="_blank">https://dobs.dobs.cloud/login</a></p>
                    </div>

                    <hr style="margin: 30px 0;">

                    <p style="text-align:center;">Regards / مع التحية,<br>Operations Team / فريق العمليات</p>

                </div>
            </body>
            </html>
            """

            mail.send(msg)

    except Exception as e:
        print("[EMAIL ERROR]", e)

    flash(f"Driver {driver.name} approved and sent to Ops Supervisor stage.", "success")
    return redirect(url_for("hr.dashboard_hr"))



@hr_bp.route("/reject_driver/<int:driver_id>", methods=["POST"])
@login_required
@require_roles("HR")
def reject_driver(driver_id):

    driver = Driver.query.get_or_404(driver_id)
    reason = request.form.get("rejection_reason", "").strip()

    if not reason:
        flash("Please provide a rejection reason.", "warning")
        return redirect(url_for("hr.dashboard_hr"))

    driver_name = driver.name
    iqaama_number = driver.iqaama_number
    nationality = driver.nationality

    try:
        # Delete driver permanently
        db.session.delete(driver)
        db.session.commit()
        current_app.logger.info(
            "hr_reject_driver",
            extra={"user": current_user.username, "driver_id": driver.id, "iqama": driver.iqaama_number, "reason": reason},
        )

        # Collect recipients (Ops, HR, Admin)
        recipients = []
        ops_managers = User.query.filter_by(role="OpsManager").all()
        hr_users = User.query.filter_by(role="HR").all()
        admins = User.query.filter_by(role="SuperAdmin").all()

        for group in (ops_managers, hr_users, admins):
            recipients.extend([u.email for u in group if u.email])

        send_rejection_email(
            mail,
            recipients,
            driver_name,
            iqaama_number,
            nationality,
            reason,
            current_user.name,
        )

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
@require_roles("HR")
def complete_sponsorship_transfer(driver_id):

    driver = Driver.query.get_or_404(driver_id)

    try:
        # Determine current case
        if not driver.qiwa_contract_created:
            # 🔹 Case 1: Driver has NO Qiwa contract
            driver.onboarding_stage = "Completed"
            _ensure_driver_code(driver)
            driver.sponsorship_transfer_status = "Not Required"
            driver.sponsorship_transfer_proof = None
            driver.sponsorship_transfer_completed_at = datetime.utcnow()
            db.session.commit()

            flash(f"✅ Driver {driver.name} marked as completed (no Qiwa contract).", "success")

        else:
            transfer_status = request.form.get("sponsorship_transfer_status")
            file = request.files.get("sponsorship_transfer_proof")
            try:
                max_bytes = current_app.config.get("MAX_CONTENT_LENGTH", 16 * 1024 * 1024)
                save_transfer_proof(driver, file, _upload_root(), transfer_status, max_bytes)
                driver.onboarding_stage = "Completed"
                _ensure_driver_code(driver)
                db.session.commit()
                current_app.logger.info(
                    "hr_complete_transfer",
                    extra={"user": current_user.username, "driver_id": driver.id, "iqama": driver.iqaama_number},
                )
                flash(f"✅ Sponsorship transfer completed for {driver.name}.", "success")
            except ValueError as ve:
                db.session.rollback()
                flash(str(ve), "warning")
                return redirect(url_for("hr.dashboard_hr"))
            except Exception as e:
                db.session.rollback()
                flash(f"Error completing transfer: {e}", "danger")
                return redirect(url_for("hr.dashboard_hr"))

        # 📧 Notify SuperAdmins after completion
        superadmins = User.query.filter_by(role="SuperAdmin").all()
        recipients = [sa.email for sa in superadmins if sa.email]
        if recipients:
            msg = Message(
                subject=f"Driver Onboarding Completed | اكتمال انضمام السائق: {driver.name}",
                recipients=recipients
            )

            msg.html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                    
                    <!-- English -->
                    <div style="text-align: left;">
                        <h2 style="color: #713183;">Driver Onboarding Completed</h2>
                        <p>Dear Team,</p>
                        <p>Driver <strong>{driver.name}</strong> has successfully completed the onboarding process.</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>iqaama</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.iqaama_number or "N/A"}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Qiwa Contract Created</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{'✅ Yes' if driver.qiwa_contract_created else '❌ No'}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Sponsorship Transfer Completed At</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.sponsorship_transfer_completed_at.strftime('%Y-%m-%d %H:%M') if driver.sponsorship_transfer_completed_at else 'N/A'}</td>
                            </tr>
                        </table>
                        <p>Please update your records accordingly.</p>
                        <p>Login to your dashboard: <a href="https://dobs.dobs.cloud/login" target="_blank">https://dobs.dobs.cloud/login</a></p>
                    </div>

                    <hr style="margin: 30px 0;">

                    <!-- Arabic -->
                    <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                        <h2 style="color: #713183;">اكتمل انضمام السائق</h2>
                        <p>السادة الفريق،</p>
                        <p>لقد أكمل السائق <strong>{driver.name}</strong> عملية الانضمام بنجاح.</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">رقم الإقامة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.iqaama_number or "N/A"}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">إنشاء عقد قوى</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{'✅ نعم' if driver.qiwa_contract_created else '❌ لا'}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">تاريخ إكمال نقل الكفالة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{driver.sponsorship_transfer_completed_at.strftime('%Y-%m-%d %H:%M') if driver.sponsorship_transfer_completed_at else 'N/A'}</td>
                            </tr>
                        </table>
                        <p>يرجى تحديث سجلاتكم وفقاً لذلك.</p>
                        <p>تسجيل الدخول إلى لوحة القيادة: <a href="https://dobs.dobs.cloud/login" target="_blank">https://dobs.dobs.cloud/login</a></p>
                    </div>

                </div>
            </body>
            </html>
            """

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
        _ensure_driver_code(driver) 
        _ensure_driver_password(driver)
        driver.sponsorship_transfer_status = "Not Required"
        driver.sponsorship_transfer_proof = None
        driver.sponsorship_transfer_completed_at = datetime.utcnow()
        db.session.commit()
        flash(f"✅ Driver {driver.name} marked as completed (no Qiwa contract).", "success")
    else:
        flash(f"⚠️ Driver {driver.name} has a Qiwa contract. Use normal transfer workflow.", "warning")

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
    flash(f"Offboarding process started for {driver.name}.", "info")
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
    flash(f"HR clearance completed for {offboarding.driver.name}.", "success")
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
                subject=f"Driver Fully Offboarded | اكتمال خروج السائق: {offboarding.driver.name}",
                recipients=recipients
            )

            msg.html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">

                    <!-- English -->
                    <div style="text-align: left;">
                        <h2 style="color: #713183;">Driver Fully Offboarded</h2>
                        <p>Hello Team,</p>
                        <p>HR has completed the offboarding process for driver <strong>{offboarding.driver.name}</strong>.</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Driver Name</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{offboarding.driver.name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Iqama Number</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{offboarding.driver.iqaama_number or 'N/A'}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;"><strong>Offboarding Completed At</strong></td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{datetime.utcnow().strftime('%Y-%m-%d %H:%M')}</td>
                            </tr>
                        </table>
                        <p>The record has been updated and the driver is fully offboarded.</p>
                    </div>

                    <hr style="margin: 30px 0;">

                    <!-- Arabic -->
                    <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                        <h2 style="color: #713183;">اكتمال خروج السائق</h2>
                        <p>مرحبًا بالفريق،</p>
                        <p>لقد قامت إدارة الموارد البشرية بإنهاء عملية مغادرة السائق <strong>{offboarding.driver.name}</strong>.</p>
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">اسم السائق</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{offboarding.driver.name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">رقم الإقامة</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{offboarding.driver.iqaama_number or 'N/A'}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px; border: 1px solid #ddd;">تاريخ اكتمال الخروج</td>
                                <td style="padding: 8px; border: 1px solid #ddd;">{datetime.utcnow().strftime('%Y-%m-%d %H:%M')}</td>
                            </tr>
                        </table>
                        <p>تم تحديث السجل وتم إلغاء تثبيت برنامج التشغيل بالكامل.</p>
                    </div>

                    <hr style="margin: 30px 0;">
                    <p style="text-align:center;">Regards / مع التحية,<br>HR Team / فريق الموارد البشرية</p>

                </div>
            </body>
            </html>
            """

            mail.send(msg)


    except Exception as e:
        print("[EMAIL ERROR]", e)
        if request.is_json:
            return jsonify({"success": False, "message": f"Email send failed: {str(e)}"}), 500
        flash(f"Email send failed: {str(e)}", "danger")
        return redirect(url_for("hr.dashboard_hr"))

    success_message = f"HR clearance completed for {offboarding.driver.name} and notified."
    if request.is_json:
        return jsonify({"success": True, "message": success_message})
    flash(success_message, "success")
    return redirect(url_for("hr.dashboard_hr"))
