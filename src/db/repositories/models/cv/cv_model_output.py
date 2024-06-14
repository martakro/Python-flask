from typing import Optional

from db.repositories.models.cv.cv_model_base import (
    ExperienceModelBase,
    SkillModelBase,
    OrganizationModelBase,
    CVModelBase,
)


class SkillModelOutput(SkillModelBase):
    id: Optional[int] = None


class OrganizationModelOutput(OrganizationModelBase):
    id: Optional[int] = None


class ExperienceModelOutput(ExperienceModelBase):
    id: Optional[int] = None
    employer: OrganizationModelOutput


class CVModelOutput(CVModelBase):
    id: Optional[int] = None
    skills: Optional[list[SkillModelOutput]]
    experience: Optional[list[ExperienceModelOutput]]
