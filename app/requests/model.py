import logging

from app.notifications.model import Notification
from app.requests import check_request, check_request_user_ride
from app.rides import check_ride
from app.user import check_user
from app import DatabaseManager
from app.user import check_details


def request_json(results):
    return  { 
        "request_id": results[0],
        "requestor": results[1],
        "ride_ref": results[2],
        "status": results[3],
        "date": results[4]
    }

class Request:
    def __init__(self, user_id, ride_id, status):

        self.user_id = user_id
        self.request_id = ''
        self.ride_id = ride_id
        self.status = status

    def create_request(self):
        sql = "INSERT INTO requests (ride_id, requestor_id, status) VALUES (%s, %s, %s) RETURNING id"
        try:
            with DatabaseManager() as cursor:
                if check_ride(self.ride_id) and check_request_user_ride(self.user_id, self.ride_id):
                    cursor.execute(
                        sql, (self.ride_id, self.user_id, self.status))
                    return {"message": "request made successfully"}
                else:
                    return {
                            "message": "Ride not found or You already Requested this Ride",
                            "status": 400
                        }
        except Exception as e:
            return e

    @staticmethod
    def get_ride_requests(ride_id, user_id):
        all_requests_on_given_ride = []
        sql = """SELECT requests.id,
                      ref_no as ride_ref, 
                     concat(f_name,' ',l_name) as requestor,
                     status,
                     date
                     FROM requests 
                     INNER JOIN users u on requests.requestor_id = u.id
                     INNER JOIN rides r on requests.ride_id = r.id
                     WHERE ride_id = %s"""
        if check_user(user_id):
            try:
                with DatabaseManager() as cursor:
                    if check_ride(ride_id):
                        cursor.execute(sql, [ride_id])
                        results = cursor.fetchall()
                        if results:
                            for result in results:
                                all_requests_on_given_ride.append(request_json(result))
                            return {
                                "requests": all_requests_on_given_ride
                            }
                        return {
                            "message": "Ride has no requests",
                            "status": 400
                        }

                    return {
                        "message": "Ride not Found",
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
        if check_request(request_id):
            try:
                ride_id = check_details("SELECT ride_id FROM requests WHERE id = %s", [request_id])
                sql = """SELECT creator_id, ref_no FROM rides WHERE 
                        id = %s AND creator_id = %s"""
                results = check_details(sql, [ride_id, user_id])
                if results:
                    creator_id = str(results[0])
                    ride_ref_no = results[1]
                    driver = check_details("SELECT l_name FROM users WHERE id = %s", creator_id)
                    update_sql = "UPDATE requests SET status = %s WHERE id = %s Returning id"
                    message = create_message(status, driver, ride_ref_no)
                    notification = Notification(
                        user_id, request_id, message)
                    Notification.create_notification(notification)
                    check_details(update_sql, [status.title(), request_id])
                    return {"message": "Approval action was successful"}
                else:
                    return {"message": "Access Denied", "status": 401}
            except Exception as e:
                logging.error(e)
        else:
            return {"message": "Request not found"}


def create_message(status, driver, ride_ref_no):
    if status.title() == "Y":
        message = "%s Accepted you to join ride %s" % (
                driver[0], ride_ref_no)
    else:
        message = "%s Rejected you to join ride %s" % (
                driver[0], ride_ref_no)
    return message
