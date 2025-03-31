from sqlalchemy.sql.elements import ColumnElement

from models.database.models import User as UserSchema
from models.domain.models import User
from repos.base import BaseRepository


class UserRepository(BaseRepository):
    _schema = UserSchema
    _model = User

    def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """
        Retrieves a user by their telegram_id.

        Args:
            telegram_id (int): The telegram ID of the user to retrieve.

        Returns:
            User: The user with the specified telegram ID, or None if not found.
        """
        filters: list[ColumnElement] = [self._schema.telegram_id == telegram_id]
        user = self._query(filters=filters).first()
        return self._model.model_validate(user) if user else None

    def get_user(self, user_id: int) -> User | None:
        """
        Retrieves a user by their id.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The user with the specified ID, or None if not found.
        """
        filters: list[ColumnElement] = [self._schema.id == user_id]
        user = self._query(filters=filters).first()
        return self._model.model_validate(user) if user else None

    def create_user(self, telegram_id: int) -> User:
        """
        Creates a user if they not exists by their telegram_id.

        Args:
            telegram_id (int): The telegram_id ID of the user to create.

        Returns:
            User: The created user.
        """
        user = self.get_by_telegram_id(telegram_id)
        if not user:
            user = self._schema(telegram_id=telegram_id)
            self.add(user)
            self.flush()
        return self._model.model_validate(user)
