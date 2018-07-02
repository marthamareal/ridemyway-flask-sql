import re

name_regex = '[a-z|A-Z]+{3,20}$'
email_regex = '[a-z|A-Z|0-9]+@[a-z].{2,4}[a-z]'
password_regex = '[a-zA-Z]{8,}'


class ValidateUserEntries:

    @staticmethod
    def signup(f_name, l_name, email, city, phone_no, password):
        if not re.match(name_regex, f_name):
            return {"error": "Name must have at least 3 characters"}

        return True
