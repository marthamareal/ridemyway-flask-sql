import logging

import psycopg2

from configs import db_configs


class DatabaseManager:

    def __init__(self, configs=db_configs):
        self.configs = configs

    def __enter__(self):
        try:
            self.connection = psycopg2.connect(**self.configs)
            self.cursor = self.connection.cursor()
            return self.cursor

        except psycopg2.ProgrammingError as error:
            logging.error(error)

        except Exception as e:
            logging.error(e)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
