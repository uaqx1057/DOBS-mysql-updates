from flask import Blueprint

sso_bp = Blueprint("sso", __name__, url_prefix="/sso")

from blueprints.sso import routes  # noqa: F401, E402
