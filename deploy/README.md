# DOBS VPS Deployment Assets

This folder contains DOBS-ready deployment assets aligned to VPS_System_Upgrade templates.

## Contents

- env/.env.vps-system-upgrade.example: production env baseline for Flask + MySQL + Redis-backed limiter
- nginx/dobs.conf: Nginx reverse proxy to Gunicorn
- systemd/dobs-gunicorn.service: Gunicorn service unit
- scripts/deploy_flask.sh: repeatable Flask deploy sequence

## Notes

- Apply in staging first, then production.
- Replace placeholder domains, paths, and credentials.
- If running on Namecheap shared hosting, keep current runtime until VPS cutover day.
