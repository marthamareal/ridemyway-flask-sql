from app.requests import check_request
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

            try:
                with DatabaseManager() as cursor:
                    if check_ride(self.ride_id):
                        cursor.execute(sql, (self.ride_id, self.user_id, self.status))
                        if cursor.fetchone():
                            return {
                                       "message": "request made successfully",
                                       "code": 201
                                   }
                        return {
                            "Message": "Failed to make request"
                        }

                    return {
                               "message": "Ride not found",
                               "code": 400
                           }
            except Exception as e:
                return e
        else:
            return {
                       "message": "You are not registered, Register to request ride",
                       "code": 401
                    }

    @staticmethod
    def get_ride_requests(ride_id, user_id):

        all_requests_on_given_ride = []

        sql = "SELECT * FROM requests WHERE ride_id = %s"
        """
            Check if user exists
        """
        if check_user(user_id):

            try:
                with DatabaseManager() as cursor:
                    if check_ride(ride_id):
                        cursor.execute(sql, [ride_id])
                        results = cursor.fetchall()
                        if results:
                            for result in results:
                                all_requests_on_given_ride.append(request_json(result[0],
                                                                               result[1], result[2], result[3]))
                            return {
                                "Ride's requests": all_requests_on_given_ride
                            }
                        return {
                            "message": "Ride has no requests"
                        }

                    return {
                        "Message": "Ride not Found"
                    }
            except Exception as e:
                return e

        return {
            "message": "You are not registered, Register to request ride"
        }

    @staticmethod
    def approve_request(request_id, user_id, status):

        if check_user(user_id):
            if check_request(request_id):

                # This sql determines whether the user to approve request is owner of ride offer
                sql = "SELECT creator_id FROM rides WHERE id=(SELECT ride_id FROM requests WHERE id= %s)"
                try:
                    with DatabaseManager() as cursor:
                        cursor.execute(sql, [request_id])

                        if cursor.fetchone():
                            update_sql = "UPDATE requests SET status = '%s' " % status
                            print(status)
                            cursor.execute(update_sql)
                            return {"Message": "Approval action was successful"}
                        return {"Message": "Access Denied"}
                except Exception as e:
                    return e

            return {"Message": "Request not found"}

        return {"message": "You are not registered, Register to request ride"}

