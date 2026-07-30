import os

# This must be forced before importing the application. Using setdefault here
# is unsafe because a shell/service DATABASE_URI can otherwise leak into pytest.
os.environ["DATABASE_URI"] = "sqlite:///:memory:"
os.environ["WTF_CSRF_ENABLED"] = "false"

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from extensions import db
from models import User


@pytest.fixture(scope="session")
def app(tmp_path_factory):
    # Isolate tests to an in-memory DB and disable CSRF for simple client tests
    upload_dir = tmp_path_factory.mktemp("uploads")
    os.environ["UPLOAD_FOLDER"] = str(upload_dir)
    test_app = create_app()
    test_app.config.update(TESTING=True)

    with test_app.app_context():
        if db.engine.url.get_backend_name() != "sqlite":
            raise RuntimeError(
                f"Refusing to run tests against non-SQLite database: {db.engine.url.render_as_string(hide_password=True)}"
            )
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
