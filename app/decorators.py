from functools import wraps

import jwt

from flask import jsonify, request
from configs import secret


def login_required(decorated_function):

    @wraps(decorated_function)
    def wrapper_func(*args, **kwargs):
        token = request.headers.get("token")
        user_id = request.headers.get("user_id")
        if not token:
            return jsonify({"Error": "Please supply the token in headers"})

        details = jwt.decode(token, secret, algorithms='HS256', verify=False)

        return decorated_function(details.get(user_id, token,  *args, **kwargs))

    return wrapper_func


