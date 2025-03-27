import pytest
from sqlalchemy.orm import Session

from src.repos.child import ChildRepository
from src.repos.diagnosis import DiagnosisRepository
from src.repos.skill import SkillRepository
from src.services.diagnosis_service import DiagnosisService
from src.tests.conftest import db_session


@pytest.fixture
def diagnosis_service(db_session: Session) -> DiagnosisService:
    """
    Fixture that provides an instance of DiagnosisService for use in tests.

    Args:
        db_session (Session): The SQLAlchemy session fixture.

    Returns:
        DiagnosisService: An instance of DiagnosisService.
    """
    diagnosis_repository = DiagnosisRepository(db_session)
    child_repository = ChildRepository(db_session)
    skill_repository = SkillRepository(db_session)
    return DiagnosisService(diagnosis_repository, child_repository, skill_repository)


def test_get_diagnosis_results(diagnosis_service: DiagnosisService):
    pass


def test_start_diagnosis(diagnosis_service: DiagnosisService):
    pass


def test_save_diagnosis(diagnosis_service: DiagnosisService):
    """
    Test the save_diagnosis method of DiagnosisService.

    This test checks if the method correctly retrieves skills recommendations
    by child's id.

    Args:
        diagnosis_service (DiagnosisService): The DiagnosisService fixture.
    """
    child_id = 1
    result = {1: True, 2: True, 3: True, 4: False, 5: True}
    results = diagnosis_service.save_diagnosis(child_id, result)
    assert len(results) == 2
    assert results[0].age_assessment == 4
    assert results[1].age_assessment == 3


def test_submit_question(diagnosis_service: DiagnosisService):
    pass


def test_finish_diagnosis(diagnosis_service: DiagnosisService):
    pass
