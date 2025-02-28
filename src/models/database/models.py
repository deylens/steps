from sqlalchemy import Integer, BigInteger, Column, Boolean, String, Text, Date,ForeignKey, create_engine, MetaData
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase

class Base(DeclarativeBase):
    metadata = MetaData()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True)
    children = relationship('Child', back_populates='user')

    def __repr__(self):
        return f"User <{self.telegram_id}>"
    
class Child(Base):
    __tablename__ = 'children'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    user = relationship('User', back_populates='children')
    diagnosis_history = relationship("DiagnosisHistory", back_populates='child')
    diagnosis_result = relationship("DiagnosisResult", back_populates='child')

    def __repr__(self):
        return f'<{self.name} {self.birth_date}>'

class SkillType(Base):
    __tablename__ = 'skill_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    skill = relationship("Skill", back_populates='skill_type')
    diagnosis_result = relationship("DiagnosisResult", back_populates='skill_type')
    diagnosis_history = relationship("DiagnosisHistory", back_populates='skill_type')

    def __repr__(self):
        return f"{self.name}"
    
class Skill(Base):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True, autoincrement=True)
    skill_type_id = Column(Integer, ForeignKey('skill_types.id'), nullable=False)
    name = Column(String, nullable=False)
    criteria = Column(Text)
    recommendation = Column(Text, nullable=False)
    age_start = Column(Integer)
    age_end = Column(Integer)
    actual_age = Column(Integer)
    skill_type = relationship("SkillType", back_populates='skill')
    diagnosis_history = relationship("DiagnosisHistory", back_populates='skill')
   
    def __repr__(self):
        return f"{self.name}"

class DiagnosisHistory(Base):
    __tablename__ = 'diagnosis_history'

    id = Column(Integer,primary_key=True, autoincrement=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    skill_type_id = Column(Integer, ForeignKey("skill_types.id"), nullable=False)
    date = Column(Date)
    mastered = Column(Boolean)
    child_id = Column(Integer, ForeignKey('children.id'), nullable=False)

    skill = relationship("Skill", back_populates='diagnosis_history')
    skill_type = relationship("SkillType", back_populates='diagnosis_history')
    child = relationship("Child", back_populates='diagnosis_history')

    def __repr__(self):
        return f"{self.child_id} {self.skill} {self.mastered}"
    
class DiagnosisResult(Base):
    __tablename__ = 'diagnosis_result'

    id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(Integer, ForeignKey('children.id'), nullable=False)
    date = Column(Date)
    skill_types_id = Column(Integer, ForeignKey("skill_types.id"), nullable=False)
    age_assessment = Column(Integer)
    skill_type = relationship("SkillType", back_populates='diagnosis_result')
    child = relationship('Child', back_populates='diagnosis_result')

    def __repr__(self):
        return f"{self.child_id} {self.skill_type_id} {self.age_assessment}"
