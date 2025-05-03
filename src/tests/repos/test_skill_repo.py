# type: ignore
import pytest
from sqlalchemy.orm import Session

from src.repos.skill import SkillRepository
from src.tests.conftest import db_session


@pytest.fixture
def skill_repository(db_session: Session) -> SkillRepository:
    """
    Fixture that provides an instance of SkillRepository for use in tests.

    Args:
        db_session (Session): The SQLAlchemy session fixture.

    Returns:
        SkillRepository: An instance of SkillRepository.
    """
    return SkillRepository(db_session)


def test_get_skills_by_age(skill_repository: SkillRepository):  # type: ignore
    """
    Test the get_skills method of SkillRepository.

    This test checks if the method correctly retrieves a list of skills
    by their age.

    Args:
        skill_repository (SkillRepository): The SkillRepository fixture.
    """
    age = 4
    skills = skill_repository.get_skills_by_age(age)
    assert len(skills) > 0
    assert len(skills) == 3
    for skill in skills:
        assert skill.age_actual <= age


def test_get_skills_by_age_not_found(skill_repository: SkillRepository):  # type: ignore
    """
    Test the get_skills method of SkillRepository when the skills
    are not found.

    This test checks if the method correctly returns empty list when skills with
    the specified age don't exist.

    Args:
        skill_repository (SkillRepository): The SkillRepository fixture.
    """
    age = -123
    skills = skill_repository.get_skills_by_age(age)
    assert skills == list()


def test_get_skill(skill_repository: SkillRepository):  # type: ignore
    """
    Test the get_skill method of SkillRepository.

    This test checks if the method correctly retrieves a skill
    by their id.

    Args:
        skill_repository (SkillRepository): The SkillRepository fixture.
    """
    skill_id = 1
    skill = skill_repository.get_skill(skill_id)
    assert skill is not None
    assert skill.id == skill_id


def test_get_skill_not_found(skill_repository: SkillRepository):  # type: ignore
    """
    Test the get_skill method of SkillRepository when the skill
    is not found.

    This test checks if the method correctly returns None when skill with
    the specified id does not exist.

    Args:
        skill_repository (SkillRepository): The SkillRepository fixture.
    """
    skill_id = -123
    skill = skill_repository.get_skill(skill_id)
    assert skill is None


def test_get_skills_list(skill_repository: SkillRepository):  # type: ignore
    """
    Test the get_skills_list method of SkillRepository.

    This test checks if the method correctly retrieves a list of all skills.

    Args:
        skill_repository (SkillRepository): The SkillRepository fixture.
    """
    skills = skill_repository.get_skills_list()
    assert len(skills) > 0
    assert len(skills) == 5


def test_get_skill_types(skill_repository: SkillRepository):  # type: ignore
    """
    Test the get_skill_types method of SkillRepository.

    This test checks if the method correctly retrieves a list of all skill types.

    Args:
        skill_repository (SkillRepository): The SkillRepository fixture.
    """
    skill_types = skill_repository.get_skill_types()
    assert len(skill_types) > 0
    assert len(skill_types) == 2
