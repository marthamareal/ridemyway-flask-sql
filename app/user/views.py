import json
import logging

from flask import Blueprint, jsonify, request, make_response
from app.decorators import login_required
from app.validators import ValidateUserEntries
from .model import User

blue_print_user = Blueprint('blue_print_user', __name__)


@blue_print_user.route('/auth/signup', methods=['POST'])
def signup():
    try:
        args = json.loads(request.data.decode())

        if not args.get("first name"):
            return make_response(jsonify({"message": "Field 'first name' is required"}), 400)
        if not args.get("last name"):
            return make_response(jsonify({"message": "Field 'last name' is required"}), 400)
        if not args.get("email"):
            return make_response(jsonify({"message": "Field 'email' is required"}), 400)
        if not args.get("city"):
            return make_response(jsonify({"message": "Field 'city' is required"}), 400)
        if not args.get("phone_no"):
            return make_response(jsonify({"message": "Field 'phone_no' is required"}), 400)
        if not args.get("password"):
            return make_response(jsonify({"message": "Field 'password' is required"}), 400)

        first_name = args.get("first name")
        last_name = args.get("last name")
        email = args.get("email")
        city = args.get("city")
        phone_no = args.get("phone_no")
        password = args.get("password")

        validate_flag = ValidateUserEntries.signup(
            first_name, last_name, email, city, phone_no, password)
        print(validate_flag)
        if validate_flag == "pass":

            user = User(first_name, last_name, email, city, phone_no, password)
            created_user = User.create_user(user)
            print(created_user)
            if created_user.get("code"):
                return make_response(jsonify({"user": created_user}), 400)
            else:
                return make_response(jsonify({"user": created_user}), 201)
        else:
            return make_response(jsonify(validate_flag), 400)

    except Exception as e:
        logging.error("Something wrong happened: ", e)
        return make_response(jsonify({"Message": "Some thing went wrong on the server"}), 500)


@blue_print_user.route('/auth/login', methods=['POST'])
def login():
    try:
        args = json.loads(request.data.decode())

        if not args.get("email"):
            return make_response(jsonify({"message": "Field 'email' is required"}), 400)
        if not args.get("password"):
            return make_response(jsonify({"message": "Field 'password' is required"}), 400)

        email = args.get("email")
        password = args.get("password")

        validate_flag = ValidateUserEntries.login(email, password)

        if validate_flag == "pass":
            _login = User.login_user(email, password)

            if _login.get("code"):
                return make_response(jsonify({"error": _login}), 400)
            else:
                return make_response(jsonify({"user": _login}), 201)
        else:

            return make_response(jsonify(validate_flag), 400)
    except Exception as e:
        logging.error(e)
        return make_response("Some thing went wrong on the server", 500)


@blue_print_user.route('/auth/logout', methods=['POST'])
@login_required
def logout(user_id):
    try:
        results = User.logout(user_id)
        return make_response(jsonify(results), 200)
    except Exception as e:
        print(e)
        return make_response("Some thing went wrong on the server", 500)
