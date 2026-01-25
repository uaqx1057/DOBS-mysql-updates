from io import BytesIO
import pytest
from werkzeug.datastructures import FileStorage

from services.hr_service import process_hr_approval
from extensions import db
from models import Driver


def _make_driver(session):
    driver = Driver(
        driver_id="D9999",
        password="hash",
        name="Test Driver",
        iqaama_number="1234567890",
    )
    session.add(driver)
    session.commit()
    return driver


def _fs(name: str, content: bytes, mimetype: str):
    return FileStorage(stream=BytesIO(content), filename=name, content_type=mimetype)


def test_process_hr_approval_sets_valid_statuses(app):
    with app.app_context():
        driver = _make_driver(db.session)
        files = {
            "company_contract_file": _fs("company.pdf", b"pdf", "application/pdf"),
        }
        form = {
            "qiwa_contract_created": True,
            "company_contract_created": True,
            "qiwa_contract_status": "Created",
            "sponsorship_transfer_status": "Pending",
        }
        process_hr_approval(driver, files, form, app.config["UPLOAD_FOLDER"], max_bytes=1_000_000)
        assert driver.qiwa_contract_status == "Created"
        assert driver.sponsorship_transfer_status == "Pending"
        assert driver.onboarding_stage == "Ops Supervisor"


def test_process_hr_approval_rejects_bad_status(app):
    with app.app_context():
        driver = _make_driver(db.session)
        files = {}
        form = {"qiwa_contract_status": "INVALID", "sponsorship_transfer_status": "Pending"}
        with pytest.raises(ValueError):
            process_hr_approval(driver, files, form, app.config["UPLOAD_FOLDER"], max_bytes=1_000_000)
