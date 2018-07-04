from app import DatabaseManager


def check_request(request_id):
    with DatabaseManager() as cursor:
        """
            Check if request exists
        """
        cursor.execute("SELECT id FROM requests WHERE  id = %s", [request_id])
        exists = cursor.fetchone()
        return exists
