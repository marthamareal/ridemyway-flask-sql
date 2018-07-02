from os import environ

db_configs = {
    "host": environ.get('HOST_NAME'),
    "dbname": environ.get('DB_NAME'),
    "user": environ.get('USER_NAME'),
    "password": environ.get('PASSWORD')
}

secret = environ.get('SECRET_KEY')
