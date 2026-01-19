import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory, session, redirect, url_for, request, make_response
from config import Config
from extensions import db, mail, login_manager

# Import blueprints
from blueprints.public.routes import public_bp
from blueprints.auth.routes import auth_bp
from blueprints.admin.routes import admin_bp
from blueprints.hr.routes import hr_bp
from blueprints.ops_coordinator.routes import ops_coordinator_bp
from blueprints.ops_manager.routes import ops_manager_bp
from blueprints.ops_supervisor.routes import ops_supervisor_bp
from blueprints.fleet.routes import fleet_bp
from blueprints.finance.routes import finance_bp
from blueprints.reports.routes import reports_bp



def create_app():
    # --- Project root ---
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # --- Flask app initialization ---
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static")
    )
    app.config.from_object(Config)
    app.secret_key = app.config.get("SECRET_KEY", "fallback_secret_key")

    # --- Initialize extensions ---
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # --- Register blueprints ---
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/dashboard")
    app.register_blueprint(hr_bp, url_prefix="/dashboard/hr")
    app.register_blueprint(ops_coordinator_bp, url_prefix="/ops_coordinator") 
    app.register_blueprint(ops_manager_bp, url_prefix="/dashboard/ops")
    app.register_blueprint(ops_supervisor_bp, url_prefix="/dashboard/ops_supervisor")
    app.register_blueprint(fleet_bp, url_prefix="/dashboard/fleet")
    app.register_blueprint(finance_bp, url_prefix="/dashboard/finance")
    app.register_blueprint(reports_bp, url_prefix="/reports")

    # --- Default language before request ---
    @app.before_request
    def set_default_lang():
        if "lang" not in session:
            preferred = request.accept_languages.best_match(["en", "ar"])
            session["lang"] = preferred or "en"

    # --- Front page route ---
    @app.route("/")
    def front_page():
        lang = session.get("lang", "en")
        filename = "rtl_index.html" if lang == "ar" else "index.html"
        return make_response(send_from_directory(base_dir, filename))

    # --- Set language route ---
    @app.route("/set_language/<lang>")
    def set_language(lang):
        if lang in ["en", "ar"]:
            session["lang"] = lang
        next_page = request.args.get("next") or url_for("front_page")
        return redirect(next_page)

    # --- Database creation ---
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print("Database initialization failed:", e)

    return app


# --- Run app directly ---
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
