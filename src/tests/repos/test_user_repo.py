import pytest
from sqlalchemy.orm import Session

from src.models.domain.models import User
from src.repos.user import UserRepository
from src.tests.conftest import db_session


@pytest.fixture
def user_repository(db_session: Session) -> UserRepository:
    """
    Fixture that provides an instance of UserRepository for use in tests.

    Args:
        db_session (Session): The SQLAlchemy session fixture.

    Returns:
        UserRepository: An instance of UserRepository.
    """
    return UserRepository(db_session)


def test_get_user_by_telegram_id(user_repository: UserRepository) -> None:
    """
    Test the get_user_by_telegram_id method of UserRepository.

    This test checks if the method correctly retrieves a user by their
    telegram_id.

    Args:
        user_repository (UserRepository): The UserRepository fixture.
    """
    telegram_id = 123456789
    user = user_repository.get_by_telegram_id(telegram_id)
    assert user is not None
    assert user.telegram_id == telegram_id


def test_get_user_by_telegram_id_not_found(user_repository: UserRepository) -> None:
    """
    Test the get_user_by_telegram_id method of UserRepository when the user
    is not found.

    This test checks if the method correctly returns None when a user with
    the specified telegram_id does not exist.

    Args:
        user_repository (UserRepository): The UserRepository fixture.
    """
    telegram_id = 111111111
    user = user_repository.get_by_telegram_id(telegram_id)
    assert user is None
