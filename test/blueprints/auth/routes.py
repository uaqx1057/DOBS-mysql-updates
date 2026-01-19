import os
import crypt
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from models import User
from extensions import db, login_manager

auth_bp = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    template = "rtl_login.html" if session.get("lang") == "ar" else "login.html"

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Find user
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Invalid username or password", "danger")
            return render_template(template)

        # Verify password
        password_matches = False
        if user.password.startswith(("pbkdf2:", "sha256:")):
            password_matches = check_password_hash(user.password, password)
        elif user.password.startswith(("scrypt:", "$")):
            password_matches = (user.password == crypt.crypt(password, user.password))

        if not password_matches:
            flash("Invalid username or password", "danger")
            return render_template(template)

        # ✅ Upgrade legacy password if matched
        if not user.password.startswith(("pbkdf2:", "sha256:")):
            user.password = generate_password_hash(password)
            db.session.commit()

        # ✅ Log in user
        login_user(user)
        flash("Login successful!", "success")

        # Redirect by role
        role_redirects = {
            "SuperAdmin": "admin.dashboard",
            "HR": "hr.dashboard_hr",
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
