from os import environ

db_configs = {
    "host": environ.get('HOST_NAME'),
    "dbname": environ.get('DB_NAME'),
    "user": environ.get('USER_NAME'),
    "password": environ.get('PASSWORD')
}

secret = environ.get('SECRET_KEY')
schema = environ.get('SCHEMA_FILE')

test_flag = False

test_db_configs = {
    "host": environ.get('HOST_NAME'),
    "dbname": environ.get('TEST_DB_NAME'),
    "user": environ.get('USER_NAME'),
    "password": environ.get('PASSWORD')
}
