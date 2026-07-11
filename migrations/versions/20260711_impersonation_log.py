"""SuperAdmin impersonation - audit log table + users.impersonate permission

Adds dobs_impersonation_log (one row per start/stop cycle) and seeds a new
users.impersonate permission code, granted to SuperAdmin by default -
consistent with the rest of the permission catalog (20260709) rather than a
hardcoded role check, so it could be delegated to another role later purely
through the Roles & Permissions screen, with no code changes.

Revision ID: 20260711_impersonation_log
Revises: 20260710_role_dashboard_endpoint
Create Date: 2026-07-11 00:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260711_impersonation_log'
down_revision = '20260710_role_dashboard_endpoint'
branch_labels = None
depends_on = None


PERMISSION_CODE = "users.impersonate"
PERMISSION_DESCRIPTION = "Log in as another employee's account to act on their behalf"
DEFAULT_GRANT_ROLES = ["SuperAdmin"]


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "dobs_impersonation_log" not in inspector.get_table_names():
        op.create_table(
            "dobs_impersonation_log",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("admin_user_id", sa.Integer(), sa.ForeignKey("dobs_user.id"), nullable=False),
            sa.Column("target_user_id", sa.Integer(), sa.ForeignKey("dobs_user.id"), nullable=False),
            sa.Column("started_at", sa.DateTime(), nullable=False),
            sa.Column("ended_at", sa.DateTime(), nullable=True),
            sa.Column("ip_address", sa.String(64), nullable=True),
        )
        op.create_index("ix_dobs_impersonation_log_admin_user_id", "dobs_impersonation_log", ["admin_user_id"])
        op.create_index("ix_dobs_impersonation_log_target_user_id", "dobs_impersonation_log", ["target_user_id"])

    existing_perm = bind.execute(
        sa.text("SELECT id FROM dobs_permission WHERE code = :code"), {"code": PERMISSION_CODE}
    ).scalar()
    if not existing_perm:
        bind.execute(
            sa.text("INSERT INTO dobs_permission (code, description) VALUES (:code, :description)"),
            {"code": PERMISSION_CODE, "description": PERMISSION_DESCRIPTION},
        )

    perm_id = bind.execute(
        sa.text("SELECT id FROM dobs_permission WHERE code = :code"), {"code": PERMISSION_CODE}
    ).scalar()
    role_ids = {row[0]: row[1] for row in bind.execute(sa.text("SELECT name, id FROM dobs_role"))}

    for role_name in DEFAULT_GRANT_ROLES:
        role_id = role_ids.get(role_name)
        if not role_id:
            continue
        exists = bind.execute(
            sa.text("SELECT 1 FROM dobs_role_permission WHERE role_id = :rid AND permission_id = :pid"),
            {"rid": role_id, "pid": perm_id},
        ).scalar()
        if not exists:
            bind.execute(
                sa.text("INSERT INTO dobs_role_permission (role_id, permission_id) VALUES (:rid, :pid)"),
                {"rid": role_id, "pid": perm_id},
            )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    perm_id = bind.execute(
        sa.text("SELECT id FROM dobs_permission WHERE code = :code"), {"code": PERMISSION_CODE}
    ).scalar()
    if perm_id:
        bind.execute(sa.text("DELETE FROM dobs_role_permission WHERE permission_id = :pid"), {"pid": perm_id})
        bind.execute(sa.text("DELETE FROM dobs_user_permission WHERE permission_id = :pid"), {"pid": perm_id})
        bind.execute(sa.text("DELETE FROM dobs_permission WHERE id = :pid"), {"pid": perm_id})

    if "dobs_impersonation_log" in inspector.get_table_names():
        op.drop_table("dobs_impersonation_log")
