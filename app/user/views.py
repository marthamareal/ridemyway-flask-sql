import json
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
            return jsonify({"message": "Field 'first name' is required"})
        if not args.get("last name"):
            return jsonify({"message": "Field 'last name' is required"})
        if not args.get("email"):
            return jsonify({"message": "Field 'email' is required"})
        if not args.get("city"):
            return jsonify({"message": "Field 'city' is required"})
        if not args.get("phone_no"):
            return jsonify({"message": "Field 'phone_no' is required"})
        if not args.get("password"):
            return jsonify({"message": "Field 'password' is required"})

        first_name = args.get("first name")
        last_name = args.get("last name")
        email = args.get("email")
        city = args.get("city")
        phone_no = args.get("phone_no")
        password = args.get("password")

        validate_flag = ValidateUserEntries.signup(first_name, last_name, email, city, phone_no, password)

        if validate_flag == "pass":

            user = User(first_name, last_name, email, city, phone_no, password)
            created_user = User.create_user(user)
            return jsonify({"user": created_user}), 201
        else:
            return jsonify(validate_flag)

    except FileNotFoundError as e:
        return jsonify({"Oops": e})


@blue_print_user.route('/auth/login', methods=['POST'])
def login():
    args = json.loads(request.data.decode())

    if not args.get("email"):
        return jsonify({"message": "Field 'email' is required"})
    if not args.get("password"):
        return jsonify({"message": "Field 'password' is required"})

    email = args.get("email")
    password = args.get("password")

    validate_flag = ValidateUserEntries.login(email, password)

    if validate_flag == "pass":
        _login = User.login_user(email, password)
        return jsonify({"user": _login}), 201
    else:

        return jsonify(validate_flag), 400


@blue_print_user.route('/auth/logout', methods=['POST'])
@login_required
def logout(user_id):
    results = User.logout(user_id)
    return jsonify(results)


@blue_print_user.errorhandler(404)
def url_not_found(error):
    print(error)
    return jsonify({"Message": "Requested url is not found"})

