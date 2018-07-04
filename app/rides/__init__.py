from app import DatabaseManager


def check_ride(ride_id):
    with DatabaseManager() as cursor:
        """
            Check if user exists
        """
        cursor.execute("SELECT id FROM rides WHERE  id = %s", [ride_id])
        exists = cursor.fetchone()
        return exists
