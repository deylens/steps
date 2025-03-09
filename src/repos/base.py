from typing import Any

from sqlalchemy.orm import Query, Session
from sqlalchemy.sql import text
from sqlalchemy.sql.elements import BinaryExpression


class BaseRepository:
    """Base repository used to abstract away related queries.

    The only requirement is that this class is extended by your own
    class and the _schema and _model private class attributes are overwritten.
    There should be one repository per entity and any specific queries
    should be written in the child repository.
    """

    _schema: type | None = None  # SQLAlchemy model
    _model: type | None = None  # Pydantic model

    def __init__(self, db: Session) -> None:
        """Instantiate the repository with a db session.

        Args:
            db: A sqlalchemy.orm.session.Session object.
        """
        self._db: Session = db

    def get(self, entity_id: int) -> Any:
        """Return a _schema by its primary key id.

        Args:
            entity_id: The id of the entity you want to find.

        Returns:
            obj: An individual _schema instance.
        """
        return self._db.query(self._schema).get(entity_id)

    def all(self) -> list[Any]:
        """Return all _schemas.

        Returns:
            A list of _schema instances.
        """
        return self._db.query(self._schema).all()  # type: ignore

    def add(self, entity: type) -> None:
        """Add an entity to the current session.

        Args:
            entity: An entity to add.
        """
        self._db.add(entity)

    def commit(self) -> None:
        """Commit all changes to persistence."""
        self._db.commit()

    def _query(
        self,
        filters: list[BinaryExpression] = None,
        joins: list = None,
        order_by: str = None,
        order_type: str = None,
        size: int = 50,
        page: int = None,
    ) -> Query:
        """Query wrapper to pre-process for given arguments.

        Args:
            filters: A list of filters for the query.
            joins: A list of joins for the query.
            order_by: Set an order field for the returned items.
            order_type: Define the order type for the returned items.
            size: Limits the amount of items returned. Defaults to 50.
            page: Page to start returning items from.

        Returns:
            A sqlalchemy.orm.query.Query object.
        """
        query: Query = self._db.query(self._schema)

        if filters:
            for query_filter in filters:
                query = query.filter(query_filter)

        if joins:
            for join in joins:
                query = query.join(join)

        if order_by:
            query = query.order_by(text(f"{order_by} {order_type or 'desc'}"))

        if size:
            query = query.limit(size)

        if page:
            query = query.offset((page - 1) * size)

        return query
