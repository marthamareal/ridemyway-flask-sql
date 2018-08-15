
from app.user import check_details


def check_ride(ride_id):
    return check_details("SELECT id FROM rides WHERE  id = %s", [ride_id])

