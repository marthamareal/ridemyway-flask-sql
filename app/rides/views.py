from flask import jsonify, Blueprint
from flask_restful import reqparse

from app.decorators import login_required
from app.rides.model import Ride
from app.validators import ValidateUserEntries

blue_print_rides = Blueprint('blue_print_rides', __name__)


@blue_print_rides.route('/rides/create', methods=['POST'])
@login_required
def _create_ride(user_id):
    parser = reqparse.RequestParser()
    parser.add_argument("date")
    parser.add_argument("time")
    parser.add_argument("source")
    parser.add_argument("destination")
    parser.add_argument("user_id")
    arguments = parser.parse_args()

    validate_flag = ValidateUserEntries.create_ride(arguments["source"], arguments["destination"],
                                                    arguments["date"], user_id, arguments["time"])
    if validate_flag == "pass":
        ride_instance = Ride(arguments["date"],
                             arguments["time"], arguments["source"], arguments["destination"], user_id)
        created_ride = Ride.create_ride(ride_instance)

        return jsonify({"ride": created_ride}), 200

    return jsonify(validate_flag)


@blue_print_rides.route('/rides/<int:ride_id>', methods=['GET'])
@login_required
def show_ride(user_id, ride_id):
    ride = Ride.get_ride(ride_id)
    return jsonify({"ride": ride}), 200


@blue_print_rides.route('/rides', methods=['GET'])
@login_required
def get_all_rides(user_id):
    rides = Ride.get_rides()
    return jsonify(rides), 200


@blue_print_rides.route('/rides/update/<int:ride_id>', methods=['PUT'])
@login_required
def update_ride_offer(user_id, ride_id):
    parser = reqparse.RequestParser()
    parser.add_argument("date")
    parser.add_argument("time")
    parser.add_argument("source")
    parser.add_argument("destination")
    arguments = parser.parse_args()

    """Here we use function create_ride because we still check for similar validations, Hence no need of repeating"""
    validate_flag = ValidateUserEntries.create_ride(arguments["source"], arguments["destination"],
                                                    arguments["date"], ride_id, arguments["time"])
    if validate_flag == "pass":

        results = Ride.update(ride_id, user_id, arguments["source"], arguments["destination"],
                              arguments["date"], arguments["time"])

        return jsonify(results), 200

    return jsonify(validate_flag)


@blue_print_rides.route('/rides/delete/<int:ride_id>', methods=['DELETE'])
@login_required
def delete_one_ride(user_id, ride_id):
    results = Ride.delete_ride(ride_id, user_id)
    return jsonify(results), 200

