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
            "password": "passworder"
        }
        return user

    @staticmethod
    def sample_ride():

        ride = {
            "id": 1,
            "ref_no": "RF001",
            "date": "2018-07-11",
            "time": "10:30 AM",
            "source": "Makerere",
            "destination": "Town",
            "creator_id": 1,
            "requests_no": '0',
            "price": 5000
        }

        return ride

    @staticmethod
    def sample_updated_ride():
        ride = {
            "id": 1,
            "ref_no": "RF001",
            "date": "2018-07-11",
            "time": "10:30 PM",
            "source": "new",
            "destination": "new",
            "creator_id": 1,
            "requests_no": '0',
            "price": 6000
        }

        return ride

    @staticmethod
    def sample_approve():
        return {
            "approval": "Y"
        }

    @staticmethod
    def sample_login():

        return {"email": 'marthamareal@gmail.com', "password": 'passworder'}
