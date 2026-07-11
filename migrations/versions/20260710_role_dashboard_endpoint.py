"""Role.dashboard_endpoint - data-driven dashboard routing

Replaces the hardcoded ROLE_DASHBOARD_ENDPOINTS dict in auth/routes.py and
the single-role elif-chain in templates/base.html's sidebar. Backfilled for
the 10 legacy roles to reproduce today's routing exactly. A role with no
endpoint set (any newly created custom role, until an admin picks one) falls
back to a generic landing page rather than a dead end.

Revision ID: 20260710_role_dashboard_endpoint
Revises: 20260709_permission_catalog
Create Date: 2026-07-10 00:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260710_role_dashboard_endpoint'
down_revision = '20260709_permission_catalog'
branch_labels = None
depends_on = None


# Mirrors auth/routes.py's ROLE_DASHBOARD_ENDPOINTS, extended to cover the
# 3 legacy role names that dict never handled (HRManager, Finance, Admin -
# a pre-existing gap where those exact role strings had nowhere to land;
# mapped here to their closest equivalent dashboard).
LEGACY_DASHBOARD_ENDPOINTS = {
    "SuperAdmin": "admin.dashboard",
    "Admin": "admin.dashboard",
    "HR": "hr.dashboard_hr",
    "HRManager": "hr.dashboard_hr",
    "OpsManager": "ops_manager.dashboard_ops",
    "OpsSupervisor": "ops_supervisor.dashboard_ops_supervisor",
    "OpsCoordinator": "ops_coordinator.dashboard_ops_coordinator",
    "FleetManager": "fleet.dashboard_fleet",
    "Finance": "finance.dashboard_finance",
    "FinanceManager": "finance.dashboard_finance",
}


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    columns = {col["name"] for col in inspector.get_columns("dobs_role")}
    if "dashboard_endpoint" not in columns:
        op.add_column("dobs_role", sa.Column("dashboard_endpoint", sa.String(100), nullable=True))

    for role_name, endpoint in LEGACY_DASHBOARD_ENDPOINTS.items():
        bind.execute(
            sa.text("UPDATE dobs_role SET dashboard_endpoint = :endpoint WHERE name = :name AND dashboard_endpoint IS NULL"),
            {"endpoint": endpoint, "name": role_name},
        )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("dobs_role")}
    if "dashboard_endpoint" in columns:
        op.drop_column("dobs_role", "dashboard_endpoint")
