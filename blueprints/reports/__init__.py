from flask import Blueprint

reports_bp = Blueprint(
    "reports_bp",
    __name__,
    template_folder="../../templates"
)

from . import routes  # import routes.py
