"""Driver rejection audit fields + fix HR reject to soft-reject

Adds rejected_by_stage/rejected_at/reject_reason to drivers - the Ops
Manager reject route was already setting columns
(ops_manager_rejected/ops_manager_rejected_at/ops_manager_reject_reason)
that never actually existed on the model, so those writes were silently
discarded (no error, just lost data). These three generalized columns
replace that dead code path and are shared between Ops Manager and HR's
reject actions.

Revision ID: 20260712_driver_reject_audit
Revises: 20260711_impersonation_log
Create Date: 2026-07-12 00:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260712_driver_reject_audit'
down_revision = '20260711_impersonation_log'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("drivers")}

    if "rejected_by_stage" not in columns:
        op.add_column("drivers", sa.Column("rejected_by_stage", sa.String(50), nullable=True))
    if "rejected_at" not in columns:
        op.add_column("drivers", sa.Column("rejected_at", sa.DateTime(), nullable=True))
    if "reject_reason" not in columns:
        op.add_column("drivers", sa.Column("reject_reason", sa.String(500), nullable=True))


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("drivers")}

    for col_name in ("reject_reason", "rejected_at", "rejected_by_stage"):
        if col_name in columns:
            op.drop_column("drivers", col_name)
