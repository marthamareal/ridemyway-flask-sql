import json

from flask import jsonify, Blueprint, request
from app.decorators import login_required
from app.rides.model import Ride
from app.validators import ValidateUserEntries, check_id

blue_print_rides = Blueprint('blue_print_rides', __name__)


@blue_print_rides.route('/rides/create', methods=['POST'])
@login_required
def create_ride(user_id):
    args = json.loads(request.data.decode())
    if not args.get("date"):
        return jsonify({"message": "Field 'date' is required"})
    if not args.get("time"):
        return jsonify({"message": "Field 'time' is required"})
    if not args.get("source"):
        return jsonify({"message": "Field 'source' is required"})
    if not args.get("destination"):
        return jsonify({"message": "Field 'destination' is required"})

    date = args.get("date")
    time = args.get("time")
    source = args.get("source")
    destination = args.get("destination")

    validate_flag = ValidateUserEntries.create_ride(source, destination, date, user_id, time)
    if validate_flag == "pass":

        ride_instance = Ride(date, time, source, destination, user_id)
        created_ride = Ride.create_ride(ride_instance)

        return jsonify({"ride": created_ride}), 201

    return jsonify(validate_flag), 400


@blue_print_rides.route('/rides/<int:ride_id>', methods=['GET'])
@login_required
def show_ride(user_id, ride_id):
    if check_id(ride_id):
        ride = Ride.get_ride(user_id, ride_id)
        return jsonify({"ride": ride}), 200
    return {"error": "ride id must be integer"}, 400


@blue_print_rides.route('/rides', methods=['GET'])
@login_required
def get_all_rides(user_id):
    rides = Ride.get_rides(user_id)
    return jsonify(rides), 200


@blue_print_rides.route('/rides/update/<int:ride_id>', methods=['PUT'])
@login_required
def update_ride_offer(user_id, ride_id):

    args = json.loads(request.data.decode())
    date = args.get("date")
    time = args.get("time")
    source = args.get("source")
    destination = args.get("destination")
    if check_id(ride_id):
        validate_flag = ValidateUserEntries.create_ride(source, destination, date, ride_id, time)

        if validate_flag == "pass":

            results = Ride.update(ride_id, user_id, source, destination, date, time)

            return jsonify(results), 201

        return jsonify(validate_flag)
    return {"error": "ride id must be integer"}, 400


@blue_print_rides.route('/rides/delete/<int:ride_id>', methods=['DELETE'])
@login_required
def delete_one_ride(user_id, ride_id):
    if check_id(ride_id):
        results = Ride.delete_ride(ride_id, user_id)
        return jsonify(results), 201
    return {"error": "ride id must be integer"}, 400

