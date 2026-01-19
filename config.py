import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI", "mysql+pymysql://dobsykjq_dms:9gj*X]MwPPy+@localhost:3306/dobsykjq_dms"

    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ File Upload Settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}

    # Mail settings
    #MAIL_SERVER = "smtp.gmail.com"
    #MAIL_USE_TLS = True
    #MAIL_USE_SSL = False
    #MAIL_USERNAME = "system.dobs@gmail.com"
    #MAIL_PASSWORD = "khoalturfsxyykgi"
    #MAIL_DEFAULT_SENDER = ("DOBS System", "system.dobs@gmail.com")
    
    # Mail settings
    MAIL_SERVER = "dobs.dobs.cloud"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "system@dobs.dobs.cloud"
    MAIL_PASSWORD = "7osg9jzh3xt6D"
    MAIL_DEFAULT_SENDER = ("DOBS System", "system@dobs.dobs.cloud")

    # Connection pool settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,         # number of persistent connections
        "max_overflow": 20,      # number of temporary overflow connections
        "pool_timeout": 30,      # seconds to wait for a free connection
        "pool_recycle": 1800,    # recycle connections after 30 minutes
        "pool_pre_ping": True    # check if connections are alive before using
    }

