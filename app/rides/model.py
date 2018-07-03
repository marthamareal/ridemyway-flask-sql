from app.db_manager import DatabaseManager


class Ride:

    def __init__(self, date, time, source, destination, creator_id):
        """
                This method acts as a constructor for our class, its used to initialise class attributes
        """
        self.id = ''
        self.ref_no = "RF001"
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
                    Create ride offer in the db
                """
                cursor.execute(sql, (self.ref_no, self.source, self.destination, self.date,
                                     self.creator_id, self.time, self.requests_no))

                """
                Search for that created ride from the db and return values
                """
                cursor.execute("SELECT * FROM rides WHERE ref_no = '%s'" % self.ref_no)
                result_ride = cursor.fetchone()

                return self.ride_json(result_ride[0], result_ride[1], result_ride[2],
                                      result_ride[3], result_ride[4], result_ride[5], result_ride[6], result_ride[7])

    @staticmethod
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
