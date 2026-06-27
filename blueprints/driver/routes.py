import os
from datetime import datetime
from pathlib import Path

from datetime import date

from flask import (
    Blueprint, current_app, flash, redirect, render_template,
    request, send_file, url_for,
)
from flask_login import current_user, login_required

from extensions import db
from models import Driver, DriverDocument
from services.file_storage import validate_upload, save_to_shared_storage
from utils.auth import require_roles

driver_bp = Blueprint("driver", __name__, url_prefix="/driver")

ALLOWED_ROLES = {"SuperAdmin", "HR", "FinanceManager", "OpsManager", "OpsSupervisor", "FleetManager"}

DOC_TYPE_LABELS = {
    "iqama":    "Iqama",
    "passport": "Passport",
    "visa":     "Visa",
    "license":  "License",
    "medical":  "Medical",
    "contract": "Contract",
    "mobile":   "Mobile Form",
    "other":    "Other",
}


def _shared_root() -> str:
    return current_app.config.get("DRIVER_DOCUMENT_PATH") or current_app.config["UPLOAD_FOLDER"]


# ---------------------------------------------------------------------------
# Document list + upload form
# ---------------------------------------------------------------------------
@driver_bp.route("/<int:driver_id>/documents")
@login_required
def documents(driver_id):
    if current_user.role not in ALLOWED_ROLES:
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    driver = Driver.query.get_or_404(driver_id)
    docs = (
        DriverDocument.query
        .filter_by(driver_id=driver_id)
        .filter(DriverDocument.deleted_at.is_(None))
        .order_by(DriverDocument.created_at.desc())
        .all()
    )
    can_upload = current_user.role in {"SuperAdmin", "HR", "FinanceManager", "OpsManager"}
    can_delete = current_user.role in {"SuperAdmin", "HR"}
    return render_template(
        "driver/documents.html",
        driver=driver,
        docs=docs,
        doc_type_labels=DOC_TYPE_LABELS,
        can_upload=can_upload,
        can_delete=can_delete,
        today=date.today(),
    )


# ---------------------------------------------------------------------------
# Upload
# ---------------------------------------------------------------------------
@driver_bp.route("/<int:driver_id>/documents/upload", methods=["POST"])
@login_required
def upload_document(driver_id):
    if current_user.role not in {"SuperAdmin", "HR", "FinanceManager", "OpsManager"}:
        flash("Access denied.", "danger")
        return redirect(url_for("driver.documents", driver_id=driver_id))

    driver = Driver.query.get_or_404(driver_id)
    file = request.files.get("document_file")
    doc_type = request.form.get("document_type", "other")
    notes = request.form.get("notes", "").strip() or None
    expires_at_str = request.form.get("expires_at", "").strip()
    expires_at = None
    if expires_at_str:
        try:
            expires_at = datetime.strptime(expires_at_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid expiry date format.", "danger")
            return redirect(url_for("driver.documents", driver_id=driver_id))

    max_bytes = current_app.config.get("MAX_CONTENT_LENGTH", 16 * 1024 * 1024)
    try:
        validate_upload(file, max_bytes)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("driver.documents", driver_id=driver_id))

    try:
        relative_path = save_to_shared_storage(file, driver_id, doc_type, _shared_root())
        file.stream.seek(0, 2)
        doc = DriverDocument(
            driver_id     = driver_id,
            document_type = doc_type,
            file_path     = relative_path,
            original_name = file.filename,
            file_size     = file.stream.tell(),
            uploaded_from = "dobs",
            uploaded_by   = current_user.id,
            notes         = notes,
            expires_at    = expires_at,
        )
        db.session.add(doc)
        db.session.commit()
        flash("Document uploaded successfully.", "success")
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("Document upload failed for driver %s", driver_id)
        flash(f"Upload failed: {e}", "danger")

    return redirect(url_for("driver.documents", driver_id=driver_id))


# ---------------------------------------------------------------------------
# Preview / download
# ---------------------------------------------------------------------------
@driver_bp.route("/documents/<int:doc_id>/preview")
@login_required
def preview_document(doc_id):
    if current_user.role not in ALLOWED_ROLES:
        flash("Access denied.", "danger")
        return redirect(url_for("auth.login"))

    doc = DriverDocument.query.get_or_404(doc_id)
    full_path = Path(_shared_root()) / doc.file_path

    if not full_path.exists():
        flash("File not found on server.", "danger")
        return redirect(url_for("driver.documents", driver_id=doc.driver_id))

    return send_file(
        full_path,
        mimetype=None,
        as_attachment=False,
        download_name=doc.original_name or full_path.name,
    )


# ---------------------------------------------------------------------------
# Soft delete
# ---------------------------------------------------------------------------
@driver_bp.route("/documents/<int:doc_id>/delete", methods=["POST"])
@login_required
@require_roles("SuperAdmin", "HR")
def delete_document(doc_id):
    doc = DriverDocument.query.get_or_404(doc_id)
    driver_id = doc.driver_id
    doc.deleted_at = datetime.utcnow()
    db.session.commit()
    flash("Document removed.", "success")
    return redirect(url_for("driver.documents", driver_id=driver_id))
