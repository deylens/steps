from datetime import datetime

import pytest
from sqlalchemy.orm import Session

from src.repos.child import ChildRepository
from src.services.child_service import ChildService
from src.tests.conftest import db_session


@pytest.fixture
def child_service(db_session: Session) -> ChildService:
    """
    Fixture that provides an instance of ChildService for use in tests.

    Args:
        db_session (Session): The SQLAlchemy session fixture.

    Returns:
        ChildService: An instance of ChildService.
    """
    child_repository = ChildRepository(db_session)
    return ChildService(child_repository)


def test_get_child(child_service: ChildService):
    """
    Test the get_child method of ChildService.

    This test checks if the method correctly retrieves a child by their id.

    Args:
        child_service (ChildService): The ChildService fixture.
    """
    child_id = 1
    child = child_service.get_child(child_id)
    assert child is not None
    assert child.id == child_id


def test_get_child_not_found(child_service: ChildService):
    """
    Test the get_child method of ChildService when the user
    is not found.

    This test checks if the method correctly returns None when a child with
    the specified id does not exist.

    Args:
        child_service (ChildService): The ChildService fixture.
    """
    child_id = -123
    child = child_service.get_child(child_id)
    assert child is None


def test_get_children(child_service: ChildService):
    """
    Test the get_child method of ChildService.

    This test checks if the method correctly retrieves a list of child
    by their parent's id.

    Args:
        child_service (ChildService): The ChildService fixture.
    """
    user_id = 1
    children = child_service.get_children(user_id)
    assert len(children) > 0
    assert len(children) == 2
    for child in children:
        assert child.user_id == user_id


def test_get_children_not_found(child_service: ChildService):
    """
    Test the get_child method of ChildService when the user
    is not found.

    This test checks if the method correctly returns empty list when children with
    the specified parent's id don't exist.

    Args:
        child_service (ChildService): The ChildService fixture.
    """
    user_id = -123
    children = child_service.get_children(user_id)
    assert children == list()


def test_add_child(child_service: ChildService):
    """
    Test the get_child method of ChildService when the user
    is not found.

    This test checks if the method correctly creates a child
    by their parent's id, name and birth_date.

    Args:
        child_service (ChildService): The ChildService fixture.
    """
    user_id = 1
    name = "Test Child"
    birth_date = datetime.strptime("2021-01-01", "%Y-%m-%d").date()
    child = child_service.add_child(user_id, name, birth_date)
    assert child is not None
    assert child.user_id == user_id
    assert child.name == name
    assert child.birth_date == birth_date
