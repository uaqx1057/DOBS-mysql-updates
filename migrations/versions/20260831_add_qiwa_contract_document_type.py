"""Allow Qiwa contracts in the shared driver document registry.

Existing production rows use ``qiwa_contract``.  SQLAlchemy must recognize
that value when the admin dashboard loads a driver's documents.  The guarded
DDL also brings any older MySQL schema into sync without rewriting a schema
that already accepts the value.

Revision ID: 20260831_add_qiwa_contract_document_type
Revises: 20260827_driver_dms_parity_fields
Create Date: 2026-08-31 00:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260831_add_qiwa_contract_document_type"
down_revision = "20260827_driver_dms_parity_fields"
branch_labels = None
depends_on = None


DOCUMENT_TYPES = (
    "iqama", "passport", "visa", "license", "medical", "contract",
    "mobile", "qiwa_contract", "other",
)


def _document_type_column(conn):
    return next(
        (
            column
            for column in sa.inspect(conn).get_columns("driver_documents")
            if column["name"] == "document_type"
        ),
        None,
    )


def upgrade():
    conn = op.get_bind()
    column = _document_type_column(conn)
    if column is None or conn.dialect.name != "mysql":
        return

    if "qiwa_contract" in (column.get("type").enums or []):
        return

    op.alter_column(
        "driver_documents",
        "document_type",
        existing_type=column["type"],
        type_=sa.Enum(*DOCUMENT_TYPES, native_enum=True),
        existing_nullable=False,
    )


def downgrade():
    # Existing rows may rely on qiwa_contract.  Never make them unreadable.
    pass
