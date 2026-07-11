from io import BytesIO
import pytest
from werkzeug.datastructures import FileStorage

from services.hr_service import process_hr_approval
from extensions import db
from models import Driver, DriverTypeSettings


def _make_driver(session, suffix="9999"):
    driver = Driver(
        driver_id=f"D{suffix}",
        password="hash",
        name="Test Driver",
        iqaama_number=f"123456{suffix}",
        driver_type_id=1,
    )
    session.add(driver)
    session.commit()
    return driver


def _require_qiwa_for_default_type(session):
    settings = DriverTypeSettings(
        driver_type_id=1,
        contract_mode="single",
        requires_qiwa_contract=True,
    )
    session.merge(settings)
    session.commit()


def _fs(name: str, content: bytes, mimetype: str):
    return FileStorage(stream=BytesIO(content), filename=name, content_type=mimetype)


def test_process_hr_approval_sets_valid_statuses(app):
    with app.app_context():
        _require_qiwa_for_default_type(db.session)
        driver = _make_driver(db.session, "9999")
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
        _require_qiwa_for_default_type(db.session)
        driver = _make_driver(db.session, "9998")
        files = {}
        form = {"qiwa_contract_status": "INVALID", "sponsorship_transfer_status": "Pending"}
        with pytest.raises(ValueError):
            process_hr_approval(driver, files, form, app.config["UPLOAD_FOLDER"], max_bytes=1_000_000)
