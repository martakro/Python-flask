from pydantic import BaseModel, EmailStr, Field


class UserModelBase(BaseModel):
    email: EmailStr
    username: str = Field(min_length=4, max_length=50)
    firstname: str = Field(min_length=1, max_length=50)
    surname: str = Field(min_length=1, max_length=50)
