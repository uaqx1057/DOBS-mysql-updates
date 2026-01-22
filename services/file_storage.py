import os
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
    return safe_name


def safe_ext_filename(base: str, field: str, original_name: str) -> str:
    ext = Path(original_name).suffix.lower()
    return f"{base}_{field}{ext}"
