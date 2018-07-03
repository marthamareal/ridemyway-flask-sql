from app.db_manager import DatabaseManager


def ride_json(_id, ref_no, source, destination, date, creator_id, time, requests_no):
    """
            This method receives an object of the class, creates and returns a ride
    """
    ride = {
        "id": _id,
        "ref_no": ref_no,
        "date": date,
        "time": time,
        "source": source,
        "destination": destination,
        "creator_id": creator_id,
        "requests_no": requests_no
    }
    return ride


def check_user(user_id):
    with DatabaseManager() as cursor:
        """
            Check if user exists
        """
        cursor.execute("SELECT id FROM users WHERE id = %s", [user_id])
        exists = cursor.fetchone()
        return exists


def check_user_ride(ride_id, user_id):
    """This method returns false when ride is not found and true when user created it"""

    with DatabaseManager() as cursor:

        cursor.execute("SELECT ref_no FROM rides WHERE id = %s", [ride_id])

        if cursor.fetchone():

            cursor.execute("SELECT ref_no FROM rides WHERE creator_id = %s AND id = %s", [user_id, ride_id])
            if cursor.fetchone():
                return True

            return False

        return "Not Found"


class Ride:

    def __init__(self, date, time, source, destination, creator_id):
        """
                This method acts as a constructor for our class, its used to initialise class attributes
        """
        self.id = ''
        self.ref_no = self.generate_ref_no()
        self.date = date
        self.time = time
        self.source = source
        self.creator_id = creator_id
        self.destination = destination
        self.requests_no = 0

    def create_ride(self):

        sql = "INSERT INTO rides (ref_no, source, destination, date, creator_id, time, requests_no)" \
              " VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id"

        with DatabaseManager() as cursor:
            """
                Check if user exists
            """

            if check_user(self.creator_id):

                """
                    Create ride offer in the db
                """
                cursor.execute(sql, (self.ref_no, self.source, self.destination, self.date,
                                     self.creator_id, self.time, self.requests_no))

                """
                Search for that created ride from the db and return values
                """
                cursor.execute("SELECT * FROM rides WHERE ref_no = '%s'" % self.ref_no)
                result_ride = cursor.fetchone()

                return ride_json(result_ride[0], result_ride[1], result_ride[2],
                                 result_ride[3], result_ride[4], result_ride[5], result_ride[6], result_ride[7])
            else:
                return {"message": "You are not registered, Register to create ride"}

    @staticmethod
    def get_ride(ride_id):
        """
                This method returns a particular ride from the database
        """
        with DatabaseManager() as cursor:
            cursor.execute("SELECT * FROM rides WHERE id = %s", [ride_id])
            ride = cursor.fetchone()
            if ride:
                return ride_json(ride[0], ride[1], ride[2], ride[3], ride[4], ride[5], ride[6], ride[7])

            return {"Message": "Requested ride is not found"}

    @staticmethod
    def get_rides():
        """
                This method returns all ride created in our database
        """
        all_rides = []

        with DatabaseManager() as cursor:
            cursor.execute("SELECT * FROM rides")
            rides = cursor.fetchall()
            if rides:
                for ride in rides:
                    all_rides.append(ride_json(ride[0], ride[1], ride[2], ride[3], ride[4], ride[5], ride[6], ride[7]))

                return {"Ride offers": all_rides}

            return {"Message": "No ride Found"}

    @staticmethod
    def update(ride_id, user_id, source, destination, date, time,):

        if check_user_ride(ride_id, user_id) == "Not Found":
            return {"ride": "ride not found"}

        if check_user(user_id):
            if check_user_ride(ride_id, user_id):

                with DatabaseManager() as cursor:

                    update = """UPDATE rides SET source = %s, destination = %s, date = %s, time = %s
                                                                   WHERE id = %s  RETURNING *
                                                 """
                    cursor.execute(update, (source, destination, date, time, ride_id))
                    ride = cursor.fetchone()

                    if ride:
                        return {"updated ride": ride_json(ride[0], ride[1], ride[2], ride[3],
                                                          ride[4], ride[5], ride[6], ride[7])}

            if not check_user_ride(ride_id, user_id):
                return {"Access Denied": "You can not edit this ride"}

        return {"message": "You are not registered, Register to create ride"}

    @staticmethod
    def delete_ride(ride_id, user_id):

        """
                This method deletes a ride which has a provided id
        """
        if check_user_ride(ride_id, user_id) == "Not Found":
            return {"ride": "ride not found"}

        if check_user(user_id):
            if check_user_ride(ride_id, user_id):

                with DatabaseManager() as cursor:

                    sql = "DELETE FROM rides WHERE id = %s AND creator_id = %s"
                    cursor.execute(sql, [ride_id, user_id])
                    return {"message": "Ride offer deleted successfully"}

            if not check_user_ride(ride_id, user_id):
                return {"Access Denied": "You can not delete this ride"}

        return {"message": "You are not registered, Register to continue"}

    @staticmethod
    def generate_ref_no():

        sql = "SELECT id FROM rides WHERE id = (select max(id) from rides)"
        with DatabaseManager() as cursor:
            cursor.execute(sql)
            results = cursor.fetchone()
            if results:
                return "RF00" + str(results[0] + 1)
            else:
                return "RF001"


