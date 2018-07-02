import unittest
import json

from app import app


def create_sample_user(f_name, l_name, email, city, phone_no, password):
    user = {
        "f_name": f_name,
        "l_name": l_name,
        "email": email,
        "city": city,
        "phone_no": phone_no,
        "password": password
    }
    return user


class UserTests(unittest.TestCase):
    json_headers = {'Content-Type': 'application/json'}
    sample_user = create_sample_user("test", "martha", "marthamareal@gmail.com", "kampala", "075566633", "pass")

    def setUp(self):
        self.test_client = app.test_client()

    def test_create_user(self):
        data = json.dumps(self.sample_user)
        response = self.test_client.post('/auth/signup', data=data, headers=self.json_headers)

        self.assertEqual(response.status_code, 201)
