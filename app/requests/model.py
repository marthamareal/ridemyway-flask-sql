import logging

from app.notifications.model import Notification
from app.requests import check_request
from app.rides import check_ride
from app.user import check_user
from app import DatabaseManager


def request_json(request_id, ride_ref, requestor, status, date):
    """
          This method receives an object of the class, creates and returns a dictionary from the object
    """
    request = {
        "request_id": request_id,
        "requestor": requestor,
        "ride_ref": ride_ref,
        "status": status,
        "date": date
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
                        cursor.execute(
                            sql, (self.ride_id, self.user_id, self.status))

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

        sql = """SELECT ride_id,
                      ref_no as ride_ref, 
                     concat(f_name,' ',l_name) as requestor,
                     status,
                     date
                     FROM requests 
                     INNER JOIN users u on requests.requestor_id = u.id
                     INNER JOIN rides r on requests.ride_id = r.id
                     WHERE ride_id = %s"""

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
                                                                  result[1], result[2], result[3], result[4]))
                            return {
                                "requests": all_requests_on_given_ride
                            }
                        return {
                            "message": "Ride has no requests",
                            "status": 400
                        }

                    return {
                        "Message": "Ride not Found",
                        "status": 400
                    }
            except Exception as e:
                logging.error(e)

        return {
            "message": "You are not registered, Register to request ride",
            "status": 400
        }

    @staticmethod
    def approve_request(request_id, user_id, status):

        if check_user(user_id):

            if check_request(request_id):
                try:
                    with DatabaseManager() as cursor:

                        cursor.execute(
                            "SELECT ride_id FROM requests WHERE id = '%s'" % request_id)
                        ride_id = cursor.fetchone()
                        # This sql determines whether the user to approve request is owner of ride offer

                        sql = """SELECT creator_id, ref_no FROM rides WHERE 
                                              id = %s AND creator_id = %s"""
                        cursor.execute(sql, (ride_id, user_id))
                        results = cursor.fetchone()

                        if results:
                            creator_id = str(results[0])
                            ride_ref_no = results[1]

                            cursor.execute(
                                "SELECT l_name FROM users WHERE id = %s", creator_id)
                            driver = cursor.fetchone()
                            update_sql = "UPDATE requests SET status = '%s' WHERE id = '%s'" % (
                                status.title(), request_id)

                            if status.title() == "Y":
                                message = "%s Accepted you to join ride %s" % (
                                    driver[0], ride_ref_no)
                            else:
                                message = "%s Rejected you to join ride %s" % (
                                    driver[0], ride_ref_no)

                            notification = Notification(
                                user_id, request_id, message)
                            Notification.create_notification(notification)
                            cursor.execute(update_sql)
                            return {"message": "Approval action was successful"}
                        else:
                            return {"message": "Access Denied", "status": 401}

                except Exception as e:
                    logging.error(e)
            else:
                return {"Message": "Request not found"}
        else:
            return {"message": "You are not registered, Register to request ride"}
