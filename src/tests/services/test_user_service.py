import pytest
from sqlalchemy.orm import Session

from src.models.domain.models import User
from src.repos.user import UserRepository
from src.services.user_service import UserService
from src.tests.conftest import db_session


@pytest.fixture
def user_service(db_session: Session) -> UserService:
    """
    Fixture that provides an instance of UserService for use in tests.

    Args:
        db_session (Session): The SQLAlchemy session fixture.

    Returns:
        UserService: An instance of UserService.
    """
    user_repository = UserRepository(db_session)
    return UserService(user_repository)


def test_get_user_by_telegram_id(user_service: UserService):
    """
    Test the get_user_by_telegram_id method of UserService.

    This test checks if the method correctly retrieves a user by their
    telegram_id.

    Args:
        user_service (UserService): The UserService fixture.
    """
    telegram_id = 123456789
    user = user_service.get_user_by_telegram_id(telegram_id)
    assert user is not None
    assert user.telegram_id == telegram_id


def test_get_user_by_telegram_id_not_found(user_service: UserService):
    """
    Test the get_user_by_telegram_id method of UserService when the user
    is not found.

    This test checks if the method correctly returns None when a user with
    the specified telegram_id does not exist.

    Args:
        user_service (UserService): The UserService fixture.
    """
    telegram_id = 111111111
    user = user_service.get_user_by_telegram_id(telegram_id)
    assert user is None
