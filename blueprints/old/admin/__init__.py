from flask import Blueprint

# Create the Blueprint
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates',  # adjust if your templates are elsewhere
    static_folder='static'        # optional
)

# Import routes to register them with this blueprint
from . import routes
