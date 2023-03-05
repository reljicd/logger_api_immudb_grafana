from app.postgres.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String, unique=True)
    api_key = db.Column(db.String, unique=True)
