"""Read/write integration with DMS's own payroll table (driver_salary_slips),
shared on the same database. DOBS pulls the driver's latest running balance
during offboarding Finance clearance, and marks the slip settled when HR
finalizes - mirroring DMS's own Livewire markAsSettledAccounts() guard
exactly (app/Livewire/DMS/Payroll/PayrollList.php: only ever transitions a
slip that's currently 'Pending' to 'SettledAccounts'), so DOBS can never
force a state DMS itself wouldn't have allowed.
"""
from sqlalchemy import text

from extensions import db


def latest_salary_slip(driver_id):
    """Returns (slip_id, closing_balance) for the driver's most recent DMS
    salary slip, or (None, 0.0) if none exists. Positive closing_balance
    means the company owes the driver."""
    row = db.session.execute(
        text(
            "SELECT id, closing_balance FROM driver_salary_slips "
            "WHERE driver_id = :driver_id "
            "ORDER BY year DESC, month DESC, id DESC LIMIT 1"
        ),
        {"driver_id": driver_id},
    ).first()
    if not row:
        return None, 0.0
    return row[0], float(row[1] or 0)


def compute_settlement(dms_balance, ops_supervisor_penalty, fleet_damage_cost, finance_adjustments):
    """Positive net_amount = company owes driver. Negative = driver owes
    company. Zero = even, no settlement action required."""
    net = (
        float(dms_balance or 0)
        - float(ops_supervisor_penalty or 0)
        - float(fleet_damage_cost or 0)
        - float(finance_adjustments or 0)
    )
    net = round(net, 2)
    if net > 0:
        direction = "company_owes_driver"
    elif net < 0:
        direction = "driver_owes_company"
    else:
        direction = "even"
    return net, direction


def mark_salary_slip_settled(slip_id) -> bool:
    """Mirrors DMS's own markAsSettledAccounts() guard exactly - only
    transitions a slip currently 'Pending' to 'SettledAccounts'. Returns
    False (not an error) if the slip has already moved on in DMS for any
    reason, or if slip_id is unset."""
    if not slip_id:
        return False
    result = db.session.execute(
        text(
            "UPDATE driver_salary_slips SET status = 'SettledAccounts' "
            "WHERE id = :slip_id AND status = 'Pending'"
        ),
        {"slip_id": slip_id},
    )
    return result.rowcount > 0
