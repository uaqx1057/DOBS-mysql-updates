"""Driver columns for type-driven onboarding: will_provide_vehicle, driving_license_upload, passport_upload

Revision ID: 20260707_driver_type_fields
Revises: 20260707_rbac_workflow_config
Create Date: 2026-07-07 01:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260707_driver_type_fields'
down_revision = '20260707_rbac_workflow_config'
branch_labels = None
depends_on = None


def _has_column(inspector, table, column):
    return any(col.get("name") == column for col in inspector.get_columns(table))


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _has_column(inspector, "drivers", "will_provide_vehicle"):
        op.add_column("drivers", sa.Column("will_provide_vehicle", sa.Boolean(), nullable=True))
    if not _has_column(inspector, "drivers", "driving_license_upload"):
        op.add_column("drivers", sa.Column("driving_license_upload", sa.String(200), nullable=True))
    if not _has_column(inspector, "drivers", "passport_upload"):
        op.add_column("drivers", sa.Column("passport_upload", sa.String(200), nullable=True))


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if _has_column(inspector, "drivers", "passport_upload"):
        op.drop_column("drivers", "passport_upload")
    if _has_column(inspector, "drivers", "driving_license_upload"):
        op.drop_column("drivers", "driving_license_upload")
    if _has_column(inspector, "drivers", "will_provide_vehicle"):
        op.drop_column("drivers", "will_provide_vehicle")
