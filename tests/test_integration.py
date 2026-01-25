from io import BytesIO

from werkzeug.security import generate_password_hash

from extensions import db
from models import Driver, User


def login(client, username, password):
    return client.post("/login", data={"username": username, "password": password}, follow_redirects=False)


def test_auth_protected_redirects(client):
    resp = client.get("/dashboard/", follow_redirects=False)
    assert resp.status_code in (302, 303)
    assert "/login" in resp.headers.get("Location", "")


def test_onboarding_complete_transfer_with_upload(app, client):
    with app.app_context():
        # Seed HR user and driver needing transfer proof
        hr = User(
            username="hr2",
            password=generate_password_hash("pass123"),
            role="HR",
            name="HR Two",
            email="hr2@example.com",
        )
        driver = Driver(
            driver_id="D1234",
            password=generate_password_hash("driverpass"),
            name="Driver One",
            iqaama_number="9911223344",
            qiwa_contract_created=True,
            onboarding_stage="HR Final",
        )
        db.session.add_all([hr, driver])
        db.session.commit()

    # Login as HR
    resp = login(client, "hr2", "pass123")
    assert resp.status_code in (302, 303)

    # Upload transfer proof
    file_data = (BytesIO(b"dummy pdf"), "proof.pdf")
    resp = client.post(
        f"/dashboard/hr/complete_transfer/{driver.id}",
        data={"sponsorship_transfer_status": "Transferred", "sponsorship_transfer_proof": file_data},
        content_type="multipart/form-data",
        follow_redirects=False,
    )
    assert resp.status_code in (302, 303)

    with app.app_context():
        refreshed = Driver.query.get(driver.id)
        assert refreshed.sponsorship_transfer_status == "Transferred"
        assert refreshed.sponsorship_transfer_proof  # filename set
        # File saved under upload folder
        import os

        saved_path = os.path.join(app.config["UPLOAD_FOLDER"], refreshed.sponsorship_transfer_proof)
        assert os.path.exists(saved_path)
