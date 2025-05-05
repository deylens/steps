# type: ignore
import pytest
from sqlalchemy.orm import Session

from src.repos.child import ChildRepository
from src.repos.diagnosis import DiagnosisRepository
from src.repos.skill import SkillRepository
from src.services.recommendation_service import RecommendationService
from src.tests.conftest import db_session


@pytest.fixture
def recommendation_service(db_session: Session) -> RecommendationService:
    """
    Fixture that provides an instance of RecommendationService for use in tests.

    Args:
        db_session (Session): The SQLAlchemy session fixture.

    Returns:
        RecommendationService: An instance of RecommendationService.
    """
    child_repository = ChildRepository(db_session)
    skill_repository = SkillRepository(db_session)
    diagnosis_repository = DiagnosisRepository(db_session)
    return RecommendationService(
        child_repository, skill_repository, diagnosis_repository
    )


def test_get_recommendations(recommendation_service: RecommendationService):
    """
    Test the get_recommendations method of RecommendationService.

    This test checks if the method correctly retrieves skills recommendations
    by child's id.

    Args:
        recommendation_service (RecommendationService): The RecommendationService fixture.
    """
    child_id = 2
    recommendations = recommendation_service.get_recommendations(child_id)
    assert len(recommendations) > 0
    assert len(recommendations) == 1
