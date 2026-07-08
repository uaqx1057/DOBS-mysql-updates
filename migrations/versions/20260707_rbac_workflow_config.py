"""RBAC tables, onboarding/contract config tables, branch_id mapping

Revision ID: 20260707_rbac_workflow_config
Revises: 20260125_status_constraints
Create Date: 2026-07-07 00:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260707_rbac_workflow_config'
down_revision = '20260125_status_constraints'
branch_labels = None
depends_on = None


# Distinct role strings observed in dobs_user.role today, seeded so Phase 1's
# permission cutover can reproduce current access exactly before anything
# starts reading from the new tables.
LEGACY_ROLES = [
    "SuperAdmin", "HR", "HRManager", "OpsManager", "OpsSupervisor",
    "OpsCoordinator", "FleetManager", "Finance", "FinanceManager", "Admin",
]

BASE_PERMISSIONS = [
    "offboarding.request",
]

# Roles that can request an offboarding today (Ops Coordinator's legacy
# route, Ops Manager's two routes) - granted this permission by default so
# behavior is unchanged until an admin grants it more broadly.
OFFBOARDING_REQUEST_ROLES = ["OpsCoordinator", "OpsManager", "SuperAdmin", "Admin"]

ONBOARDING_SEQUENCE_SPONSOR = [
    ("Ops Manager", None, None),
    ("HR", None, None),
    ("Ops Supervisor", None, None),
    ("Fleet Manager", None, None),
    ("Finance", None, None),
    ("HR Final", None, None),
    ("Completed", None, None),
]

# Fleet Manager row is skipped unless the driver's will_provide_vehicle
# column is true - see services/onboarding_workflow.py.
ONBOARDING_SEQUENCE_FREELANCE_SHAPE = [
    ("Ops Manager", None, None),
    ("HR", None, None),
    ("Ops Supervisor", None, None),
    ("Fleet Manager", "will_provide_vehicle", "false"),
    ("HR Final", None, None),
    ("Completed", None, None),
]


def _has_table(inspector, name):
    return name in inspector.get_table_names()


def _has_column(inspector, table, column):
    return any(col.get("name") == column for col in inspector.get_columns(table))


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # --- branch_id mapping on drivers ---------------------------------
    # Column may already exist physically (it's part of the shared table
    # DMS/Laravel owns); guard so this is a no-op if so.
    if not _has_column(inspector, "drivers", "branch_id"):
        op.add_column("drivers", sa.Column("branch_id", sa.BigInteger(), nullable=True))

    if _has_table(inspector, "branches"):
        dammam_id = bind.execute(
            sa.text("SELECT id FROM branches WHERE name = :name LIMIT 1"),
            {"name": "Dammam"},
        ).scalar()
        if dammam_id is not None:
            bind.execute(
                sa.text("UPDATE drivers SET branch_id = :bid WHERE branch_id IS NULL"),
                {"bid": dammam_id},
            )

    # --- Engine fix: dobs_user predates this app's InnoDB-by-default
    # tables and was created as MyISAM (a legacy default from however the
    # original schema was provisioned) - MyISAM does not support foreign
    # keys at all, so dobs_user_role/dobs_user_permission below cannot
    # reference it with a real FK constraint until this runs. Pure engine
    # conversion, no data changes; MySQL/MariaDB handles it online.
    if bind.dialect.name != "sqlite":
        engine_row = bind.execute(
            sa.text(
                "SELECT ENGINE FROM information_schema.TABLES "
                "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'dobs_user'"
            )
        ).scalar()
        if engine_row and engine_row.lower() != "innodb":
            bind.execute(sa.text("ALTER TABLE dobs_user ENGINE=InnoDB"))

    # --- RBAC tables (additive only, nothing reads them yet) -----------
    if not _has_table(inspector, "dobs_role"):
        op.create_table(
            "dobs_role",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("name", sa.String(50), nullable=False, unique=True),
            sa.Column("description", sa.String(255), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
        )

    if not _has_table(inspector, "dobs_permission"):
        op.create_table(
            "dobs_permission",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("code", sa.String(100), nullable=False, unique=True),
            sa.Column("description", sa.String(255), nullable=True),
        )

    if not _has_table(inspector, "dobs_role_permission"):
        op.create_table(
            "dobs_role_permission",
            sa.Column("role_id", sa.Integer(), sa.ForeignKey("dobs_role.id"), primary_key=True),
            sa.Column("permission_id", sa.Integer(), sa.ForeignKey("dobs_permission.id"), primary_key=True),
        )

    if not _has_table(inspector, "dobs_user_role"):
        op.create_table(
            "dobs_user_role",
            sa.Column("user_id", sa.Integer(), sa.ForeignKey("dobs_user.id"), primary_key=True),
            sa.Column("role_id", sa.Integer(), sa.ForeignKey("dobs_role.id"), primary_key=True),
        )

    if not _has_table(inspector, "dobs_user_permission"):
        op.create_table(
            "dobs_user_permission",
            sa.Column("user_id", sa.Integer(), sa.ForeignKey("dobs_user.id"), primary_key=True),
            sa.Column("permission_id", sa.Integer(), sa.ForeignKey("dobs_permission.id"), primary_key=True),
            sa.Column("granted", sa.Boolean(), nullable=False, server_default=sa.true()),
        )

    # --- Onboarding / contract config tables ----------------------------
    if not _has_table(inspector, "dobs_onboarding_stage_template"):
        op.create_table(
            "dobs_onboarding_stage_template",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("driver_type_id", sa.Integer(), nullable=False),
            sa.Column("sequence_order", sa.Integer(), nullable=False),
            sa.Column("stage_name", sa.String(50), nullable=False),
            sa.Column("skip_condition_field", sa.String(100), nullable=True),
            sa.Column("skip_condition_value", sa.String(50), nullable=True),
            sa.UniqueConstraint("driver_type_id", "sequence_order", name="ux_stage_template_type_order"),
        )

    if not _has_table(inspector, "dobs_driver_type_settings"):
        op.create_table(
            "dobs_driver_type_settings",
            sa.Column("driver_type_id", sa.Integer(), primary_key=True),
            sa.Column("contract_mode", sa.String(20), nullable=False, server_default="single"),
        )

    if not _has_table(inspector, "dobs_contract_template"):
        op.create_table(
            "dobs_contract_template",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("business_id", sa.BigInteger(), nullable=True),
            sa.Column("driver_type_id", sa.Integer(), nullable=True),
            sa.Column("name", sa.String(150), nullable=False),
            sa.Column("body_content", sa.Text(), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("version", sa.String(20), nullable=True, server_default="1.0"),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
        )

    # Refresh so seed queries below see the tables just created.
    inspector = sa.inspect(bind)

    _seed_roles_and_user_roles(bind)
    _seed_base_permissions(bind)
    _seed_onboarding_and_contract_config(bind, inspector)


def _seed_roles_and_user_roles(bind):
    existing_roles = {row[0] for row in bind.execute(sa.text("SELECT name FROM dobs_role"))}
    distinct_user_roles = [
        r[0] for r in bind.execute(sa.text("SELECT DISTINCT role FROM dobs_user WHERE role IS NOT NULL"))
    ]
    for role_name in sorted(set(LEGACY_ROLES) | set(distinct_user_roles)):
        if role_name and role_name not in existing_roles:
            bind.execute(sa.text("INSERT INTO dobs_role (name) VALUES (:name)"), {"name": role_name})

    role_ids = {row[0]: row[1] for row in bind.execute(sa.text("SELECT name, id FROM dobs_role"))}

    for user_id, role_name in bind.execute(sa.text("SELECT id, role FROM dobs_user WHERE role IS NOT NULL")):
        role_id = role_ids.get(role_name)
        if not role_id:
            continue
        exists = bind.execute(
            sa.text("SELECT 1 FROM dobs_user_role WHERE user_id = :uid AND role_id = :rid"),
            {"uid": user_id, "rid": role_id},
        ).scalar()
        if not exists:
            bind.execute(
                sa.text("INSERT INTO dobs_user_role (user_id, role_id) VALUES (:uid, :rid)"),
                {"uid": user_id, "rid": role_id},
            )


def _seed_base_permissions(bind):
    existing_perms = {row[0] for row in bind.execute(sa.text("SELECT code FROM dobs_permission"))}
    for code in BASE_PERMISSIONS:
        if code not in existing_perms:
            bind.execute(sa.text("INSERT INTO dobs_permission (code) VALUES (:code)"), {"code": code})

    role_ids = {row[0]: row[1] for row in bind.execute(sa.text("SELECT name, id FROM dobs_role"))}
    perm_ids = {row[0]: row[1] for row in bind.execute(sa.text("SELECT code, id FROM dobs_permission"))}
    offboarding_perm_id = perm_ids.get("offboarding.request")
    if not offboarding_perm_id:
        return

    for role_name in OFFBOARDING_REQUEST_ROLES:
        role_id = role_ids.get(role_name)
        if not role_id:
            continue
        exists = bind.execute(
            sa.text("SELECT 1 FROM dobs_role_permission WHERE role_id = :rid AND permission_id = :pid"),
            {"rid": role_id, "pid": offboarding_perm_id},
        ).scalar()
        if not exists:
            bind.execute(
                sa.text("INSERT INTO dobs_role_permission (role_id, permission_id) VALUES (:rid, :pid)"),
                {"rid": role_id, "pid": offboarding_perm_id},
            )


def _seed_onboarding_and_contract_config(bind, inspector):
    if not _has_table(inspector, "driver_types"):
        return

    type_ids = {
        row[0]: row[1]
        for row in bind.execute(sa.text("SELECT name, id FROM driver_types WHERE deleted_at IS NULL"))
    }

    def type_id_for(*names):
        for n in names:
            if n in type_ids:
                return type_ids[n]
        return None

    sponsor_id = type_id_for("Sponsor")
    freelancer_id = type_id_for("Freelancer (VMFG)", "Freelancer")
    manpower_id = type_id_for("Manpower")

    seeded_stage_types = {
        row[0] for row in bind.execute(sa.text("SELECT DISTINCT driver_type_id FROM dobs_onboarding_stage_template"))
    }

    def seed_sequence(type_id, stages):
        if not type_id or type_id in seeded_stage_types:
            return
        for order, (stage_name, skip_field, skip_value) in enumerate(stages, start=1):
            bind.execute(
                sa.text(
                    "INSERT INTO dobs_onboarding_stage_template "
                    "(driver_type_id, sequence_order, stage_name, skip_condition_field, skip_condition_value) "
                    "VALUES (:tid, :ord, :stage, :sfield, :svalue)"
                ),
                {"tid": type_id, "ord": order, "stage": stage_name, "sfield": skip_field, "svalue": skip_value},
            )

    seed_sequence(sponsor_id, ONBOARDING_SEQUENCE_SPONSOR)
    seed_sequence(freelancer_id, ONBOARDING_SEQUENCE_FREELANCE_SHAPE)
    seed_sequence(manpower_id, ONBOARDING_SEQUENCE_FREELANCE_SHAPE)

    existing_settings = {
        row[0] for row in bind.execute(sa.text("SELECT driver_type_id FROM dobs_driver_type_settings"))
    }

    def seed_settings(type_id, mode):
        if type_id and type_id not in existing_settings:
            bind.execute(
                sa.text(
                    "INSERT INTO dobs_driver_type_settings (driver_type_id, contract_mode) VALUES (:tid, :mode)"
                ),
                {"tid": type_id, "mode": mode},
            )

    seed_settings(sponsor_id, "single")
    seed_settings(freelancer_id, "per_business")
    seed_settings(manpower_id, "per_business")


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    for table in [
        "dobs_contract_template",
        "dobs_driver_type_settings",
        "dobs_onboarding_stage_template",
        "dobs_user_permission",
        "dobs_user_role",
        "dobs_role_permission",
        "dobs_permission",
        "dobs_role",
    ]:
        if _has_table(inspector, table):
            op.drop_table(table)

    if _has_column(inspector, "drivers", "branch_id"):
        op.drop_column("drivers", "branch_id")
