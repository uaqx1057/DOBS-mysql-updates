import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"


def _read_env_file_value(key: str) -> str | None:
    if not ENV_FILE.exists():
        return None

    prefix = f"{key}="
    for raw in ENV_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or not line.startswith(prefix):
            continue
        return line[len(prefix):].strip().strip('"').strip("'")

    return None


def _env_or_file(key: str, default: str = "") -> str:
    val = os.getenv(key)
    if val is not None and val != "":
        return val

    file_val = _read_env_file_value(key)
    if file_val is not None and file_val != "":
        return file_val

    return default


def _env_bool(key: str, default: bool) -> bool:
    raw = _env_or_file(key, "")
    if raw == "":
        return default
    return raw.lower() in {"1", "true", "yes", "on"}


def _env_int(key: str, default: int) -> int:
    raw = _env_or_file(key, "")
    if raw == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default

# --- Static configuration (no .env) ---
SECRET_KEY_DEFAULT = "change-me-secret-key"
# Replace with your real DSN or set DATABASE_URI/DATABASE_URL env vars.
DATABASE_URI_DEFAULT = "mysql+pymysql://dobsykjq_dms:9gj*X]MwPPy+@localhost:3306/dobsykjq_dms"
UPLOAD_ROOT_DEFAULT = BASE_DIR / "static" / "uploads"
MAIL_DEFAULT_NAME = "DOBS System"
MAIL_DEFAULT_ADDRESS = "system@dobs.com"
RATE_LIMIT_STORAGE_DEFAULT = "memory://"
REDIS_URL_DEFAULT = ""
CONTRACT_FIRST_PARTY_NAME_DEFAULT = "Speed Logi Transport"
CONTRACT_FIRST_PARTY_NAME_AR_DEFAULT = "سبيد لوجي للنقل"
CONTRACT_FIRST_PARTY_LABEL_DEFAULT = "First Party"
CONTRACT_FIRST_PARTY_LABEL_AR_DEFAULT = "الطرف الأول"
CONTRACT_SECOND_PARTY_LABEL_DEFAULT = "Second Party / Driver"
CONTRACT_SECOND_PARTY_LABEL_AR_DEFAULT = "الطرف الثاني / السائق"
CONTRACT_COMPANY_SIGNATORY_NAME_DEFAULT = "Authorized Signatory"
CONTRACT_COMPANY_SIGNATORY_TITLE_DEFAULT = "Operations Director"
DRIVER_CONTRACT_LETTERHEAD_PDF_DEFAULT = ""
DRIVER_CONTRACT_REFERENCE_PDF_DEFAULT = ""


