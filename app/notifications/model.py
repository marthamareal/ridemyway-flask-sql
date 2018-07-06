class Notification:
    def __init__(self, request_id, message):
        """
                This method acts as a constructor for our class, its used to initialise class attributes
        """
        self.id = ''
        self.user_id = ''
        self.request_id = request_id
        self.message = message

