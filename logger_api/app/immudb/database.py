from immudb import ImmudbClient
from immudb.datatypesv2 import DatabaseSettingsV2

from app.immudb.config.env_vars import (IMMUDB_DB, IMMUDB_HOST, IMMUDB_PASSWORD,
                                        IMMUDB_PORT, IMMUDB_USER)

immu_db = ImmudbClient(immudUrl=f'{IMMUDB_HOST}:{IMMUDB_PORT}')

CREATE_LOGS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS logs (
    id          INTEGER AUTO_INCREMENT,
    user        VARCHAR NOT NULL,
    device      VARCHAR NOT NULL,
    app         VARCHAR NOT NULL,
    log         VARCHAR NOT NULL,
    PRIMARY KEY (id)
);
"""


def init_immudb(app):
    db = app.config.get('IMMUDB_DB', IMMUDB_DB)

    immu_db.login(IMMUDB_USER, IMMUDB_PASSWORD)

    immu_db.createDatabaseV2(db, settings=DatabaseSettingsV2(),
                             ifNotExists=True)
    immu_db.useDatabase(db.encode('utf8'))

    immu_db.sqlExec(CREATE_LOGS_TABLE_SQL)
