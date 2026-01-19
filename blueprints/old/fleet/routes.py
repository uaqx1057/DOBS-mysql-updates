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
        .options(joinedload(Driver.platforms))
        .filter_by(onboarding_stage="Fleet Manager")
        .all()
    )

    # Latest offboarding per driver
    latest_requests_subq = (
        db.session.query(
            Offboarding.driver_id,
            db.func.max(Offboarding.requested_at).label("latest_request")
        )
        .filter(Offboarding.status.in_(["Fleet", "pending_tamm", "FinanceManager"]))
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
    if current_user.role != "FleetManager":
        flash("Access denied. Fleet Manager role required.", "danger")
        return redirect(url_for("auth.login"))

    driver = Driver.query.get_or_404(driver_id)
    vehicle_plate = request.form.get("vehicle_plate", "").strip()
    vehicle_details = request.form.get("vehicle_details", "").strip()
    assignment_date = request.form.get("assignment_date", "").strip()
    tamm_authorized = request.form.get("tamm_authorized")
    tamm_file = request.files.get("tamm_authorization_ss")

    if not (vehicle_plate and vehicle_details and assignment_date and tamm_authorized):
        flash("All fields including TAMM Authorization must be filled before approval.", "danger")
        return redirect(url_for("fleet.dashboard_fleet"))

    if not tamm_file or not tamm_file.filename:
        flash("⚠️ TAMM Authorization Screenshot is required before approval.", "danger")
        return redirect(url_for("fleet.dashboard_fleet"))

    try:
        parsed_date = datetime.strptime(assignment_date, "%Y-%m-%d").date()
        if parsed_date > date.today():
            flash("Assignment date cannot be in the future.", "danger")
            return redirect(url_for("fleet.dashboard_fleet"))

        ext = os.path.splitext(tamm_file.filename)[1].lower()
        safe_name = secure_filename(
            f"{driver.full_name}_{driver.iqama_number}_{vehicle_plate}_TAMM_Authorisation{ext}"
        )
        upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], safe_name)
        tamm_file.save(upload_path)

        driver.car_details = f"{vehicle_plate} - {vehicle_details}"
        driver.assignment_date = parsed_date
        driver.tamm_authorized = True
        driver.tamm_authorization_ss = safe_name
        driver.mark_fleet_manager_approved()

        # Determine next stage
        if not driver.qiwa_contract_created:
            next_stage = "HR Final"
            recipients = [u.email for u in User.query.filter(User.role.in_(["HR", "HRManager"])).all() if u.email]
        else:
            next_stage = "Finance"
            recipients = [u.email for u in User.query.filter(User.role.in_(["Finance", "FinanceManager"])).all() if u.email]

        driver.onboarding_stage = next_stage
        db.session.commit()

        if recipients:
            msg = Message(
                subject=f"Driver Ready for {next_stage} Stage: {driver.full_name}",
                recipients=recipients,
                body=f"""
            Hello {next_stage} Team,
            
            Driver {driver.full_name} has been assigned a vehicle by Fleet Manager.
            
            Assigned Vehicle:
            - Plate: {vehicle_plate or "N/A"}
            - Details: {vehicle_details or "N/A"}
            - Assignment Date: {driver.assignment_date.strftime('%Y-%m-%d') if driver.assignment_date else "N/A"}
            - TAMM Authorized: ✅ Yes (Screenshot uploaded)
            
            Please log in and complete your next stage.
            
            Login here: http://127.0.0.1:5000/dashboard/{next_stage.lower()}
            
            ------------------------------------------------------
            
            فريق {next_stage} المحترم،
            
            تم تعيين مركبة للسائق {driver.full_name} بواسطة مدير الأسطول.
            
            المركبة المعينة:
            - اللوحة: {vehicle_plate or "N/A"}
            - التفاصيل: {vehicle_details or "N/A"}
            - تاريخ التعيين: {driver.assignment_date.strftime('%Y-%m-%d') if driver.assignment_date else "N/A"}
            - TAMM مصرح: ✅ نعم (تم رفع لقطة الشاشة)
            
            يرجى تسجيل الدخول وإتمام المرحلة التالية.
            
            Login هنا: http://127.0.0.1:5000/dashboard/{next_stage.lower()}
            
            Regards / مع التحية,
            Fleet Team / فريق الأسطول
            """
            )
            mail.send(msg)

            current_app.logger.info(f"[FLEET] {next_stage} notification email sent successfully.")
        else:
            current_app.logger.warning(f"[FLEET] No {next_stage} users with email found. Skipping notification.")

        flash(f"✅ Vehicle assigned to {driver.full_name} and driver moved to {next_stage} stage.", "success")

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"[FLEET] Error assigning vehicle: {e}")
        flash(f"❌ Error assigning vehicle: {str(e)}", "danger")

    return redirect(url_for("fleet.dashboard_fleet"))


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
                    subject=f"Driver Fully Offboarded: {record.driver.full_name}",
                    recipients=recipients,
                    body=f"""
                Dear HR / Admin Team,
                
                Driver {record.driver.full_name} (Iqama: {record.driver.iqama_number or "N/A"}) has been fully offboarded.
                
                Offboarding completed at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}
                TAMM Revoked at: {record.tamm_revoked_at.strftime('%Y-%m-%d %H:%M') if record.tamm_revoked_at else 'N/A'}
                
                Please update your records accordingly.
                
                ------------------------------------------------------
                
                السادة فريق الموارد البشرية / الإدارة،
                
                تم إتمام خروج السائق {record.driver.full_name} (رقم الإقامة: {record.driver.iqama_number or "N/A"}).
                
                تاريخ إتمام الخروج: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}
                تاريخ إلغاء صلاحية TAMM: {record.tamm_revoked_at.strftime('%Y-%m-%d %H:%M') if record.tamm_revoked_at else 'N/A'}
                
                يرجى تحديث سجلاتكم حسب ذلك.
                
                Regards / مع التحية,
                Fleet Team / فريق الأسطول
                """
                )
                mail.send(msg)


            return jsonify({"success": True, "message": f"Driver {record.driver.full_name} fully offboarded."})

        else:
            # Send to FinanceManager
            record.status = "Finance"
            db.session.commit()

            # Notify Finance
            finance_users = User.query.filter(User.role.in_(["FinanceManager", "Finance"])).all()
            emails = [f.email for f in finance_users if f.email]
            if emails:
                msg = Message(
                    subject=f"Driver Sent to Finance Manager: {record.driver.full_name}",
                    recipients=emails,
                    body=f"""
                Dear Finance Team,
                
                Driver {record.driver.full_name} (Iqama: {record.driver.iqama_number or "N/A"}) has been cleared by Fleet Manager.
                
                Fleet Damage Report: {record.fleet_damage_report or "N/A"}
                Damage Cost: {record.fleet_damage_cost or 0} SAR
                TAMM Revoked: {"Yes" if record.tamm_revoked else "No"}
                
                Please proceed with the settlement.
                
                ------------------------------------------------------
                
                السادة فريق المالية،
                
                تم تحويل السائق {record.driver.full_name} (رقم الإقامة: {record.driver.iqama_number or "N/A"}) من قِبل مدير الأسطول.
                
                تقرير أضرار الأسطول: {record.fleet_damage_report or "N/A"}
                تكلفة الأضرار: {record.fleet_damage_cost or 0} ريال سعودي
                إلغاء صلاحية TAMM: {"نعم" if record.tamm_revoked else "لا"}
                
                يرجى متابعة التسوية حسب الإجراءات.
                
                Regards / مع التحية,
                Fleet Team / فريق الأسطول
                """
                )
                mail.send(msg)


            return jsonify({
                "success": True,
                "message": f"Driver {record.driver.full_name} cleared by Fleet and sent to Finance Manager.",
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
