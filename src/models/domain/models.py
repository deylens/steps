from datetime import date

from pydantic import BaseModel, computed_field


class Base(BaseModel):
    """Base model with common pydantic configuration."""

    class Config:
        orm_mode = True
        from_attributes = True


class User(Base):
    """User model representing a user in the system."""

    id: int
    telegram_id: int
    children: list["Child"] = []


class Child(Base):
    """Child model representing a child associated with a user."""

    id: int
    user_id: int
    name: str
    birth_date: date
    diagnosis_history: list["DiagnosisHistory"] = []

    @computed_field  # type: ignore
    @property
    def age_months(self) -> int:
        today = date.today()
        years_diff = today.year - self.birth_date.year
        months_diff = today.month - self.birth_date.month
        full_months = years_diff * 12 + months_diff

        if today.day < self.birth_date.day:
            full_months -= 1

        return full_months

    diagnosis_result: list["DiagnosisResult"] = []


class SkillType(Base):
    """SkillType model representing a type of skill."""

    id: int
    name: str
    skill: list["Skill"] = []
    diagnosis_result: list["DiagnosisResult"] = []
    diagnosis_history: list["DiagnosisHistory"] = []


class Skill(Base):
    """Skill model representing a specific skill."""

    id: int
    skill_type_id: int
    name: str
    criteria: str | None
    recommendation: str
    age_start: int | None
    age_end: int | None
    age_actual: int | None
    diagnosis_history: list["DiagnosisHistory"] = []


class DiagnosisHistory(Base):
    """DiagnosisHistory model representing the history of a diagnosis."""

    id: int
    skill_id: int
    skill_type_id: int
    date: date
    mastered: bool
    child_id: int


class DiagnosisResult(Base):
    """DiagnosisResult model representing the result of a diagnosis."""

    id: int
    child_id: int
    date: date
    skill_types_id: int
    age_assessment: int | None
