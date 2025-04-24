import datetime

from src.repos.child import ChildRepository
from src.repos.diagnosis import DiagnosisRepository
from src.repos.skill import SkillRepository


class RecommendationService:
    def __init__(
        self,
        child_repository: ChildRepository,
        skill_repository: SkillRepository,
        diagnosis_repository: DiagnosisRepository,
    ):
        self.child_repository = child_repository
        self.skill_repository = skill_repository
        self.diagnosis_repository = diagnosis_repository

    def get_recommendations(
        self, child_id: int, date: datetime.date | None
    ) -> list[str]:
        """Retrieves a list of recommendations by child's id."""
        results = []
        skill_types = self.skill_repository.get_skill_types()

        for skill_type in skill_types:
            if diagnosis := self.diagnosis_repository.get_diagnosis(
                child_id, skill_type.id
            ):
                results.append(diagnosis)

        if not results:
            return []

        child = self.child_repository.get_child(child_id)
        mastered = self.diagnosis_repository.mastered_skill(
            child_id=child_id, date=date
        )
        if child:
            skill_type_age = {
                result.skill_types_id: result.age_assessment for result in results
            }
            skills = self.skill_repository.get_skills_list()
            skills.sort(
                key=lambda skill: skill.age_actual if skill.age_actual else float("inf")
            )
            recommendations = []
            mastered = self.diagnosis_repository.mastered_skill(
                child_id=child_id, date=date
            )
            for skill in skills:
                if skill.skill_type_id in skill_type_age:
                    if (
                        skill.age_actual is not None
                        and child.age_months >= skill.age_actual
                        and skill.age_actual > skill_type_age[skill.skill_type_id]  # type: ignore
                        and mastered.get(skill.id) == False
                    ):
                        recommendations.append(skill.recommendation)

            return recommendations
        else:
            raise ValueError("Child not found")
