
from flask import Flask
from app.user.views import blue_print_user

app = Flask(__name__)
app.register_blueprint(blue_print_user)

