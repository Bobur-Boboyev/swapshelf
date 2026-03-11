import enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Enum, TIMESTAMP, func
from datetime import datetime

from .base import Base


class StatusBookEnum(str, enum.Enum):
    NEW = "New"
    GOOD = "Good"
    FAIR = "Fair"
    WORN = "Worn"


class TypeBookEnum(str, enum.Enum):
    BORROW = "Borrow"
    PERMANENT = "Permanent"
    BOTH = "Both"


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id", ondelete="SET NULL"))
    status: Mapped[StatusBookEnum] = mapped_column(
        Enum(
            StatusBookEnum,
            name="status_enum",
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
        default=StatusBookEnum.NEW,
    )
    type_: Mapped[TypeBookEnum] = mapped_column(
        Enum(
            TypeBookEnum,
            name="type_enum",
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
        default=TypeBookEnum.BORROW,
    )
    added_by: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    added_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="books")
    genre: Mapped["Genre"] = relationship("Genre", back_populates="books")
    requests: Mapped[list["SwapRequest"]] = relationship(
        "SwapRequest", uselist=True, back_populates="book"
    )
