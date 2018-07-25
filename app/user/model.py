import hashlib
import jwt

from app.db_manager import DatabaseManager
from configs import secret
from app.validators import ValidateUserEntries


class User:

    def __init__(self, f_name, l_name, email, city, phone_no, password):
        self.id = ''
        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        self.city = city
        self.password = password
        self.phone_no = phone_no
        self.logged_in = 0

    def create_user(self):

        sql = "INSERT INTO users (f_name, l_name, email, city, phone_no, password)" \
              " VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"
        try:
            with DatabaseManager() as cursor:
                # check if email already exists
                cursor.execute(
                    "SELECT email FROM users WHERE email = ('%s')" % self.email)
                results = cursor.fetchone()

                if results:
                    return {"message": "Email already registered"}

                else:
                    cursor.execute(sql, (self.f_name, self.l_name, self.email,
                                         self.city, self.phone_no, hash_password(self.password)))

                    cursor.execute(
                        "SELECT * FROM users WHERE email = '%s'" % self.email)
                    result_user = cursor.fetchone()

                    return self.user_json(result_user[0], result_user[1], result_user[2],
                                          result_user[3], result_user[4], result_user[5], result_user[6])
        except Exception as e:
            return e

    @staticmethod
    def login_user(email, password):
        try:
            with DatabaseManager() as cursor:

                sql = "select id,email, password from users where email = %s and password = %s"
                logged_in = "update users set logged_in = TRUE where email = %s and password = %s"

                cursor.execute(sql, (email, hash_password(password)))
                results = cursor.fetchone()
                if results:

                    token = jwt.encode(
                        {'email': email, 'user_id': results[0]}, secret, algorithm='HS256').decode()

                    cursor.execute(logged_in, (email, hash_password(password)))
                    return {"message": "You are logged in", "token": token}
                else:
                    return {
                        "message": "Email and password don't match"}
        except Exception as e:
            return e

    @staticmethod
    def logout(user_id):
        try:
            with DatabaseManager() as cursor:
                print(user_id)
                logged_out = "update users set logged_in = FALSE where id = %s returning id"
                cursor.execute(logged_out, [user_id])
                results = cursor.fetchone()
                if results:
                    return {"message": "You are logged out successfully"}
        except Exception as e:
            return e

    @staticmethod
    def user_json(user_id, f_name, l_name, email, city, phone_no, password):
        return {
            "id": user_id,
            "first name": f_name,
            "last name": l_name,
            "email": email,
            "city": city,
            "phone_no": phone_no,
            "password": password
        }


def hash_password(_password):
    result = hashlib.md5(_password.encode())
    return result.hexdigest()
