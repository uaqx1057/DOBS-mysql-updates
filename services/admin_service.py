from datetime import datetime, date
from typing import Iterable

from extensions import db
from models import (
    BusinessDriver,
    BusinessID,
    Driver,
    DriverBusinessIDS,
    Offboarding,
    User,
    _next_driver_id,
)
import sqlalchemy as sa
from werkzeug.security import generate_password_hash


def _to_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "y", "on"}


def _parse_date_value(value):
    if value in (None, ""):
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return value
    try:
        if "T" in value:
            return datetime.fromisoformat(value)
        return datetime.fromisoformat(value).date()
    except Exception:
        return None


def update_driver_from_form(driver: Driver, form_data, business_ids: Iterable[str], platform_ids: Iterable[str]):
    """Update driver fields and business assignments from submitted form data."""
    bool_fields = {"saudi_driving_license", "mobile_issued", "tamm_authorized", "transfer_fee_paid"}
    date_fields = {"iqaama_expiry", "assignment_date", "transfer_fee_paid_at"}

    for field in form_data.keys():
        if field in {"csrf_token", "business_id[]", "platform_id[]", "driver_id"}:
            continue

        if not hasattr(driver, field):
            continue

        value = form_data.get(field)
        if field in bool_fields:
            setattr(driver, field, _to_bool(value))
        elif field in date_fields:
            setattr(driver, field, _parse_date_value(value))
        elif field == "transfer_fee_amount":
            try:
                setattr(driver, field, float(value) if value not in (None, "") else None)
            except (TypeError, ValueError):
                setattr(driver, field, None)
        else:
            setattr(driver, field, value)

    # --- Unify assignment logic with DMS ---
    # In DMS, assignments are made by BusinessID (business_ids.id)
    selected_business_id_ids = [int(str(p).strip()) for p in platform_ids if str(p).strip()]

    # Close assignments removed from this driver
    active_assignments = (
        DriverBusinessIDS.query
        .filter_by(driver_id=driver.id, transferred_at=None)
        .all()
    )
    active_id_set = {a.business_id_id for a in active_assignments}
    new_id_set = set(selected_business_id_ids)

    for old in active_assignments:
        if old.business_id_id not in new_id_set:
            old.transferred_at = datetime.utcnow()
            # Remove current link for this business ID
            BusinessDriver.query.filter_by(business_id=old.business_id_id).delete()

    # Assign new/kept IDs
    for b_id in selected_business_id_ids:
        # If already active for this driver, keep link and continue
        if b_id in active_id_set:
            BusinessDriver.query.filter_by(business_id=b_id).delete()
            db.session.add(
                BusinessDriver(
                    driver_id=driver.id,
                    business_id=b_id,
                )
            )
            continue

        # Check if assigned to another driver (active)
        existing = (
            DriverBusinessIDS.query
            .filter_by(business_id_id=b_id, transferred_at=None)
            .first()
        )
        previous_driver_id = None
        if existing and existing.driver_id != driver.id:
            existing.transferred_at = datetime.utcnow()
            previous_driver_id = existing.driver_id

        # Always create a fresh history record
        db.session.add(
            DriverBusinessIDS(
                driver_id=driver.id,
                business_id_id=b_id,
                assigned_at=datetime.utcnow(),
                transferred_at=None,
                previous_driver_id=previous_driver_id,
            )
        )

        # Replace current link (one active per business_id_id)
        BusinessDriver.query.filter_by(business_id=b_id).delete()
        db.session.add(
            BusinessDriver(
                driver_id=driver.id,
                business_id=b_id,
            )
        )

    # Keep legacy fields in sync for modules still reading drivers.platform/platform_id
    selected_business_ids = (
        BusinessID.query
        .filter(BusinessID.id.in_(selected_business_id_ids))
        .all()
    ) if selected_business_id_ids else []

    business_id_map = {int(bid.id): bid for bid in selected_business_ids}
    business_names = []
    for b_id in selected_business_id_ids:
        bid = business_id_map.get(b_id)
        if not bid or not bid.business or not bid.business.name:
            continue
        if bid.business.name not in business_names:
            business_names.append(bid.business.name)

    driver.platform_id = ",".join(str(b_id) for b_id in selected_business_id_ids) if selected_business_id_ids else None
    driver.platform = ", ".join(business_names) if business_names else None

    db.session.commit()
    return driver


def delete_driver_and_offboarding(driver_id: int):
    driver = Driver.query.get_or_404(driver_id)
    Offboarding.query.filter_by(driver_id=driver.id).delete()
    db.session.delete(driver)
    db.session.commit()


def create_user_from_form(username: str, raw_password: str, role: str, name: str, designation: str, branch_city: str, email: str) -> User:
    user = User(
        username=username,
        password=generate_password_hash(raw_password),
        role=role,
        name=name,
        designation=designation,
        branch_city=branch_city,
        email=email,
    )
    db.session.add(user)
    db.session.commit()
    return user


def update_user_from_form(user: User, username: str, name: str, designation: str, branch_city: str, email: str, role: str) -> User:
    user.username = username or user.username
    user.name = name or user.name
    user.designation = designation or user.designation
    user.branch_city = branch_city or user.branch_city
    user.email = email or user.email
    user.role = role or user.role
    db.session.commit()
    return user


def delete_user(user: User, acting_user_id: int | None = None):
    """Delete a user safely by reassigning required references.

    Offboarding.requested_by_id is non-nullable, so we reassign those records
    to the acting user before deletion.
    """
    if acting_user_id is None:
        raise ValueError("acting_user_id is required to delete a user safely")

    # Reassign offboarding requests to the acting user
    Offboarding.query.filter(Offboarding.requested_by_id == user.id).update(
        {Offboarding.requested_by_id: acting_user_id}, synchronize_session=False
    )

    # Clear HR approvals linked to this user (nullable)
    Driver.query.filter(Driver.hr_approved_by == user.id).update(
        {Driver.hr_approved_by: None}, synchronize_session=False
    )

    db.session.delete(user)
    db.session.commit()


def change_user_password(user: User, new_password: str):
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return user


def backfill_driver_ids() -> int:
    """Assign sequential driver_id values to drivers missing one."""

    missing_drivers = (
        Driver.query
        .filter(sa.or_(Driver.driver_id == None, Driver.driver_id == ""))  # noqa: E711
        .order_by(Driver.id.asc())
        .with_for_update()
        .all()
    )

    if not missing_drivers:
        return 0

    conn = db.session.connection()
    updated = 0

    for driver in missing_drivers:
        driver.driver_id = _next_driver_id(conn)
        updated += 1

    db.session.commit()
    return updated
