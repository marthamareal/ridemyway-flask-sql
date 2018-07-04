from app.rides import check_ride
from app.user import check_user
from app import DatabaseManager


def request_json(request_id, ride_id, user_id, status):
    """
          This method receives an object of the class, creates and returns a dictionary from the object
    """
    request = {
        "id": request_id,
        "requestor_id": user_id,
        "ride_id": ride_id,
        "status": status
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
        sql = "INSERT INTO requests (ride_id, requestor_id, status) VALUES (%s, %s, %s) RETURNING id"
        """
             Check if user exists
        """
        if check_user(self.user_id):
            with DatabaseManager() as cursor:
                if check_ride(self.ride_id):
                    cursor.execute(sql, (self.ride_id, self.user_id, self.status))
                    if cursor.fetchone():
                        return {"Message": "request made successfully"}
                    return {"Message": "Failed to make request"}
                return {"message": "Ride not found"}
        else:
            return {"message": "You are not registered, Register to request ride"}

    @staticmethod
    def get_ride_requests(ride_id, user_id):

        all_requests_on_given_ride = []

        sql = "SELECT * FROM requests WHERE ride_id = %s"
        """
            Check if user exists
        """
        if check_user(user_id):
            with DatabaseManager() as cursor:
                if check_ride(ride_id):
                    cursor.execute(sql, [ride_id])
                    results = cursor.fetchall()
                    if results:
                        for result in results:
                            all_requests_on_given_ride.append(request_json(result[0], result[1], result[2], result[3]))
                        return {"Ride's requests": all_requests_on_given_ride}
                    return {"message": "Ride has no requests"}

                return {"Message": "Ride not Found"}

        return {"message": "You are not registered, Register to request ride"}


