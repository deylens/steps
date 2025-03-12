from src.models.domain.models import User
from src.repos.user import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        """Retrieves a user by their telegram_id."""
        return self.user_repository.get_by_telegram_id(telegram_id)
