"""RBAC: multi-role support + grantable permissions, layered on top of the
legacy single `User.role` string column rather than replacing it outright.

Effective permission for a user = granted via any of their roles
(RolePermission), UNLESS there's an explicit per-user UserPermission
override, which always wins (so a permission can be revoked from one user
even if their role would otherwise grant it, or granted to a user whose
role wouldn't).

`require_permission(*codes)` is the RBAC-aware building block for gating a
route. Existing per-route role checks (`current_user.role != "X"`,
`utils.auth.require_roles`, `utils.auth_utils.roles_required`) keep working
unchanged - blueprints move over to `require_permission` one at a time as
they're touched, not all at once (see plan_dobs_revamp).
"""
from functools import wraps

from flask import abort
from flask_login import current_user

from extensions import db
from models import Permission, Role, RolePermission, UserPermission, UserRole


def user_role_names(user) -> set:
    """All role names granted to `user` via UserRole, plus their legacy
    `role` column so unmigrated users still resolve correctly."""
    names = {
        row.role.name
        for row in UserRole.query.filter_by(user_id=user.id).all()
        if row.role
    }
    if getattr(user, "role", None):
        names.add(user.role)
    return names


def user_has_role(user, *role_names) -> bool:
    if not role_names:
        return True
    return bool(user_role_names(user) & set(role_names))


def user_has_permission(user, code: str) -> bool:
    override = (
        UserPermission.query
        .join(Permission, UserPermission.permission_id == Permission.id)
        .filter(UserPermission.user_id == user.id, Permission.code == code)
        .first()
    )
    if override is not None:
        return bool(override.granted)

    role_names = user_role_names(user)
    if not role_names:
        return False

    granted = (
        RolePermission.query
        .join(Permission, RolePermission.permission_id == Permission.id)
        .join(Role, RolePermission.role_id == Role.id)
        .filter(Permission.code == code, Role.name.in_(role_names))
        .first()
    )
    return granted is not None


def require_permission(*codes):
    """Route decorator: allow access if the current user holds ANY of the
    given permission codes (via role or explicit grant)."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if codes and not any(user_has_permission(current_user, code) for code in codes):
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def get_or_create_permission(code: str, description: str = None) -> Permission:
    perm = Permission.query.filter_by(code=code).first()
    if not perm:
        perm = Permission(code=code, description=description)
        db.session.add(perm)
        db.session.flush()
    return perm


def grant_role(user, role_name: str):
    role = Role.query.filter_by(name=role_name).first()
    if not role:
        raise ValueError(f"Unknown role: {role_name}")
    if not UserRole.query.filter_by(user_id=user.id, role_id=role.id).first():
        db.session.add(UserRole(user_id=user.id, role_id=role.id))


def revoke_role(user, role_name: str):
    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return
    UserRole.query.filter_by(user_id=user.id, role_id=role.id).delete()


def set_permission_override(user, code: str, granted: bool):
    """Grant or revoke `code` for `user` directly, independent of role."""
    perm = get_or_create_permission(code)
    row = UserPermission.query.filter_by(user_id=user.id, permission_id=perm.id).first()
    if row:
        row.granted = granted
    else:
        db.session.add(UserPermission(user_id=user.id, permission_id=perm.id, granted=granted))


def clear_permission_override(user, code: str):
    """Remove a per-user override, falling back to role-derived permission."""
    perm = Permission.query.filter_by(code=code).first()
    if not perm:
        return
    UserPermission.query.filter_by(user_id=user.id, permission_id=perm.id).delete()


def role_permission_codes(role) -> set:
    """All permission codes currently granted to `role` by default."""
    return {
        row.permission.code
        for row in RolePermission.query.filter_by(role_id=role.id).all()
        if row.permission
    }


def set_role_permissions(role, codes: set):
    """Replace `role`'s default permission grants with exactly `codes`."""
    current = RolePermission.query.filter_by(role_id=role.id).all()
    current_codes = {row.permission_id: row for row in current}
    perm_by_code = {p.code: p for p in Permission.query.filter(Permission.code.in_(codes)).all()}

    wanted_ids = {perm_by_code[c].id for c in codes if c in perm_by_code}
    for perm_id, row in current_codes.items():
        if perm_id not in wanted_ids:
            db.session.delete(row)

    existing_ids = set(current_codes.keys())
    for perm_id in wanted_ids - existing_ids:
        db.session.add(RolePermission(role_id=role.id, permission_id=perm_id))
