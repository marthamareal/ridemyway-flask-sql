from app import DatabaseManager


def check_user(user_id):
    with DatabaseManager() as cursor:
        """
            Check if user exists
        """
        cursor.execute("SELECT id FROM users WHERE id = %s", [user_id])
        exists = cursor.fetchone()
        return exists
