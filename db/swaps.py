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


def get_my_swaps(user_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT s.id, s.status, b.title, u.full_name AS responder_username
            FROM swaps s
            JOIN books b ON s.book_id = b.id
            JOIN users u ON s.responder_id = u.id
            WHERE s.requester_id = %s
                AND s.status = 'Active'
            """,
            (user_id,),
        )
        swaps = cursor.fetchall()
    return swaps


def update_swap_status(swap_id, new_status):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            """
            UPDATE swaps
            SET status = %s
            WHERE id = %s
            """,
            (new_status, swap_id),
        )
    db.commit()


def get_swap_by_id(swap_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, swap_request_id, requester_id, responder_id, book_id, status
            FROM swaps
            WHERE id = %s
            """,
            (swap_id,),
        )
        swap = cursor.fetchone()
    return swap
