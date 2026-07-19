"""Remove the redundant driver license number field.

Saudi driving licences are identified by the driver's Iqama number, so a
separate driver-level license number duplicates the identity record.

Revision ID: 20260718_remove_driver_license_number
Revises: 20260716_driver_profile_license_number
Create Date: 2026-07-18 00:00:00
"""
from alembic import op
import sqlalchemy as sa


revision = "20260718_remove_driver_license_number"
down_revision = "20260716_driver_profile_license_number"
branch_labels = None
depends_on = None


def upgrade():
    columns = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("drivers")}
    if "license_number" in columns:
        op.drop_column("drivers", "license_number")


def downgrade():
    columns = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("drivers")}
    if "license_number" not in columns:
        op.add_column("drivers", sa.Column("license_number", sa.String(100), nullable=True))
