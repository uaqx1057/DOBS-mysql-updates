"""Password verification compatible with both DOBS and legacy Laravel hashes."""

import bcrypt
from werkzeug.security import check_password_hash


_BCRYPT_PREFIXES = ("$2a$", "$2b$", "$2y$")


def verify_password(password_hash: str, password: str) -> bool:
    if not password_hash or password is None:
        return False

    try:
        if password_hash.startswith(_BCRYPT_PREFIXES):
            return bcrypt.checkpw(
                password.encode("utf-8"),
                password_hash.encode("utf-8"),
            )
        return check_password_hash(password_hash, password)
    except (TypeError, ValueError):
        return False
