from datetime import datetime

from sqlalchemy.orm import Session

from ..models import Swap


class SwapService:
    def __init__(self, session: Session):
        self.session = session

    def create_swap(
        self,
        swap_request_id: int,
        requester_id: int,
        responder_id: int,
        book_id: int,
        status: str,
    ) -> Swap:
        swap = Swap(
            swap_request_id=swap_request_id,
            requester_id=requester_id,
            responder_id=responder_id,
            book_id=book_id,
            status=status,
        )
        self.session.add(swap)
        self.session.commit()
        self.session.refresh(swap)

        return swap

    def get_swaps_by_user_id(self, user_id: int) -> list[Swap]:
        return (
            self.session.query(Swap)
            .filter((Swap.requester_id == user_id) & (Swap.status == "active"))
            .all()
        )

    def get_swap_by_request_id(self, swap_request_id: int) -> Swap:
        return (
            self.session.query(Swap)
            .filter_by(Swap.swap_request_id == swap_request_id)
            .first()
        )

    def get_swap_by_id(self, swap_id: int) -> Swap:
        return self.session.query(Swap).filter(Swap.id == swap_id).first()

    def update_swap_status(self, swap_id: int, new_status: str) -> Swap:
        existing_swap = self.get_swap_by_id(swap_id)
        if not existing_swap:
            return

        existing_swap.status = new_status
        existing_swap.completed_at = datetime.now()

        self.session.add(existing_swap)
        self.session.commit()
        self.session.refresh(existing_swap)

        return existing_swap
