"""Offboarding fields for unified state machine: request_reason, ops_manager_approved_at, ops_supervisor penalty fields

Revision ID: 20260707_offboarding_fields
Revises: 20260707_driver_type_fields
Create Date: 2026-07-07 02:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260707_offboarding_fields'
down_revision = '20260707_driver_type_fields'
branch_labels = None
depends_on = None


def _has_column(inspector, table, column):
    return any(col.get("name") == column for col in inspector.get_columns(table))


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _has_column(inspector, "offboarding", "request_reason"):
        op.add_column("offboarding", sa.Column("request_reason", sa.Text(), nullable=True))
    if not _has_column(inspector, "offboarding", "ops_manager_approved_at"):
        op.add_column("offboarding", sa.Column("ops_manager_approved_at", sa.DateTime(), nullable=True))
    if not _has_column(inspector, "offboarding", "ops_supervisor_penalty_amount"):
        op.add_column("offboarding", sa.Column("ops_supervisor_penalty_amount", sa.Numeric(12, 2), nullable=True))
    if not _has_column(inspector, "offboarding", "ops_supervisor_penalty_note"):
        op.add_column("offboarding", sa.Column("ops_supervisor_penalty_note", sa.Text(), nullable=True))


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if _has_column(inspector, "offboarding", "ops_supervisor_penalty_note"):
        op.drop_column("offboarding", "ops_supervisor_penalty_note")
    if _has_column(inspector, "offboarding", "ops_supervisor_penalty_amount"):
        op.drop_column("offboarding", "ops_supervisor_penalty_amount")
    if _has_column(inspector, "offboarding", "ops_manager_approved_at"):
        op.drop_column("offboarding", "ops_manager_approved_at")
    if _has_column(inspector, "offboarding", "request_reason"):
        op.drop_column("offboarding", "request_reason")
