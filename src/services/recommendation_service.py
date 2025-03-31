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

    def get_recommendations(self, child_id: int) -> list[str]:
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
        skill_type_age = {
            result.skill_types_id: result.age_assessment for result in results
        }
        skills = self.skill_repository.get_skills_list()
        skills.sort(key=lambda skill: skill.age_actual)
        recommendations = []

        for skill in skills:
            if skill.skill_type_id in skill_type_age:
                if (
                    child.age_months
                    >= skill.age_actual
                    > skill_type_age[skill.skill_type_id]
                ):
                    recommendations.append(skill.recommendation)

        return recommendations
