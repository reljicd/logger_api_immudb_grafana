from app.immudb.database import immu_db
from app.immudb.logs_repo import LogsRepo
from app.immudb.models import Log

TEST_USER = 'test_user'
TEST_DEVICE_1 = 'test_device_1'
TEST_APP_1 = 'test_app_1'
TEST_LOG_1 = 'test_1'
TEST_LOG_2 = 'test_2'


def test_insert_one(app):
    with app.app_context():
        log = Log(user=TEST_USER, device=TEST_DEVICE_1,
                  app=TEST_APP_1, log=TEST_LOG_1)
        assert LogsRepo.insert_one(log)


def test_batch(app):
    with app.app_context():
        log_1 = Log(user=TEST_USER, device=TEST_DEVICE_1,
                    app=TEST_APP_1, log=TEST_LOG_1)
        log_2 = Log(user=TEST_USER, device=TEST_DEVICE_1,
                    app=TEST_APP_1, log=TEST_LOG_2)
        assert LogsRepo.insert_batch([log_1, log_2])


def test_count(app):
    with app.app_context():
        insert_sql = (
            f"INSERT INTO logs (user, device, app, log) "
            f"VALUES ('{TEST_USER}', '{TEST_DEVICE_1}', "
            f"'{TEST_APP_1}', '{TEST_LOG_1}');")
        immu_db.sqlExec(insert_sql)

        assert LogsRepo.count() > 0
