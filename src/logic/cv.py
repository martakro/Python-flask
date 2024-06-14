# pylint: disable=too-few-public-methods
from uuid import UUID

from db.repositories.create_cv_repository import CVRepository
from db.repositories.models.cv.cv_model_input import CVModelInput
from db.repositories.models.cv.cv_model_output import CVModelOutput
from exceptions.db_exceptions import DataExistsException
from models.create_cv.create_cv_request import CreateCVRequest
from models.create_cv.create_cv_response import CreateCVResponse


def candidate_cv_exists(session, candidate_id: UUID) -> bool:
    """
    Checks if candidate has cv saved in db
    """
    return bool(CVRepository(session).get_candidate_cv_via_id(candidate_id))


def add_cv(session, cv_data: CreateCVRequest) -> CreateCVResponse:
    """
    Adds candidate cv
    """

    # Check if user has saved cv
    if candidate_cv_exists(session, cv_data.candidate_id):
        raise DataExistsException("CV exists in database")

    # Add CV
    cv_data = CreateCVRequest.model_dump(cv_data)
    cv_data = CVModelInput.model_validate(cv_data)
    new_cv = CVRepository(session).create_cv(cv_data)
    return CreateCVResponse.model_validate(CVModelOutput.model_dump(new_cv))
