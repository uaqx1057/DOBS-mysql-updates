"""Real Arabic content fields for contract/promissory note templates

Previously the Arabic side of a rendered document only ever showed a
translation for one hardcoded English sentence set (the built-in driver
contract defaults) - any other admin-authored body/intro/eligibility/
general-terms/signature text (e.g. a promissory note's statement) rendered
as English on both sides. This adds a real _ar column next to each of
those fields so admins can author the actual Arabic text directly.

Revision ID: 20260717_contract_template_arabic_content
Revises: 20260716_company_preset
Create Date: 2026-07-17 00:00:00
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260717_contract_template_arabic_content'
down_revision = '20260716_company_preset'
branch_labels = None
depends_on = None


NEW_COLUMNS = [
    "intro_content_ar",
    "eligibility_content_ar",
    "general_terms_content_ar",
    "body_content_ar",
    "signature_notes_ar",
]


def _has_column(inspector, table, column):
    return any(col.get("name") == column for col in inspector.get_columns(table))


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "dobs_contract_template" in inspector.get_table_names():
        for column_name in NEW_COLUMNS:
            if not _has_column(inspector, "dobs_contract_template", column_name):
                op.add_column("dobs_contract_template", sa.Column(column_name, sa.Text(), nullable=True))


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "dobs_contract_template" in inspector.get_table_names():
        for column_name in reversed(NEW_COLUMNS):
            if _has_column(inspector, "dobs_contract_template", column_name):
                op.drop_column("dobs_contract_template", column_name)
