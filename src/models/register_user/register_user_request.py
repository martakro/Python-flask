import string

from pydantic import Field, model_validator, field_validator

from models.register_user.register_user_base import RegisterUserBase


class RegisterUserRequest(RegisterUserBase):
    password: str = Field(min_length=12, pre=True)
    repeat_password: str = Field(exclude=True)

    @model_validator(mode="before")
    @classmethod
    def passwords_are_equal(cls, values: dict[str, str]) -> dict[str, str]:
        """
        Validates equality of password and repeat_password values
        """
        password, repeat_password = values.get("password", None), values.get(
            "repeat_password", None
        )
        if password != repeat_password:
            raise ValueError("password and repeat_password: values are not equal")
        return values

    @field_validator("password")
    @classmethod
    def password_valid(cls, value: str) -> str:
        """
        Validates password, with rules:
        - min 12 characters
        - must contain min one: special char, upper case letter, lower case letter, one digit
        """

        validation_notifications = []
        if not any(u in value for u in string.ascii_uppercase):
            validation_notifications.append("Password must contain upper case")
        if not any(l in value for l in string.ascii_lowercase):
            validation_notifications.append("Password must contain lower case")
        if not any(d in value for d in string.digits):
            validation_notifications.append("Password must contain number")
        if not any(p in value for p in string.punctuation):
            validation_notifications.append("Password must contain special character")

        if validation_notifications:
            raise ValueError(", ".join(validation_notifications))
        return value
