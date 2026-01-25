import os
import subprocess
from pathlib import Path
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}


def is_allowed_file(filename: str, allowed_ext=ALLOWED_EXTENSIONS) -> bool:
    ext = Path(filename).suffix.lower()
    return ext in allowed_ext


def save_upload(file_storage, dest_dir: str, filename: str) -> str:
    """Save an uploaded file to dest_dir ensuring the directory exists."""
    Path(dest_dir).mkdir(parents=True, exist_ok=True)
    safe_name = secure_filename(filename)
    target = Path(dest_dir) / safe_name
    file_storage.save(target)
    # Optional AV scan using external command (e.g., clamdscan)
    if os.getenv("AV_SCAN_ENABLED", "false").lower() == "true":
        cmd = os.getenv("AV_SCAN_COMMAND")
        if not cmd:
            raise ValueError("AV scan enabled but AV_SCAN_COMMAND is not set")
        proc = subprocess.run(f"{cmd} {target}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            target.unlink(missing_ok=True)
            raise ValueError("Upload failed AV scan")
    return safe_name


def safe_ext_filename(base: str, field: str, original_name: str) -> str:
    ext = Path(original_name).suffix.lower()
    return f"{base}_{field}{ext}"


def validate_upload(file_storage, max_bytes: int, allowed_ext=ALLOWED_EXTENSIONS, allowed_mime_prefixes=("image/", "application/pdf")):
    """Validate extension, MIME type, and size for an uploaded file."""
    if not file_storage or not getattr(file_storage, "filename", None):
        raise ValueError("File is required.")

    filename = file_storage.filename
    if not is_allowed_file(filename, allowed_ext):
        raise ValueError("Invalid file type. Only JPG, PNG, and PDF are allowed.")

    content_type = (getattr(file_storage, "mimetype", "") or "").lower()
    if not any(content_type.startswith(prefix) for prefix in allowed_mime_prefixes):
        raise ValueError("Invalid file content. Only images or PDF are accepted.")

    file_storage.stream.seek(0, os.SEEK_END)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)
    if size > max_bytes:
        raise ValueError(f"File too large. Maximum {max_bytes // (1024 * 1024)} MB.")
