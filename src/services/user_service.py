from src.models.domain.models import User
from src.repos.user import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        """Retrieves a user by their telegram_id."""
        return self.user_repository.get_by_telegram_id(telegram_id)

    def get_user(self, user_id: int) -> User | None:
        """Retrieves a user by their id."""
        return self.user_repository.get_user(user_id)

    def register_user(self, telegram_id: int) -> User:
        """
        Creates a user by their telegram_id.
        """
        user = self.user_repository.create_user(telegram_id)
        self.user_repository.commit()
        return user
