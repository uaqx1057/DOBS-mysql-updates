# DOBS Deployment Guide (VPS Alignment)

This document aligns DOBS deployment with VPS_System_Upgrade templates.

## 1. One-time VPS setup

```bash
cd /var/www/dobs/current
cp deploy/env/.env.vps-system-upgrade.example .env
# update DB, Redis, mail and secrets
```

## 2. Install Nginx and systemd templates

```bash
# Nginx
sudo cp deploy/nginx/dobs.conf /etc/nginx/sites-available/dobs.conf
sudo ln -s /etc/nginx/sites-available/dobs.conf /etc/nginx/sites-enabled/dobs.conf

# Gunicorn service
sudo cp deploy/systemd/dobs-gunicorn.service /etc/systemd/system/dobs-gunicorn.service

sudo nginx -t
sudo systemctl daemon-reload
sudo systemctl enable dobs-gunicorn
sudo systemctl restart dobs-gunicorn
sudo systemctl reload nginx
```

## 3. Deploy app updates

```bash
cd /var/www/dobs/current
bash deploy/scripts/deploy_flask.sh /var/www/dobs/current
```

## 4. Verify

```bash
sudo systemctl status dobs-gunicorn --no-pager
curl -I http://127.0.0.1:8001/healthz
curl -I https://dobs.yourdomain.com/healthz
curl https://dobs.yourdomain.com/ops/runtime-backends
```

## 5. Notes

- Keep production .env only on server.
- Set `USE_REDIS_RUNTIME=true` on VPS to enable Redis-backed limiter/session/cache.
- For Namecheap shared hosting, do not apply VPS Nginx/systemd files until VPS cutover.
- Apply in staging first, then production.

## 6. Preflight validation script

```bash
cd /var/www/dobs/current
bash deploy/scripts/vps_preflight_check.sh /var/www/dobs/current https://dobs.yourdomain.com
```
