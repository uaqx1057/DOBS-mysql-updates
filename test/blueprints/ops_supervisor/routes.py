from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models import Driver, DriverPlatform, User
from extensions import db, mail
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from utils.email_utils import send_password_change_email 


ops_supervisor_bp = Blueprint("ops_supervisor", __name__)

# -------------------------
# Ops Supervisor Dashboard
# -------------------------

@ops_supervisor_bp.route("/dashboard")
@login_required
def dashboard_ops_supervisor():
    if current_user.role != "OpsSupervisor":
        flash("Access denied", "danger")
        return redirect(url_for("auth.login"))

    # 🔹 Drivers still in onboarding (Ops Supervisor stage)
    onboarding_drivers = (
        Driver.query
        .filter_by(onboarding_stage="Ops Supervisor")
        .order_by(Driver.id.desc())
        .all()
    )
    
    current_app.logger.info(f"[OPS_SUP DASHBOARD] onboarding_drivers={onboarding_drivers}")

        # 🔹 Offboarding requests at Ops Supervisor stage
    offboarding_requests = (
        Offboarding.query
        .filter(Offboarding.status.in_(["Requested", "OpsSupervisor"]))
        .order_by(Offboarding.requested_at.desc())
        .all()
    )
    total_drivers = Driver.query.filter_by(onboarding_stage="Ops Supervisor").count()
    total_users = Offboarding.query.filter(Offboarding.status.in_(["Requested", "OpsSupervisor"])).count()

    from flask import session
    lang = session.get("lang", "en")
    template = (
        "rtl_dashboard_ops_supervisor.html" if lang == "ar" else "dashboard_ops_supervisor.html"
    )

    return render_template(
        template,
        total_drivers=total_drivers,
        total_users=total_users,
        onboarding_drivers=onboarding_drivers,
        offboarding_requests=offboarding_requests
    )

# -------------------------
# Approve & Send to Fleet Manager
# -------------------------
# Replace your existing approve_driver with this
@ops_supervisor_bp.route("/approve_driver/<int:driver_id>", methods=["POST"])
@login_required
def approve_driver(driver_id):
    """Approve driver, assign multiple platforms, update optional issued data, and forward to Fleet Manager."""
    if current_user.role != "OpsSupervisor":
        flash("Access denied. Ops Supervisor role required.", "danger")
        return redirect(url_for("auth.login"))

    driver = Driver.query.get_or_404(driver_id)

    current_app.logger.info(f"[OPS_SUPERVISOR][START] driver_id={driver_id} form={dict(request.form)}")

    # Collect multiple platforms & IDs
    platform_names = request.form.getlist("platform_name[]")
    platform_ids = request.form.getlist("platform_id[]")
    issued_mobile_number = (request.form.get("issued_mobile_number") or "").strip() or None
    issued_device_id = (request.form.get("issued_device_id") or "").strip() or None
    mobile_issued = bool(request.form.get("mobile_issued"))  # True if checked, False if not

    # Validate minimum one platform
    if not platform_names or not platform_ids or len(platform_names) != len(platform_ids):
        flash("Please provide at least one platform and its ID.", "danger")
        return redirect(url_for("ops_supervisor.dashboard_ops_supervisor"))

    try:
        # Clear existing platforms (overwrite)
        driver.platforms.clear()

        # Add multiple platforms
        for name, pid in zip(platform_names, platform_ids):
            dp = DriverPlatform(
                driver_id=driver.id,
                platform_name=name.strip(),
                platform_user_id=pid.strip()
            )
            db.session.add(dp)

        # Update optional issued info
        driver.issued_mobile_number = issued_mobile_number
        driver.issued_device_id = issued_device_id
        driver.mobile_issued = mobile_issued
        driver.ops_supervisor_approved_at = datetime.utcnow()
        driver.onboarding_stage = "Fleet Manager"

        db.session.add(driver)
        db.session.commit()

        current_app.logger.info(f"[OPS_SUPERVISOR][SAVED] driver_id={driver.id} platforms={platform_names}")

        flash(f"✅ Driver {driver.full_name} processed and sent to Fleet Manager.", "success")

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("[OPS_SUPERVISOR][ERROR] saving driver:")
        flash(f"❌ Error saving driver data: {str(e)}", "danger")
        return redirect(url_for("ops_supervisor.dashboard_ops_supervisor"))

    # Notify Fleet
    try:
        fleet_users = User.query.filter_by(role="FleetManager").all()
        recipients = [u.email for u in fleet_users if u.email]
        if recipients:
            platforms_text = "\n".join([f"- {n} (ID: {i})" for n, i in zip(platform_names, platform_ids)])
            msg = Message(
                subject=f"Driver Ready for Fleet Assignment: {driver.full_name}",
                recipients=recipients,
                body=f"""Hello Fleet Team,

Driver {driver.full_name} has been processed by Ops Supervisor.

Platforms Assigned:
{platforms_text}

Issued Mobile: {driver.issued_mobile_number or 'N/A'}
Issued Device: {driver.issued_device_id or 'N/A'}
Mobile & SIM Issued: {'✅ Yes' if mobile_issued else '❌ No'}
Approved At: {driver.ops_supervisor_approved_at.strftime('%Y-%m-%d %H:%M')}

Please assign a vehicle and complete Fleet stage processing.
"""
            )
            mail.send(msg)
    except Exception as e:
        current_app.logger.warning("[OPS_SUPERVISOR] fleet email error: %s", e)

    return redirect(url_for("ops_supervisor.dashboard_ops_supervisor"))

