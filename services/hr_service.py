import os
from datetime import datetime
from typing import Dict

from flask_mail import Message

from services.file_storage import is_allowed_file, save_upload, safe_ext_filename, validate_upload
from models import QIWA_CONTRACT_STATUSES, TRANSFER_STATUSES


def process_hr_approval(driver, files: Dict[str, object], form_data: Dict[str, object], upload_folder: str, max_bytes: int):
    """Handle HR approval: save files, update flags and stage."""
    base_name = (driver.name or "driver").replace(" ", "_")
    iqama = driver.iqaama_number or "unknown"
    prefix = f"{base_name}_{iqama}"

    for db_field, file_storage in files.items():
        if file_storage and getattr(file_storage, "filename", None):
            original = file_storage.filename
            validate_upload(file_storage, max_bytes)
            filename = safe_ext_filename(prefix, db_field, original)
            save_upload(file_storage, upload_folder, filename)
            setattr(driver, db_field, filename)

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
    driver.onboarding_stage = "Ops Supervisor"


def save_transfer_proof(driver, file_storage, upload_folder: str, status: str, max_bytes: int):
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
