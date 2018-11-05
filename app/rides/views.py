import json
import logging

from flasgger import swag_from
from flask import Blueprint, jsonify, make_response, request

from app.decorators import login_required
from app.rides.model import Ride
from app.user import check_form_fields, missing_form_fields
from app.validators import ValidateUserEntries, form_errors

blue_print_rides = Blueprint('blue_print_rides', __name__)


@swag_from('/app/apidocs/create_ride.yml')
@blue_print_rides.route('/rides/create', methods=['POST'])
@login_required
def create_ride(user_id):
    try:
        args = json.loads(request.data.decode())
        missing_form_fields.clear()
        form_errors.clear()
        for field in ["date", "price", "destination", "time", "source"]:
            check_form_fields(args, field)

        if missing_form_fields:
            return make_response(
                jsonify({"message": "These fields:  %s  are required" % (",".join([str(x) for x in missing_form_fields]))}),
                400)

        validate_flag = ValidateUserEntries.create_ride(args)

        if validate_flag == "pass":
            ride_instance = Ride(user_id, args)
            created_ride = Ride.create_ride(ride_instance)
            return make_response(jsonify({"ride": created_ride}), 201)
        return make_response(jsonify({"message": validate_flag}), 400)

    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"message": "Some thing went wrong on the server"}), 500)


@swag_from('/app/apidocs/get_ride.yml')
@blue_print_rides.route('/rides/<int:ride_id>', methods=['GET'])
@login_required
def show_ride(user_id, ride_id):
    try:
        ride = Ride.get_ride(ride_id)
        if ride.get("message"):
            return make_response(jsonify(ride), 404)
        return make_response(jsonify({"ride": ride}), 200)
    except Exception as e:
        logging.error(e)
        make_response(jsonify({"message": "Some thing went wrong on the server"}), 500)


@swag_from('/app/apidocs/get_rides.yml')
@blue_print_rides.route('/rides', methods=['GET'])
@login_required
def get_all_rides(user_id):
    try:
        rides = Ride.get_rides(user_id)
        return make_response(jsonify(rides), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"message": "Some thing went wrong on the server"}), 500)


@blue_print_rides.route('/rides/update/<int:ride_id>', methods=['PUT'])
@login_required
def update_ride_offer(user_id, ride_id):
    try:
        args = json.loads(request.data.decode())
        missing_form_fields.clear()
        form_errors.clear()
        for field in ["date", "price", "destination", "time", "source"]:
            check_form_fields(args, field)

        if missing_form_fields:
            return make_response(
                jsonify({"message": "These fields:  %s  are required" % (",".join([str(x) for x in missing_form_fields]))}),
                400)

        validate_flag = ValidateUserEntries.create_ride(args)

        if validate_flag == "pass":
            results = Ride.update(user_id, ride_id, args)

            if results.get("status"):
                return make_response(jsonify(results), 401)

            return make_response(jsonify(results), 201)
        return make_response(jsonify({"message": validate_flag}), 400)
    except Exception as e:
        logging.error(e)
        make_response(jsonify({"message": "Some thing went wrong on the server"}), 500)


@swag_from('/app/apidocs/delete_ride.yml')
@blue_print_rides.route('/rides/delete/<int:ride_id>', methods=['DELETE'])
@login_required
def delete_one_ride(user_id, ride_id):
    try:
        results = Ride.delete_ride(ride_id, user_id)

        return make_response(jsonify(results), results['status'])
    except Exception as e:
        logging.error(e)
        make_response(jsonify({"message": "Some thing went wrong on the server"}), 500)


@swag_from('/app/apidocs/get_rides.yml')
@blue_print_rides.route('/driver/rides', methods=['GET'])
@login_required
def get_driver_rides(user_id):
    try:
        rides = Ride.get_driver_offers(user_id)
        if rides.get("status"):
            return make_response(jsonify(rides), 400)
        return make_response(jsonify(rides), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"message": "Some thing went wrong on the server"}), 500)
