from app.postgres.database import db


def test_session(app):
    with app.app_context():
        assert db.session.is_active


def test_metadata(app):
    with app.app_context():
        assert 'users' in db.metadata.tables
        assert 'null' not in db.metadata.tables
