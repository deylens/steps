import datetime

from sqlalchemy.sql.elements import ColumnElement

from src.models.database.models import DiagnosisHistory as DiagnosisHistorySchema
from src.models.database.models import DiagnosisResult as DiagnosisSchema
from src.models.domain.models import DiagnosisHistory, DiagnosisResult
from src.repos.base import BaseRepository


class DiagnosisRepository(BaseRepository):
    _schema = DiagnosisHistorySchema
    _model = DiagnosisHistory
    _schema_result = DiagnosisSchema
    _model_result = DiagnosisResult

    def get_diagnosis(
        self, child_id: int, skill_type_id: int
    ) -> DiagnosisResult | None:
        """
        Retrieves last child's diagnosis result for skill type.

        Args:
            child_id (int): The ID of the child.
            skill_type_id (int): The ID of the skill type.

        Returns:
            DiagnosisResult: The diagnosis result with the specified child_id
            and skill_type_id, or None if not found.
        """
        filters: list[ColumnElement] = [
            self._schema_result.child_id == child_id,
            self._schema_result.skill_types_id == skill_type_id,
        ]
        diagnosis = self._query_schema(
            schema=self._schema_result,
            filters=filters,
            order_by="date",
            order_type="desc",
            size=1,
        ).first()
        return self._model_result.model_validate(diagnosis) if diagnosis else None

    def create_diagnosis_history(
        self, child_id: int, skill_id: int, skill_type_id: int, answer: bool
    ) -> DiagnosisHistory:
        """
        Creates diagnosis history for child's skill.

        Args:
            child_id (int): The ID of the child.
            skill_id (int): The ID of the skill.
            skill_type_id (int): The ID of the skill type.
            answer (bool): Skill mastered.

        Returns:
            DiagnosisHistory: The created diagnosis history.
        """
        history = self._schema(
            child_id=child_id,
            skill_id=skill_id,
            skill_type_id=skill_type_id,
            mastered=answer,
            date=datetime.date.today(),
        )
        self.add(history)
        self.flush()
        return self._model.model_validate(history)

    def get_diagnosis_history(self, child_id: int) -> list[DiagnosisHistory]:
        """
        Retrieves child's diagnosis history.

        Args:
            child_id (int): The ID of the child.

        Returns:
            list[DiagnosisHistory]: The diagnosis history list with the specified child_id
            or empty list if not found.
        """
        filters: list[ColumnElement] = [self._schema.child_id == child_id]
        diagnosis_history = self._query(filters=filters).all()
        return [self._model.model_validate(el) for el in diagnosis_history]

    def create_diagnosis_result(
        self, child_id: int, skill_type_id: int, age_assessment: int
    ) -> DiagnosisResult:
        """
        Creates diagnosis result for child's skill type.

        Args:
            child_id (int): The ID of the child.
            skill_type_id (int): The ID of the skill type.
            age_assessment (int): Assessment age.

        Returns:
            DiagnosisResult: The created diagnosis result.
        """
        result = self._schema_result(
            child_id=child_id,
            skill_types_id=skill_type_id,
            age_assessment=age_assessment,
            date=datetime.date.today(),
        )
        self.add(result)
        self.flush()
        return self._model_result.model_validate(result)

    def mastered_skill(
        self, child_id: int, date: datetime.date | None
    ) -> dict[int, bool]:
        """
        Checks if a skill is mastered by a child.

        Args:
            child_id (int): The ID of the child.
            date (datetime.datetime): Date for filters, or None for all

        Returns:
            dict: skill_id as key and mastered as value
        """
        filters = (
            [self._schema.child_id == child_id, self._schema.date == date]
            if date
            else [self._schema.child_id == child_id]
        )
        res = self._query(filters=filters, order_by="date DESC").all()
        result_dict: dict[int, bool] = {}
        if not res:
            return result_dict
        for item in res:
            result_dict[item.skill_id] = item.mastered
        return result_dict
