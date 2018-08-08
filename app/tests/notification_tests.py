from flask import jsonify, current_app

import unittest
import json

from configs import drop_schema
from app import app
from . import create_login_user
from app.db_manager import DatabaseManager
from app.user.model import hash_password
from app.tests.test_samples import TestSamples


class RideTests(unittest.TestCase):
    json_headers = {'Content-Type': 'application/json'}
    sample_user = TestSamples.sample_user()
    sample_ride = TestSamples.sample_ride()
    sample_updated_ride = TestSamples.sample_updated_ride()
    sample_login = TestSamples.sample_login()
    sample_approval = TestSamples.sample_approve()

    def setUp(self):
        app.config['TESTING'] = True
        self.application = current_app
        self.test_client = app.test_client()
        login_response = create_login_user(self)
        self.token = json.loads(login_response.data.decode())['token']
        self.login_headers = {'token': self.token,
                              'content_type': 'application/json'}
        # create ride
        ride_data = json.dumps(self.sample_ride)
        self.test_client.post(
            '/rides/create', data=ride_data, headers=self.login_headers)
        # Request ride
        self.test_client.post(
            '/rides/requests/create/1', headers=self.login_headers)
        # Approve Ride
        data = json.dumps(self.sample_approval)
        self.test_client.post(
            '/rides/requests/approve/1', data=data, headers=self.login_headers)

    def test_get_all_notifications(self):
        response = self.test_client.get(
            '/notifications', headers=self.login_headers)
        print(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        with app.app_context():
            with DatabaseManager() as cursor:
                with open(drop_schema, 'r')as file:
                    sql = file.read()
                    cursor.execute(sql)