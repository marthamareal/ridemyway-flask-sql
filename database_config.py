import psycopg2

hostname = 'hostname'
database = 'dbname'
username = 'username'
password = 'password'

"""
    The psycopg2.connect takes params host,user,dbname,password
"""
connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)


def start_connection():
    cursor = connection.cursor()
    if cursor:
        return True
    return False


def end_connection():
    return connection.close()

