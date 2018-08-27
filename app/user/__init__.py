from app import DatabaseManager

missing_form_fields = []

def check_user(user_id):
        return check_details("SELECT id FROM users WHERE id = %s", [user_id])

def check_form_fields(args, field_name):
    if not args.get(field_name):
        missing_form_fields.append(field_name)
    return args.get(field_name)

def check_details(sql, value):
    with DatabaseManager() as cursor:
        cursor.execute(sql,value)
        return cursor.fetchone()
