from pydantic import Field

from db.repositories.models.user.user_model_base import UserModelBase


class UserModelInput(UserModelBase):
    password: str = Field(min_length=12, pre=True)
    repeat_password: str = Field(exclude=True)
