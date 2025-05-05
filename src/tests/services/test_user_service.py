# type: ignore
import pytest
from sqlalchemy.orm import Session

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


def test_get_user(user_service: UserService):
    """
    Test the get_user of UserService.

    This test checks if the method correctly retrieves a user by their id.

    Args:
        user_service (UserService): The UserService fixture.
    """
    user_id = 1
    user = user_service.get_user(user_id)
    assert user is not None
    assert user.id == user_id


def test_get_user_not_found(user_service: UserService):
    """
    Test the get_user method of UserService when the user
    is not found.

    This test checks if the method correctly returns None when a user with
    the specified id does not exist.

    Args:
        user_service (UserService): The UserService fixture.
    """
    user_id = -123
    user = user_service.get_user(user_id)
    assert user is None


def test_register_user(user_service: UserService):
    """
    Test the register_user method of UserService.

    This test checks if the method correctly creates a user by their
    telegram_id.

    Args:
        user_service (UserService): The UserService fixture.
    """
    telegram_id = 111111111
    user = user_service.register_user(telegram_id)
    assert user is not None
    assert user.telegram_id == telegram_id


def test_register_user_not_unique(user_service: UserService):
    """
    Test the register_user method of UserService.

    This test checks if the method correctly returns existing user.

    Args:
        user_service (UserService): The UserService fixture.
    """
    telegram_id = 123456789
    user = user_service.register_user(telegram_id)
    assert user is not None
    assert user.telegram_id == telegram_id
