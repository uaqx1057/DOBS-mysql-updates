"""Unified offboarding state machine.

Single entry point (request_offboarding) replaces what used to be three
disconnected/inconsistent creation paths: ops_coordinator's route only ever
flipped legacy Driver flags without creating a real Offboarding row, and
ops_manager had two routes that created rows with different starting
statuses. Every offboarding now starts life as exactly one Offboarding row.

Sequence:
  Requested -> (Ops Manager approves) -> OpsSupervisor
    -> (Ops Supervisor clears, reclaims platform IDs, records any penalty)
    -> has the driver EVER had a vehicle assignment (not just an active one)?
         yes -> Fleet   |   no -> skip straight to Finance
    -> (Fleet reviews details, adds deductions) -> Finance
    -> (Finance does all calculations) -> HR
    -> (HR gives final verdict) -> Completed
"""
from datetime import datetime

from extensions import db
from models import AssignDriver, Offboarding


def has_ever_had_vehicle(driver) -> bool:
    """True if the driver has any vehicle assignment history at all, active
    or not - this decides whether Fleet is part of the pipeline."""
    return AssignDriver.query.filter_by(driver_id=driver.id).count() > 0


def get_open_offboarding(driver) -> Offboarding:
    """The driver's current in-flight offboarding, if any (anything not
    already Completed)."""
    return (
        Offboarding.query
        .filter(Offboarding.driver_id == driver.id, Offboarding.status != "Completed")
        .order_by(Offboarding.requested_at.desc())
        .first()
    )


def request_offboarding(driver, requested_by_user, reason: str = None) -> Offboarding:
    """Single entry point for starting an offboarding. Idempotent - if the
    driver already has an open offboarding, that record is returned instead
    of creating a duplicate. Callers gate access with
    @require_permission("offboarding.request") rather than a role check, so
    this is grantable to any employee, not just Ops Coordinator/Ops Manager.
    """
    existing = get_open_offboarding(driver)
    if existing:
        return existing

    record = Offboarding(
        driver_id=driver.id,
        requested_by_id=requested_by_user.id,
        requested_at=datetime.utcnow(),
        request_reason=(reason or "").strip() or None,
        status="Requested",
    )
    db.session.add(record)
    db.session.commit()
    return record


def approve_by_ops_manager(record: Offboarding) -> Offboarding:
    """Ops Manager approves a Requested offboarding, sending it to Ops
    Supervisor to reclaim platform IDs and record any penalty."""
    record.ops_manager_approved_at = datetime.utcnow()
    record.status = "OpsSupervisor"
    db.session.commit()
    return record


def next_status_after_ops_supervisor(driver) -> str:
    """Fleet is only in the pipeline for drivers who have ever had a vehicle
    assignment; everyone else skips straight to Finance."""
    return "Fleet" if has_ever_had_vehicle(driver) else "Finance"
