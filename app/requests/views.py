import json
import logging

from flasgger import swag_from
from flask import Blueprint, jsonify, request, make_response
from app.decorators import login_required
from app.requests import not_approved
from app.requests.model import Request
from app.validators import check_feild, id_regex, check_approval

blue_print_requests = Blueprint('blue_print_requests', __name__)


@swag_from('/app/apidocs/create_request.yml')
@blue_print_requests.route('/rides/requests/create/<int:ride_id>', methods=['POST'])
@login_required
def create_request(user_id, ride_id):
    try:
        instance = Request(user_id, ride_id, "pending".title())
        results = Request.create_request(instance)
        if results.get("status"):
            return make_response(jsonify(results), 400)
        return make_response(jsonify(results), 201)
    except Exception as e:
        logging.error(e)
        return make_response("Some thing went wrong on the server", 500)


@blue_print_requests.route('/rides/requests/<int:ride_id>', methods=['GET'])
@login_required
def get_requests(user_id, ride_id):
    try:
        requests = Request.get_ride_requests(ride_id, user_id)
        if requests.get("status"):
            return make_response(jsonify(requests), 400)
        else:
            return make_response(jsonify(requests), 200)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"message": "Some thing went wrong on the server"}), 500)


@blue_print_requests.route('/rides/requests/approve/<int:request_id>', methods=['POST', 'PUT'])
@login_required
def approve_ride_request(user_id, request_id):
    try:
        if not_approved(request_id) is "not_approved":
            inputs = json.loads(request.data.decode())
            if not inputs.get("approval"):
                return make_response(jsonify({"message": "Field 'approval' is required"}), 400)
            approval = inputs.get("approval")
            if check_approval(approval) is "error":
                return make_response(jsonify({"message": "Approval must be Y or N"}), 400)
            results = Request.approve_request(request_id, user_id, approval)
            if results.get("status"):
                return make_response(jsonify(results), 401)
            return make_response(jsonify(results), 201)
        else:
            return make_response(jsonify({"message": "Request is already approved"}), 400)
    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"message": "Some thing went wrong on the server"}), 500)
