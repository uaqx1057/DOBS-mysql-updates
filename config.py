import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load .env only when not in production
if os.getenv("FLASK_ENV", "production") != "production":
    load_dotenv(BASE_DIR / ".env")


class Config:
    """Base application configuration (override via environment)."""
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)

    # Database URI should be provided via env; keep placeholder default for local dev only.
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI") or os.getenv("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        # Allow a lightweight fallback only for local dev 
        if os.getenv("FLASK_ENV", "production") != "production":
            SQLALCHEMY_DATABASE_URI = "mysql+pymysql://dobsykjq_dms:9gj*X]MwPPy+@localhost:3306/dobsykjq_dms"
        else:
            raise RuntimeError("DATABASE_URI is required in production")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File upload settings (keep under static/uploads for serving)
    UPLOAD_FOLDER = os.getenv("UPLOAD_ROOT") or str(BASE_DIR / "static" / "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}
    UPLOAD_CDN_BASE = os.getenv("UPLOAD_CDN_BASE")  # e.g., https://cdn.example.com/uploads
    UPLOAD_SIGNING_SECRET = os.getenv("UPLOAD_SIGNING_SECRET")

    # Anti-virus scanning (optional)
    AV_SCAN_ENABLED = os.getenv("AV_SCAN_ENABLED", "false").lower() == "true"
    AV_SCAN_COMMAND = os.getenv("AV_SCAN_COMMAND")  # e.g., "clamdscan --no-summary"

    # Session cookies
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "true").lower() == "true"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")

    # CSRF
    WTF_CSRF_ENABLED = os.getenv("WTF_CSRF_ENABLED", "true").lower() == "true"

    # Mail settings (all env-driven; defaults are safe fallbacks for local testing only)
    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "25"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "false").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = (
        os.getenv("MAIL_DEFAULT_NAME", "DOBS System"),
        os.getenv("MAIL_DEFAULT_ADDRESS", "noreply@example.com"),
    )

    # Rate limiting
    RATELIMIT_DEFAULTS = os.getenv("RATELIMIT_DEFAULTS", "200 per hour;50 per minute")
    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "redis://localhost:6379/0")

    # Two-factor auth (email OTP)
    TWO_FA_EMAIL_ENABLED = os.getenv("TWO_FA_EMAIL_ENABLED", "false").lower() == "true"
    TWO_FA_EMAIL_EXPIRY_MIN = int(os.getenv("TWO_FA_EMAIL_EXPIRY_MIN", "10"))

    # Observability
    SLOW_QUERY_MS = int(os.getenv("SLOW_QUERY_MS", "500"))

    # Localization
    LANGUAGES = ["en", "ar"]
    BABEL_DEFAULT_LOCALE = os.getenv("BABEL_DEFAULT_LOCALE", "en")
    BABEL_DEFAULT_TIMEZONE = os.getenv("BABEL_DEFAULT_TIMEZONE", "UTC")

    # Connection pool settings (applied only when not using SQLite)
    if not SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_size": int(os.getenv("DB_POOL_SIZE", "10")),
            "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "20")),
            "pool_timeout": int(os.getenv("DB_POOL_TIMEOUT", "30")),
            "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", "1800")),
            "pool_pre_ping": True,
        }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {}

