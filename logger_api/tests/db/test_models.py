from app.postgres.models import User


def test_users(app):
    with app.app_context():
        assert User.query.first()
