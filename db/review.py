from .connection import get_db_connection


def create_review(reviewer_id, reviewee_id, rating, comment=None):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO reviews (reviewer_id, reviewee_id, rating, comment)
            VALUES (%s, %s, %s, %s)
            """,
            (reviewer_id, reviewee_id, rating, comment),
        )
    db.commit()


def get_reviews_for_user(user_id) -> list:
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT r.rating, r.comment, u.full_name AS reviewer_name
            FROM reviews r
            JOIN users u ON r.reviewer_id = u.id
            WHERE r.reviewee_id = %s
            """,
            (user_id,),
        )
        reviews = cursor.fetchall()
    return reviews
