from flask import jsonify, Blueprint
from flask_restful import reqparse

from app.rides.model import Ride

blue_print_rides = Blueprint('blue_print_rides', __name__)


@blue_print_rides.route('/api/v1/rides/create/<int:user_id>', methods=['POST'])
def _create_ride(user_id):
    parser = reqparse.RequestParser()
    parser.add_argument("date")
    parser.add_argument("time")
    parser.add_argument("source")
    parser.add_argument("destination")
    parser.add_argument("user_id")
    arguments = parser.parse_args()
    print(arguments)

    ride_instance = Ride(arguments["date"],
                         arguments["time"], arguments["source"], arguments["destination"], user_id)
    created_ride = Ride.create_ride(ride_instance)

    return jsonify({"ride": created_ride}), 200




