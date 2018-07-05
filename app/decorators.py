from functools import wraps

import jwt

from flask import jsonify, request
from configs import secret


def login_required(decorated_function):

    @wraps(decorated_function)
    def wrapper_func(*args, **kwargs):
        token = request.headers.get("token")

        if not token:
            return jsonify({"Error": "Please supply the token in headers"})
        try:
            details = jwt.decode(token, secret, verify=False)
            user_id = details["user_id"]
            return decorated_function(user_id, *args, **kwargs)

        except jwt.InvalidTokenError:
            return {"error": "invalid token"}

    return wrapper_func


