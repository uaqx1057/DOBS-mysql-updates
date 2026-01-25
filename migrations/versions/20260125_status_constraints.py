"""Status constraints and unique indexes

Revision ID: 20260125_status_constraints
Revises: 20260125_user_lockout
Create Date: 2026-01-25 01:10:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260125_status_constraints'
down_revision = '20260125_user_lockout'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    insp = sa.inspect(conn)
    is_sqlite = conn.dialect.name == "sqlite"

    def has_index(table, name):
        return any(ix.get("name") == name for ix in insp.get_indexes(table))

    def has_check(table, name):
        return any(ck.get("name") == name for ck in insp.get_check_constraints(table))

    def has_unique(table, name):
        return any(uc.get("name") == name for uc in insp.get_unique_constraints(table))

    # Unique indexes for identifiers (guarded to avoid duplicates across engines)
    if not has_index("drivers", "ux_drivers_driver_id") and not has_unique("drivers", "ux_drivers_driver_id"):
        op.create_index("ux_drivers_driver_id", "drivers", ["driver_id"], unique=True)
    if not has_index("drivers", "ux_drivers_iqaama_number") and not has_unique("drivers", "ux_drivers_iqaama_number"):
        op.create_index("ux_drivers_iqaama_number", "drivers", ["iqaama_number"], unique=True)

    # Check constraints for controlled status values (skip on SQLite which lacks ALTER CONSTRAINT)
    if not is_sqlite:
        if not has_check("drivers", "ck_drivers_onboarding_stage"):
            op.create_check_constraint(
                "ck_drivers_onboarding_stage",
                "drivers",
                "onboarding_stage IN ('Ops Manager','HR','HR Final','Ops Supervisor','Fleet Manager','Finance','Completed','Rejected')",
            )
        if not has_check("drivers", "ck_drivers_qiwa_status"):
            op.create_check_constraint(
                "ck_drivers_qiwa_status",
                "drivers",
                "qiwa_contract_status IN ('Pending','Created','Approved','Rejected')",
            )
        if not has_check("drivers", "ck_drivers_transfer_status"):
            op.create_check_constraint(
                "ck_drivers_transfer_status",
                "drivers",
                "sponsorship_transfer_status IN ('Pending','Transferred','Completed','Not Required')",
            )
        if not has_check("offboarding", "ck_offboarding_status"):
            op.create_check_constraint(
                "ck_offboarding_status",
                "offboarding",
                "status IN ('Requested','OpsSupervisor','Fleet','Finance','HR','Completed','pending_tamm')",
            )


def downgrade():
    conn = op.get_bind()
    insp = sa.inspect(conn)
    is_sqlite = conn.dialect.name == "sqlite"

    def has_index(table, name):
        return any(ix.get("name") == name for ix in insp.get_indexes(table))

    def has_check(table, name):
        return any(ck.get("name") == name for ck in insp.get_check_constraints(table))

    # Drop constraints first to avoid dependency on indexes
    if not is_sqlite:
        if has_check("offboarding", "ck_offboarding_status"):
            op.drop_constraint("ck_offboarding_status", "offboarding", type_="check")
        if has_check("drivers", "ck_drivers_transfer_status"):
            op.drop_constraint("ck_drivers_transfer_status", "drivers", type_="check")
        if has_check("drivers", "ck_drivers_qiwa_status"):
            op.drop_constraint("ck_drivers_qiwa_status", "drivers", type_="check")
        if has_check("drivers", "ck_drivers_onboarding_stage"):
            op.drop_constraint("ck_drivers_onboarding_stage", "drivers", type_="check")

    if has_index("drivers", "ux_drivers_iqaama_number"):
        op.drop_index("ux_drivers_iqaama_number", table_name="drivers")
    if has_index("drivers", "ux_drivers_driver_id"):
        op.drop_index("ux_drivers_driver_id", table_name="drivers")
