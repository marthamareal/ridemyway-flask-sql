import re

form_errors = []

name_regex = "^[a-zA-Z]{3,25}$"
address_regex = "^[a-zA-Z0-9,-s]{3,45}$"
email_regex = "^[a-zA-Z0-9]+@[a-z]+\.[a-z]{2,4}$"
password_regex = "^[a-z|A-Z|0-9|^\s|\s$@#$%^&!]+"
phone_regex = "^\+[0-9]{3}\s[0-9]{9,15}$"
id_regex = "^[1-9]+[0-9]*$"
time_regex = "^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]\s(AM|PM)$"
date_regex = "^(0[1-9]{1}|1[0-9]{1})/(0[1-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0|1])/[0-9]{4}$"
approval_regex = "[y|n|Y|N]{1}$"
price_regex = "^[0-9]{3,}$"


def check_email(email):
    if not re.match(email_regex, email):
        return False
    else:
        return True


def check_price(price):
    if not re.match(price_regex, str(price)):
        return False
    else:
        return True


def check_password(password):
    if re.match(password_regex, password.lstrip(' ')):
        if len(password) < 8:
            return False
        else:
            return True


def check_name(name):
    if not re.match(name_regex, name):
        return False
    else:
        return True


def check_address(address):
    if not re.match(address_regex, address):
        return False
    else:
        return True


def check_id(_id):
    if not re.match(id_regex, str(_id)):
        return False
    else:
        return True


def check_time(time):
    if not re.match(time_regex, time):
        return False
    else:
        return True


def check_date(date):
    if not re.match(date_regex, date):
        return False
    else:
        return True


def check_approval(approval):
    if not re.match(approval_regex, approval):
        return "error"
    else:
        return "pass"


class ValidateUserEntries:

    @staticmethod
    def signup(f_name, l_name, email, city, phone_no, password):

        if not check_name(f_name):
            form_errors.append("first name must have at least 3 "
                               "characters and no numbers and spaces in it")

        if not check_name(l_name):
            form_errors.append("last name must have at least 3 "
                               "characters and no numbers and spacesin it")

        if not check_name(city):
            form_errors.append("city must have at least 3 characters")

        if not re.match(phone_regex, phone_no):
            form_errors.append("Enter a valid phone number eg +256 777777886")

        if not check_password(password):
            form_errors.append("password length must be 8 ore more")

        if not check_email(email):
            form_errors.append("Provide a valid email")
        if form_errors:
            return form_errors
        else:
            return "pass"

    @staticmethod
    def login(email, password):

        if check_email(email) and check_password(password):
            return "pass"
        else:
            return {"message": "Provide a correct email address and password", "status": 400}

    @staticmethod
    def create_ride(source, destination, date, creator_id, time, price):

        if not check_address(source):
            return {"message": "Fill in a valid source avoid spaces, use , or -"}

        if not check_address(destination):
            return {"message": "Fill in a valid "
                    "destination avoid spaces, use , or -"}

        if not check_id(creator_id):
            return {"message": "Id must be an integer"}

        if not check_time(time):
            return {"message": "Input valid "
                    "time attributes eg 10:30 AM"}

        if not check_date(date):
            return {
                "message": "Input a valid date format(dd/mm/yyyy) eg 26/07/2018"
            }
        if not check_price(price):
            return {
                "message": "Input a correct price eg 50,5000,10000....."
            }

        return "pass"
