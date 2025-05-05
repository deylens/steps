from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config.settings import app_config
from src.repos.child import ChildRepository
from src.repos.diagnosis import DiagnosisRepository
from src.repos.skill import SkillRepository
from src.repos.user import UserRepository
from src.services.child_service import ChildService
from src.services.diagnosis_service import DiagnosisService
from src.services.recommendation_service import RecommendationService
from src.services.user_service import UserService

engine = create_engine(app_config.db.db_url, pool_size=20, max_overflow=20)
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


def get_child_repository() -> ChildRepository:
    """Provides an instance of ChildRepository."""
    db = next(get_db())
    return ChildRepository(db)


def get_child_service() -> ChildService:
    """Provides an instance of ChildService."""
    child_repository = get_child_repository()
    return ChildService(child_repository)


def get_diagnosis_repository() -> DiagnosisRepository:
    """Provides an instance of DiagnosisRepository."""
    db = next(get_db())
    return DiagnosisRepository(db)


def get_skill_repository() -> SkillRepository:
    db = next(get_db())
    return SkillRepository(db)


def get_diagnosis_service() -> DiagnosisService:
    """Provides an instance of DiagnosisService."""
    diagnosis_repository = get_diagnosis_repository()
    child_repository = get_child_repository()
    skill_repository = get_skill_repository()
    return DiagnosisService(diagnosis_repository, child_repository, skill_repository)


def get_recommendation_service() -> RecommendationService:
    """Provides an instance of RecommendationService."""
    diagnosis_repository = get_diagnosis_repository()
    child_repository = get_child_repository()
    skill_repository = get_skill_repository()
    return RecommendationService(
        child_repository, skill_repository, diagnosis_repository
    )
