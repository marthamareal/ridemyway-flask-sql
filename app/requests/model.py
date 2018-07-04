from app.user import check_user
from app import DatabaseManager


def request_json(self):
    """
          This method receives an object of the class, creates and returns a dictionary from the object
    """
    request = {
        "id": self.request_id,
        "user_id": self.user_id,
        "ride_id": self.ride_id,
        "status": self.status
    }
    return request


class Request:
    def __init__(self, user_id, ride_id, status):
        """
               This method acts as a constructor for our class, its used to initialise class attributes
        """
        self.request_id = ''
        self.user_id = user_id
        self.ride_id = ride_id
        self.status = status

    def create_request(self):
        sql = "INSERT INTO requests (creator_id, requestor_id, status) VALUES (%s, %s, %s) RETURNING id"
        """
             Check if user exists
        """
        if check_user(self.user_id):
            with DatabaseManager() as cursor:
                cursor.execute(sql, (self.user_id, self.ride_id, self.status))
                if cursor.fetchone():
                    return {"Message": "request made successfully"}
                return {"Message": "Failed to make request"}
        else:
            return {"message": "You are not registered, Register to request ride"}

