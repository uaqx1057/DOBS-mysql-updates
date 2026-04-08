#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${1:-/var/www/dobs/current}"
APP_URL="${2:-https://dobs.yourdomain.com}"

cd "${APP_DIR}"

echo "[1/6] Gunicorn service"
sudo systemctl is-active dobs-gunicorn

echo "[2/6] Local health endpoint"
curl -fsS http://127.0.0.1:8001/healthz >/dev/null

echo "[3/6] Public health endpoint"
curl -fsS "${APP_URL}/healthz" >/dev/null

echo "[4/6] Runtime backends"
curl -fsS "${APP_URL}/ops/runtime-backends" || true

echo "[5/6] Redis ping (optional, if configured)"
if [ -n "${REDIS_URL:-}" ]; then
  redis-cli -u "${REDIS_URL}" ping || true
else
  echo "REDIS_URL not set; skipping redis ping"
fi

echo "[6/6] Done"
echo "DOBS VPS preflight check completed"
