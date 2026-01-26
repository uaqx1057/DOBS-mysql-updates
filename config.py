import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# --- Static configuration (no .env) ---
SECRET_KEY_DEFAULT = "change-me-secret-key"
# Replace with your real DSN or set DATABASE_URI/DATABASE_URL env vars.
DATABASE_URI_DEFAULT = "mysql+pymysql://dobsykjq_dms:9gj*X]MwPPy+@localhost:3306/dobsykjq_dms"
UPLOAD_ROOT_DEFAULT = BASE_DIR / "static" / "uploads"
MAIL_DEFAULT_NAME = "DOBS System"
MAIL_DEFAULT_ADDRESS = "system@dobs.com"
RATE_LIMIT_STORAGE_DEFAULT = "memory://"


class Config:
    """Base application configuration (override via environment)."""
    SECRET_KEY = os.getenv("SECRET_KEY", SECRET_KEY_DEFAULT)

    # Database URI (env overrides static default).
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI") or os.getenv("DATABASE_URL") or DATABASE_URI_DEFAULT
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File upload settings (keep under static/uploads for serving)
    UPLOAD_FOLDER = str(UPLOAD_ROOT_DEFAULT)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}
    UPLOAD_CDN_BASE = None
    UPLOAD_SIGNING_SECRET = None

    # Anti-virus scanning (optional)
    AV_SCAN_ENABLED = False
    AV_SCAN_COMMAND = None

    # Session cookies
    # Allow local HTTP testing; set to True in production/https.
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # CSRF
    WTF_CSRF_ENABLED = True

    # Mail settings
    MAIL_SERVER = "localhost"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "system@dobs.com"
    MAIL_PASSWORD = "change-me"
    MAIL_DEFAULT_SENDER = (MAIL_DEFAULT_NAME, MAIL_DEFAULT_ADDRESS)

    # Rate limiting
    RATELIMIT_DEFAULTS = "200 per hour;50 per minute"
    RATELIMIT_STORAGE_URI = RATE_LIMIT_STORAGE_DEFAULT
    RATELIMIT_STORAGE_URL = RATE_LIMIT_STORAGE_DEFAULT

    # Two-factor auth (email OTP)
    TWO_FA_EMAIL_ENABLED = False
    TWO_FA_EMAIL_EXPIRY_MIN = 10

    # Observability
    SLOW_QUERY_MS = 500

    # Localization
    LANGUAGES = ["en", "ar"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

    # Connection pool settings (applied only when not using SQLite)
    if not SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_size": 10,
            "max_overflow": 20,
            "pool_timeout": 30,
            "pool_recycle": 1800,
            "pool_pre_ping": True,
        }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {}

