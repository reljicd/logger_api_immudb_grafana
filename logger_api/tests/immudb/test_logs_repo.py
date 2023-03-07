import uuid

from app.immudb.logs_repo import LogsRepo
from app.immudb.models import Log

TEST_USER = 'test_user'


def dummy_log(app: str = 'test_app') -> Log:
    return Log(user=TEST_USER, device='test_device',
               app=app, log=str(uuid.uuid4()))


def test_insert_one(app):
    with app.app_context():
        assert LogsRepo.insert_one(dummy_log())


def test_batch(app):
    with app.app_context():
        assert LogsRepo.insert_batch([dummy_log(), dummy_log()])


def test_count(app):
    with app.app_context():
        inserted_pk = LogsRepo.insert_one(dummy_log())
        assert LogsRepo.count() == inserted_pk


def test_select_one(app):
    with app.app_context():
        log_to_insert = dummy_log()
        inserted_pk = LogsRepo.insert_one(log_to_insert)
        assert LogsRepo.select_one(inserted_pk) == log_to_insert


def test_select_all(app):
    with app.app_context():
        num_of_logs = 5
        LogsRepo.insert_batch([dummy_log() for _ in range(num_of_logs)])

        returned_logs = LogsRepo.select_all(limit=num_of_logs)
        assert len(returned_logs) == num_of_logs


def test_select_last_n(app):
    with app.app_context():
        num_of_logs = 2
        logs_to_insert = [dummy_log() for _ in range(num_of_logs)]
        LogsRepo.insert_batch(logs_to_insert)

        returned_logs = LogsRepo.select_last_n(num_of_logs)
        for returned_log in returned_logs:
            assert returned_log in logs_to_insert


def test_select_bucket(app):
    with app.app_context():
        num_of_logs = 2
        app = str(uuid.uuid4())
        logs_to_insert = [dummy_log(app) for _ in range(num_of_logs)]
        LogsRepo.insert_batch(logs_to_insert)

        returned_logs = LogsRepo.select_bucket(user=TEST_USER, app=app)
        for returned_log in returned_logs:
            assert returned_log in logs_to_insert


def test_verified_select_one(app):
    with app.app_context():
        log_to_insert = dummy_log()
        inserted_pk = LogsRepo.insert_one(log_to_insert)
        assert LogsRepo.verified_select_one(inserted_pk) == (log_to_insert,
                                                             True)
