import os
from datetime import datetime
from typing import Dict

from flask_mail import Message

from services.file_storage import is_allowed_file, save_upload, safe_ext_filename


def process_hr_approval(driver, files: Dict[str, object], form_data: Dict[str, object], upload_folder: str):
    """Handle HR approval: save files, update flags and stage."""
    base_name = (driver.name or "driver").replace(" ", "_")
    iqama = driver.iqaama_number or "unknown"
    prefix = f"{base_name}_{iqama}"

    for db_field, file_storage in files.items():
        if file_storage and getattr(file_storage, "filename", None):
            original = file_storage.filename
            if not is_allowed_file(original):
                raise ValueError(f"Invalid file type for {db_field}. Only JPG, PNG, PDF allowed.")
            filename = safe_ext_filename(prefix, db_field, original)
            save_upload(file_storage, upload_folder, filename)
            setattr(driver, db_field, filename)

    driver.qiwa_contract_created = bool(form_data.get("qiwa_contract_created"))
    driver.company_contract_created = bool(form_data.get("company_contract_created"))
    driver.qiwa_contract_status = form_data.get("qiwa_contract_status", "Pending")
    driver.sponsorship_transfer_status = form_data.get("sponsorship_transfer_status", "Pending")

    driver.hr_approved_at = datetime.utcnow()
    driver.onboarding_stage = "Ops Supervisor"


def save_transfer_proof(driver, file_storage, upload_folder: str, status: str):
    if status != "Transferred":
        raise ValueError("Transfer status must be 'Transferred' when uploading proof.")
    if not file_storage or not getattr(file_storage, "filename", None):
        raise ValueError("Transfer proof file is required.")
    if not is_allowed_file(file_storage.filename):
        raise ValueError("Invalid file type. Only JPG, PNG, and PDF are allowed.")

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
