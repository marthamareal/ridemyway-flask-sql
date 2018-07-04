from flask import Blueprint, jsonify
from flask_restful import reqparse

from app.requests.model import Request

blue_print_requests = Blueprint('blue_print_requests', __name__)


@blue_print_requests.route('/requests/create/<int:ride_id>/<int:user_id>', methods=['POST'])
def create_request(user_id, ride_id):

    instance = Request(user_id, ride_id, "pending")

    results = Request.create_request(instance)
    return jsonify(results), 201


@blue_print_requests.route('/rides/requests/<int:ride_id>/<int:user_id>', methods=['GET'])
def get_requests(ride_id, user_id):
    requests = Request.get_ride_requests(ride_id, user_id)
    return jsonify(requests), 200


@blue_print_requests.route('/requests/approve/<int:request_id>/<int:user_id>', methods=['POST', 'PUT'])
def approve_ride_request(user_id, request_id):
    parser = reqparse.RequestParser()
    parser.add_argument("approval")
    args = parser.parse_args()

    results = Request.approve_request(request_id, user_id, args["approval"])

    return jsonify(results), 200
