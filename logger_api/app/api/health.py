from flask import Blueprint

from app.auth.api_key_auth import api_key_required

bp = Blueprint('health', __name__, url_prefix='/health')


@bp.route('/')
def health_check():
    return 'OK'


@bp.route('/auth')
@api_key_required
def health_check_with_auth(user):
    return f'OK {user.username}'
