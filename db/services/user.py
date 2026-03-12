from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models import User, Review


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def register(self, full_name: str, telegram_id: int, phone_number: str) -> User:
        existing_user = self.get_user_by_tg_id(telegram_id)
        if existing_user:
            return

        user = User(
            full_name=full_name, telegram_id=telegram_id, phone_number=phone_number
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def update_user_rating(self, user_id: int) -> float:
        avg = (
            self.session.query(func.avg(Review.rating))
            .filter(Review.reviewee_id == user_id)
            .scalar()
        )

        user = self.get_user_by_id(user_id)

        if not user:
            return 0

        user.rating = float(avg or 0)

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user.rating

    def get_user_by_id(self, user_id: int) -> User:
        return self.session.query(User).filter_by(id=user_id).first()

    def get_user_by_tg_id(self, telegram_id: int) -> User:
        return self.session.query(User).filter_by(telegram_id=telegram_id).first()
