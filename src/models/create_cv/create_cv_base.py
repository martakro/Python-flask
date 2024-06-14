from decimal import Decimal
from typing import Optional

from pydantic import UUID4, BaseModel, Field, model_validator, field_validator


class SkillBase(BaseModel):
    """
    Schema reflects single candidate skill
    """

    name: str = Field(min_length=1, max_length=50)
    level: int

    @field_validator("level")
    @classmethod
    def level_between_1_and_5(cls, value: int):
        """
        Validates value of skill level
        """
        if value < 1 or value > 5:
            raise ValueError("skill level should be in range from 1 to 5")
        return value


class OrganizationBase(BaseModel):
    """
    Schema reflects employer data
    """

    name: str = Field(min_length=1)
    address: str = Field(min_length=1)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return bool(self.name == other.name and self.address == other.address)
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.name, self.address))


class ExperienceBase(BaseModel):
    """
    Schema reflects candidate single work experience
    """

    employer: OrganizationBase
    years_of_employment: Decimal
    project_description: str = Field(min_length=10, max_length=500)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return bool(
                self.employer == other.employer
                and self.years_of_employment == other.years_of_employment
                and self.project_description == other.project_description
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.employer, self.years_of_employment, self.project_description))

    @field_validator("years_of_employment")
    @classmethod
    def years_of_employment_is_above_zero(cls, value: int):
        """
        Validates value of years of employment
        """
        if value <= 0:
            raise ValueError("Years of employment value should be greater than 0")

        return value


class CreateCVBase(BaseModel):
    """
    Schema contains all candidate data
    """

    candidate_id: UUID4
    skills: Optional[list[SkillBase]] = None
    experience: Optional[list[ExperienceBase]] = None

    @model_validator(mode="before")
    def cv_not_empty(cls, values: dict[str, str]) -> dict[str, str]:
        """
        Validates that passed cv is not empty
        """
        skills, experience = values.get("skills", None), values.get("experience", None)
        if not skills and not experience:
            raise ValueError(
                "skills and experience: "
                "Provided cv has no data. Add at least one skill or experience"
            )
        return values

    @field_validator("experience")
    @classmethod
    def experience_data_is_unique(cls, value: list[ExperienceBase]):
        """
        Validates experience data if they are unique
        """
        if not value:
            return value

        if len(set(value)) != len(value):
            raise ValueError("Provided experience is not unique")
        return value

    @field_validator("skills")
    @classmethod
    def skills_are_unique(cls, value: list[SkillBase]):
        """
        Validates skills data basing on their names if they are unique
        """
        if value:
            skills_names = [element.name for element in value]
            if len(skills_names) != len(set(skills_names)):
                raise ValueError("Provided skills are not unique")
        return value
