import pytest

from app import create_app
from app.postgres.models import User


@pytest.fixture
def app():
    app = create_app({'IMMUDB_DB': 'test'})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def user(app):
    with app.app_context():
        return User.query.first()
