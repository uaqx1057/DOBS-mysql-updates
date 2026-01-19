# blueprints/auth/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from models import User  # dob_user model
from extensions import db, login_manager

auth_bp = Blueprint("auth", __name__)

# Load user callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Choose template based on session language
    template = "rtl_login.html" if session.get("lang") == "ar" else "login.html"

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Find user in dob_user table
        user = User.query.filter_by(username=username).first()

        # Verify user exists and password matches
        if not user or not check_password_hash(user.password, password):
            flash("Invalid username or password", "danger")
            return render_template(template)

        # ✅ Log in the user
        login_user(user)
        flash("Login successful!", "success")

        # Redirect based on role
        role_redirects = {
            "SuperAdmin": "admin.dashboard",
            "HR": "hr.dashboard_hr",
            "OpsCoordinator": "ops_coordinator.dashboard_ops_coordinator",
            "OpsManager": "ops_manager.dashboard_ops",
            "OpsSupervisor": "ops_supervisor.dashboard_ops_supervisor",
            "FleetManager": "fleet.dashboard_fleet",
            "FinanceManager": "finance.dashboard_finance"
        }

        return redirect(url_for(role_redirects.get(user.role, "auth.login")))

    return render_template(template)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
