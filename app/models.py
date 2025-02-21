
from sqlalchemy import Integer,BigInteger, Column, Boolean,String,Text,Date,ForeignKey,create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,autoincrement=True)
    telegram_id = Column(BigInteger,unique=True)
    childrens = relationship('Children',back_populates='user')

    def __repr__(self):
        return f"{self.telegram_id}"
    
class Children(Base):
    __tablename__ = 'childrens'

    id = Column(Integer,primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)

    user = relationship('User',back_populates='childrens')
    diagnosis_history = relationship("DiagnosisHistory",back_populates='child')
    diagnosis_result = relationship("DiagnosisResult",back_populates='child')

    def __repr__(self):
        return f'{self.user_id}, {self.name} {self.birth_date}'

class SkillTypes(Base):
    __tablename__ = 'skill_types'

    id = Column(Integer,primary_key=True, autoincrement=True)
    name = Column(String, unique=True, index=True)

    skills = relationship("Skills",back_populates='skill_type')
    diagnosis_result = relationship("DiagnosisResult",back_populates='skill_type')
    diagnosis_history = relationship("DiagnosisHistory",back_populates='skill_type')

    def __repr__(self):
        return f"{self.name}"
    
class Skills(Base):
    __tablename__ = 'skills'

    id = Column(Integer,primary_key=True, autoincrement=True)
    skill_type_id = Column(Integer, ForeignKey('skill_types.id'), nullable=False)
    name = Column(String, nullable=False)
    criteria = Column(Text)
    recommendation = Column(Text, nullable=False)
    age_start = Column(Integer)
    age_end = Column(Integer)
    actual_age = Column(Integer)

    skill_type = relationship("SkillTypes", back_populates='skills')
    diagnosis_history = relationship("DiagnosisHistory",back_populates='skill')
   


    def __repr__(self):
        return f"{self.name}"

class DiagnosisHistory(Base):
    __tablename__ = 'diagnosis_history'

    id = Column(Integer,primary_key=True, autoincrement=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    skill_type_id = Column(Integer, ForeignKey("skill_types.id"), nullable=False)
    date = Column(Date)
    mastered = Column(Boolean)
    child_id = Column(Integer, ForeignKey('childrens.id'), nullable=False)

    skill = relationship("Skills", back_populates='diagnosis_history')
    skill_type = relationship("SkillTypes", back_populates='diagnosis_history')
    child = relationship("Children", back_populates='diagnosis_history')

    def __repr__(self):
        return f"{self.child_id} {self.skill} {self.mastered}"
    
class DiagnosisResult(Base):
    __tablename__ = 'diagnosis_result'

    id = Column(Integer,primary_key=True, autoincrement=True)
    child_id = Column(Integer, ForeignKey('childrens.id'), nullable=False)
    date = Column(Date)
    skill_types_id = Column(Integer, ForeignKey("skill_types.id"), nullable=False)
    age_assessment = Column(Integer)

    skill_type = relationship("SkillTypes",back_populates='diagnosis_result')
    child = relationship('Children',back_populates='diagnosis_result')


    def __repr__(self):
        return f"{self.child_id} {self.skill_type_id} {self.age_assessment}"




DATABASE_URL_TEST = "postgresql://test_postgres:test_postgres@localhost:5435/test_steps_db"
engine = create_engine(DATABASE_URL_TEST)

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)