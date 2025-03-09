from typing import Optional

from sqlalchemy.sql.elements import ColumnElement

from src.models.database.models import User as UserSchema
from src.models.domain.models import User
from src.repos.base import BaseRepository


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
