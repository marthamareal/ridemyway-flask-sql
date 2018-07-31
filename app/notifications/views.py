import logging

from flask import Blueprint, jsonify, make_response

from app.decorators import login_required
from .model import Notification

blue_print_notifications = Blueprint('blue_print_notifications', __name__)


@blue_print_notifications.route('/notifications', methods=['GET'])
@login_required
def get_all_notifications(user_id):
    try:
        notifications = Notification.get_notifications(user_id)

        if notifications.get("status"):
            return make_response(jsonify(notifications), 400)
        return make_response(jsonify(notifications), 200)

    except Exception as e:
        logging.error(e)
        return make_response(jsonify({"message": "Some thing went wrong on the server"}), 500)
