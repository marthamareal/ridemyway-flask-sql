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

        with DatabaseManager() as cursor:

            validate_flag = ValidateUserEntries.signup(self.f_name, self.l_name,
                                                       self.email, self.city, self.phone_no, self.password)
            if validate_flag == "pass":

                """
                    check if email already exists
                """
                cursor.execute("SELECT email FROM users WHERE email = ('%s')" % self.email)
                results = cursor.fetchone()

                if results:
                    return "Email already registered"

                else:
                    """
                        Create user account in the db
                    """
                    cursor.execute(sql, (self.f_name, self.l_name, self.email,
                                         self.city, self.phone_no, hash_password(self.password)))

                    """
                    Search for that created user from the db and return values
                    """
                    cursor.execute("SELECT * FROM users WHERE email = '%s'" % self.email)
                    result_user = cursor.fetchone()

                    return self.user_json(result_user[0], result_user[1], result_user[2],
                                          result_user[3], result_user[4], result_user[5], result_user[6], )
            return validate_flag

    @staticmethod
    def login_user(email, password):
        with DatabaseManager() as cursor:

            sql = "select id,email, password from users where email = %s and password = %s"
            logged_in = "update users set logged_in = TRUE where email = %s and password = %s"

            cursor.execute(sql, (email, hash_password(password)))
            results = cursor.fetchone()
            if results:
                token = jwt.encode({'email': email, 'user_id': results[0]}, secret, algorithm='HS256').decode()
                cursor.execute(logged_in, (email, hash_password(password)))
                return {"message": "You are logged in", "token": token}
            else:
                return "Email and password don't match"

    @staticmethod
    def logout(user_id):
        with DatabaseManager() as cursor:

            logged_out = "update users set logged_in = FALSE where id = %s"
            cursor.execute(logged_out, user_id)
            results = cursor.fetchone()
            if results:
                return {"Message": "You are logged out successfully"}

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

