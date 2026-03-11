import enum
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, TIMESTAMP, Enum, ForeignKey, func

from .base import Base


class RequestEnum(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class SwapRequest(Base):
    __tablename__ = "swap_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    requester_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(
        Enum(
            RequestEnum,
            name="request_enum",
            create_constraint=True,
            validate_strings=True,
        ),
        nullable=False,
        default=RequestEnum.PENDING,
    )
    requested_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )
    responded_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)

    requester: Mapped["User"] = relationship("User", back_populates="requests")
    book: Mapped["Book"] = relationship("Book", back_populates="requests")
