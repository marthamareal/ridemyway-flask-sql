import unittest
import json

from app import app
from app.decorators import tear_down


def create_sample_user(f_name, l_name, email, city, phone_no, password):
    user = {
        "id": 1,
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
    sample_user = create_sample_user("test", "martha", "marthamareal@gmail.com",
                                     "kampala", "+256 7556663367", "passworder")
    sample_login = {"email": 'marthamareal@gmail.com', "password": 'passworder'}

    def setUp(self):
        app.config['TESTING'] = True

        self.test_client = app.test_client()

    def test_create_user(self):
        data = json.dumps(self.sample_user)
        response = self.test_client.post('/auth/signup', data=data, headers=self.json_headers)
        results = json.loads(response.data.decode())
        self.assertEqual(results, {"user": self.sample_user})
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):

        data = json.dumps(self.sample_login)
        response = self.test_client.post('/auth/login', data=data, headers=self.json_headers)
        results = json.loads(response.data.decode())
        self.assertEqual(results[0]["message"], 'You are logged in')
        self.assertEqual(response.status_code, 201)

    def tear_down(self):
        pass

