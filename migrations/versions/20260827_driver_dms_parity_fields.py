"""Bridge: declare driver fields DMS already added to the shared table

DOBS and DMS share the same physical `drivers` table (dobsykjq_dms_hr_merge).
DMS's own migrations already added dob, driver_profession, email,
license_type, license_expiry, passport_no, passport_expiry_date, and
remarks (create_drivers_table.php; license_type/driver_profession most
recently via 2026_08_23_150000_add_license_type_and_profession_to_drivers_table.php)
- DOBS's SQLAlchemy model just never declared them. This migration is a
guarded no-op on any environment where the columns are already there (i.e.
production today), and only actually adds them on an environment that
somehow lacks them (e.g. a DOBS-only fresh schema, or this local dev DB).

Deliberately no DB-level CHECK constraint on license_type: DMS only
enforces that enum ('Private','Commercial','Heavy','Motorcycle') in its own
Laravel validation layer, not at the DB level. Adding one here could break
DMS's own writes to this shared table if it ever inserts a value DOBS
doesn't know about.

Also NOT included: sponsor_company_id (a linked SponsorCompany entity,
scoped by driver_type in DMS) and bank_accounts (a repeatable bank/STC-Pay
sub-form). DOBS has no SponsorCompany/DriverBankAccount tables at all -
matching those would mean introducing new models/relationships, not just
new columns. Also skipped: DMS's driver-facing `language` field, which has
no corresponding use in DOBS (no driver-facing portal/app here to localize).

Revision ID: 20260827_driver_dms_parity_fields
Revises: 20260809_completed_contract_permission
Create Date: 2026-08-27 00:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260827_driver_dms_parity_fields'
down_revision = '20260809_completed_contract_permission'
branch_labels = None
depends_on = None


NEW_COLUMNS = [
    ("dob", sa.Date()),
    ("driver_profession", sa.String(255)),
    ("email", sa.String(120)),
    ("license_type", sa.String(20)),
    ("license_expiry", sa.Date()),
    ("passport_no", sa.String(50)),
    ("passport_expiry_date", sa.Date()),
    ("remarks", sa.Text()),
]


def upgrade():
    conn = op.get_bind()
    insp = sa.inspect(conn)

    existing_columns = {c["name"] for c in insp.get_columns("drivers")}
    for name, col_type in NEW_COLUMNS:
        if name not in existing_columns:
            op.add_column("drivers", sa.Column(name, col_type, nullable=True))


def downgrade():
    # Deliberately a no-op: on the real (shared) DB these columns are owned
    # by DMS, not DOBS - downgrading DOBS's migration state must never drop
    # columns DMS still relies on. Only meaningful on an isolated
    # DOBS-only schema, which is exactly the case this migration itself was
    # guarded against creating anything on in the first place.
    pass
