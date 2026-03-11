from sqlalchemy.orm import Session

from ..models import Review
from .user import UserService


class ReviewService:
    def __init__(self, session: Session):
        self.session = session
        self.user_service = UserService(session)

    def creat_review(
        self, reviewer_id: int, reviewee_id: int, rating: int, comment: str = "A'lo"
    ) -> Review:
        review = Review(
            reviewer_id=reviewer_id,
            reviewee_id=reviewee_id,
            rating=rating,
            comment=comment,
        )

        self.session.add(review)
        self.session.commit()
        self.session.refresh(review)

        user = self.user_service.user_rating(reviewee_id)

        return review
