from .connection import get_db_connection

def save_book_request(user_id, book_id, status):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO swap_requests (requester_id, book_id, status)
            VALUES (%s, %s, %s)
            """,
            (user_id, book_id, status),
        )
    db.commit()