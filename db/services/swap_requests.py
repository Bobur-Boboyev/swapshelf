from datetime import datetime

from sqlalchemy.orm import Session

from ..models import SwapRequest


class SwapRequestService:
    def __init__(self, session: Session):
        self.session = session

    def create_request(
        self, requester_id: int, book_id: int, status: str = "pending"
    ) -> SwapRequest:
        existing_request = self.get_request_by_requester_id_and_book_id(
            requester_id, book_id
        )
        if existing_request:
            return

        swap_request = SwapRequest(
            requester_id=requester_id, book_id=book_id, status=status
        )
        self.session.add(swap_request)
        self.session.commit()
        self.session.refresh(swap_request)

        return swap_request

    def update_request_status(
        self, swap_request_id: int, new_status: str
    ) -> SwapRequest:
        existing_request = self.get_request_by_id(swap_request_id)
        if not existing_request:
            return

        existing_request.status = new_status
        existing_request.responded_at = datetime.now()

        self.session.add(existing_request)
        self.session.commit()
        self.session.refresh(existing_request)

        return existing_request

    def get_request_by_id(self, swap_request_id: int) -> SwapRequest:
        return self.session.query(SwapRequest).filter_by(id=swap_request_id).first()

    def get_request_by_requester_id_and_book_id(
        self, requester_id: int, book_id: int
    ) -> SwapRequest:
        return (
            self.session.query(SwapRequest)
            .filter_by(requester_id=requester_id, book_id=book_id)
            .first()
        )
