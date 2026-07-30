import bcrypt
from werkzeug.security import generate_password_hash

from utils.passwords import verify_password


def test_verifies_werkzeug_hash():
    password_hash = generate_password_hash("secret")
    assert verify_password(password_hash, "secret")
    assert not verify_password(password_hash, "wrong")


def test_verifies_laravel_bcrypt_hash():
    password_hash = bcrypt.hashpw(b"secret", bcrypt.gensalt()).decode()
    laravel_hash = "$2y$" + password_hash[4:]
    assert verify_password(laravel_hash, "secret")
    assert not verify_password(laravel_hash, "wrong")


def test_invalid_hash_fails_closed():
    assert not verify_password("", "secret")
    assert not verify_password("not-a-supported-hash", "secret")
