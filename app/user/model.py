import hashlib
import jwt

from app.db_manager import DatabaseManager
from configs import secret
from app.validators import ValidateUserEntries


class User:

    def __init__(self,args):
        self.id = ''
        self.f_name = args.get("first name")
        self.l_name = args.get("last name")
        self.email = args.get("email")
        self.city = args.get("city")
        self.password = args.get("password")
        self.phone_no = args.get("phone_no")
        self.logged_in = 0

    def create_user(self):
        sql = "INSERT INTO users (f_name, l_name, email, city, phone_no, password)" \
              " VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"
        try:
            with DatabaseManager() as cursor:
                cursor.execute(
                    "SELECT email FROM users WHERE email = ('%s')" % self.email)
                if cursor.fetchone():
                    return {"message": "Email already registered", "status":400}
                else:
                    cursor.execute(sql, (self.f_name, self.l_name, self.email,
                                         self.city, self.phone_no, hash_password(self.password)))
                    cursor.execute(
                        "SELECT * FROM users WHERE email = '%s'" % self.email)
                    result_user = cursor.fetchone()
                    return {"message":self.user_json(result_user),
                            "status":201}
        except Exception as e:
            return e

    @staticmethod
    def login_user(email, password):
        try:
            with DatabaseManager() as cursor:
                sql = "select id,email, password, l_name from users where email = %s and password = %s"
                logged_in = "update users set logged_in = TRUE where email = %s and password = %s"

                cursor.execute(sql, (email, hash_password(password)))
                results = cursor.fetchone()
                if results:
                    token = jwt.encode(
                        {'email': email, 'user_id': results[0]}, secret, algorithm='HS256').decode()

                    cursor.execute(logged_in, (email, hash_password(password)))
                    return {"message": "You are logged in", "token": token, 'lname': results[3], 'user_id': results[0]}
                return {"message": "Email and password don't match"}
        except Exception as e:
            return e

    @staticmethod
    def logout(user_id):
        try:
            with DatabaseManager() as cursor:
                logged_out = "update users set logged_in = FALSE where id = %s returning id"
                cursor.execute(logged_out, [user_id])
                results = cursor.fetchone()
                if results:
                    return {"message": "You are logged out successfully"}
        except Exception as e:
            return e

    @staticmethod
    def user_json(user):
        return {
            "id": user[0],
            "first name": user[1],
            "last name": user[2],
            "email": user[3],
            "city": user[4],
            "phone_no": user[5],
            "password": user[6]
        }


def hash_password(_password):
    result = hashlib.md5(_password.encode())
    return result.hexdigest()
