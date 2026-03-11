from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, BigInteger, TIMESTAMP, func
from datetime import datetime

from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    rating: Mapped[int] = mapped_column(Integer, default=0)
    phone_number: Mapped[str] = mapped_column(String(20))
    joined_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )

    books: Mapped[list["Book"]] = relationship(
        "Book", uselist=True, back_populates="user"
    )
    my_reviews: Mapped[list["Review"]] = relationship(
        "Review",
        uselist=True,
        back_populates="reviewer",
        foreign_keys="Review.reviewer_id",
    )
    reviewee: Mapped[list["Review"]] = relationship(
        "Review",
        uselist=True,
        back_populates="reviewee",
        foreign_keys="Review.reviewee_id",
    )
    requests: Mapped[list["SwapRequest"]] = relationship(
        "SwapRequest", uselist=True, back_populates="requester"
    )
    my_taken_swaps: Mapped[list["Swap"]] = relationship(
        "Swap",
        uselist=True,
        back_populates="requester",
        foreign_keys="Swap.requester_id",
    )
    my_given_swaps: Mapped[list["Swap"]] = relationship(
        "Swap",
        uselist=True,
        back_populates="responder",
        foreign_keys="Swap.responder_id",
    )
