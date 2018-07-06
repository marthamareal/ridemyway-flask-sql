from flask import Flask, make_response, jsonify, redirect

from app.db_manager import DatabaseManager
from app.requests.views import blue_print_requests
from app.rides.views import blue_print_rides
from app.user.views import blue_print_user

app = Flask(__name__)

app.register_blueprint(blue_print_user)
app.register_blueprint(blue_print_rides)
app.register_blueprint(blue_print_requests)


@app.route('/')
def index():
    return redirect('/apidocs/')


@app.route('/<path:path>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def url_not_found(path):
    return make_response(jsonify({"Message": "Requested url is not found"}), 404)



