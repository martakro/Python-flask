from factory import Factory, Faker

from models.register_user.register_user_response import (
    RegisterUserResponse,
)


class RandomUserFactory(Factory):
    class Meta:
        model = RegisterUserResponse

    email = Faker("email")
    username = Faker("user_name")
    firstname = Faker("first_name")
    surname = Faker("last_name")
    password = Faker("password", length=12)
