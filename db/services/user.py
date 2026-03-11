from sqlalchemy.orm import Session

from ..models import User


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def register(self, full_name: str, telegram_id: int, phone_number: str) -> User:
        existing_user = self.get_user_by_tg_id(telegram_id)
        if existing_user:
            return

        user = User(
            full_name=full_name,
            telegram_id=telegram_id,
            phone_number=phone_number
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user
    
    def user_rating(self, user_id) -> int | float:
        user = self.get_user_by_id(user_id)
        if not user:
            return 0

        reviews = getattr(user, "my_reviews", [])

        if reviews:
            average = sum([r.rating for r in reviews]) / len(reviews)
            user.rating = average
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return average

        return 0
        
    def get_user_by_id(self, user_id: int) -> User:
        return self.session.query(User).filter_by(id=user_id).first()

    def get_user_by_tg_id(self, telegram_id: int) -> User:
        return self.session.query(User).filter_by(telegram_id=telegram_id).first()