class Config:
    """Base application configuration (override via environment)."""
    SECRET_KEY = _env_or_file("SECRET_KEY", SECRET_KEY_DEFAULT)

    # Database URI (env overrides static default).
    SQLALCHEMY_DATABASE_URI = _env_or_file("DATABASE_URI") or _env_or_file("DATABASE_URL") or DATABASE_URI_DEFAULT
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File upload settings (keep under static/uploads for serving)
    UPLOAD_FOLDER = str(UPLOAD_ROOT_DEFAULT)
    DRIVER_DOCUMENT_PATH = _env_or_file("DRIVER_DOCUMENT_PATH", str(UPLOAD_ROOT_DEFAULT))
    MAX_UPLOAD_MB = _env_int("MAX_UPLOAD_MB", 100)
    MAX_CONTENT_LENGTH = MAX_UPLOAD_MB * 1024 * 1024
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
    SESSION_PERMANENT = False

    # Redis runtime backends
    REDIS_URL = _env_or_file("REDIS_URL", REDIS_URL_DEFAULT).strip()

    # Feature flag: keep false if you want old memory/file behavior even with REDIS_URL set.
    USE_REDIS_RUNTIME = _env_bool("USE_REDIS_RUNTIME", True)

    # Flask-Session defaults (overridden at runtime when Redis is available)
    SESSION_TYPE = _env_or_file("SESSION_TYPE", "filesystem")
    SESSION_FILE_DIR = _env_or_file("SESSION_FILE_DIR") or str(BASE_DIR / "instance" / "flask_session")
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = _env_or_file("SESSION_KEY_PREFIX", "dobs:session:")

    # Flask-Caching defaults (overridden at runtime when Redis is available)
    CACHE_TYPE = _env_or_file("CACHE_TYPE", "SimpleCache")
    CACHE_DEFAULT_TIMEOUT = int(_env_or_file("CACHE_DEFAULT_TIMEOUT", "120"))
    CACHE_KEY_PREFIX = _env_or_file("CACHE_KEY_PREFIX", "dobs:cache:")

    # CSRF
    WTF_CSRF_ENABLED = True

    # Mail settings
    MAIL_SERVER = _env_or_file("MAIL_SERVER", "localhost")
    MAIL_PORT = int(_env_or_file("MAIL_PORT", "587"))
    MAIL_USE_TLS = _env_bool("MAIL_USE_TLS", True)
    MAIL_USE_SSL = _env_bool("MAIL_USE_SSL", False)
    MAIL_USERNAME = _env_or_file("MAIL_USERNAME", "system@dobs.com")
    MAIL_PASSWORD = _env_or_file("MAIL_PASSWORD", "change-me")
    MAIL_DEFAULT_NAME = _env_or_file("MAIL_DEFAULT_NAME", MAIL_DEFAULT_NAME)
    MAIL_DEFAULT_ADDRESS = _env_or_file("MAIL_DEFAULT_ADDRESS", MAIL_DEFAULT_ADDRESS)
    MAIL_DEFAULT_SENDER = (MAIL_DEFAULT_NAME, MAIL_DEFAULT_ADDRESS)

    CONTRACT_FIRST_PARTY_NAME = _env_or_file("CONTRACT_FIRST_PARTY_NAME", CONTRACT_FIRST_PARTY_NAME_DEFAULT)
    CONTRACT_FIRST_PARTY_NAME_AR = _env_or_file("CONTRACT_FIRST_PARTY_NAME_AR", CONTRACT_FIRST_PARTY_NAME_AR_DEFAULT)
    CONTRACT_FIRST_PARTY_LABEL = _env_or_file("CONTRACT_FIRST_PARTY_LABEL", CONTRACT_FIRST_PARTY_LABEL_DEFAULT)
    CONTRACT_FIRST_PARTY_LABEL_AR = _env_or_file("CONTRACT_FIRST_PARTY_LABEL_AR", CONTRACT_FIRST_PARTY_LABEL_AR_DEFAULT)
    CONTRACT_SECOND_PARTY_LABEL = _env_or_file("CONTRACT_SECOND_PARTY_LABEL", CONTRACT_SECOND_PARTY_LABEL_DEFAULT)
    CONTRACT_SECOND_PARTY_LABEL_AR = _env_or_file("CONTRACT_SECOND_PARTY_LABEL_AR", CONTRACT_SECOND_PARTY_LABEL_AR_DEFAULT)
    CONTRACT_COMPANY_SIGNATORY_NAME = _env_or_file("CONTRACT_COMPANY_SIGNATORY_NAME", CONTRACT_COMPANY_SIGNATORY_NAME_DEFAULT)
    CONTRACT_COMPANY_SIGNATORY_TITLE = _env_or_file("CONTRACT_COMPANY_SIGNATORY_TITLE", CONTRACT_COMPANY_SIGNATORY_TITLE_DEFAULT)
    DRIVER_CONTRACT_LETTERHEAD_PDF = _env_or_file("DRIVER_CONTRACT_LETTERHEAD_PDF", DRIVER_CONTRACT_LETTERHEAD_PDF_DEFAULT)
    DRIVER_CONTRACT_REFERENCE_PDF = _env_or_file("DRIVER_CONTRACT_REFERENCE_PDF", DRIVER_CONTRACT_REFERENCE_PDF_DEFAULT)

    # Rate limiting
    RATELIMIT_DEFAULTS = "200 per hour;50 per minute"
    RATELIMIT_STORAGE_URI = _env_or_file("RATELIMIT_STORAGE_URI", RATE_LIMIT_STORAGE_DEFAULT)
    RATELIMIT_STORAGE_URL = _env_or_file("RATELIMIT_STORAGE_URL", RATELIMIT_STORAGE_URI)

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

