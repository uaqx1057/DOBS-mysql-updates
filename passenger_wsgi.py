#!/opt/alt/python313/bin/python3.13

import os
import sys
import logging
import tempfile

BASE_DIR = os.path.dirname(__file__)
# Default to deployed virtualenv path; override via VENV_PATH env.
VENV_PATH = os.environ.get(
    "VENV_PATH", "/home/dobsykjq/virtualenv/dobs2/3.13"
)
LOG_DIR = os.environ.get("APP_LOG_DIR", os.path.join(BASE_DIR, "logs"))
APP_LOG = os.path.join(LOG_DIR, os.environ.get("APP_LOG_FILE", "passenger.log"))


def configure_logging():
    """Prefer file logging; fall back to stdout if the path is not writable."""
    handlers = []

    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        handlers.append(logging.FileHandler(APP_LOG))
    except (OSError, PermissionError) as exc:
        fallback_dir = os.path.join(tempfile.gettempdir(), "dobs", "logs")
        try:
            os.makedirs(fallback_dir, exist_ok=True)
            fallback_path = os.path.join(fallback_dir, os.path.basename(APP_LOG))
            handlers.append(logging.FileHandler(fallback_path))
        except (OSError, PermissionError):
            sys.stderr.write(
                f"Logging to {APP_LOG} failed ({exc}); falling back to stdout.\n"
            )
            handlers.append(logging.StreamHandler(sys.stdout))

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers,
        force=True,
    )


configure_logging()
logging.info("Starting WSGI application...")

# ---------- activate venv ----------
activate = os.path.join(VENV_PATH, "bin", "activate_this.py")
if not os.path.exists(activate):
    logging.error("activate_this.py not found at %s", activate)
else:
    with open(activate) as f:
        exec(f.read(), {"__file__": activate})
    logging.info("Virtualenv activated from %s", VENV_PATH)

# ---------- sys.path ----------
sys.path.insert(0, BASE_DIR)  # /home/dobsykjq/dobs

# ---------- create app ----------
try:
    from app import create_app
    application = create_app()
    logging.info("WSGI application loaded successfully.")
except Exception:
    logging.exception("Failed to load WSGI application")
    raise