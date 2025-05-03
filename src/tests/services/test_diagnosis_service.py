# type: ignore
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
    """
    Test the get_diagnosis_results method of DiagnosisService.

    This test checks if the method correctly retrieves the assessment ages
    of skill types by child's id.

    Args:
        diagnosis_service (DiagnosisService): The DiagnosisService fixture.
    """
    skill_type_id_1 = 1
    skill_type_id_2 = 2
    age_assessment_st_1 = 4
    age_assessment_st_2 = 2
    result = diagnosis_service._get_diagnosis_results(2)
    assert len(result) == 2
    assert result[skill_type_id_1] == age_assessment_st_1
    assert result[skill_type_id_2] == age_assessment_st_2


def test_start_diagnosis(diagnosis_service: DiagnosisService):
    """
    Test the start_diagnosis method of DiagnosisService.

    This test checks if the method correctly retrieves a list of skills
    by the age of the child.

    Args:
        diagnosis_service (DiagnosisService): The DiagnosisService fixture.
    """
    child_id = 2
    result = diagnosis_service.start_diagnosis(child_id)
    assert len(result) == 3


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
    """
    Test the submit_question method of DiagnosisService.

    This test checks if the method correctly creates a skill mastered status.

    Args:
        diagnosis_service (DiagnosisService): The DiagnosisService fixture.
    """
    child_id = 2
    skill_id = 2
    skill_type_id = 2
    answer = True
    result = diagnosis_service.submit_question(
        child_id, skill_id, skill_type_id, answer
    )
    assert result.child_id == child_id
    assert result.skill_id == skill_id
    assert result.skill_type_id == skill_type_id
    assert result.mastered == answer


def test_finish_diagnosis(diagnosis_service: DiagnosisService):
    """
    Test the finish_diagnosis method of DiagnosisService.

    This test checks if the method correctly retrieves the results of the diagnosis.

    Args:
        diagnosis_service (DiagnosisService): The DiagnosisService fixture.
    """
    child_id = 2
    result = diagnosis_service.finish_diagnosis(child_id)
    assert result["child_name"] == "Jane"
    assert result["child_age"] == 5
    assert len(result["skill_types_age"]) == 2
    assert len(result["skill_mastered"]) == 4
