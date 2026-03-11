from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String

from .base import Base


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    books: Mapped[list["Book"]] = relationship(
        "Book", uselist=True, back_populates="genre"
    )
