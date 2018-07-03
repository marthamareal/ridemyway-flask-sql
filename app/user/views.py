from flask import Blueprint, jsonify
from flask_restful import reqparse, request

from app.decorators import login_required
from app.validators import ValidateUserEntries
from .model import User

blue_print_user = Blueprint('blue_print_user', __name__)


@blue_print_user.route('/auth/signup', methods=['POST'])
def signup():
    parser = reqparse.RequestParser()
    parser.add_argument("first name")
    parser.add_argument("last name")
    parser.add_argument("email")
    parser.add_argument("city")
    parser.add_argument("phone_no")
    parser.add_argument("password")
    arguments = parser.parse_args()
    print(arguments)
    validate_flag = ValidateUserEntries.signup(arguments["first name"], arguments["last name"], arguments["email"],
                                               arguments["city"], arguments["phone_no"], arguments["password"])
    if validate_flag == "pass":
        user = User(arguments["first name"], arguments["last name"], arguments["email"],
                    arguments["city"], arguments["phone_no"], arguments["password"])
        created_user = User.create_user(user)
        return jsonify({"user": created_user}), 201
    else:
        return jsonify(validate_flag), 400


@blue_print_user.route('/auth/login', methods=['POST'])
def login():
    parser = reqparse.RequestParser()
    parser.add_argument("email")
    parser.add_argument("password")
    arguments = parser.parse_args()

    validate_flag = ValidateUserEntries.login(arguments["email"],  arguments["password"])

    if validate_flag == "pass":
        _login = User.login_user(arguments["email"],  arguments["password"])
        return jsonify({"user": _login}), 201
    else:

        return jsonify(validate_flag), 400


@blue_print_user.route('/auth/logout',)
@login_required
def logout():
    results = User.logout(logout)
    return jsonify(results)
