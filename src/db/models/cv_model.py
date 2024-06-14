from sqlalchemy import (
    UUID,
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, relationship
from db.models.base import Base


class OrganizationModel(Base):
    __tablename__ = "organization"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)

    experiences: Mapped[list["ExperienceModel"]] = relationship("ExperienceModel")

    __table_args__ = (UniqueConstraint(name, address, name="org_unique"),)


class ExperienceModel(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True)
    years_of_employment = Column(Integer, nullable=False)
    project_description = Column(String(500), nullable=False)

    cv_id = Column(Integer, ForeignKey("cv.id"))
    cv: Mapped["CVModel"] = relationship("CVModel")

    employer_id = Column(Integer, ForeignKey("organization.id"))
    employer: Mapped["OrganizationModel"] = relationship("OrganizationModel")


class SkillAssociation(Base):
    __tablename__ = "skill_association"

    skill_id = Column(Integer, ForeignKey("skill.id"), primary_key=True)
    cv_id = Column(Integer, ForeignKey("cv.id"), primary_key=True)
    skill_level = Column(Integer)

    skill = relationship("SkillModel", backref="cv")
    cv = relationship("CVModel", backref="skill")


class SkillModel(Base):
    __tablename__ = "skill"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True)


class CVModel(Base):
    __tablename__ = "cv"

    id = Column(Integer, primary_key=True)
    candidate_id = Column(UUID, nullable=False)
    experience: Mapped[list["ExperienceModel"]] = relationship("ExperienceModel")

    __table_args__ = (UniqueConstraint(candidate_id, name="cv_unique"),)
