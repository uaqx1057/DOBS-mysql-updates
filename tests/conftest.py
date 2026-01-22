import os

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from extensions import db
from models import User


@pytest.fixture(scope="session")
def app():
    # Isolate tests to an in-memory DB and disable CSRF for simple client tests
    os.environ.setdefault("DATABASE_URI", "sqlite:///:memory:")
    os.environ.setdefault("WTF_CSRF_ENABLED", "false")
    test_app = create_app()
    test_app.config.update(TESTING=True)

    with test_app.app_context():
        db.create_all()
    yield test_app

    with test_app.app_context():
        db.drop_all()
        db.session.remove()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def hr_user(app):
    with app.app_context():
        user = User(
            username="hr1",
            password=generate_password_hash("pass123"),
            role="HR",
            name="HR User",
            email="hr@example.com",
        )
        db.session.add(user)
        db.session.commit()
        return user