# -------------------------
# Change Password
# -------------------------
@ops_supervisor_bp.route("/change_password", methods=["POST"])
@login_required
def change_password():
    """Allow Ops Supervisor to change their own password securely and get an email notification."""
    if current_user.role != "OpsSupervisor":
        flash("Access denied. Ops Supervisor role required.", "danger")
        return redirect(url_for("auth.login"))

    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not check_password_hash(current_user.password, current_password):
        flash("❌ Current password is incorrect.", "danger")
        return redirect(url_for("ops_supervisor.dashboard_ops_supervisor"))

    if new_password != confirm_password:
        flash("❌ New passwords do not match.", "danger")
        return redirect(url_for("ops_supervisor.dashboard_ops_supervisor"))

    try:
        # Update password in database
        current_user.password = generate_password_hash(new_password)
        db.session.commit()

        # Send email using helper
        if send_password_change_email(current_user, new_password):
            flash("✅ Password updated and email notification sent.", "success")
        else:
            flash("✅ Password updated, but email could not be sent.", "warning")

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"[OPS_SUPERVISOR] Password update failed: {e}")
        flash("❌ Could not update password. Please try again.", "danger")

    return redirect(url_for("ops_supervisor.dashboard_ops_supervisor"))

# -------------------------
# Offboarding Dashboard
# -------------------------
from models import Offboarding
@ops_supervisor_bp.route("/offboarding")
@login_required
def offboarding_dashboard():
    if current_user.role != "OpsSupervisor":
        flash("Access denied", "danger")
        return redirect(url_for("auth.login"))

    # fetch all offboarding requests pending at ops supervisor stage
    offboarding_requests = (
    Offboarding.query
    .filter(Offboarding.status.in_(["Requested", "OpsSupervisor"]))
    .order_by(Offboarding.requested_at.desc())
    .all() )
    
    return render_template("dashboard_ops_supervisor.html", offboarding_requests=offboarding_requests)

# Handle Ops Supervisor Clearance
@ops_supervisor_bp.route("/api/clear_offboarding/<int:offboarding_id>", methods=["POST"])
@login_required
def api_clear_offboarding(offboarding_id):
    if current_user.role != "OpsSupervisor":
        return {"success": False, "message": "Access denied"}, 403

    record = Offboarding.query.get_or_404(offboarding_id)

    try:
        data = request.get_json(force=True)  # parse JSON payload
        record.ops_supervisor_cleared = True
        record.ops_supervisor_cleared_at = datetime.utcnow()
        record.company_mobile_returned = bool(data.get("company_mobile_returned"))
        record.company_sim_returned = bool(data.get("company_sim_returned"))
        record.platform_returned = bool(data.get("platform_returned"))
        record.ops_supervisor_note = data.get("ops_supervisor_note", "")
        record.ops_supervisor_id = current_user.id
        record.status = "Fleet"

        db.session.commit()

         # ✅ Notify Fleet Managers by email
        try:
            fleet_managers = User.query.filter_by(role="FleetManager").all()
            emails = [u.email for u in fleet_managers if u.email]
            if emails:
                msg = Message(
                    subject=f"Offboarding ready for Fleet Clearance: {record.driver.full_name}",
                    recipients=emails,
                    sender=current_app.config.get("MAIL_DEFAULT_SENDER"),
                    body=f"""Dear Fleet Manager,

Driver {record.driver.full_name} (Iqama: {record.driver.iqama_number})
has been cleared by Ops Supervisor and is now ready for Fleet clearance.

Please log in to continue processing.

Cleared At: {record.ops_supervisor_cleared_at.strftime('%Y-%m-%d %H:%M')}
"""
                )
                mail.send(msg)
        except Exception as e:
            current_app.logger.warning("[OPS_SUPERVISOR] Fleet email error: %s", e)

        return {
            "success": True,
            "driver_name": record.driver.full_name,
            "cleared_at": record.ops_supervisor_cleared_at.strftime("%Y-%m-%d %H:%M"),
            "status": record.status
        }

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("[OPS_SUPERVISOR][API CLEAR ERROR]")
        return {"success": False, "message": str(e)}, 500
