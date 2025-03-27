from src.models.domain.models import DiagnosisHistory, DiagnosisResult, Skill
from src.repos.child import ChildRepository
from src.repos.diagnosis import DiagnosisRepository
from src.repos.skill import SkillRepository
from src.tests.repos.test_skill_repo import skill_repository


class DiagnosisService:
    def __init__(
        self,
        diagnosis_repository: DiagnosisRepository,
        child_repository: ChildRepository,
        skill_repository: SkillRepository,
    ):
        self.diagnosis_repository = diagnosis_repository
        self.child_repository = child_repository
        self.skill_repository = skill_repository

    def _get_diagnosis_results(self, child_id) -> dict:
        """Retrieves the assessment ages of skill types by child's id."""
        skill_types = self.skill_repository.get_skill_types()
        result = {}

        for skill_type in skill_types:
            if diagnosis := self.diagnosis_repository.get_diagnosis(
                child_id, skill_type.id
            ):
                result[skill_type.id] = diagnosis.age_assessment
            else:
                result[skill_type.id] = 0

        return result

    def start_diagnosis(self, child_id: int) -> list[Skill]:
        """Retrieves a list of skills by the age of the child."""
        child = self.child_repository.get_child(child_id)
        return self.skill_repository.get_skills_by_age(child.age_months)

    def save_diagnosis(self, child_id: int, result: dict) -> list[DiagnosisResult]:
        """Saves the results of the diagnosis."""
        skills = self.skill_repository.get_skills_list()
        skill_type_dict = {skill.id: skill.skill_type_id for skill in skills}
        skill_age_dict = {skill.id: skill.age_actual for skill in skills}
        child_skill_types_age = {skill.skill_type_id: 0 for skill in skills}
        skill_type_age_skill_mastered = []

        for key, value in result.items():
            skill_type_age_skill_mastered.append(
                [skill_type_dict[int(key)], skill_age_dict[int(key)], int(key), value]
            )
        skill_type_age_skill_mastered.sort(key=lambda el: (el[0], el[1]))

        for el in skill_type_age_skill_mastered:
            if not el[3] and (el[1] >= child_skill_types_age[el[0]]):
                break
            if el[3] and (el[1] >= child_skill_types_age[el[0]]):
                child_skill_types_age[el[0]] = el[1]

        diagnosis_results = []

        for key, value in child_skill_types_age.items():
            diagnosis_results.append(
                self.diagnosis_repository.create_diagnosis_result(child_id, key, value)
            )

        self.diagnosis_repository.commit()
        return diagnosis_results

    def submit_question(
        self, child_id: int, skill_id: int, skill_type: int, answer: bool
    ) -> DiagnosisHistory:
        """Save the skill mastered status."""
        diagnosis = self.diagnosis_repository.create_diagnosis_history(
            child_id, skill_id, skill_type, answer
        )
        self.diagnosis_repository.commit()
        return diagnosis

    def finish_diagnosis(self, child_id: int) -> dict:
        """Retrieves the results of the diagnosis."""
        child = self.child_repository.get_child(child_id)
        skill_types = self.skill_repository.get_skill_types()
        skill_types_id_name = {skill.id: skill.name for skill in skill_types}
        diagnosis_results = self._get_diagnosis_results(child_id)
        skill_types_age = {
            skill_types_id_name[key]: value for key, value in diagnosis_results.items()
        }
        skill_history = self.diagnosis_repository.get_diagnosis_history(child_id)
        skill_mastered = {}

        if skill_history:
            skill_history.sort(key=lambda el: el.date)
            last_date = skill_history[-1].date
            for el in skill_history:
                if el.date == last_date:
                    skill_mastered[el.skill_id] = el.mastered

        return {
            "child_name": child.name,
            "child_age": child.age_months,
            "skill_types_age": skill_types_age,
            "skill_mastered": skill_mastered,
        }
