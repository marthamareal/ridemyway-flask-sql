import json
import logging

from . import check_form_fields, missing_form_fields
from flask import Blueprint, jsonify, request, make_response
from app.decorators import login_required
from app.validators import ValidateUserEntries, form_errors
from .model import User

blue_print_user = Blueprint('blue_print_user', __name__)


@blue_print_user.route('/auth/signup', methods=['POST'])
def signup():
    try:
        args = json.loads(request.data.decode())
        check_form_fields(args, "first name")
        check_form_fields(args, "last name")
        check_form_fields(args, "email")
        check_form_fields(args, "city")
        check_form_fields(args, "phone_no")
        check_form_fields(args, "password")

        if missing_form_fields:
            message = "Fields %s are required" % missing_form_fields
            missing_form_fields.clear()
            return make_response(jsonify({"message": message}), 400)
        else:
            first_name = args.get("first name")
            last_name = args.get("last name")
            email = args.get("email")
            city = args.get("city")
            phone_no = args.get("phone_no")
            password = args.get("password")

            validate_flag = ValidateUserEntries.signup(
                first_name, last_name, email, city, phone_no, password)
            if validate_flag == "pass":

                user = User(first_name, last_name, email, city, phone_no, password)
                created_user = User.create_user(user)
                if created_user.get("code"):
                    return make_response(jsonify({"message": created_user.get("message")}), 400)
                else:
                    return make_response(jsonify({"message": created_user}), 201)
            else:
                message = "Your form has the following errors %s fix them before you submit" % form_errors
                form_errors.clear()
                return make_response(jsonify({"message": message}), 400)

    except Exception as e:
        logging.error("Something wrong happened: ", e)
        return make_response(jsonify({"message": "Some thing went wrong on the server"}), 500)


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
                return make_response(jsonify({"message": _login}), 401)
            else:
                return make_response(jsonify({"message": _login}), 201)
        else:
            print(validate_flag)
            return make_response(jsonify(validate_flag), 400)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"message": "Some thing went wrong on the server"}), 500)


@blue_print_user.route('/auth/logout', methods=['POST'])
@login_required
def logout(user_id):
    try:
        results = User.logout(user_id)
        return make_response(jsonify(results), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"message": "Some thing went wrong on the server"}), 500)
