from app import DatabaseManager


def not_json(_id, user_id, request_id, message):
    return {
        "id": _id,
        "user_id": user_id,
        "request_id": request_id,
        "message": message
    }


class Notification:
    def __init__(self, user_id, request_id, message):
        """
                This method acts as a constructor for our class, its used to initialise class attributes
        """
        self.id = ''
        self.user_id = user_id
        self.request_id = request_id
        self.message = message

    def create_notification(self):

        sql = """INSERT INTO notifications (user_id, request_id, message)
                  VALUES( %s, %s, %s) RETURNING id"""
        try:
            with DatabaseManager() as cursor:
                cursor.execute(sql, (self.user_id, self.request_id, self.message))
                results = cursor.fetchone()
                if results:
                    return not_json(results[0], results[1],
                                    results[2], results[3])
                return "Failed to create notification"
        except Exception as e:
            print(e)

    @staticmethod
    def get_notifications():
        sql = "SELECT * FROM notifications"
        notifications = []
        try:
            with DatabaseManager() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
                if results:
                    print(results)
                    for notification in results:
                        print(notification)
                        notifications.append(
                            not_json(notification[0], notification[1],
                                     notification[2], notification[3]))
                        print(notifications)
                    return {"notifications": notifications}
                return "no results"
        except Exception as e:
            print(e)

