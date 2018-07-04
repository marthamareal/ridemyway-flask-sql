import unittest
import json

from app import app
from app.db_manager import DatabaseManager
from app.user.model import hash_password
from app.tests.test_samples import TestSamples
from configs import drop_schema


class RideTests(unittest.TestCase):

    json_headers = {'Content-Type': 'application/json'}
    sample_user = TestSamples.sample_user()
    sample_ride = TestSamples.sample_ride()

    def setUp(self):
        app.config['TESTING'] = True

        self.test_client = app.test_client()

    def test_create_ride(self):
        data = json.dumps(self.sample_user)
        response = self.test_client.post('/', data=data, headers=self.json_headers)
        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        with app.app_context():
            with DatabaseManager() as cursor:
                drop_tables_file = drop_schema
                with open(drop_tables_file, 'r')as file:
                    sql = file.read()
                    cursor.execute(sql)




