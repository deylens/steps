from models.database.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_in_memory_database(tables: list = None) -> Session:
    """
    Create an in-memory SQLAlchemy session for use in tests.

    This function creates an in-memory SQLite database session for testing
    purposes. It can be used to create tables for the specified models.

    Args:
        tables (list): List of SQLAlchemy model classes to create tables for.

    Returns:
        Session: A SQLAlchemy session object.
    """
    engine = create_engine("sqlite:///:memory:")
    session = sessionmaker(bind=engine)()

    if tables:
        Base.metadata.create_all(engine, tables=[table.__table__ for table in tables])
    else:
        Base.metadata.create_all(engine)

    return session


def create_in_memory_database(data: dict) -> Session:
    """
    Create an in-memory database populated with data.

    This function creates an in-memory SQLite database session and populates
    it with the provided data.

    Example data:
        {
            User: [
                {'id': 1, 'telegram_id': 123456789},
                {'id': 2, 'telegram_id': 987654321}
            ],
            Child: [
                {'id': 1, 'user_id': 1, 'name': 'John', 'birth_date': '2020-01-01'},
                {'id': 2, 'user_id': 2, 'name': 'Jane', 'birth_date': '2019-05-15'}
            ],
        }

    Args:
        data (dict): Dictionary of SQLAlchemy models and their data.

    Returns:
        Session: A populated SQLAlchemy session object.
    """
    db = get_in_memory_database(tables=list(data.keys()))

    for model, records in data.items():
        db.bulk_insert_mappings(model, records)

    db.commit()

    return db
