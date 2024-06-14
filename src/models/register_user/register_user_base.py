from pydantic import BaseModel, EmailStr, Field


class RegisterUserBase(BaseModel):
    """
    Schema reflects data which should be provided during registration of new user
    """

    email: EmailStr
    username: str = Field(min_length=4, max_length=50)
    firstname: str = Field(min_length=1, max_length=50)
    surname: str = Field(min_length=1, max_length=50)
