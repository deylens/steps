from datetime import date

from sqlalchemy.sql.elements import ColumnElement

from models.database.models import Child as ChildSchema
from models.domain.models import Child
from repos.base import BaseRepository


class ChildRepository(BaseRepository):
    _schema = ChildSchema
    _model = Child

    def get_child(self, child_id: int) -> Child | None:
        """
        Retrieves a child by their id.

        Args:
            child_id (int): The ID of the child to retrieve.

        Returns:
            Child: The child with the specified ID, or None if not found.
        """
        filters: list[ColumnElement] = [self._schema.id == child_id]
        child = self._query(filters=filters).first()
        return self._model.model_validate(child) if child else None

    def get_children(self, user_id: int) -> list[Child]:
        """
        Retrieves a list of children by their parent's id.

        Args:
            user_id (int): The parent's ID of the child to retrieve.

        Returns:
            Child: The child with the specified parent's ID, or None if not found.
        """
        filters: list[ColumnElement] = [self._schema.user_id == user_id]
        children = self._query(filters=filters).all()
        return [self._model.model_validate(child) for child in children]

    def create_child(self, user_id: int, name: str, birth_date: date) -> Child:
        """
        Creates a child by their parent's ID, name and birth_date.

        Args:
            user_id (int): The parent's ID of the child to create.
            name (str): The name of the child to create.
            birth_date (date): The birth_date ID of the child to create.

        Returns:
            Child: The created child.
        """
        child = self._schema(user_id=user_id, name=name, birth_date=birth_date)
        self.add(child)
        self.flush()
        return self._model.model_validate(child)
