from .connection import get_db_connection


def create_swap(swap_request_id, requester_id, responder_id, book_id, status):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO swaps (swap_request_id, requester_id, responder_id, book_id, status)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (swap_request_id, requester_id, responder_id, book_id, status),
        )
    db.commit()
