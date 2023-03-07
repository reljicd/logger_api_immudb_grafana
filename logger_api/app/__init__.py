from flask import Flask

from app.immudb.database import init_immudb
from app.postgres.config.env_vars import (POSTGRES_DB, POSTGRES_HOST,
                                          POSTGRES_PASSWORD, POSTGRES_PORT,
                                          POSTGRES_USER)
from app.postgres.database import init_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=(
            f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@'
            f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    init_db(app)
    init_immudb(app)

    from .api import health
    app.register_blueprint(health.bp)
    from .api import logs
    app.register_blueprint(logs.bp)

    return app
