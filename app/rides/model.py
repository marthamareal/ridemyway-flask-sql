from app.user import check_user
from app.db_manager import DatabaseManager
from app.user import check_details


class Ride:

    def __init__(self, creator_id, args):
         """
                 This method acts as a constructor for our class, its used to initialise class attributes
         """
         self.id = ''
         self.ref_no = self.generate_ref_no()
         self.date = args.get("date")
         self.time = args.get("time")
         self.source = args.get("source")
         self.creator_id = creator_id
         self.destination = args.get("destination")
         self.requests_no = 0
         self.price = args.get("price")

    def create_ride(self):

        sql = "INSERT INTO rides (ref_no, source, destination, date, creator_id, time, requests_no, price)" \
              " VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"
        try:
            check_details(sql, (self.ref_no, self.source, self.destination, self.date,
                                self.creator_id, self.time, self.requests_no, self.price))
            result_ride = check_details(
                "SELECT * FROM rides WHERE ref_no = %s", [self.ref_no])
            return ride_json(result_ride)
        except Exception as e:
            return e

    @staticmethod
    def get_ride(user_id, ride_id):
        if check_user_ride(ride_id, user_id) == "Not Found":
            return {"ride": "ride not found"}

        with DatabaseManager() as cursor:
            try:

                sql = """SELECT date, ref_no, source, destination,time,
                          concat(l_name,' ',f_name)  as creator,
                          phone_no as phone,
                          price
                          FROM rides
                           INNER JOIN users ON rides.creator_id = users.id
                           WHERE rides.id = %s"""
                ride = check_details(sql, [ride_id])
                if ride:

                    return ride_details(ride)
                return {"message": "Requested ride is not found"}
            except Exception as e:
                return e

    @staticmethod
    def get_rides(user_id):
        all_rides = []
        if check_user(user_id):
            with DatabaseManager() as cursor:
                try:
                    cursor.execute("SELECT id, ref_no, source, destination, date, "
                                   "creator_id, time, requests_no, price FROM rides")
                    rides = cursor.fetchall()
                    if rides:
                        for ride in rides:
                            all_rides.append(ride_json(ride))
                        return {"Ride offers": all_rides}
                    return {"Message": "No ride Found"}
                except Exception as e:
                    return e
        return {"Message": "Login (create account) to view the offers"}

    @staticmethod
    def update(user_id, ride_id, args):
        if check_user_ride(ride_id, user_id):
            try:
                update = """UPDATE rides SET source = %s, destination = %s, date = %s, time = %s , price = %s
                                                                   WHERE id = %s  RETURNING *
                                                 """
                ride = check_details(update, (args.get("source"), args.get("destination"), args.get("date"),
                            args.get("time"), args.get("ride_id"), args.get("price")))
                if ride:
                    return {"updated ride": ride_json(ride)}
            except Exception as e:
                return e

        if not check_user_ride(ride_id, user_id):
            return {"Access Denied": "You can not edit this ride"}

    @staticmethod
    def delete_ride(ride_id, user_id):
        if check_user_ride(ride_id, user_id):
            with DatabaseManager() as cursor:
                try:
                    sql = "DELETE FROM rides WHERE id = %s AND creator_id = %s"
                    cursor.execute(sql, [ride_id, user_id])
                    return {"message": "Ride offer deleted successfully"}
                except Exception as e:
                    return e
        if not check_user_ride(ride_id, user_id):
            return {"Access Denied": "You can not delete this ride"}

    @staticmethod
    def generate_ref_no():
        sql = "SELECT id FROM rides WHERE id = (select max(id) from rides)"
        with DatabaseManager() as cursor:
            try:
                cursor.execute(sql)
                results = cursor.fetchone()
                if results:
                    return "RF00" + str(results[0] + 1)
                else:
                    return "RF001"
            except Exception as e:
                return e

    @staticmethod
    def get_driver_offers(user_id):
        driver_rides = []
        try:
            with DatabaseManager() as cursor:
                cursor.execute("""SELECT rides.id as id, ref_no, source, destination, date, 
                                       creator_id, time,
                                        (SELECT count(id) FROM requests where ride_id = rides.id) as requests_no,
                                         price
                                          FROM rides
                                           WHERE creator_id = %s
                                           """, [user_id])
                rides = cursor.fetchall()
                if rides:
                    for ride in rides:
                        driver_rides.append(ride_json(ride))
                    return {"driver_offers": driver_rides}
                return {"message": "You have no rides created  create one to drive", "status": 400}

        except Exception as e:
            return {"message": e}


def check_user_ride(ride_id, user_id):
    """This method returns false when ride is not found and true when user created it"""
    try:
        if check_details("SELECT ref_no FROM rides WHERE creator_id = %s AND id = %s", [
                          user_id, ride_id]):
            return True
        return False
    except Exception as e:
        return e


def ride_json(result_turple):
    return {
        "id": result_turple[0],
        "ref_no": result_turple[1],
        "source": result_turple[2],
        "destination": result_turple[3],
        "date": result_turple[4],
        "creator_id": result_turple[5],
        "time": result_turple[6],
        "requests_no": result_turple[7],
        "price": result_turple[8]
    }


def ride_details(ride):
    return {"date": ride[0],
            "ref_no": ride[1],
            "source": ride[2],
            "destination": ride[3],
            "time": ride[4],
            "creator": ride[5],
            "phone": ride[6],
            "price": ride[7]
            }
