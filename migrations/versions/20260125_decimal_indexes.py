"""Add indexes and numeric money columns

Revision ID: 20260125_decimal_indexes
Revises: 20260125_add_reset_token
Create Date: 2026-01-25 00:30:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260125_decimal_indexes'
down_revision = '20260125_add_reset_token'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    is_sqlite = bind.dialect.name == "sqlite"

    # Monetary fields to DECIMAL (skip type change on SQLite which lacks ALTER TYPE)
    if not is_sqlite:
        op.alter_column(
            'drivers',
            'transfer_fee_amount',
            existing_type=sa.Float(),
            type_=sa.Numeric(12, 2),
            existing_nullable=True,
        )
        op.alter_column(
            'offboarding',
            'finance_adjustments',
            existing_type=sa.Float(),
            type_=sa.Numeric(12, 2),
            existing_nullable=True,
        )
        op.alter_column(
            'offboarding',
            'fleet_damage_cost',
            existing_type=sa.Float(),
            type_=sa.Numeric(12, 2),
            existing_nullable=True,
        )

    # Indexes for common filters
    op.create_index('ix_drivers_onboarding_stage', 'drivers', ['onboarding_stage'])
    op.create_index('ix_offboarding_status', 'offboarding', ['status'])


def downgrade():
    op.drop_index('ix_offboarding_status', table_name='offboarding')
    op.drop_index('ix_drivers_onboarding_stage', table_name='drivers')

    bind = op.get_bind()
    is_sqlite = bind.dialect.name == "sqlite"

    if not is_sqlite:
        op.alter_column(
            'offboarding',
            'fleet_damage_cost',
            existing_type=sa.Numeric(12, 2),
            type_=sa.Float(),
            existing_nullable=True,
        )
        op.alter_column(
            'offboarding',
            'finance_adjustments',
            existing_type=sa.Numeric(12, 2),
            type_=sa.Float(),
            existing_nullable=True,
        )
        op.alter_column(
            'drivers',
            'transfer_fee_amount',
            existing_type=sa.Numeric(12, 2),
            type_=sa.Float(),
            existing_nullable=True,
        )
