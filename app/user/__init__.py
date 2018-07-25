from app import DatabaseManager

missing_form_fields = []


def check_user(user_id):
    with DatabaseManager() as cursor:
        """
            Check if user exists
        """
        cursor.execute("SELECT id FROM users WHERE id = %s", [user_id])
        exists = cursor.fetchone()
        return exists


def check_form_fields(args, field_name):
    if not args.get(field_name):
        missing_form_fields.append(field_name)
