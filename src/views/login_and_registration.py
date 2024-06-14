from http import HTTPStatus
from typing import Any

from flask import abort

from db.create_db import get_session
from logic.registration import register_candidate
from models.register_user.register_user_request import RegisterUserRequest


def register_user(body: dict[str, Any]) -> tuple[dict[str, Any], HTTPStatus]:
    """
    Register to the system
    """
    user_data = RegisterUserRequest.parse_obj(body)

    session = get_session()
    new_user = register_candidate(session, user_data)
    return (
        new_user.model_dump(),
        HTTPStatus.CREATED,
    )


def login():
    """
    Logs user to the system
    """
    abort(501)


def logout():
    """
    Logs out from system
    """
    abort(501)
