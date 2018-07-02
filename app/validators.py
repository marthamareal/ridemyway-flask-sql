import re

name_regex = "^[a-zA-Z]{3,25}$"
email_regex = "^[a-zA-Z0-9]+@[a-z]+\.[a-z]{2,4}$"
password_regex = "^[a-z|A-Z|0-9|@#$%^&!]+"
phone_regex = "^\+[0-9]{3}\s[0-9]{9,15}$"


class ValidateUserEntries:

    @staticmethod
    def signup(f_name, l_name, email, city, phone_no, password):

        if not re.match(name_regex, f_name):

            return {"error": "first name must have at least 3 characters and no numbers in it"}

        if not re.match(name_regex, l_name):

            return {"error": "last name must have at least 3 characters and no numbers in it"}

        if not re.match(email_regex, email):

            return {"error": "Enter a valid email"}

        if not re.match(name_regex, city):

            return {"error": "city must have at least 3 characters"}

        if not re.match(phone_regex, phone_no):

            return {"error": "Enter a valid phone number eg +256 77777788"}
        print(password)
        if re.match(password_regex, password):
            if len(password) < 8:
                return {"error": "password minimum length is 8 "}

        return "pass"
