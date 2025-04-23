from sqlalchemy import and_, or_
from sqlalchemy.sql.elements import ColumnElement

from src.models.database.models import Skill as SkillSchema
from src.models.database.models import SkillType as SkillTypeSchema
from src.models.domain.models import Skill, SkillType
from src.repos.base import BaseRepository


class SkillRepository(BaseRepository):
    _schema = SkillSchema
    _model = Skill
    _schema_skill_type = SkillTypeSchema
    _model_skill_type = SkillType

    def get_skills_by_age(self, age: int) -> list[Skill]:
        """
        Retrieves a list of skills by its age.

        Args:
            age (int): The age of the skills to retrieve.

        Returns:
            list[Skill]: The list of skills with the specified age, or empty list if not found.
        """
        filters: list[ColumnElement] = [
            and_(self._schema.age_start <= age, self._schema.age_end >= age)
        ]
        skills = self._query(filters=filters).limit(200).all()
        return [self._model.model_validate(skill) for skill in skills]

    def get_skill(self, skill_id: int) -> Skill | None:
        """
        Retrieves a skill by its id.

        Args:
            skill_id (int): The ID of the skill to retrieve.

        Returns:
            Skill: The skill with the specified ID, or None if not found.
        """
        filters: list[ColumnElement] = [self._schema.id == skill_id]
        skill = self._query(filters=filters).first()
        return self._model.model_validate(skill) if skill else None

    def get_skills_list(self) -> list[Skill]:
        """
        Retrieves a list of all skills.

        Args:

        Returns:
            list[Skill]: The list of all skills.
        """
        skills = self.all()
        return [self._model.model_validate(skill) for skill in skills]

    def get_skill_types(self) -> list[SkillType]:
        """
        Retrieves a list of all skill types.

        Args:

        Returns:
            list[SkillType]: The list of all skills.
        """
        skill_types = self._query_schema(self._schema_skill_type).all()
        return [
            self._model_skill_type.model_validate(skill_type)
            for skill_type in skill_types
        ]
