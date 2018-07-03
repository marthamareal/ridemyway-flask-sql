import unittest
import json

from app import app
from app.db_manager import DatabaseManager
from app.user.model import hash_password
from configs import drop_schema


def create_sample_user(f_name, l_name, email, city, phone_no, password):
    user = {
        "id": 1,
        "first name": f_name,
        "last name": l_name,
        "email": email,
        "city": city,
        "phone_no": phone_no,
        "password": hash_password(password)
    }
    return user


class UserTests(unittest.TestCase):

    json_headers = {'Content-Type': 'application/json'}
    sample_user = create_sample_user("test", "martha", "marthamareal@gmail.com",
                                     "kampala", "+256 7556663367", "passworder")

    sample_login = {"email": 'marthamareal@gmail.com', "password": 'passworder'}
    sample_logout = {"user_id": 1}

    def setUp(self):
        app.config['TESTING'] = True

        self.test_client = app.test_client()

    def test_create_user(self):
        data = json.dumps(self.sample_user)
        response = self.test_client.post('/auth/signup', data=data, headers=self.json_headers)
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        data = json.dumps(self.sample_login)
        response = self.test_client.post('/auth/login', data=data, headers=self.json_headers)
        results = json.loads(response.data.decode())
        # self.assertEqual(results.get("message"), 'You are logged in')
        self.assertEqual(response.status_code, 201)

    # def test_logout(self):
    #     self.assertEqual()

    def tearDown(self):
        with app.app_context():
            with DatabaseManager() as cursor:
                drop_tables_file = drop_schema
                with open(drop_tables_file, 'r')as file:
                    sql = file.read()
                    cursor.execute(sql)




