#!/opt/alt/python313/bin/python3.13

import sys
import os
import logging
import site

# --------------------------
# Logging setup
# --------------------------
log_file = os.path.join(os.path.dirname(__file__), "app.log")
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

sys.stdout = open(log_file, "a")
sys.stderr = open(log_file, "a")

logging.info("Starting WSGI application...")

# --------------------------
# Add project path
# --------------------------
project_dir = os.path.dirname(__file__)
sys.path.insert(0, project_dir)

# --------------------------
# Add virtualenv site-packages
# --------------------------
venv_path = '/home/dobsykjq/virtualenv/dobs2/3.13'
site.addsitedir(os.path.join(venv_path, "lib/python3.13/site-packages"))
logging.info(f"Added virtualenv site-packages: {venv_path}")

# --------------------------
# Import Flask app
# --------------------------
try:
    from app import create_app
    application = create_app()
    logging.info("WSGI application loaded successfully.")
except Exception as e:
    logging.exception("Failed to load WSGI application")
    raise
