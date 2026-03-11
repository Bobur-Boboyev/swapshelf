from sqlalchemy.orm import Session

from ..models import Book


class BookService:
    def __init__(self, session: Session):
        self.session = session

    def add_book(
        self,
        title: str,
        author: str,
        genre_id: int,
        status: str,
        type_: str,
        added_by: int,
    ) -> Book:
        book = Book(
            title=title,
            author=author,
            genre_id=genre_id,
            status=status,
            type_=type_,
            added_by=added_by,
        )
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)

        return book

    def get_book_by_id(self, book_id: int) -> Book:
        return self.session.query(Book).filter_by(id=book_id).first()
