from datetime import date

from src.models.domain.models import Child
from src.repos.child import ChildRepository


class ChildService:
    def __init__(self, child_repository: ChildRepository):
        self.child_repository = child_repository

    def get_child(self, child_id: int) -> Child | None:
        """Retrieves a child by their ID."""
        return self.child_repository.get_child(child_id)

    def get_children(self, user_id: int) -> list[Child]:
        """Retrieves a list of children by their parent's ID."""
        return self.child_repository.get_children(user_id)

    def add_child(self, user_id: int, name: str, birth_date: date) -> Child:
        """Creates a child by their parent's ID, name and birth_date."""
        child = self.child_repository.create_child(user_id, name, birth_date)
        self.child_repository.commit()
        return child
