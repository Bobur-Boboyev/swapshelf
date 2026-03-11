import enum
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, Enum, TIMESTAMP, func

from .base import Base


class SwapEnum(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Swap(Base):
    __tablename__ = "swaps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    swap_request_id: Mapped[int] = mapped_column(
        ForeignKey("swap_requests.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    requester_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    responder_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[SwapEnum] = mapped_column(
        Enum(SwapEnum, name="swap_enum", create_constraint=True, validate_string=True),
        default=SwapEnum.ACTIVE,
    )
    started_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )
    completed_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=True)

    request: Mapped["SwapRequest"] = relationship("SwapRequest")
    requester: Mapped["User"] = relationship(
        "User", back_populates="my_taken_swaps", foreign_keys=[requester_id]
    )
    responder: Mapped["User"] = relationship(
        "User", back_populates="my_given_swaps", foreign_keys=[responder_id]
    )
    book: Mapped["Book"] = relationship("Book")
