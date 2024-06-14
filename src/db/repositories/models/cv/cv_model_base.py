from decimal import Decimal
from typing import Optional

from pydantic import UUID4, BaseModel, Field


class SkillModelBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    level: int


class OrganizationModelBase(BaseModel):
    name: str = Field(min_length=1)
    address: str = Field(min_length=1)


class ExperienceModelBase(BaseModel):
    employer: OrganizationModelBase
    years_of_employment: Decimal
    project_description: str = Field(min_length=10, max_length=500)


class CVModelBase(BaseModel):
    candidate_id: UUID4
    skills: Optional[list[SkillModelBase]] = None
    experience: Optional[list[ExperienceModelBase]] = None
