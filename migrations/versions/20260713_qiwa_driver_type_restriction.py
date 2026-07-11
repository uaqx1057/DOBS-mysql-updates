"""Restrict Qiwa contracts to Sponsor-type drivers only

Qiwa (Ministry of HR/Qiwa platform) contracts are a company-sponsorship
concept - they only apply to Sponsor-type drivers, never Freelancer or
Manpower. Previously HR could mark qiwa_contract_created=true for any
driver type; this adds a data-driven per-type flag (matching how
contract_mode already works) so it's enforced consistently and stays
admin-editable rather than hardcoded.

Revision ID: 20260713_qiwa_driver_type_restriction
Revises: 20260712_driver_reject_audit
Create Date: 2026-07-13 00:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260713_qiwa_driver_type_restriction'
down_revision = '20260712_driver_reject_audit'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("dobs_driver_type_settings")}

    if "requires_qiwa_contract" not in columns:
        op.add_column(
            "dobs_driver_type_settings",
            sa.Column("requires_qiwa_contract", sa.Boolean(), nullable=False, server_default=sa.false()),
        )

    # Seed True for Sponsor only, if a settings row already exists for it.
    # (driver_types.name = 'Sponsor' per the original seed data.)
    sponsor_id = bind.execute(
        sa.text("SELECT id FROM driver_types WHERE name = 'Sponsor' AND deleted_at IS NULL LIMIT 1")
    ).scalar()
    if sponsor_id:
        existing = bind.execute(
            sa.text("SELECT 1 FROM dobs_driver_type_settings WHERE driver_type_id = :id"),
            {"id": sponsor_id},
        ).scalar()
        if existing:
            bind.execute(
                sa.text("UPDATE dobs_driver_type_settings SET requires_qiwa_contract = TRUE WHERE driver_type_id = :id"),
                {"id": sponsor_id},
            )
        else:
            bind.execute(
                sa.text(
                    "INSERT INTO dobs_driver_type_settings (driver_type_id, contract_mode, requires_qiwa_contract) "
                    "VALUES (:id, 'single', TRUE)"
                ),
                {"id": sponsor_id},
            )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("dobs_driver_type_settings")}
    if "requires_qiwa_contract" in columns:
        op.drop_column("dobs_driver_type_settings", "requires_qiwa_contract")
