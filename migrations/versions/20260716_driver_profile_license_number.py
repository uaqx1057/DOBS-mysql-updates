"""Add the driver license number used by the DOBS profile.

Revision ID: 20260716_driver_profile_license_number
Revises: 20260715_driver_contract_system
Create Date: 2026-07-16 00:00:00
"""
from alembic import op
import sqlalchemy as sa


revision = "20260716_driver_profile_license_number"
down_revision = "20260715_driver_contract_system"
branch_labels = None
depends_on = None


def upgrade():
    columns = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("drivers")}
    if "license_number" not in columns:
        op.add_column("drivers", sa.Column("license_number", sa.String(100), nullable=True))


def downgrade():
    columns = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("drivers")}
    if "license_number" in columns:
        op.drop_column("drivers", "license_number")
