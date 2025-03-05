from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config.settings import app_config
from src.repos.user import UserRepository
from src.services.user_service import UserService

engine = create_engine(app_config.db.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session]:
    """
    Provides a SQLAlchemy session.

    This function is used to provide a database session. It ensures that the
    session is properly closed after use.

    Yields:
        Session: A SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repository() -> UserRepository:
    """Provides an instance of UserRepository."""
    db = next(get_db())
    return UserRepository(db)


def get_user_service() -> UserService:
    """Provides an instance of UserService."""
    user_repository = get_user_repository()
    return UserService(user_repository)
