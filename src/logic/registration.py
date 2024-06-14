# pylint: disable=duplicate-code, too-few-public-methods
from db.repositories import RegisterUserRepository
from db.repositories.models.user.user_model_base import UserModelBase
from db.repositories.models.user.user_model_output import UserModelOutput
from exceptions.db_exceptions import DataExistsException
from models.register_user.register_user_request import RegisterUserRequest
from models.register_user.register_user_response import (
    RegisterUserResponse,
)


def candidate_exists(session, user_email: str) -> bool:
    """
    Checks if candidate exists in db
    """
    return bool(RegisterUserRepository(session).get_user_by_email(user_email))


def register_candidate(
    session,
    user_data: RegisterUserRequest,
) -> RegisterUserResponse:
    """
    Registers and validate candidate data
    """
    # Check if user exist
    if candidate_exists(session, user_data.email):
        raise DataExistsException(
            "User with this email exists in database. "
            "Please provide correct data or reset your password"
        )
    user_data = RegisterUserRequest.model_dump(user_data)
    user_data = UserModelBase.model_validate(user_data)
    user = RegisterUserRepository(session).create_user(user_data)
    return RegisterUserResponse.model_validate(UserModelOutput.model_dump(user))
