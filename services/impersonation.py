"""SuperAdmin 'login as user' impersonation.

Session mechanics: starting impersonation stashes the admin's own id in
session["impersonator_id"] plus the audit-log row id in
session["impersonation_log_id"], then swaps Flask-Login's current_user to
the target via login_user(). Every dashboard guard, sidebar builder, and
permission check already keys off current_user (see services/rbac.py,
app.py's current_user_nav_sections), so the impersonated view falls out of
that machinery for free - nothing else needs to know impersonation is
happening.

Stopping does the reverse: close the audit row, log the admin back in,
clear both session keys. A regular logout while impersonating closes the
audit row too (via close_dangling_log), so there's never a row left with
ended_at still NULL after the session actually ends.
"""
from datetime import datetime

from extensions import db
from models import ImpersonationLog, User


class ImpersonationError(Exception):
    """Raised for invalid impersonation attempts (self, already active)."""


def start(admin_user, target_user, session, ip_address=None) -> ImpersonationLog:
    if session.get("impersonator_id"):
        raise ImpersonationError("Already impersonating - return to your account first.")
    if target_user.id == admin_user.id:
        raise ImpersonationError("You can't impersonate yourself.")

    log = ImpersonationLog(
        admin_user_id=admin_user.id,
        target_user_id=target_user.id,
        started_at=datetime.utcnow(),
        ip_address=ip_address,
    )
    db.session.add(log)
    db.session.commit()

    session["impersonator_id"] = admin_user.id
    session["impersonation_log_id"] = log.id
    return log


def stop(session) -> User:
    """Ends the active impersonation and returns the admin user to log back
    in as. Raises ImpersonationError if nothing is active."""
    admin_id = session.get("impersonator_id")
    if not admin_id:
        raise ImpersonationError("Not currently impersonating.")

    log_id = session.get("impersonation_log_id")
    if log_id:
        log = ImpersonationLog.query.get(log_id)
        if log and not log.ended_at:
            log.ended_at = datetime.utcnow()
            db.session.commit()

    admin_user = User.query.get(admin_id)
    session.pop("impersonator_id", None)
    session.pop("impersonation_log_id", None)
    return admin_user


def close_dangling_log(session) -> None:
    """Safety net for a plain logout while impersonating - closes the audit
    row so it never sits with ended_at NULL after the session actually
    ends, without restoring the admin's login."""
    log_id = session.get("impersonation_log_id")
    if log_id:
        log = ImpersonationLog.query.get(log_id)
        if log and not log.ended_at:
            log.ended_at = datetime.utcnow()
            db.session.commit()
    session.pop("impersonator_id", None)
    session.pop("impersonation_log_id", None)
