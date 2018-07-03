import re

name_regex = "^[a-zA-Z]{3,25}$"
address_regex = "^[a-zA-Z0-9,-s]{3,45}$"
email_regex = "^[a-zA-Z0-9]+@[a-z]+\.[a-z]{2,4}$"
password_regex = "^[a-z|A-Z|0-9|@#$%^&!]+"
phone_regex = "^\+[0-9]{3}\s[0-9]{9,15}$"
id_regex = "^[1-9]+[0-9]*$"
time_regex = "^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]\s(AM|PM)$"
date_regex = "^(0[1-9]{1}|1[0-9]{1})/(0[1-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0|1])/[0-9]{4}$"


def check_email(email):
    if not re.match(email_regex, email):
        return False
    else:
        return True


def check_password(password):
    if re.match(password_regex, password):
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
    print(date)
    if not re.match(date_regex, date):
        return False
    else:
        return True


class ValidateUserEntries:

    @staticmethod
    def signup(f_name, l_name, email, city, phone_no, password):

        if not check_name(f_name):
            return {"error": "first name must have at least 3 characters and no numbers in it"}

        if not check_name(l_name):
            return {"error": "last name must have at least 3 characters and no numbers in it"}

        if not check_name(city):
            return {"error": "city must have at least 3 characters"}

        if not re.match(phone_regex, phone_no):
            return {"error": "Enter a valid phone number eg +256 77777788"}

        check_password(password)

        check_email(email)

        return "pass"

    @staticmethod
    def login(email, password):

        if check_email(email) and check_password(password):
            return "pass"
        else:
            return {"error": "Email and password don't match"}

    @staticmethod
    def create_ride(source, destination, date, creator_id, time):

        if not check_address(source):
            return {"error": "Fill in a valid source avoid spaces, use , or -"}

        if not check_address(destination):
            return {"error": "Fill in a valid destination avoid spaces, use , or -"}

        if not check_id(creator_id):
            return {"error": "Id must be an integer"}

        if not check_time(time):
            return {"error": "Input valid time attributes eg 10:30 AM"}

        if not check_date(date):
            return {"error": "Input a valid date format(dd/mm/yyyy) eg 26/07/2018"}

        return "pass"
