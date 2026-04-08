#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${1:-/var/www/dobs/current}"

cd "${APP_DIR}"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

sudo systemctl daemon-reload
sudo systemctl restart dobs-gunicorn
sudo systemctl status dobs-gunicorn --no-pager

echo "Flask deploy steps completed for ${APP_DIR}"
