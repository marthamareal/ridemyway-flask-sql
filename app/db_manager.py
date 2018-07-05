import logging

import psycopg2

from configs import db_configs, test_db_configs
from flask import current_app
from configs import schema


class DatabaseManager:
    tables_file = schema

    def __init__(self):
        if current_app.config['TESTING']:
            self.configs = test_db_configs
        else:
            self.configs = db_configs

    def __enter__(self):
        try:
            self.connection = psycopg2.connect(**self.configs)
            self.cursor = self.connection.cursor()

            with open(self.tables_file, 'r') as file:
                sql = file.read()
                try:
                    self.cursor.execute(sql)
                except Exception as e:
                    self.connection.rollback()
                    raise e

            return self.cursor
        except psycopg2.ProgrammingError as error:
            logging.error(error)

        except Exception as e:
            logging.error(e)
            return e

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()





