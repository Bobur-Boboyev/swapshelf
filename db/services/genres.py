from sqlalchemy.orm import Session

from ..models import Genre


class GenreService:
    def __init__(self, session: Session):
        self.session = session

    def add_genre(self, name: str) -> Genre:
        genre = Genre(name=name)
        self.session.add(genre)
        self.session.commit()
        self.session.refresh(genre)

        return genre

    def get_genre_by_id(self, genre_id: int) -> Genre:
        return self.session.query(Genre).filter_by(id=genre_id).first()

    def get_all_genres(self) -> list[Genre]:
        return self.session.query(Genre).all()
