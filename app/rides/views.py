import json
from flasgger import swag_from

from flask import jsonify, Blueprint, request, make_response
from app.decorators import login_required
from app.rides.model import Ride
from app.validators import ValidateUserEntries, check_id

blue_print_rides = Blueprint('blue_print_rides', __name__)


@swag_from('/app/apidocs/create_ride.yml')
@blue_print_rides.route('/rides/create', methods=['POST'])
@login_required
def create_ride(user_id):
    try:
        args = json.loads(request.data.decode())
        if not args.get("date"):
            return make_response(jsonify({"message": "Field 'date' is required"}), 400)
        if not args.get("time"):
            return make_response(jsonify({"message": "Field 'time' is required"}), 400)
        if not args.get("source"):
            return make_response(jsonify({"message": "Field 'source' is required"}), 400)
        if not args.get("destination"):
            return make_response(jsonify({"message": "Field 'destination' is required"}), 400)
        if not args.get("price"):
            return make_response(jsonify({"message": "Field 'price' is required"}), 400)

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
        print(e)
        return make_response("Some thing went wrong on the server", 500)


@swag_from('/app/apidocs/get_ride.yml')
@blue_print_rides.route('/rides/<int:ride_id>', methods=['GET'])
@login_required
def show_ride(user_id, ride_id):
    try:
        if check_id(ride_id):
            ride = Ride.get_ride(user_id, ride_id)

            return make_response(jsonify({"ride": ride}), 200)

        return make_response(jsonify({"error": "ride id must be integer"}), 400)
    except Exception as e:
        print(e)
        return make_response("Some thing went wrong on the server", 500)


@swag_from('/app/apidocs/get_rides.yml')
@blue_print_rides.route('/rides', methods=['GET'])
@login_required
def get_all_rides(user_id):
    try:
        rides = Ride.get_rides(user_id)
        return make_response(jsonify(rides), 200)
    except Exception as e:
        print(e)
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

        if check_id(ride_id):
            validate_flag = ValidateUserEntries.create_ride(
                source, destination, date, ride_id, time, price)

            if validate_flag == "pass":

                results = Ride.update(user_id,
                                      ride_id, source, destination, date, time, price)

                return make_response(jsonify(results), 201)

            return jsonify(validate_flag)
        return make_response(jsonify({"error": "ride id must be integer"}), 400)

    except Exception as e:
        print(e)
        return make_response("Some thing went wrong on the server", 500)


@swag_from('/app/apidocs/delete_ride.yml')
@blue_print_rides.route('/rides/delete/<int:ride_id>', methods=['DELETE'])
@login_required
def delete_one_ride(user_id, ride_id):
    try:
        if check_id(ride_id):
            results = Ride.delete_ride(ride_id, user_id)

            return make_response(jsonify(results), 201)

        return make_response(jsonify({"error": "ride id must be integer"}), 400)
    except Exception as e:
        print(e)
        return make_response("Some thing went wrong on the server", 500)
