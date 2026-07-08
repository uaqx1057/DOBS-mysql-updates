"""Granular permission catalog for onboarding/offboarding actions

Adds the 11 action-level permission codes covering driver approval, platform
ID assignment, vehicle assignment, offboarding approval/clearance, finance
calculations, and HR finalization - replacing what today are hardcoded
`current_user.role != "X"` checks scattered across blueprints. Pure INSERT
migration (no schema changes) - the RolePermission grants below exactly
reproduce today's existing access per role, plus SuperAdmin gets every code
as a deliberate new bypass capability (confirmed with user - SuperAdmin has
no bypass on any of these routes today).

Nothing reads these rows yet; routes are switched over to
@require_permission(...) in a later change, one blueprint at a time.

Revision ID: 20260709_permission_catalog
Revises: 20260707_offboarding_fields
Create Date: 2026-07-09 00:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260709_permission_catalog'
down_revision = '20260707_offboarding_fields'
branch_labels = None
depends_on = None


# code -> (description, [role names granted by default])
# SuperAdmin is added to every entry separately below rather than repeated
# here, so the "reproduces today's behavior" mapping stays readable on its
# own.
PERMISSION_GRANTS = {
    "onboarding.ops_manager.approve": (
        "Approve/reject a driver at the Ops Manager onboarding stage",
        ["OpsManager"],
    ),
    "onboarding.hr.approve": (
        "Approve/reject a driver at the HR onboarding stage (creates contract/document fields)",
        ["HR"],
    ),
    "onboarding.hr_final.complete": (
        "Complete sponsorship transfer / Qiwa handling, generating driver contracts",
        ["HR"],
    ),
    "onboarding.ops_supervisor.approve": (
        "Assign platform/business IDs at the Ops Supervisor onboarding stage",
        ["OpsSupervisor"],
    ),
    "onboarding.fleet_manager.approve": (
        "Assign a vehicle at the Fleet Manager onboarding stage",
        ["FleetManager"],
    ),
    "onboarding.finance.approve": (
        "Approve transfer-fee payment at the Finance onboarding stage",
        ["FinanceManager"],
    ),
    "offboarding.ops_manager.approve": (
        "Approve or reject an offboarding request",
        ["OpsManager"],
    ),
    "offboarding.ops_supervisor.clear": (
        "Reclaim platform/business IDs and record penalties during offboarding",
        ["OpsSupervisor"],
    ),
    "offboarding.fleet_manager.clear": (
        "Release the vehicle and record damage/deductions during offboarding",
        ["FleetManager"],
    ),
    "offboarding.finance.clear": (
        "Perform financial calculations/clearance during offboarding",
        ["FinanceManager"],
    ),
    "offboarding.hr.finalize": (
        "Give the final HR verdict on an offboarding, generating the settlement",
        ["HR"],
    ),
}


def upgrade():
    bind = op.get_bind()

    existing_perms = {row[0] for row in bind.execute(sa.text("SELECT code FROM dobs_permission"))}
    for code, (description, _roles) in PERMISSION_GRANTS.items():
        if code not in existing_perms:
            bind.execute(
                sa.text("INSERT INTO dobs_permission (code, description) VALUES (:code, :description)"),
                {"code": code, "description": description},
            )

    role_ids = {row[0]: row[1] for row in bind.execute(sa.text("SELECT name, id FROM dobs_role"))}
    perm_ids = {row[0]: row[1] for row in bind.execute(sa.text("SELECT code, id FROM dobs_permission"))}

    def grant(role_name, code):
        role_id = role_ids.get(role_name)
        perm_id = perm_ids.get(code)
        if not role_id or not perm_id:
            return
        exists = bind.execute(
            sa.text("SELECT 1 FROM dobs_role_permission WHERE role_id = :rid AND permission_id = :pid"),
            {"rid": role_id, "pid": perm_id},
        ).scalar()
        if not exists:
            bind.execute(
                sa.text("INSERT INTO dobs_role_permission (role_id, permission_id) VALUES (:rid, :pid)"),
                {"rid": role_id, "pid": perm_id},
            )

    for code, (_description, roles) in PERMISSION_GRANTS.items():
        for role_name in roles:
            grant(role_name, code)
        grant("SuperAdmin", code)


def downgrade():
    bind = op.get_bind()
    codes = list(PERMISSION_GRANTS.keys())
    for code in codes:
        perm_id = bind.execute(
            sa.text("SELECT id FROM dobs_permission WHERE code = :code"), {"code": code}
        ).scalar()
        if not perm_id:
            continue
        bind.execute(sa.text("DELETE FROM dobs_role_permission WHERE permission_id = :pid"), {"pid": perm_id})
        bind.execute(sa.text("DELETE FROM dobs_user_permission WHERE permission_id = :pid"), {"pid": perm_id})
        bind.execute(sa.text("DELETE FROM dobs_permission WHERE id = :pid"), {"pid": perm_id})
