import logging

from app import DatabaseManager


def not_json(_id, message):
    return {
        "id": _id,
        "message": message
    }


class Notification:
    def __init__(self, user_id, request_id, message):

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
                    return {"message": "created notification"}
                return {"message": "Failed to create notification"}
        except Exception as e:
            logging.error(e)

    @staticmethod
    def get_notifications(user_id):
        sql = "SELECT  id, message FROM notifications WHERE user_id = '%s' " % user_id
        notifications = []
        try:
            with DatabaseManager() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
                if results:
                    for notification in results:
                        notifications.append(
                            not_json(notification[0], notification[1]))

                    return {"notifications": notifications}
                return {"message": "You have no notifications", "status": 400}
        except Exception as e:
            logging.error(e)

