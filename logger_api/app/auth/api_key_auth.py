import functools

from flask import request

from app.postgres.models import User


def api_key_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if request.headers.get('api-key'):
            api_key = request.headers.get('api-key')
        else:
            return {"message": "Please provide an API key"}, 400

        # Check if API key is correct and valid
        user = User.find_by_api_key(api_key)
        if user:
            return func(user, *args, **kwargs)
        else:
            return {"message": "The provided API key is not valid"}, 403

    return decorator
