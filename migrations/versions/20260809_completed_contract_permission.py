"""Permission for managing contract packs on already-completed drivers

Adds "onboarding.completed.manage_contracts" - lets HR retroactively
generate/attach a contract pack and record signed copies for drivers who
finished onboarding before a system contract existed for them (or whose
contract records are otherwise missing), without reopening onboarding.
Granted to HR and SuperAdmin by default, matching the
onboarding.hr.approve pattern in 20260709_permission_catalog. Admin
dashboard access to the same routes goes through the legacy
current_user.role in ("Admin", "SuperAdmin") check instead of this
permission code - see _can_manage_completed_contracts in
blueprints/hr/routes.py - so "Admin" is deliberately not granted this code
here even if a matching Role row exists.

Note: at the time of writing, migrations/versions has two divergent heads
(20260718_remove_driver_license_number and
20260717_contract_template_arabic_content, both branching from
20260716_* with no merge revision reconverging them). This migration
chains after the more recent of the two by date without attempting to fix
that pre-existing split - flagged separately, not addressed here.

Revision ID: 20260809_completed_contract_permission
Revises: 20260718_remove_driver_license_number
Create Date: 2026-08-09 00:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260809_completed_contract_permission'
down_revision = '20260718_remove_driver_license_number'
branch_labels = None
depends_on = None


PERMISSION_CODE = "onboarding.completed.manage_contracts"
PERMISSION_DESCRIPTION = (
    "Generate/attach a contract pack and upload signed copies for a driver "
    "who already finished onboarding (retroactive, outside the normal HR "
    "approval flow)"
)
GRANTED_ROLES = ["HR"]


def upgrade():
    bind = op.get_bind()

    existing = bind.execute(
        sa.text("SELECT id FROM dobs_permission WHERE code = :code"), {"code": PERMISSION_CODE}
    ).scalar()
    if not existing:
        bind.execute(
            sa.text("INSERT INTO dobs_permission (code, description) VALUES (:code, :description)"),
            {"code": PERMISSION_CODE, "description": PERMISSION_DESCRIPTION},
        )

    role_ids = {row[0]: row[1] for row in bind.execute(sa.text("SELECT name, id FROM dobs_role"))}
    perm_id = bind.execute(
        sa.text("SELECT id FROM dobs_permission WHERE code = :code"), {"code": PERMISSION_CODE}
    ).scalar()

    def grant(role_name):
        role_id = role_ids.get(role_name)
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

    for role_name in GRANTED_ROLES:
        grant(role_name)
    grant("SuperAdmin")


def downgrade():
    bind = op.get_bind()
    perm_id = bind.execute(
        sa.text("SELECT id FROM dobs_permission WHERE code = :code"), {"code": PERMISSION_CODE}
    ).scalar()
    if not perm_id:
        return
    bind.execute(sa.text("DELETE FROM dobs_role_permission WHERE permission_id = :pid"), {"pid": perm_id})
    bind.execute(sa.text("DELETE FROM dobs_user_permission WHERE permission_id = :pid"), {"pid": perm_id})
    bind.execute(sa.text("DELETE FROM dobs_permission WHERE id = :pid"), {"pid": perm_id})
