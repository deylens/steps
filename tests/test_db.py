import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.models import Base, User, Child

DATABASE_URL_TEST = "postgresql://test_postgres:test_postgres@localhost:5435/test_steps_db"


@pytest.fixture(scope='function')
def db_session():
    """func with fixture for create data and drop after test"""
    engine = create_engine(DATABASE_URL_TEST)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind = engine)
    session = Session()

    yield session

    session.rollback()
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()



def test_create_data(db_session):
    user = User(telegram_id = 12345)
    db_session.add(user)
    db_session.commit()

    result = db_session.query(User).filter_by(telegram_id=12345).first()

    assert result is not None
    assert result.telegram_id == 12345