from sqlalchemy import create_engine

from config.settings import app_config
from models.database.models import DiagnosisHistory, DiagnosisResult, Skill, SkillType


def main() -> None:
    engine = create_engine(app_config.db.db_url)
    DiagnosisHistory.__table__.drop(engine)
    DiagnosisResult.__table__.drop(engine)
    Skill.__table__.drop(engine)
    SkillType.__table__.drop(engine)
    SkillType.__table__.create(engine)
    Skill.__table__.create(engine)
    DiagnosisHistory.__table__.create(engine)
    DiagnosisResult.__table__.create(engine)
    print("Done")


if __name__ == "__main__":
    main()
