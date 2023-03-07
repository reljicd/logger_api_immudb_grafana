import uuid

from app.immudb.logs_repo import LogsRepo
from app.immudb.models import Log


def dummy_log(user: str, app: str = 'test_app') -> Log:
    return Log(user=user, device='test_device',
               app=app, log=str(uuid.uuid4()))


def test_count(app, client, user):
    with app.app_context():
        LogsRepo.insert_batch([dummy_log(user.username) for _ in range(5)])
        count = LogsRepo.count(user.username)

    expected_message = str(count)
    expected_status_code = 200

    response = client.get('/logs/count',
                          headers={'api-key': user.api_key})

    assert response.status_code == expected_status_code
    assert response.text == expected_message


def test_tail(app, client, user):
    num_of_logs = 2
    logs_to_insert = [dummy_log(user.username) for _ in range(num_of_logs)]

    with app.app_context():
        LogsRepo.insert_batch(logs_to_insert)

    expected_status_code = 200

    response = client.get(f'/logs/tail?n={num_of_logs}',
                          headers={'api-key': user.api_key})
    response_json = response.json

    assert response.status_code == expected_status_code
    for log in logs_to_insert:
        assert log.log in response_json


def test_all_limit(app, client, user):
    num_of_logs = 10
    logs_to_insert = [dummy_log(user.username) for _ in range(num_of_logs)]

    with app.app_context():
        LogsRepo.insert_batch(logs_to_insert)

    expected_status_code = 200
    limit = 7

    response = client.get(f'/logs/all?limit={limit}',
                          headers={'api-key': user.api_key})
    response_json = response.json

    assert response.status_code == expected_status_code
    assert len(response_json) == limit


def test_all_bucket(app, client, user):
    num_of_logs = 2
    _app = str(uuid.uuid4())
    logs_to_insert = [dummy_log(user.username, _app)
                      for _ in range(num_of_logs)]

    with app.app_context():
        LogsRepo.insert_batch(logs_to_insert)

    expected_status_code = 200

    response = client.get(f'/logs/all?app={_app}',
                          headers={'api-key': user.api_key})
    response_json = response.json

    assert len(response_json) == num_of_logs
    assert response.status_code == expected_status_code
    for log in logs_to_insert:
        assert log.log in response_json


def test_insert(app, client, user):
    _app = str(uuid.uuid4())
    _device = str(uuid.uuid4())
    logs = [str(uuid.uuid4()) for _ in range(3)]

    expected_status_code = 201

    response = client.post(f'/logs/',
                           content_type="application/json",
                           headers={'api-key': user.api_key},
                           json={'app': _app,
                                 'device': _device,
                                 'logs': logs})

    with app.app_context():
        inserted_logs = LogsRepo.select_bucket(user=user.username, app=_app,
                                               device=_device)

    assert response.status_code == expected_status_code
    for inserted_log in inserted_logs:
        assert inserted_log.log in logs
