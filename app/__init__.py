from flasgger import Swagger
from flask import Flask, make_response, jsonify, redirect
from flask_cors import CORS

from app.db_manager import DatabaseManager
from app.notifications.views import blue_print_notifications
from app.requests.views import blue_print_requests
from app.rides.views import blue_print_rides
from app.user.views import blue_print_user

app = Flask(__name__)
CORS(app)

# creating my swagger ui info

template = {
    "swagger": 2.0,
    "version": "v1",
    "info": {
        "title": "RIDE MY WAY API",
        "description": "This is a web api built in flask. and you can test its endpoints from here. Enjoy my API"
    }
}
Swagger(app, template=template)


app.register_blueprint(blue_print_user)
app.register_blueprint(blue_print_rides)
app.register_blueprint(blue_print_requests)
app.register_blueprint(blue_print_notifications)


@app.route('/')
def index():
    return redirect('/apidocs/')


@app.route('/<path:path>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def url_not_found(path):
    return make_response(jsonify({"message": "Requested url is not found"}), 404)



