from .models import Base
from .session import engine, SessionLocal
from .services.genres import GenreService

session = SessionLocal()
genre_service = GenreService(session)


def create_tables():
    Base.metadata.create_all(bind=engine)


def add_genre(name: str):
    genre_service.add_genre(name=name)


create_tables()
add_genre("Fantastika")
add_genre("Detektiv")
add_genre("Tarixiy")
add_genre("Ilmiy")
add_genre("Badiiy")
add_genre("Boshqa")
