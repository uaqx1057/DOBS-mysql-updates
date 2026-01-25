from io import BytesIO
import os
import pytest
from werkzeug.datastructures import FileStorage

from services.file_storage import validate_upload, save_upload


def _make_filestorage(name: str, content: bytes, mimetype: str) -> FileStorage:
    stream = BytesIO(content)
    return FileStorage(stream=stream, filename=name, content_type=mimetype)


def test_validate_upload_accepts_allowed_types(tmp_path):
    data = b"x" * 1024
    fs = _make_filestorage("test.jpg", data, "image/jpeg")
    validate_upload(fs, max_bytes=2048)


def test_validate_upload_rejects_bad_extension(tmp_path):
    fs = _make_filestorage("malware.exe", b"boom", "application/octet-stream")
    with pytest.raises(ValueError):
        validate_upload(fs, max_bytes=1024)


def test_validate_upload_rejects_oversize(tmp_path):
    fs = _make_filestorage("big.pdf", b"x" * 4096, "application/pdf")
    with pytest.raises(ValueError):
        validate_upload(fs, max_bytes=1024)


def test_save_upload_writes_file(tmp_path, monkeypatch):
    fs = _make_filestorage("doc.pdf", b"content", "application/pdf")
    monkeypatch.setenv("AV_SCAN_ENABLED", "false")
    saved_name = save_upload(fs, str(tmp_path), "saved.pdf")
    saved_path = tmp_path / saved_name
    assert saved_path.exists()
    assert saved_path.read_bytes() == b"content"
