import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_from_directory, make_response
from extensions import db, mail
from models import Driver
from flask_mail import Message
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from models import User  # make sure User is imported for email recipients

public_bp = Blueprint("public", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ------------------------
# Landing / Front page
# ------------------------
@public_bp.route("/")
def index():
    lang = session.get("lang", "en")
    filename = "rtl_index.html" if lang == "ar" else "index.html"
    if not os.path.exists(filename):
        return "Front page not found", 404
    resp = make_response(send_from_directory('.', filename))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return resp

# ------------------------
# Serve any other static HTML pages (RTL support)
# ------------------------
@public_bp.route("/<page_name>.html")
def serve_page(page_name):
    lang = session.get("lang", "en")
    filename = f"rtl_{page_name}.html" if lang == "ar" else f"{page_name}.html"
    if not os.path.exists(filename):
        return "Page not found", 404
    resp = make_response(send_from_directory('.', filename))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return resp

# ------------------------
# Driver registration (dynamic page)
# ------------------------


@public_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"]
        iqama_number = request.form["iqama_number"]
        iqama_expiry_date = request.form["iqama_expiry_date"]
        saudi_driving_license = request.form["saudi_driving_license"] == "yes"
        nationality = request.form["nationality"]
        city = request.form.get("city")
        mobile_number = request.form["mobile_number"]
        previous_sponsor_number = request.form["previous_sponsor_number"]
        iqama_card_upload = request.files.get("iqama_card_upload")

        file_name = None
        if iqama_card_upload and allowed_file(iqama_card_upload.filename):
            upload_folder = "static/uploads/"
            os.makedirs(upload_folder, exist_ok=True)
            safe_name = f"{full_name.replace(' ', '_').lower()}_{iqama_number.replace(' ', '_')}"
            ext = iqama_card_upload.filename.rsplit(".", 1)[1].lower()
            file_name = secure_filename(f"{safe_name}.{ext}")
            iqama_card_upload.save(os.path.join(upload_folder, file_name))

        new_driver = Driver(
            full_name=full_name,
            iqama_number=iqama_number,
            iqama_expiry_date=iqama_expiry_date,
            saudi_driving_license=saudi_driving_license,
            nationality=nationality,
            city=city,
            mobile_number=mobile_number,
            previous_sponsor_number=previous_sponsor_number,
            iqama_card_upload=file_name,
            onboarding_stage="Ops Manager"
        )

        db.session.add(new_driver)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if "driver_iqama_number_key" in str(e.orig):
                flash("❌ This IQAMA number already exists in the system.", "danger")
            else:
                flash("⚠️ An unexpected error occurred. Please try again.", "danger")
            return redirect(url_for("public.register"))

        # Send email notification
        try:
            recipients = [u.email for u in User.query.filter(User.role.in_(["SuperAdmin", "OpsManager"])).all()]
            if recipients:
                msg = Message(
                    "New Driver Registration Submitted",
                    recipients=recipients,
                    body=f"Driver {full_name} has submitted a new registration form. Please review the details."
                )
                mail.send(msg)
        except Exception as e:
            print(f"Error sending email: {e}")

        flash("✅ Driver data received successfully!", "success")
        return redirect(url_for("public.register"))

    # Render RTL or English template automatically
    template = "rtl_register.html" if session.get("lang") == "ar" else "register.html"
    return render_template(template)
# ------------------------
# Language switch route
# ------------------------
@public_bp.route("/set_language/<lang>")
def set_language(lang):
    if lang in ["en", "ar"]:
        session["lang"] = lang
    # Redirect back to the page the user came from
    next_page = request.referrer
    if not next_page:
        next_page = url_for("public.index")
    return redirect(next_page)
