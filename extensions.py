from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_babel import Babel
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
migrate = Migrate()
csrf = CSRFProtect()
babel = Babel()
# Default to in-memory storage; overridden by app config if a supported backend is available.
limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")
