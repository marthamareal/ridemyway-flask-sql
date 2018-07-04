from flask import Blueprint, jsonify

from app.requests.model import Request

blue_print_requests = Blueprint('blue_print_requests', __name__)


@blue_print_requests.route('/rides/requests/<int:ride_id>/<int:user_id>', methods=['POST'])
def create_request(user_id, ride_id):

    instance = Request(user_id, ride_id, "pending")

    results = Request.create_request(instance)
    return jsonify(results), 201
