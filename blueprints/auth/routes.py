# blueprints/auth/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_login import login_user, logout_user, login_required
from sqlalchemy.exc import OperationalError
from werkzeug.security import check_password_hash

from forms.auth import LoginForm
from models import User  # dob_user model
from extensions import db, login_manager, limiter

auth_bp = Blueprint("auth", __name__)

# Load user callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data

        try:
            user = User.query.filter_by(username=username).first()
        except OperationalError:
            db.session.rollback()
            current_app.logger.exception("Database unavailable during login")
            flash("Database is unavailable. Please try again in a moment.", "danger")
            return render_template("login.html", form=form), 503

        if not user or not check_password_hash(user.password, password):
            flash("Invalid username or password", "danger")
            return render_template("login.html", form=form)

        login_user(user)
        flash("Login successful!", "success")

        role_redirects = {
            "SuperAdmin": "admin.dashboard",
            "HR": "hr.dashboard_hr",
            "OpsCoordinator": "ops_coordinator.dashboard_ops_coordinator",
            "OpsManager": "ops_manager.dashboard_ops",
            "OpsSupervisor": "ops_supervisor.dashboard_ops_supervisor",
            "FleetManager": "fleet.dashboard_fleet",
            "FinanceManager": "finance.dashboard_finance",
        }

        return redirect(url_for(role_redirects.get(user.role, "auth.login")))

    return render_template("login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
