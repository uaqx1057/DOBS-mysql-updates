from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, session
from flask_login import login_required, current_user
from extensions import db, mail
from flask_mail import Message
from datetime import datetime, date
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_, func
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

    # -------------------------
    # Latest offboarding per driver
    latest_requests_subq = (
        db.session.query(
            Offboarding.driver_id,
            func.max(Offboarding.requested_at).label("latest_request")
        )
        .filter(Offboarding.status.in_(["Fleet", "pending_tamm"]))
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
# Assign Vehicle & Send to Finance or HR
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
- Plate: {vehicle_plate}
- Details: {vehicle_details}
- Assignment Date: {driver.assignment_date.strftime('%Y-%m-%d')}
- TAMM Authorized: ✅ Yes (Screenshot uploaded)

Please log in and complete your next stage.

Login here: http://127.0.0.1:5000/dashboard/{next_stage.lower()}

Regards,
Fleet Team
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


# -------------------------
# Fleet Manager Offboarding Clearance
# -------------------------
@fleet_bp.route("/api/clear_offboarding/<int:offboarding_id>", methods=["POST"])
@login_required
def fleet_clear_offboarding(offboarding_id):
    if current_user.role != "FleetManager":
        return jsonify({"success": False, "message": "Access denied"}), 403

    record = Offboarding.query.get_or_404(offboarding_id)
    try:
        data = request.get_json()
        record.fleet_cleared = True
        record.fleet_cleared_at = datetime.utcnow()
        record.fleet_damage_report = data.get("fleet_damage_report")
        record.fleet_damage_cost = float(data.get("fleet_damage_cost") or 0)
        record.status = "Finance"
        db.session.commit()

        finance_users = User.query.filter(User.role.in_(["Finance", "FinanceManager"])).all()
        emails = [f.email for f in finance_users if f.email]
        if emails:
            msg = Message(
                subject=f"Driver sent to Finance for Offboarding: {record.driver.full_name}",
                recipients=emails,
                body=(
                    f"Dear Finance Team,\n\n"
                    f"Driver {record.driver.full_name} (Iqama: {record.driver.iqama_number}) "
                    f"has been cleared by Fleet Manager.\n\n"
                    f"Damage Report: {record.fleet_damage_report or 'N/A'}\n"
                    f"Damage Cost: {record.fleet_damage_cost or 0} SAR\n\n"
                    f"Please log in and proceed with settlement."
                )
            )
            mail.send(msg)

        return jsonify({
            "success": True,
            "driver_name": record.driver.full_name,
            "cleared_at": record.fleet_cleared_at.strftime("%Y-%m-%d %H:%M"),
            "damage_cost": record.fleet_damage_cost,
            "damage_report": record.fleet_damage_report
        })

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"[FLEET CLEAR OFFBOARDING ERROR] {e}")
        return jsonify({"success": False, "message": str(e)}), 500


# -------------------------
# TAMM Revocation / Full Offboarding
# -------------------------
@fleet_bp.route("/api/revoke_tamm/<int:offboarding_id>", methods=["POST"])
@login_required
def revoke_tamm(offboarding_id):
    if current_user.role != "FleetManager":
        return jsonify({"success": False, "message": "Access denied"}), 403

    record = Offboarding.query.get_or_404(offboarding_id)
    data = request.get_json()

    try:
        if not data.get("tamm_revoked"):
            return jsonify({"success": False, "message": "TAMM not revoked"}), 400

        record.status = "Completed"
        record.fleet_cleared = True
        record.fleet_cleared_at = datetime.utcnow()
        record.tamm_revoked = True
        record.tamm_revoked_at = datetime.utcnow()

        db.session.commit()

        recipients = [u.email for u in User.query.filter(User.role.in_(["HR", "Admin"])).all() if u.email]
        if recipients:
            msg = Message(
                subject=f"Driver Fully Offboarded: {record.driver.full_name}",
                recipients=recipients,
                body=f"""
Dear HR / Admin Team,

Driver {record.driver.full_name} (Iqama: {record.driver.iqama_number}) has been fully offboarded by the Fleet Manager after TAMM revocation.

Offboarding completed at: {record.fleet_cleared_at.strftime('%Y-%m-%d %H:%M')}
TAMM Revoked at: {record.tamm_revoked_at.strftime('%Y-%m-%d %H:%M')}

Please update your records accordingly.

Regards,
Fleet Team
"""
            )
            mail.send(msg)

        return jsonify({
            "success": True,
            "message": f"Driver {record.driver.full_name} fully offboarded and email sent.",
            "tamm_revoked_at": record.tamm_revoked_at.strftime("%Y-%m-%d %H:%M")
        })

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"[TAMM REVOCATION ERROR] {e}")
        return jsonify({"success": False, "message": str(e)}), 500
