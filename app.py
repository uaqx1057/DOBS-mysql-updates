import sys
import os
import time
from sqlalchemy import event

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory, session, redirect, url_for, request, make_response, g
from flask_limiter.errors import RateLimitExceeded
from config import Config
from extensions import db, mail, login_manager, migrate, csrf, babel, limiter
# Ensure models are registered with SQLAlchemy metadata for migrations
import models  # noqa: F401

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
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Configure rate limiting from config/env for flexibility
    default_limits_raw = app.config.get("RATELIMIT_DEFAULTS")
    if default_limits_raw:
        app.config["RATELIMIT_DEFAULT"] = default_limits_raw
    storage_uri = app.config.get("RATELIMIT_STORAGE_URI")
    if storage_uri:
        app.config["RATELIMIT_STORAGE_URI"] = storage_uri
    limiter.init_app(app)

    # --- Slow query logging ---
    slow_threshold_ms = app.config.get("SLOW_QUERY_MS", 500)

    def _setup_query_timing():
        with app.app_context():
            engine = db.get_engine()

            @event.listens_for(engine, "before_cursor_execute")
            def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
                context._query_start_time = time.perf_counter()

            @event.listens_for(engine, "after_cursor_execute")
            def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
                start = getattr(context, "_query_start_time", None)
                if start is None:
                    return
                duration_ms = int((time.perf_counter() - start) * 1000)
                if duration_ms >= slow_threshold_ms:
                    app.logger.warning(
                        "[SLOW QUERY] %sms %s params=%s", duration_ms, statement.strip().split("\n")[0][:200], parameters
                    )

    _setup_query_timing()

    # --- Localization (Babel) ---
    def select_locale():
        return session.get("lang") or request.accept_languages.best_match(app.config["LANGUAGES"]) or "en"

    babel.init_app(app, locale_selector=select_locale)

    # --- Basic logging setup ---
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler

        log_path = os.path.join(base_dir, "logs")
        os.makedirs(log_path, exist_ok=True)
        handler = RotatingFileHandler(os.path.join(log_path, "app.log"), maxBytes=1_000_000, backupCount=5)
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        app.logger.addHandler(handler)

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
        g.request_started_at = time.perf_counter()
        if "lang" not in session:
            preferred = request.accept_languages.best_match(["en", "ar"])
            session["lang"] = preferred or "en"
        g.current_lang = session.get("lang", "en")
        g.text_direction = "rtl" if g.current_lang == "ar" else "ltr"

    @app.after_request
    def add_timing_header(response):
        started = getattr(g, "request_started_at", None)
        if started is not None:
            duration_ms = int((time.perf_counter() - started) * 1000)
            response.headers["X-Request-Duration-ms"] = str(duration_ms)
        return response

    @app.errorhandler(RateLimitExceeded)
    def handle_ratelimit(exc):
        app.logger.warning(
            "Rate limit exceeded", extra={"path": request.path, "ip": request.remote_addr, "endpoint": request.endpoint}
        )
        if request.accept_mimetypes.best == "application/json":
            return {"message": "Too many requests. Please slow down."}, 429
        return "Too many requests. Please slow down.", 429

    @app.context_processor
    def inject_lang():
        return {
            "current_lang": getattr(g, "current_lang", "en"),
            "text_direction": getattr(g, "text_direction", "ltr"),
        }

    # --- Front page route ---
    @app.route("/")
    def front_page():
        lang = session.get("lang", "en")
        filename = "rtl_index.html" if lang == "ar" else "index.html"
        return make_response(send_from_directory(base_dir, filename))

    # --- Health endpoint for ops ---
    @app.route("/healthz")
    def healthz():
        return {"status": "ok"}, 200

    # --- Set language route ---
    @app.route("/set_language/<lang>")
    def set_language(lang):
        if lang in ["en", "ar"]:
            session["lang"] = lang
        next_page = request.args.get("next") or url_for("front_page")
        return redirect(next_page)

    return app


# --- Run app directly ---
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
