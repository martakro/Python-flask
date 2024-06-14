from typing import Optional
from uuid import UUID

from sqlalchemy.dialects.postgresql import insert

from db.models.cv_model import (
    CVModel,
    ExperienceModel,
    OrganizationModel,
    SkillAssociation,
    SkillModel,
)
from db.repositories.models.cv.cv_model_base import ExperienceModelBase, SkillModelBase
from db.repositories.models.cv.cv_model_input import CVModelInput
from db.repositories.models.cv.cv_model_output import (
    CVModelOutput,
    OrganizationModelOutput,
    ExperienceModelOutput,
    SkillModelOutput,
)
from exceptions.db_exceptions import DataNotUniqueException


class CVRepository:
    def __init__(self, session) -> None:
        self.session = session

    def add_single_experience(self, cv: CVModel, experience: ExperienceModelBase):
        add_org_to_db = insert(OrganizationModel).values(
            name=experience.employer.name, address=experience.employer.address
        )
        add_org_to_db = add_org_to_db.on_conflict_do_update(
            index_elements=[OrganizationModel.name, OrganizationModel.address],
            set_={
                "name": experience.employer.name,
                "address": experience.employer.address,
            },
        )
        self.session.execute(add_org_to_db)

        get_org_from_db = (
            self.session.query(OrganizationModel)
            .filter(OrganizationModel.name == experience.employer.name)
            .filter(OrganizationModel.address == experience.employer.address)
            .first()
        )

        return ExperienceModel(
            cv_id=cv.id,
            project_description=experience.project_description,
            years_of_employment=experience.years_of_employment,
            employer_id=get_org_from_db.id,
        )

    def add_experiences(self, cv: CVModel, experiences: list[ExperienceModelBase]):
        exps = []

        for experience in experiences:
            exp = self.add_single_experience(cv, experience)
            exps.append(exp)

        self.session.add_all(exps)
        return exps

    def add_single_skill(self, cv: CVModel, skill: SkillModelBase):
        skill_to_add = SkillModel(name=skill.name)

        add_skill_to_db = (
            insert(SkillModel)
            .values({"name": skill_to_add.name})
            .on_conflict_do_nothing(index_elements=[SkillModel.name])
        )

        self.session.execute(add_skill_to_db)

        get_skill_from_db = (
            self.session.query(SkillModel)
            .filter(SkillModel.name == skill_to_add.name)
            .first()
        )

        skill_to_add.id = get_skill_from_db.id

        associated_skills_table = SkillAssociation(skill_level=skill.level)
        associated_skills_table.skill_id = get_skill_from_db.id
        associated_skills_table.cv_id = cv.id
        associated_skills_table.skill_id = get_skill_from_db.id

        return associated_skills_table

    def add_skills(self, cv: CVModel, skills: list[SkillModelBase]):
        skill_names = [skill.name for skill in skills]
        if len(skill_names) != len(set(skill_names)):
            raise DataNotUniqueException(
                f"There cannot be more than one skills with different level {skill_names}"
            )
        added_skills = []

        for skill in skills:
            added_skill = self.add_single_skill(cv, skill)
            added_skills.append(added_skill)

        self.session.add_all(added_skills)

        return added_skills

    def create_cv(self, cv_data: CVModelInput) -> CVModelOutput:
        """
        Creates new cv
        """

        cv = CVModel(candidate_id=cv_data.candidate_id)
        self.session.add(cv)

        exps = []
        if cv_data.experience:
            exps = self.add_experiences(cv=cv, experiences=cv_data.experience)

        skills = []
        skills_names = []
        if cv_data.skills:
            skills = self.add_skills(cv=cv, skills=cv_data.skills)
            skills_names = [skill.name for skill in cv_data.skills]

        self.session.commit()

        return CVModelOutput(
            id=cv.id,
            candidate_id=cv.candidate_id,
            experience=[
                ExperienceModelOutput(
                    id=exp.id,
                    employer=OrganizationModelOutput(
                        id=exp.employer.id,
                        name=exp.employer.name,
                        address=exp.employer.address,
                    ),
                    project_description=exp.project_description,
                    years_of_employment=exp.years_of_employment,
                )
                for exp in exps
            ],
            skills=[
                SkillModelOutput(
                    id=skill.skill_id, name=skills_names[index], level=skill.skill_level
                )
                for index, skill in enumerate(skills)
            ],
        )

    def get_candidate_cv_via_id(self, candidate_id: UUID) -> Optional[CVModelOutput]:
        """
        Searches cv db for candidate cv
        """
        cv = (
            self.session.query(CVModel)
            .filter(CVModel.candidate_id == candidate_id)
            .first()
        )

        if not cv:
            return None

        skills = (
            self.session.query(SkillAssociation)
            .filter(SkillAssociation.cv_id == cv.id)
            .all()
        )
        skills = [
            {"name": skill.skill.name, "level": skill.skill_level} for skill in skills
        ]
        if not skills:
            skills = []

        experience = self.session.query(ExperienceModel).filter(
            ExperienceModel.cv_id == cv.id
        )

        experience = [
            {
                "employer": {
                    "name": exp.employer.name,
                    "address": exp.employer.address,
                },
                "project_description": exp.project_description,
                "years_of_employment": exp.years_of_employment,
            }
            for exp in experience
        ]
        if not experience:
            experience = []

        return CVModelOutput(
            id=cv.id,
            candidate_id=candidate_id,
            experience=experience,
            skills=skills,
        )
