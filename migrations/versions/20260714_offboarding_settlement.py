"""Offboarding financial settlement fields

Finance's offboarding clearance now pulls DMS's own payroll running balance
(driver_salary_slips.closing_balance) alongside the existing Ops Supervisor
penalty and Fleet damage cost to compute one net settlement figure and
direction, so HR's final step can branch: company owes driver (pay, or
issue a payment letter) vs driver owes company (pay, or issue a promissory
note).

Revision ID: 20260714_offboarding_settlement
Revises: 20260713_qiwa_driver_type_restriction
Create Date: 2026-07-14 00:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260714_offboarding_settlement'
down_revision = '20260713_qiwa_driver_type_restriction'
branch_labels = None
depends_on = None

NEW_COLUMNS = [
    ("dms_salary_balance", sa.Numeric(12, 2)),
    ("dms_salary_slip_id", sa.Integer()),
    ("net_settlement_amount", sa.Numeric(12, 2)),
    ("settlement_direction", sa.String(20)),
    ("promissory_note_issued", sa.Boolean()),
    ("promissory_note_at", sa.DateTime()),
    ("payment_letter_issued", sa.Boolean()),
    ("payment_letter_due_days", sa.Integer()),
    ("payment_letter_at", sa.DateTime()),
]


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("offboarding")}

    for name, coltype in NEW_COLUMNS:
        if name not in columns:
            default = sa.false() if isinstance(coltype, sa.Boolean) else None
            if default is not None:
                op.add_column("offboarding", sa.Column(name, coltype, nullable=False, server_default=default))
            else:
                op.add_column("offboarding", sa.Column(name, coltype, nullable=True))


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("offboarding")}

    for name, _coltype in reversed(NEW_COLUMNS):
        if name in columns:
            op.drop_column("offboarding", name)
