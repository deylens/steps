from datetime import datetime

import pytest
from sqlalchemy.orm import Session

from src.repos.child import ChildRepository
from src.tests.conftest import db_session


@pytest.fixture
def child_repository(db_session: Session) -> ChildRepository:
    """
    Fixture that provides an instance of ChildRepository for use in tests.

    Args:
        db_session (Session): The SQLAlchemy session fixture.

    Returns:
        ChildRepository: An instance of ChildRepository.
    """
    return ChildRepository(db_session)


def test_get_child(child_repository: ChildRepository):
    """
    Test the get_child method of ChildRepository.

    This test checks if the method correctly retrieves a child by their id.

    Args:
        child_repository (ChildRepository): The ChildRepository fixture.
    """
    child_id = 1
    child = child_repository.get_child(child_id)
    assert child is not None
    assert child.id == child_id


def test_get_child_not_found(child_repository: ChildRepository):
    """
    Test the get_child method of ChildRepository when the child
    is not found.

    This test checks if the method correctly returns None when a child with
    the specified id does not exist.

    Args:
        child_repository (ChildRepository): The ChildRepository fixture.
    """
    child_id = -123
    child = child_repository.get_child(child_id)
    assert child is None


def test_get_children(child_repository: ChildRepository):
    """
    Test the get_children method of ChildRepository.

    This test checks if the method correctly retrieves a list of child
    by their parent's id.

    Args:
        child_repository (ChildRepository): The ChildRepository fixture.
    """
    user_id = 1
    children = child_repository.get_children(user_id)
    assert len(children) > 0
    assert len(children) == 2
    for child in children:
        assert child.user_id == user_id


def test_get_children_not_found(child_repository: ChildRepository):
    """
    Test the get_children method of ChildRepository when the children
    are not found.

    This test checks if the method correctly returns empty list when children with
    the specified parent's id don't exist.

    Args:
        child_repository (ChildRepository): The ChildRepository fixture.
    """
    user_id = -123
    children = child_repository.get_children(user_id)
    assert children == list()


def test_create_child(child_repository: ChildRepository):
    """
    Test the create_child method of ChildRepository.

    This test checks if the method correctly creates a child
    by their parent's id, name and birth_date.

    Args:
        child_repository (ChildRepository): The ChildRepository fixture.
    """
    user_id = 1
    name = "Test Child"
    birth_date = datetime.strptime("2021-01-01", "%Y-%m-%d").date()
    child = child_repository.create_child(user_id, name, birth_date)
    assert child is not None
    assert child.user_id == user_id
    assert child.name == name
    assert child.birth_date == birth_date
