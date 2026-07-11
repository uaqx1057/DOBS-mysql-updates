"""Editable company preset for contract/promissory note templates

Adds dobs_company_preset, a singleton settings row holding the company
identity/signatory defaults that used to only be configurable via
CONTRACT_* environment variables - now editable by SuperAdmin under
Workflow & Contracts.

Revision ID: 20260716_company_preset
Revises: 20260715_driver_contract_system
Create Date: 2026-07-16 00:00:00
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260716_company_preset'
down_revision = '20260715_driver_contract_system'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "dobs_company_preset" not in inspector.get_table_names():
        op.create_table(
            "dobs_company_preset",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("first_party_name", sa.String(150), nullable=True),
            sa.Column("first_party_name_ar", sa.String(150), nullable=True),
            sa.Column("first_party_label", sa.String(100), nullable=True),
            sa.Column("first_party_label_ar", sa.String(100), nullable=True),
            sa.Column("second_party_label", sa.String(100), nullable=True),
            sa.Column("second_party_label_ar", sa.String(100), nullable=True),
            sa.Column("company_signatory_name", sa.String(150), nullable=True),
            sa.Column("company_signatory_title", sa.String(150), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
        )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "dobs_company_preset" in inspector.get_table_names():
        op.drop_table("dobs_company_preset")
