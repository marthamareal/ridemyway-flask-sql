import json

from flask import Blueprint, jsonify, request
from app.decorators import login_required
from app.requests.model import Request
from app.validators import check_id

blue_print_requests = Blueprint('blue_print_requests', __name__)


@blue_print_requests.route('/rides/requests/create/<int:ride_id>', methods=['POST'])
@login_required
def create_request(user_id, ride_id):
    if check_id(ride_id):
        instance = Request(user_id, ride_id, "pending")
        results = Request.create_request(instance)
        return jsonify(results), 201
    return {"error": "ride id must be integer"}, 400


@blue_print_requests.route('/rides/requests/<int:ride_id>', methods=['GET'])
@login_required
def get_requests(user_id, ride_id):
    if check_id(ride_id):
        requests = Request.get_ride_requests(ride_id, user_id)
        return jsonify(requests), 200
    return {"error": "ride id must be integer"}, 400


@blue_print_requests.route('/rides/requests/approve/<int:request_id>', methods=['POST', 'PUT'])
@login_required
def approve_ride_request(user_id, request_id):
    if check_id(request_id):
        inputs = json.loads(request.data.decode())
        if not inputs.get("approval"):
            return jsonify({"message": "Field 'approval' is required"})
        approval = inputs.get("approval")
        results = Request.approve_request(request_id, user_id, approval)

        return jsonify(results), 200
    return {"error": "request id must be integer"}, 400
