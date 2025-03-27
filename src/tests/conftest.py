from collections.abc import Generator

import pytest
from sqlalchemy.orm import Session

from src.models.database.models import Base
from src.tests.seed_data import SEED_DATA
from src.tests.test_helpers import create_in_memory_database


@pytest.fixture(scope="function")
def db_session() -> Generator[Session]:
    """
    Fixture that provides a SQLAlchemy session for use in tests.

    This fixture creates an in-memory SQLite database session and populates
    it with the provided seed data. The session is scoped to the entire test
    session, so it will be reused across multiple tests.

    Returns:
        Session: A SQLAlchemy session object.
    """
    # Create an in-memory database and populate it with seed data
    db = create_in_memory_database(SEED_DATA)
    yield db
    db.close()


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db(db_session: Session):
    """
    Fixture that sets up and tears down the database for each test function.

    This fixture ensures that the database is in a clean state before each
    test function runs. It rolls back any changes made during the test and
    re-populates the database with the seed data.

    Args:
        db_session (Session): The SQLAlchemy session fixture.
    """
    # Begin a new transaction
    transaction = db_session.begin_nested()
    yield
    # Roll back the transaction after the test function completes
    transaction.rollback()
    # Re-populate the database with seed data
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()
    create_in_memory_database(SEED_DATA)
