from app.user.model import hash_password


class TestSamples:

    @staticmethod
    def sample_user():

        user = {
            "id": 1,
            "first name": "test",
            "last name": "martha",
            "email": "marthamareal@gmail.com",
            "city": "kampala",
            "phone_no": "+256 7556663367",
            "password": hash_password("passworder")
        }
        return user

    @staticmethod
    def sample_ride():

        ride = {
            "id": 1,
            "ref_no": "RF001",
            "date": "02/03/2018",
            "time": "10:30 AM",
            "source": "Makerere",
            "destination": "Towm",
            "creator_id": 1,
            "requests_no": 0
        }

        return ride

    @staticmethod
    def sample_login():

        return {"email": 'marthamareal@gmail.com', "password": 'passworder'}
