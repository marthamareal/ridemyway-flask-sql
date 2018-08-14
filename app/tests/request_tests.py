from flask import jsonify, current_app

import unittest
import json

from configs import drop_schema
from app import app
from app.db_manager import DatabaseManager
from app.user.model import hash_password
from app.tests.test_samples import TestSamples
from . import create_login_user


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
        
        self.login_headers = create_login_user(self)
        
        # create ride
        ride_data = json.dumps(self.sample_ride)
        self.test_client.post(
            '/rides/create', data=ride_data, headers=self.login_headers)

    def test_create_request(self):
        response = self.test_client.post(
            '/rides/requests/create/1', headers=self.login_headers)
        self.assertEqual(response.status_code, 201)

    def test_get_requests(self):
        self.test_client.post('/rides/requests/create/1',
                              headers=self.login_headers)
        response = self.test_client.get(
            '/rides/requests/1', headers=self.login_headers)
        self.assertEqual(response.status_code, 200)

    def test_approve_ride_request(self):
        self.test_client.post('/rides/requests/create/1',
                              headers=self.login_headers)
        data = json.dumps(self.sample_approval)
        response = self.test_client.post(
            '/rides/requests/approve/1', data=data, headers=self.login_headers)
        self.assertEqual(response.status_code, 201)

    def test_ride_not_found(self):
        response = self.test_client.post(
            '/rides/requests/create/2', headers=self.login_headers)
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        with app.app_context():
            with DatabaseManager() as cursor:
                drop_tables_file = drop_schema
                with open(drop_tables_file, 'r')as file:
                    sql = file.read()
                    cursor.execute(sql)
