import datetime

import pytest
from sqlalchemy.orm import Session

from src.repos.diagnosis import DiagnosisRepository
from src.tests.conftest import db_session


@pytest.fixture
def diagnosis_repository(db_session: Session) -> DiagnosisRepository:
    """
    Fixture that provides an instance of DiagnosisRepository for use in tests.

    Args:
        db_session (Session): The SQLAlchemy session fixture.

    Returns:
        DiagnosisRepository: An instance of DiagnosisRepository.
    """
    return DiagnosisRepository(db_session)


def test_get_diagnosis(diagnosis_repository: DiagnosisRepository):
    """
    Test the get_diagnosis method of DiagnosisRepository.

    This test checks if the method correctly retrieves
    last child's diagnosis result for skill type.

    Args:
        diagnosis_repository (DiagnosisRepository): The DiagnosisRepository fixture.
    """
    child_id = 1
    skill_type_id = 1
    diagnosis = diagnosis_repository.get_diagnosis(child_id, skill_type_id)
    assert diagnosis is not None
    assert diagnosis.skill_types_id == skill_type_id


def test_get_diagnosis_not_found_skill_type(diagnosis_repository: DiagnosisRepository):
    """
    Test the get_diagnosis method of DiagnosisRepository.

    This test checks if the method correctly returns None when a diagnosis result with
    the specified skill type id does not exist.

    Args:
        diagnosis_repository (DiagnosisRepository): The DiagnosisRepository fixture.
    """
    child_id = 1
    skill_type_id = -123
    diagnosis = diagnosis_repository.get_diagnosis(child_id, skill_type_id)
    assert diagnosis is None


def test_get_diagnosis_not_found_child(diagnosis_repository: DiagnosisRepository):
    """
    Test the get_diagnosis method of DiagnosisRepository.

    This test checks if the method correctly returns None when a diagnosis result with
    the specified child id does not exist.

    Args:
        diagnosis_repository (DiagnosisRepository): The DiagnosisRepository fixture.
    """
    child_id = -123
    skill_type_id = 1
    diagnosis = diagnosis_repository.get_diagnosis(child_id, skill_type_id)
    assert diagnosis is None


def test_create_diagnosis_history(diagnosis_repository: DiagnosisRepository):
    """
    Test the create_diagnosis_history method of DiagnosisRepository.

    This test checks if the method correctly creates a diagnosis history
    by child_id, skill_id, skill_type_id and answer.

    Args:
        diagnosis_repository (DiagnosisRepository): The DiagnosisRepository fixture.
    """
    child_id = 1
    skill_id = 1
    skill_type_id = 1
    answer = True
    history = diagnosis_repository.create_diagnosis_history(
        child_id, skill_id, skill_type_id, answer
    )
    assert history is not None
    assert history.child_id == child_id
    assert history.skill_id == skill_id
    assert history.skill_type_id == skill_type_id


def test_get_diagnosis_history(diagnosis_repository: DiagnosisRepository):
    """
    Test the get_diagnosis_history method of DiagnosisRepository.

    This test checks if the method correctly returns diagnosis history with
    the specified child's id.

    Args:
        diagnosis_repository (DiagnosisRepository): The DiagnosisRepository fixture.
    """
    child_id = 1
    diagnosis_history = diagnosis_repository.get_diagnosis_history(child_id)
    assert len(diagnosis_history) > 0
    assert len(diagnosis_history) == 1
    for el in diagnosis_history:
        assert el.child_id == child_id


def test_get_diagnosis_history_not_found(diagnosis_repository: DiagnosisRepository):
    """
    Test the get_diagnosis_history method of DiagnosisRepository.

    This test checks if the method correctly returns None when a diagnosis history with
    the specified child id does not exist.

    Args:
        diagnosis_repository (DiagnosisRepository): The DiagnosisRepository fixture.
    """
    child_id = -123
    diagnosis_history = diagnosis_repository.get_diagnosis_history(child_id)
    assert diagnosis_history == list()


def test_create_diagnosis_result(diagnosis_repository: DiagnosisRepository):
    """
    Test the create_diagnosis_result method of DiagnosisRepository.

    This test checks if the method correctly creates a diagnosis result
    by child_id, skill_type_id and age_assessment.

    Args:
        diagnosis_repository (DiagnosisRepository): The DiagnosisRepository fixture.
    """
    child_id = 1
    skill_type_id = 1
    age_assessment = 5
    result = diagnosis_repository.create_diagnosis_result(
        child_id, skill_type_id, age_assessment
    )
    assert result is not None
    assert result.child_id == child_id
    assert result.skill_types_id == skill_type_id
    assert result.age_assessment == age_assessment
    assert result.date == datetime.date.today()
