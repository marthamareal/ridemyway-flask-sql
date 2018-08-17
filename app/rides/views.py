import json
import logging

from flasgger import swag_from
from app.user import check_form_fields, missing_form_fields
from flask import Blueprint, jsonify, make_response, request

from app.decorators import login_required
from app.rides.model import Ride
from app.validators import ValidateUserEntries, check_feild

blue_print_rides = Blueprint('blue_print_rides', __name__)


@swag_from('/app/apidocs/create_ride.yml')
@blue_print_rides.route('/rides/create', methods=['POST'])
@login_required
def create_ride(user_id):
    try:
        args = json.loads(request.data.decode())
        check_form_fields(args,"date")
        check_form_fields(args,"time")
        check_form_fields(args,"source")
        check_form_fields(args,"destination")
        check_form_fields(args,"price")

        date = args.get("date")
        time = args.get("time")
        source = args.get("source")
        destination = args.get("destination")
        price = args.get("price")
        validate_flag = ValidateUserEntries.create_ride(
            source, destination, date, user_id, time, price)
        if validate_flag == "pass":

            ride_instance = Ride(date, time, source, destination, user_id, price)
            created_ride = Ride.create_ride(ride_instance)

            return make_response(jsonify({"ride": created_ride}), 201)

        return make_response(jsonify(validate_flag), 400)
    except Exception as e:
        logging.error(e)
        return make_response("Some thing went wrong on the server ", 500)


@swag_from('/app/apidocs/get_ride.yml')
@blue_print_rides.route('/rides/<int:ride_id>', methods=['GET'])
@login_required
def show_ride(user_id, ride_id):
    try:
        ride = Ride.get_ride(user_id, ride_id)
        return make_response(jsonify({"ride": ride}), 200)
    except Exception as e:
        logging.error(e)
        return make_response("Some thing went wrong on the server", 500)


@swag_from('/app/apidocs/get_rides.yml')
@blue_print_rides.route('/rides', methods=['GET'])
@login_required
def get_all_rides(user_id):
    try:
        rides = Ride.get_rides(user_id)
        print("dkcdshcfdfcvhdf")
        print(rides)
        return make_response(jsonify(rides), 200)
    except Exception as e:
        logging.error(e)
        return make_response("Some thing went wrong on the server", 500)


@blue_print_rides.route('/rides/update/<int:ride_id>', methods=['PUT'])
@login_required
def update_ride_offer(user_id, ride_id):
    try:

        args = json.loads(request.data.decode())
        date = args.get("date")
        time = args.get("time")
        source = args.get("source")
        destination = args.get("destination")
        price = args.get("price")

        validate_flag = ValidateUserEntries.create_ride(
            source, destination, date, ride_id, time, price)

        if validate_flag == "pass":
            results = Ride.update(user_id,
                                    ride_id, source, destination, date, time, price)

            return make_response(jsonify(results), 201)

        return jsonify(validate_flag)
    except Exception as e:
        logging.error(e)
        return make_response("Some thing went wrong on the server", 500)


@swag_from('/app/apidocs/delete_ride.yml')
@blue_print_rides.route('/rides/delete/<int:ride_id>', methods=['DELETE'])
@login_required
def delete_one_ride(user_id, ride_id):
    try:
        results = Ride.delete_ride(ride_id, user_id)

        return make_response(jsonify(results), 201)
    except Exception as e:
        logging.error(e)
        return make_response("Some thing went wrong on the server", 500)


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
