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


def find_request_id(requester_id, book_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT id FROM swap_requests
            WHERE requester_id = %s AND book_id = %s
            """,
            (requester_id, book_id),
        )
        result = cursor.fetchone()
        return result[0] if result else None


def update_request_status(request_id, new_status):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            """
            UPDATE swap_requests
            SET status = %s
            WHERE id = %s
            """,
            (new_status, request_id),
        )
    db.commit()


def get_my_requests(user_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT r.id, b.title, r.status
            FROM swap_requests r
            JOIN books b ON r.book_id = b.id
            WHERE r.requester_id = %s
            """,
            (user_id,),
        )
        return cursor.fetchall()
