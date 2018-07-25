from flask import Blueprint, jsonify, make_response

from app.decorators import login_required
from .model import Notification

blue_print_notifications = Blueprint('blue_print_notifications', __name__)


@blue_print_notifications.route('/notifications', methods=['GET'])
@login_required
def get_all_notifications(user_id):
    try:
        notifications = Notification.get_notifications()
        return make_response(jsonify(notifications), 200)

    except Exception as e:
        print(e)
        return make_response("Some thing went wrong on the server", 500)
