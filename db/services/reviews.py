from sqlalchemy.orm import Session

from ..models import Review
from .user import UserService


class ReviewService:
    def __init__(self, session: Session):
        self.session = session
        self.user_service = UserService(session)

    def create_review(
        self, reviewer_id: int, reviewee_id: int, rating: int, comment: str = "A'lo"
    ) -> Review:

        if reviewer_id == reviewee_id:
            raise ValueError("User cannot review themselves")

        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")

        existing = (
            self.session.query(Review)
            .filter_by(reviewer_id=reviewer_id, reviewee_id=reviewee_id)
            .first()
        )

        review = Review(
            reviewer_id=reviewer_id,
            reviewee_id=reviewee_id,
            rating=rating,
            comment=comment,
        )

        self.session.add(review)
        self.session.commit()
        self.session.refresh(review)

        self.user_service.update_user_rating(reviewee_id)

        return review
