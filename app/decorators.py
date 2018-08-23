import logging
from functools import wraps

import jwt

from flask import jsonify, request, make_response
from configs import secret


def login_required(decorated_function):

    @wraps(decorated_function)
    def wrapper_func(*args, **kwargs):
        token = request.headers.get("token")
        if not token:
            return make_response(jsonify({"message": "Please supply the token in headers"}), 400)
        try:
            details = jwt.decode(token, secret, verify=False)
        except Exception as e:
            logging.error(e)
            return make_response(jsonify({"message": "Invalid Token, Fill in a valid token"}), 400)
        return decorated_function(details["user_id"], *args, **kwargs)

    return wrapper_func
