import json

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from config.settings import app_config
from models.database import models


def main() -> None:
    engine = create_engine(app_config.db.db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    with open("src/data.json", encoding="utf-8") as file:
        data = json.load(file)

    skill_types = {}

    for el in data:
        skill_types[el["skill_type"]] = models.SkillType(name=el["skill_type"])

    skills = []

    for el in data:
        el["name"] = el["skill"]
        del el["skill"]
        skill_type = skill_types[el["skill_type"]]
        del el["skill_type"]
        skills.append(models.Skill(skill_type=skill_type, **el))

    with Session(engine) as session:
        for item in skill_types.values():
            try:
                session.add(item)
                session.commit()
            except IntegrityError:
                session.rollback()
                continue
        for item in skills:
            try:
                session.add(item)
                session.commit()
            except IntegrityError:
                session.rollback()
                continue

    return None


if __name__ == "__main__":
    main()
    print("Done")
