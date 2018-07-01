import psycopg2
from configs import *
from flask import Flask
from app.user.views import blue_print_user

app = Flask(__name__)
app.register_blueprint(blue_print_user)


def create_tables(sql_file, connection):
    with app.open_resource(sql_file, mode='r') as file:
        cursor = connection.cursor()
        for query in ''.join(file.readlines()).split(';'):
            print(query)
            cursor.execute(query)
        connection.commit()


def main():
    pass
    # connection = psycopg2.connect(host=dbhostname, user=dbusername, password=dbpassword, dbname=dbdatabase)
    # create_tables('tables.sql', connection)
    # connection.close()

