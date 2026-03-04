from .connection import get_db_connection


def create_user(telegram_id, name, phone):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (telegram_id, full_name, phone_number) VALUES (%s, %s, %s)",
            (telegram_id, name, phone),
        )
    db.commit()


def get_user_by_tg_id(telegram_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT id, telegram_id, full_name, phone_number FROM users WHERE telegram_id = %s",
            (telegram_id,),
        )
        return cursor.fetchone()


def get_user_by_id(user_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            "SELECT id, telegram_id, full_name, phone_number FROM users WHERE id = %s",
            (user_id,),
        )
        return cursor.fetchone()
