import os
from datetime import datetime, timezone

from flask import current_app, redirect, render_template, request, url_for
from flask_login import login_user
from sqlalchemy import text

from blueprints.sso import sso_bp
from extensions import db
from models import User


def _hr_url():
    return os.environ.get("HR_URL", "https://hr.speedlogi.sa")


# Role → dashboard endpoint mapping (mirrors auth/routes.py)
ROLE_REDIRECTS = {
    "superadmin":     "admin.dashboard",
    "hr":             "hr.dashboard_hr",
    "opscoordinator": "ops_coordinator.dashboard_ops_coordinator",
    "opsmanager":     "ops_manager.dashboard_ops",
    "opssupervisor":  "ops_supervisor.dashboard_ops_supervisor",
    "fleetmanager":   "fleet.dashboard_fleet",
    "financemanager": "finance.dashboard_finance",
}


def _error(message, status=400):
    return render_template("sso_error.html", message=message, hr_url=_hr_url()), status


@sso_bp.route("/login")
def sso_login():
    token = request.args.get("token", "").strip()

    if len(token) != 64:
        return _error("Invalid login link.")

    # DOBS and HR share dobsykjq_dms_hr_merge, so sso_tokens is accessible via our own DB session.
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)

    try:
        # Atomic claim via UPDATE — prevents replay even under concurrent requests
        result = db.session.execute(
            text("""UPDATE sso_tokens
                    SET used_at = :now
                    WHERE token = :token
                      AND target_system = 'dobs'
                      AND used_at IS NULL
                      AND expires_at > :now"""),
            {"now": now_utc, "token": token},
        )
        db.session.commit()
        affected = result.rowcount

        if affected == 0:
            return _error(
                "This login link has expired or already been used. "
                "Return to the HR portal and try again."
            )

        row = db.session.execute(
            text("SELECT system_user_id FROM sso_tokens WHERE token = :token"),
            {"token": token},
        ).fetchone()

    except Exception as exc:
        db.session.rollback()
        current_app.logger.error("SSO token validation error: %s", exc)
        return _error("Authentication service temporarily unavailable. Please try again.", 503)

    if not row:
        return _error("Login link error. Please try again.")

    user = User.query.get(int(row[0]))

    if not user:
        return _error(
            "No DOBS account is linked to your HR profile. Contact your administrator.",
            403,
        )

    login_user(user, remember=False)

    role_key = (user.role or "").lower().replace(" ", "")
    endpoint = ROLE_REDIRECTS.get(role_key, "auth.login")
    return redirect(url_for(endpoint))
