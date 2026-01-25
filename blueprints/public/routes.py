import os
import re
from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash, session, send_from_directory, make_response
from extensions import db, mail, limiter
from models import Driver, User
from utils.validation import parse_date
from flask_mail import Message
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from forms.common import PublicRegisterForm

public_bp = Blueprint("public", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}
ENGLISH_PATTERN = re.compile(r'^[A-Za-z0-9\s]+$')  # Letters, numbers, spaces

ALLOWED_EXT = {'.jpg', '.jpeg', '.png', '.pdf'}


def _upload_root() -> str:
    path = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(path, exist_ok=True)
    return path

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_english(value, field_name):
    """Check if input contains only English letters/numbers."""
    if not value or not ENGLISH_PATTERN.match(value):
        flash(f"❌ {field_name} must contain only English letters and numbers.", "danger")
        return False
    return True


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
# Serve static HTML pages
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
# Driver registration
# ------------------------
@public_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def register():
    form = PublicRegisterForm()

    if form.validate_on_submit():
        name = form.name.data
        iqaama_number = form.iqaama_number.data
        absher_number = form.absher_number.data

        if not validate_english(name, "Name") or not validate_english(iqaama_number, "Iqama Number") or not validate_english(absher_number, "Absher Number"):
            return redirect(url_for("public.register"))

        iqaama_expiry = parse_date(form.iqaama_expiry_date.data)
        saudi_driving_license = form.saudi_driving_license.data == "yes"
        nationality = form.nationality.data
        city = form.city.data
        previous_sponsor_number = form.previous_sponsor_number.data
        iqama_card_upload = form.iqama_card_upload.data

        # File validation (size + MIME)
        if not iqama_card_upload or not iqama_card_upload.filename:
            flash("❌ Iqama card upload is required.", "danger")
            return redirect(url_for("public.register"))

        content_type = (iqama_card_upload.mimetype or "").lower()
        if not (content_type.startswith("image/") or content_type == "application/pdf"):
            flash("❌ Invalid file content. Only images or PDF are accepted.", "danger")
            return redirect(url_for("public.register"))

        max_len = current_app.config.get("MAX_CONTENT_LENGTH", 16 * 1024 * 1024)
        iqama_card_upload.stream.seek(0, os.SEEK_END)
        file_size = iqama_card_upload.stream.tell()
        iqama_card_upload.stream.seek(0)
        if file_size > max_len:
            flash("❌ File too large. Maximum 16 MB.", "danger")
            return redirect(url_for("public.register"))

        upload_folder = _upload_root()
        safe_name = f"{name.replace(' ', '_').lower()}_{iqaama_number}"
        ext = iqama_card_upload.filename.rsplit(".", 1)[1].lower()
        file_name = secure_filename(f"{safe_name}.{ext}")
        iqama_card_upload.save(os.path.join(upload_folder, file_name))

        new_driver = Driver(
            name=name,
            iqaama_number=iqaama_number,
            iqaama_expiry=iqaama_expiry,
            saudi_driving_license=saudi_driving_license,
            nationality=nationality,
            city=city,
            absher_number=absher_number,
            previous_sponsor_number=previous_sponsor_number,
            iqama_card_upload=file_name,
            onboarding_stage="Ops Manager",
            driver_type_id=1,
        )

        db.session.add(new_driver)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if "drivers_iqaama_number_key" in str(e.orig):
                flash("❌ This IQAMA number already exists.", "danger")
            else:
                flash("⚠️ Unexpected error occurred. Try again.", "danger")
            return redirect(url_for("public.register"))

        try:
            recipients = [u.email for u in User.query.filter(User.role.in_(["OpsManager"])).all() if u.email]
            if recipients:
                msg = Message(
                    subject="New Driver Registration Submitted | تسجيل سائق جديد",
                    recipients=recipients
                )

                msg.html = f"""
                <html>
                <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">

                        <!-- English LTR -->
                        <div style="text-align: left;">
                            <h2 style="color: #713183;">Driver Onboarding System</h2>
                            <p>Dear Team,</p>
                            <p>A new driver has submitted a registration form. Please review:</p>
                            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>Driver Name</strong></td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{name}</td>
                                </tr>
                            </table>
                            <p><a href="https://dobs.dobs.cloud/login">Login to the system</a></p>
                        </div>

                        <hr style="margin: 30px 0;">

                        <!-- Arabic RTL -->
                        <div dir="rtl" lang="ar" style="text-align: right; font-family: Tahoma, sans-serif;">
                            <h2 style="color: #713183;">نظام إدارة السائقين</h2>
                            <p>الفريق المحترم،</p>
                            <p>لقد قام السائق بتقديم نموذج تسجيل جديد. يرجى مراجعة التفاصيل:</p>
                            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                                <tr>
                                    <td style="padding: 8px; border: 1px solid #ddd;">اسم السائق</td>
                                    <td style="padding: 8px; border: 1px solid #ddd;">{name}</td>
                                </tr>
                            </table>
                            <p><a href="https://dobs.dobs.cloud/login">تسجيل الدخول إلى النظام</a></p>
                        </div>

                    </div>
                </body>
                </html>
                """

                mail.send(msg)

        except Exception as e:
            current_app.logger.exception("Public registration email failed")

        flash("✅ Driver data received successfully!", "success")
        return redirect(url_for("public.register"))

    if request.method == "POST":
        flash("Please fix the highlighted errors and try again.", "danger")

    template = "rtl_register.html" if session.get("lang") == "ar" else "register.html"
    return render_template(template, form=form)


# ------------------------
# Language switch
# ------------------------
@public_bp.route("/set_language/<lang>")
def set_language(lang):
    if lang in ["en", "ar"]:
        session["lang"] = lang
    next_page = request.referrer or url_for("public.index")
    return redirect(next_page)
