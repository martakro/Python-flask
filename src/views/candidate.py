from http import HTTPStatus
from typing import Any

from flask import abort

from db.create_db import get_session
from logic.cv import add_cv
from models.create_cv.create_cv_request import CreateCVRequest


def add_new_cv(body: dict[str, Any]) -> tuple[dict[str, Any], HTTPStatus]:
    """
    Allows candidate add cv
    """
    cv_data = CreateCVRequest.model_validate(body)

    session = get_session()
    new_cv = add_cv(session, cv_data)

    return new_cv.model_dump(), HTTPStatus.CREATED


def delete_cv():
    """
    Deletes candidate cv
    """
    abort(501)


def update_cv():
    """
    Update candidate cv
    """
    abort(501)


def get_cv():
    """
    View candidate cv
    """
    abort(501)


def get_my_skills():
    """
    Get candidate skills - candidate purposes
    """
    abort(501)


def get_my_exp():
    """
    Get candidate experience - candidate purposes
    """
    abort(501)
