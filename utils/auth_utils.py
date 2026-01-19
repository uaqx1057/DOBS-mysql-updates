from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role not in roles:
                # Redirect to proper dashboard based on role
                if current_user.role == "HR":
                    return redirect(url_for("hr.dashboard_hr"))
                elif current_user.role == "SuperAdmin":   # <- use the correct role name
                    return redirect(url_for("admin.dashboard"))  # <- actual Admin blueprint endpoint
                else:
                    return redirect(url_for("front_page"))  # fallback
            return f(*args, **kwargs)
        return decorated_function
    return decorator

