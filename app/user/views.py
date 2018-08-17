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
        missing_form_fields.clear()
        first_name = check_form_fields(args, "first name")
        last_name = check_form_fields(args, "last name")
        email = check_form_fields(args, "email")
        city = check_form_fields(args, "city")
        phone_no = check_form_fields(args, "phone_no")
        password = check_form_fields(args, "password")
        if missing_form_fields:
            return make_response(jsonify({"these fields are required": missing_form_fields}), 400)
        validate_flag = ValidateUserEntries.signup(
            first_name, last_name, email, city, phone_no, password)
        if validate_flag == "pass":
            user = User(first_name, last_name, email, city, phone_no, password)
            created_user = User.create_user(user)
            return make_response(jsonify({"message": created_user["message"]}),  created_user["status"])
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
        missing_form_fields.clear()
        email = check_form_fields(args, "email")
        password = check_form_fields(args, "password")
        if missing_form_fields:
            return make_response(jsonify({"these fields are required": missing_form_fields}), 400)

        validate_flag = ValidateUserEntries.login(email, password)
        if validate_flag == "pass":
            _login = User.login_user(email, password)
            if _login.get("token"):
                return make_response(jsonify(_login), 200)
                
        validate_flag = {"message": "Email and password don't match"}
        return make_response(jsonify(validate_flag), 400)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"message": "Some thing went wrong on the server"}), 500)


@blue_print_user.route('/auth/logout', methods=['GET'])
@login_required
def logout(user_id):
    try:
        results = User.logout(user_id)
        return make_response(jsonify(results), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"message": "Some thing went wrong on the server"}), 500)
