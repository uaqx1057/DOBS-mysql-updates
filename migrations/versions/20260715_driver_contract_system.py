"""Shared driver contract system schema

Extends the existing contract template table so templates can store the
structured package terms and section content required by driver contracts,
and adds a shared generated-contract tracking table used by both DOBS and
DMS while files live in the shared driver_documents storage path.

Revision ID: 20260715_driver_contract_system
Revises: 20260714_offboarding_settlement
Create Date: 2026-07-15 00:00:00
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260715_driver_contract_system'
down_revision = '20260714_offboarding_settlement'
branch_labels = None
depends_on = None


NEW_TEMPLATE_COLUMNS = [
    ("document_kind", sa.String(40), "driver_contract"),
    ("language_mode", sa.String(20), "bilingual"),
    ("layout_type", sa.String(40), "structured_contract"),
    ("first_party_name", sa.String(150), None),
    ("first_party_name_ar", sa.String(150), None),
    ("first_party_label", sa.String(100), None),
    ("first_party_label_ar", sa.String(100), None),
    ("second_party_label", sa.String(100), None),
    ("second_party_label_ar", sa.String(100), None),
    ("intro_content", sa.Text(), None),
    ("eligibility_content", sa.Text(), None),
    ("general_terms_content", sa.Text(), None),
    ("target_orders", sa.Integer(), None),
    ("target_salary", sa.Numeric(12, 2), None),
    ("bonus_per_extra_order", sa.Numeric(12, 2), None),
    ("deduction_per_missing_order", sa.Numeric(12, 2), None),
    ("calculation_tiers_json", sa.Text(), None),
    ("company_signatory_name", sa.String(150), None),
    ("company_signatory_title", sa.String(150), None),
    ("signature_notes", sa.Text(), None),
]


def _has_table(inspector, name):
    return name in inspector.get_table_names()


def _has_column(inspector, table, column):
    return any(col.get("name") == column for col in inspector.get_columns(table))


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if _has_table(inspector, "dobs_contract_template"):
        for column_name, column_type, server_default in NEW_TEMPLATE_COLUMNS:
            if not _has_column(inspector, "dobs_contract_template", column_name):
                kwargs = {"nullable": True}
                if server_default is not None:
                    kwargs["server_default"] = sa.text(f"'{server_default}'")
                op.add_column("dobs_contract_template", sa.Column(column_name, column_type, **kwargs))

    if not _has_table(inspector, "shared_generated_driver_contracts"):
        op.create_table(
            "shared_generated_driver_contracts",
            sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
            sa.Column("reference_number", sa.String(40), nullable=False, unique=True),
            sa.Column("driver_id", sa.BigInteger(), nullable=False),
            sa.Column("template_id", sa.BigInteger(), nullable=True),
            sa.Column("driver_document_id", sa.BigInteger(), nullable=True),
            sa.Column("business_id", sa.BigInteger(), nullable=True),
            sa.Column("generated_by", sa.BigInteger(), nullable=True),
            sa.Column("driver_type_id", sa.Integer(), nullable=True),
            sa.Column("generated_from_system", sa.String(20), nullable=False),
            sa.Column("generated_at", sa.DateTime(), nullable=True),
            sa.Column("file_path", sa.String(500), nullable=False),
            sa.Column("original_name", sa.String(255), nullable=True),
            sa.Column("storage_disk", sa.String(100), nullable=False, server_default="shared_driver_documents"),
            sa.Column("signed_status", sa.String(30), nullable=False, server_default="pending"),
            sa.Column("signed_at", sa.DateTime(), nullable=True),
            sa.Column("signed_copy_path", sa.String(500), nullable=True),
            sa.Column("notes", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
            sa.Column("deleted_at", sa.DateTime(), nullable=True),
        )
        op.create_index("sgdc_driver_generated_idx", "shared_generated_driver_contracts", ["driver_id", "generated_at"])
        op.create_index("sgdc_business_type_idx", "shared_generated_driver_contracts", ["business_id", "driver_type_id"])
        op.create_index("sgdc_system_status_idx", "shared_generated_driver_contracts", ["generated_from_system", "signed_status"])


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if _has_table(inspector, "shared_generated_driver_contracts"):
        for idx in ["sgdc_driver_generated_idx", "sgdc_business_type_idx", "sgdc_system_status_idx"]:
            op.drop_index(idx, table_name="shared_generated_driver_contracts")
        op.drop_table("shared_generated_driver_contracts")

    if _has_table(inspector, "dobs_contract_template"):
        for column_name, _column_type, _server_default in reversed(NEW_TEMPLATE_COLUMNS):
            if _has_column(inspector, "dobs_contract_template", column_name):
                op.drop_column("dobs_contract_template", column_name)
