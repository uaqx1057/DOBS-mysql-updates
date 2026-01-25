#!/opt/alt/python313/bin/python3.13

import os
import sys
import logging

BASE_DIR = os.path.dirname(__file__)
VENV_PATH = os.environ.get("VENV_PATH", os.path.join(BASE_DIR, "venv"))
LOG_DIR = os.environ.get("APP_LOG_DIR", os.path.join(BASE_DIR, "logs"))
os.makedirs(LOG_DIR, exist_ok=True)
APP_LOG = os.path.join(LOG_DIR, os.environ.get("APP_LOG_FILE", "passenger.log"))

# ---------- logging ----------
logging.basicConfig(
    filename=APP_LOG,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
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