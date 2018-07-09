import unittest
import json

from app import app
from app.db_manager import DatabaseManager
from configs import drop_schema
from app.tests.test_samples import TestSamples


class UserTests(unittest.TestCase):

    json_headers = {'Content-Type': 'application/json'}
    user = TestSamples.sample_user()
    user_logedin = TestSamples.sample_login()

    def setUp(self):
        app.config['TESTING'] = True

        self.test_client = app.test_client()

    def test_create_user(self):
        data = json.dumps(self.user)
        response = self.test_client.post(
            '/auth/signup', data=data, headers=self.json_headers)
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        data = json.dumps(self.user)
        self.test_client.post('/auth/signup', data=data,
                              headers=self.json_headers)
        data = json.dumps(self.user_logedin)
        response = self.test_client.post(
            '/auth/login', data=data, headers=self.json_headers)
        results = json.loads(response.data.decode())
        # self.assertEqual(results.get("message"), 'You are logged in')
        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        with app.app_context():
            with DatabaseManager() as cursor:
                drop_tables_file = drop_schema
                with open(drop_tables_file, 'r')as file:
                    sql = file.read()
                    cursor.execute(sql)
