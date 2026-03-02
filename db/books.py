from .connection import get_db_connection


def get_genres():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute("SELECT id, name FROM genres")
        return cursor.fetchall()


def create_book(telegram_id, title, author, genre_id, status, type_):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO books (added_by, title, author, genre_id, status, type)
            VALUES (
                (SELECT id FROM users WHERE telegram_id = %s),
                %s, %s, %s, %s, %s
            )
            RETURNING id
            """,
            (telegram_id, title, author, genre_id, status, type_),
        )
        book_id = cursor.fetchone()[0]
    db.commit()
    return book_id


def get_my_books(telegram_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT b.id, b.title, b.author, g.name AS genre, b.status, b.type
            FROM books b
            JOIN genres g ON b.genre_id = g.id
            WHERE b.added_by = (SELECT id FROM users WHERE telegram_id = %s)
            """,
            (telegram_id,),
        )
        return cursor.fetchall()


def get_book(book_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT b.id, b.title, b.author, g.name AS genre, b.status, b.type, b.added_by
            FROM books b
            JOIN genres g ON b.genre_id = g.id
            WHERE b.id = %s
            """,
            (book_id,),
        )
        return cursor.fetchone()

def get_books_by_genre(genre_id):
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT b.id, b.title, b.author, g.name AS genre, b.status, b.type
            FROM books b
            JOIN genres g ON b.genre_id = g.id
            WHERE b.genre_id = %s
            """,
            (genre_id,),
        )
        return cursor.fetchall()
