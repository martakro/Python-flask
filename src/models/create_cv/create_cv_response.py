from typing import Optional

from models.create_cv.create_cv_base import (
    SkillBase,
    OrganizationBase,
    ExperienceBase,
    CreateCVBase,
)


class SkillResponse(SkillBase):
    id: int


class OrganizationResponse(OrganizationBase):
    id: int


class ExperienceResponse(ExperienceBase):
    id: int
    employer: OrganizationResponse


class CreateCVResponse(CreateCVBase):
    id: int
    skills: Optional[list[SkillResponse]]
    experience: Optional[list[ExperienceResponse]]
