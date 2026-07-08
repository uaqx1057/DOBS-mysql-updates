import os
from datetime import datetime
from typing import Dict

from flask import current_app
from flask_mail import Message

from services.file_storage import is_allowed_file, save_upload, safe_ext_filename, validate_upload, save_to_shared_storage
from services import onboarding_workflow
from models import QIWA_CONTRACT_STATUSES, TRANSFER_STATUSES

# Maps Driver column names used in HR approval -> shared document_type
_HR_FIELD_TO_DOC_TYPE = {
    "company_contract_file": "contract",
    "promissory_note_file":  "other",
    "qiwa_contract_file":    "contract",
}


def _insert_driver_document(db, driver, document_type: str, file_storage, relative_path: str, uploaded_by_id=None):
    from models import DriverDocument
    file_storage.stream.seek(0, 2)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)
    doc = DriverDocument(
        driver_id     = driver.id,
        document_type = document_type,
        file_path     = relative_path,
        original_name = file_storage.filename,
        file_size     = size,
        uploaded_from = "dobs",
        uploaded_by   = uploaded_by_id,
    )
    db.session.add(doc)


def process_hr_approval(driver, files: Dict[str, object], form_data: Dict[str, object], upload_folder: str, max_bytes: int, db=None, uploaded_by_id=None):
    """Handle HR approval: save files to legacy location and dual-write to shared storage."""
    base_name = (driver.name or "driver").replace(" ", "_")
    iqama = driver.iqaama_number or "unknown"
    prefix = f"{base_name}_{iqama}"

    shared_root = current_app.config.get("DRIVER_DOCUMENT_PATH", upload_folder)

    for db_field, file_storage in files.items():
        if file_storage and getattr(file_storage, "filename", None):
            original = file_storage.filename
            validate_upload(file_storage, max_bytes)
            filename = safe_ext_filename(prefix, db_field, original)
            save_upload(file_storage, upload_folder, filename)
            setattr(driver, db_field, filename)

            if db is not None and driver.id:
                doc_type = _HR_FIELD_TO_DOC_TYPE.get(db_field, "other")
                try:
                    relative_path = save_to_shared_storage(file_storage, driver.id, doc_type, shared_root)
                    _insert_driver_document(db, driver, doc_type, file_storage, relative_path, uploaded_by_id)
                except Exception:
                    current_app.logger.exception("Shared storage dual-write failed for field %s", db_field)

    driver.qiwa_contract_created = bool(form_data.get("qiwa_contract_created"))
    driver.company_contract_created = bool(form_data.get("company_contract_created"))

    qiwa_status = form_data.get("qiwa_contract_status", "Pending") or "Pending"
    transfer_status = form_data.get("sponsorship_transfer_status", "Pending") or "Pending"
    if qiwa_status not in QIWA_CONTRACT_STATUSES:
        raise ValueError("Invalid qiwa_contract_status")
    if transfer_status not in TRANSFER_STATUSES:
        raise ValueError("Invalid sponsorship_transfer_status")

    driver.qiwa_contract_status = qiwa_status
    driver.sponsorship_transfer_status = transfer_status

    driver.hr_approved_at = datetime.utcnow()
    onboarding_workflow.advance(driver, from_stage="HR")

    # Generic promissory note - not business-specific, so it can be
    # generated now even though platform/business assignment hasn't
    # happened yet (that's Ops Supervisor's job, still ahead in the
    # sequence). The business-specific Driver Contract is generated later,
    # at HR Final, once the business assignment is known.
    if db is not None and driver.id:
        try:
            from services import contracts
            contracts.generate_promissory_note(driver, uploaded_by_id=uploaded_by_id)
        except Exception:
            current_app.logger.exception("Promissory note generation failed for driver_id=%s", driver.id)


def save_transfer_proof(driver, file_storage, upload_folder: str, status: str, max_bytes: int, db=None, uploaded_by_id=None):
    if status != "Transferred":
        raise ValueError("Transfer status must be 'Transferred' when uploading proof.")
    validate_upload(file_storage, max_bytes)

    base_name = (driver.name or "driver").replace(" ", "_")
    iqama = driver.iqaama_number or "unknown"
    filename = safe_ext_filename(base_name, "transfer_proof", file_storage.filename)
    save_upload(file_storage, upload_folder, filename)

    driver.sponsorship_transfer_status = status
    driver.sponsorship_transfer_proof = filename
    driver.sponsorship_transfer_completed_at = datetime.utcnow()

    if db is not None and driver.id:
        shared_root = current_app.config.get("DRIVER_DOCUMENT_PATH", upload_folder)
        try:
            relative_path = save_to_shared_storage(file_storage, driver.id, "other", shared_root)
            _insert_driver_document(db, driver, "other", file_storage, relative_path, uploaded_by_id)
        except Exception:
            current_app.logger.exception("Shared storage dual-write failed for transfer_proof")


def send_rejection_email(mail, recipients, driver_name, driver_iqaama, nationality, reason, rejected_by):
    if not recipients:
        return
    msg = Message(
        subject=f"Driver Rejected by HR | تم رفض السائق: {driver_name}",
        recipients=recipients,
    )
    msg.html = f"""
    <html><body style='font-family: Arial, sans-serif;'>
    <div style='max-width:600px;margin:auto;padding:20px;background:#fff;'>
      <h2 style='color:#713183;'>Driver Rejection Notification</h2>
      <p>Driver <strong>{driver_name}</strong> (iqaama: <strong>{driver_iqaama or 'N/A'}</strong>, Nationality: <strong>{nationality}</strong>) was rejected by HR.</p>
      <p><strong>Reason:</strong><br>{reason}</p>
      <p>Rejected by: {rejected_by}</p>
      <hr>
      <h3 dir='rtl' style='text-align:right;color:#713183;'>إشعار رفض السائق</h3>
      <p dir='rtl' style='text-align:right;'>تم رفض السائق <strong>{driver_name}</strong> (رقم الإقامة: <strong>{driver_iqaama or 'N/A'}</strong>) من قبل الموارد البشرية.</p>
      <p dir='rtl' style='text-align:right;'><strong>سبب الرفض:</strong><br>{reason}</p>
    </div></body></html>
    """
    mail.send(msg)
