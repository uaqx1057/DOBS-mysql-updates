from datetime import datetime, date
from typing import Iterable

from extensions import db
from models import (
    BusinessDriver,
    Driver,
    DriverBusinessIDS,
    Offboarding,
    User,
)
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

    # Mark old history links as transferred
    old_links = DriverBusinessIDS.query.filter_by(driver_id=driver.id, transferred_at=None).all()
    for old in old_links:
        old.transferred_at = datetime.utcnow()

    # Replace active links
    BusinessDriver.query.filter_by(driver_id=driver.id).delete()

    for b_id, p_id in zip(business_ids, platform_ids):
        db.session.add(
            DriverBusinessIDS(
                driver_id=driver.id,
                business_id_id=int(b_id),
                assigned_at=datetime.utcnow(),
                transferred_at=None,
            )
        )
        db.session.add(
            BusinessDriver(
                driver_id=driver.id,
                business_id=int(b_id),
                platform_id=int(p_id),
            )
        )

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


def delete_user(user: User):
    db.session.delete(user)
    db.session.commit()


def change_user_password(user: User, new_password: str):
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return user
