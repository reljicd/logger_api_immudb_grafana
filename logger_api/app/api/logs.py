from flask import Blueprint, request

from app.auth.api_key_auth import api_key_required
from app.immudb.logs_repo import LogsRepo
from app.immudb.models import Log

bp = Blueprint('logs', __name__, url_prefix='/logs')


@bp.get('/count')
@api_key_required
def count(user):
    return str(LogsRepo.count(user.username))


@bp.get('/tail')
@api_key_required
def tail(user):
    n = request.args.get('n', default=5)

    logs = LogsRepo.select_last_n(user.username, n)
    return [log.log for log in logs]


@bp.get('/all')
@api_key_required
def all_logs(user):
    device = request.args.get('device', default=None)
    app = request.args.get('app', default=None)
    limit = request.args.get('limit', default=5)
    offset = request.args.get('offset', default=0)

    logs = LogsRepo.select_bucket(user=user.username, app=app, device=device,
                                  limit=limit, offset=offset)
    return [log.log for log in logs]


@bp.post('/')
@api_key_required
def insert(user):
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        logs = [Log(user=user.username, app=json['app'],
                    device=json['device'], log=log) for log in json['logs']]
        LogsRepo.insert_batch(logs)
        return json, 201
    else:
        return 'Content-Type not supported!', 406


@bp.get('/verified/<int:log_id>')
@api_key_required
def verified_select_one(user, log_id):
    log, verified = LogsRepo.verified_select_one(log_id)
    return {'log': log.log, 'verified': verified}
