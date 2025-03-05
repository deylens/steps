from datetime import date

from src.models.database.models import (
    Base,
    Child,
    DiagnosisHistory,
    DiagnosisResult,
    Skill,
    SkillType,
    User,
)

SEED_DATA = {
    User: [{"id": 1, "telegram_id": 123456789}, {"id": 2, "telegram_id": 987654321}],
    Child: [
        {"id": 1, "user_id": 1, "name": "John", "birth_date": date(2020, 1, 1)},
        {"id": 2, "user_id": 2, "name": "Jane", "birth_date": date(2019, 5, 15)},
    ],
    SkillType: [{"id": 1, "name": "Cognitive"}, {"id": 2, "name": "Motor"}],
    Skill: [
        {
            "id": 1,
            "skill_type_id": 1,
            "name": "Counting",
            "criteria": "Count to 10",
            "recommendation": "Practice counting objects",
            "age_start": 3,
            "age_end": 5,
            "age_actual": 4,
        },
        {
            "id": 2,
            "skill_type_id": 2,
            "name": "Jumping",
            "criteria": "Jump with both feet",
            "recommendation": "Practice jumping exercises",
            "age_start": 2,
            "age_end": 4,
            "age_actual": 3,
        },
    ],
    DiagnosisHistory: [
        {
            "id": 1,
            "skill_id": 1,
            "skill_type_id": 1,
            "date": date(2023, 1, 1),
            "mastered": True,
            "child_id": 1,
        },
        {
            "id": 2,
            "skill_id": 2,
            "skill_type_id": 2,
            "date": date(2023, 2, 1),
            "mastered": False,
            "child_id": 2,
        },
    ],
    DiagnosisResult: [
        {
            "id": 1,
            "child_id": 1,
            "date": date(2023, 3, 1),
            "skill_types_id": 1,
            "age_assessment": 4,
        },
        {
            "id": 2,
            "child_id": 2,
            "date": date(2023, 4, 1),
            "skill_types_id": 2,
            "age_assessment": 3,
        },
    ],
}
