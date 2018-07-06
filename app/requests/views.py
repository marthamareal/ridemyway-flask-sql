import json
from flasgger import swag_from
from flask import Blueprint, jsonify, request, make_response
from app.decorators import login_required
from app.requests.model import Request
from app.validators import check_id

blue_print_requests = Blueprint('blue_print_requests', __name__)


@swag_from('/api/apidocs/create_request.yml')
@blue_print_requests.route('/rides/requests/create/<int:ride_id>', methods=['POST'])
@login_required
def create_request(user_id, ride_id):
    try:
        if check_id(ride_id):
            instance = Request(user_id, ride_id, "pending")
            results = Request.create_request(instance)
            return make_response(jsonify({"message": results.get('message')}), results.get('code'))
        return make_response({"error": "ride id must be integer"}, 400)
    except Exception as e:
        print(e)
        return make_response("Some thing went wrong on the server", 500)


@blue_print_requests.route('/rides/requests/<int:ride_id>', methods=['GET'])
@login_required
def get_requests(user_id, ride_id):
    try:
        if check_id(ride_id):
            requests = Request.get_ride_requests(ride_id, user_id)
            results = jsonify(requests)
            return make_response(results, 200)
        return make_response({"error": "ride id must be integer"}, 400)
    except Exception as e:
        print(e)
        return make_response("Some thing went wrong on the server", 500)


@blue_print_requests.route('/rides/requests/approve/<int:request_id>', methods=['POST', 'PUT'])
@login_required
def approve_ride_request(user_id, request_id):
    try:
        if check_id(request_id):
            inputs = json.loads(request.data.decode())
            if not inputs.get("approval"):
                return make_response(jsonify({"message": "Field 'approval' is required"}))
            approval = inputs.get("approval")
            results = Request.approve_request(request_id, user_id, approval)

            return jsonify(results), 201
        return make_response({"error": "request id must be integer"}, 400)
    except Exception as e:
        print(e)
        return make_response("Some thing went wrong on the server", 500)
