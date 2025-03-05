<<<<<<< HEAD
from sqlalchemy import Integer, BigInteger, Column, Boolean, String, Text, Date,ForeignKey, create_engine, MetaData
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase

class Base(DeclarativeBase):
    metadata = MetaData()
=======
from __future__ import annotations

from datetime import date

from sqlalchemy import BigInteger, Date, ForeignKey, String, Text, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

>>>>>>> 5b2ecbb8756cc92dd5e988d30da3f83f04eee85e

class User(Base):
    __tablename__ = 'users'

<<<<<<< HEAD
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
=======
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)

    children: Mapped[list["Child"]] = relationship( back_populates='user')

    def __repr__(self):
        return f"User <{self.telegram_id}>"


class Child(Base):
    __tablename__ = 'children'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)

    user: Mapped["User"] = relationship('User', back_populates='children')
    diagnosis_history: Mapped[list["DiagnosisHistory"]] = relationship(back_populates='child')
    diagnosis_result: Mapped[list["DiagnosisResult"]] = relationship(back_populates='child')
>>>>>>> 5b2ecbb8756cc92dd5e988d30da3f83f04eee85e

    def __repr__(self):
        return f'<{self.name} {self.birth_date}>'

<<<<<<< HEAD
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
=======

class SkillType(Base):
    __tablename__ = 'skill_types'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    skill: Mapped[list["Skill"]] = relationship(back_populates='skill_type')

    diagnosis_result: Mapped[list["DiagnosisResult"]] = relationship(back_populates='skill_type')
    diagnosis_history: Mapped[list["DiagnosisHistory"]] = relationship(back_populates='skill_type')

    def __repr__(self):
        return f"{self.name}"


class Skill(Base):
    __tablename__ = 'skills'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    skill_type_id: Mapped[int] = mapped_column(ForeignKey('skill_types.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    criteria: Mapped[str] = mapped_column(Text)
    recommendation: Mapped[str] = mapped_column(Text, nullable=False)
    age_start: Mapped[int] = mapped_column()
    age_end: Mapped[int] = mapped_column()
    age_actual: Mapped[int] = mapped_column()

    skill_type: Mapped["SkillType"] = relationship(back_populates='skill')
    diagnosis_history: Mapped[list["DiagnosisHistory"]] = relationship(back_populates='skill')

    def __repr__(self):
        return f"{self.name}"


class DiagnosisHistory(Base):
    __tablename__ = 'diagnosis_history'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), nullable=False)
    skill_type_id: Mapped[int] = mapped_column(ForeignKey("skill_types.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date)
    mastered: Mapped[bool] = mapped_column(Boolean)
    child_id: Mapped[int] = mapped_column(ForeignKey('children.id'), nullable=False)

    skill: Mapped["Skill"] = relationship(back_populates='diagnosis_history')
    skill_type: Mapped["SkillType"] = relationship(back_populates='diagnosis_history')
    child: Mapped["Child"] = relationship(back_populates='diagnosis_history')

    def __repr__(self):
        return f"{self.child_id} {self.skill} {self.mastered}"


class DiagnosisResult(Base):
    __tablename__ = 'diagnosis_result'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    child_id: Mapped[int] = mapped_column(ForeignKey('children.id'), nullable=False)
    date: Mapped[date] = mapped_column(Date)
    skill_types_id: Mapped[int] = mapped_column(ForeignKey("skill_types.id"), nullable=False)
    age_assessment: Mapped[int] = mapped_column()

    skill_type: Mapped["SkillType"] = relationship(back_populates='diagnosis_result')
    child: Mapped["Child"] = relationship(back_populates='diagnosis_result')

    def __repr__(self):
        return f"{self.child_id} {self.skill_types_id} {self.age_assessment}"
>>>>>>> 5b2ecbb8756cc92dd5e988d30da3f83f04eee85e
