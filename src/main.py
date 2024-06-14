import json
from http import HTTPStatus
from http.client import HTTPException

from connexion import FlaskApp
from connexion.lifecycle import ConnexionResponse, ConnexionRequest
from pydantic import ValidationError

from exceptions.db_exceptions import (
    DatabaseError,
    DataExistsException,
    DataNotUniqueException,
)
from helpers.error_msg_formater import format_error_msg


def handle_validation_error(request: ConnexionRequest, exc: Exception):
    """
    Handles validation error
    """
    error_msg = format_error_msg(exc.errors())
    return ConnexionResponse(
        status_code=HTTPStatus.BAD_REQUEST, body=json.dumps(error_msg)
    )


def handle_http_error(request: ConnexionRequest, exc: Exception):
    """
    Returns error in json format
    """
    ConnexionResponse(status_code=HTTPStatus.BAD_REQUEST, body=json.dumps(exc.__dict__))


def handle_data_errors(request: ConnexionRequest, exc: Exception):
    """
    Handles database errors connected with data e.g. providing not unique data
    """
    return ConnexionResponse(
        status_code=HTTPStatus.BAD_REQUEST, body=json.dumps({"error": exc.message})
    )


def handle_database_error(request: ConnexionRequest, exc: Exception):
    """
    Handles database errors related with connections
    """
    return ConnexionResponse(
        status_code=HTTPStatus.BAD_REQUEST, body=json.dumps({"error": exc.message})
    )


def create_app():
    """
    Creates flask app
    """
    flask_app = FlaskApp(__name__)
    flask_app.add_api(
        "swagger.yml",
        strict_validation=True,
        validate_responses=True,
    )
    flask_app.add_error_handler(ValidationError, handle_validation_error)
    flask_app.add_error_handler(HTTPException, handle_http_error)
    flask_app.add_error_handler(DataNotUniqueException, handle_data_errors)
    flask_app.add_error_handler(DataExistsException, handle_data_errors)
    flask_app.add_error_handler(DatabaseError, handle_database_error)
    return flask_app


if __name__ == "__main__":
    app = create_app()
    app.run()
