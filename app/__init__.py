from flask import Flask

from app.db_manager import DatabaseManager
from app.requests.views import blue_print_requests
from app.rides.views import blue_print_rides
from app.user.views import blue_print_user

app = Flask(__name__)

app.register_blueprint(blue_print_user)
app.register_blueprint(blue_print_rides)
app.register_blueprint(blue_print_requests)


