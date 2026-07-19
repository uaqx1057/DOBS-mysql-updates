from datetime import datetime, date
from typing import Iterable, Optional

from extensions import db
from models import (
    AssignDriver,
    AssignDriverReport,
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


DEFAULT_DRIVER_PASSWORD = "12344321"


def _normalize_onboarding_stage(value):
    if value in (None, ""):
        return value

    text = str(value).strip()
    key = text.lower().replace(" ", "")
    if key in {"fleet", "fleetmanager"}:
        return "Fleet Manager"
    return text


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
        text_value = str(value).strip()
        if "T" in text_value:
            try:
                return datetime.fromisoformat(text_value)
            except AttributeError:
                return datetime.strptime(text_value, "%Y-%m-%dT%H:%M:%S")
        try:
            return datetime.fromisoformat(text_value).date()
        except AttributeError:
            return datetime.strptime(text_value, "%Y-%m-%d").date()
    except Exception:
        return None


def update_driver_from_form(driver: Driver, form_data, business_ids: Iterable[str], platform_ids: Iterable[str]):
    """Update driver fields and business assignments from submitted form data."""
    bool_fields = {"saudi_driving_license", "mobile_issued", "tamm_authorized", "transfer_fee_paid", "ops_manager_approved"}
    date_fields = {
        "iqaama_expiry", "assignment_date", "transfer_fee_paid_at",
        "ops_manager_approved_at", "hr_approved_at", "ops_supervisor_approved_at",
        "fleet_manager_approved_at", "finance_approved_at",
    }

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
        elif field == "onboarding_stage":
            setattr(driver, field, _normalize_onboarding_stage(value))
        elif field == "transfer_fee_amount":
            try:
                setattr(driver, field, float(value) if value not in (None, "") else None)
            except (TypeError, ValueError):
                setattr(driver, field, None)
        elif field == "branch_id":
            try:
                setattr(driver, field, int(value) if value not in (None, "") else driver.branch_id)
            except (TypeError, ValueError):
                pass
        else:
            setattr(driver, field, value)

    if driver.onboarding_stage == "Completed":
        driver.password = generate_password_hash(DEFAULT_DRIVER_PASSWORD)

    # --- Unify assignment logic with DMS ---
    # Assignments are made by BusinessID (business_ids.id) for history,
    # while business_driver stores Business type IDs (businesses.id).
    selected_business_id_ids = [int(str(p).strip()) for p in platform_ids if str(p).strip()]

    selected_business_ids = (
        BusinessID.query
        .filter(BusinessID.id.in_(selected_business_id_ids))
        .all()
    ) if selected_business_id_ids else []

    selected_business_type_ids = list({int(bid.business_id) for bid in selected_business_ids if bid.business_id is not None})

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

    # Assign new/kept IDs
    for b_id in selected_business_id_ids:
        # If already active for this driver, keep history as-is
        if b_id in active_id_set:
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

    # Sync business_driver using Business type IDs (businesses.id) for this driver only
    if selected_business_type_ids:
        BusinessDriver.query.filter(
            BusinessDriver.driver_id == driver.id,
            ~BusinessDriver.business_id.in_(selected_business_type_ids)
        ).delete(synchronize_session=False)
    else:
        BusinessDriver.query.filter_by(driver_id=driver.id).delete(synchronize_session=False)

    existing_business_links = {
        row.business_id for row in BusinessDriver.query.filter_by(driver_id=driver.id).all()
    }
    for business_type_id in selected_business_type_ids:
        if business_type_id not in existing_business_links:
            db.session.add(
                BusinessDriver(
                    driver_id=driver.id,
                    business_id=business_type_id,
                )
            )

    # Keep legacy fields in sync for modules still reading drivers.platform/platform_id
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

    # Remove dependent rows that can block driver deletion via FK constraints.
    AssignDriver.query.filter_by(driver_id=driver.id).delete(synchronize_session=False)
    AssignDriverReport.query.filter_by(driver_id=driver.id).delete(synchronize_session=False)
    Offboarding.query.filter_by(driver_id=driver.id).delete()
    DriverBusinessIDS.query.filter_by(driver_id=driver.id).delete(synchronize_session=False)
    BusinessDriver.query.filter_by(driver_id=driver.id).delete(synchronize_session=False)

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


def delete_user(user: User, acting_user_id: Optional[int] = None):
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
