import unittest
import json

from flask import jsonify

from app import app
from app.db_manager import DatabaseManager
from app.user.model import hash_password
from app.tests.test_samples import TestSamples
from configs import drop_schema
from . import create_login_user


class RideTests(unittest.TestCase):
    json_headers = {'Content-Type': 'application/json'}
    sample_user = TestSamples.sample_user()
    sample_ride = TestSamples.sample_ride()
    sample_updated_ride = TestSamples.sample_updated_ride()
    sample_login = TestSamples.sample_login()

    def setUp(self):
        app.config['TESTING'] = True
        self.test_client = app.test_client()
        self.login_headers = create_login_user(self)

    def test_create_ride(self):
        data = json.dumps(self.sample_ride)
        response = self.test_client.post(
            '/rides/create', data=data, headers=self.login_headers)
        print(response.data.decode())
        self.assertEqual(response.status_code, 201)

    def test_show_ride(self):
        data = json.dumps(self.sample_ride)
        self.test_client.post(
            '/rides/create', data=data, headers=self.login_headers)
        response = self.test_client.get('/rides/1', headers=self.login_headers)
        self.assertEqual(response.status_code, 200)

    def test_get_rides(self):
        data = json.dumps(self.sample_ride)
        self.test_client.post('/rides/create', data=data,
                              headers=self.login_headers)
        response = self.test_client.get('/rides', headers=self.login_headers)
        self.assertEqual(response.status_code, 200)

    def test_update_ride_offer(self):
        data = json.dumps(self.sample_ride)
        self.test_client.post('/rides/create', data=data,
                              headers=self.login_headers)

        new_data = json.dumps(self.sample_updated_ride)

        response = self.test_client.put(
            '/rides/update/1', data=new_data, headers=self.login_headers)
        self.assertEqual(response.status_code, 201)

    def test_delete_ride_offer(self):
        data = json.dumps(self.sample_ride)
        self.test_client.post('/rides/create', data=data,
                              headers=self.login_headers)
        response = self.test_client.delete(
            '/rides/delete/1', headers=self.login_headers)
        results = json.loads(response.data.decode())
        self.assertEqual(
            results, {'message': 'Ride offer deleted successfully'})
        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        with app.app_context():
            with DatabaseManager() as cursor:
                drop_tables_file = drop_schema
                with open(drop_tables_file, 'r')as file:
                    sql = file.read()
                    cursor.execute(sql)
