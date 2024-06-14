# pylint: disable=missing-function-docstring, unused-variable, redefined-outer-name
from datetime import datetime
from unittest.mock import MagicMock, create_autospec

import pytest
from freezegun import freeze_time


from db.create_db import get_session
from db.models.user_model import UserModel
from exceptions.db_exceptions import DatabaseError, DataExistsException
from models.register_user.register_user_response import (
    RegisterUserResponse,
)
from logic.registration import RegisterUserRepository, register_candidate
from tests.assets.fake_user import RandomUserFactory

RANDOM_USER = RandomUserFactory()
RANDOM_USER_2 = RandomUserFactory()

USER_EMAIL = RANDOM_USER.email
USER_USERNAME = RANDOM_USER.username
USER_FIRSTNAME = RANDOM_USER.firstname
USER_SURNAME = RANDOM_USER.surname
USER_PASSWORD = USER_REPEAT_PASSWORD = RANDOM_USER.password

USER_VALID_DATA = {
    "email": RANDOM_USER.email,
    "username": RANDOM_USER.username,
    "firstname": RANDOM_USER.firstname,
    "surname": RANDOM_USER.surname,
    "password": RANDOM_USER.password,
    "repeat_password": RANDOM_USER.password,
}

USER_TEST_LOGIC_DATA = RegisterUserResponse(
    **{
        "email": RANDOM_USER_2.email,
        "username": RANDOM_USER_2.username,
        "firstname": RANDOM_USER_2.firstname,
        "surname": RANDOM_USER_2.surname,
        "password": RANDOM_USER_2.password,
    }
)

USER_EXTRA_DATA = {
    "email": RANDOM_USER.email,
    "username": RANDOM_USER.username,
    "firstname": RANDOM_USER.firstname,
    "surname": RANDOM_USER.surname,
    "password": RANDOM_USER.password,
    "repeat_password": RANDOM_USER.password,
    "user_id": 5,
}

NEW_USER = RegisterUserResponse(
    **{
        "user_id": 1,
        "email": RANDOM_USER_2.email,
        "username": RANDOM_USER_2.username,
        "firstname": RANDOM_USER_2.firstname,
        "surname": RANDOM_USER_2.surname,
        "password": RANDOM_USER_2.password,
    }
)

PASSWORD_TOO_SHORT = "ensure this value has at least 12 characters"
PASSWORD_MISSING_REQUIRED_NUMBER = "Password must contain number"
PASSWORD_WITHOUT_SPECIAL_CHAR = "Password must contain special character"
PASSWORD_WITHOUT_UPPER_CASE = "Password must contain upper case"
PASSWORD_WITHOUT_LOWER_CASE = "Password must contain lower case"


def test_create_user_successful():
    session = get_session()
    user_rep = RegisterUserRepository(session)
    user_rep.create_user = MagicMock(return_value=NEW_USER)
    assert user_rep.create_user(USER_TEST_LOGIC_DATA) == NEW_USER


def test_create_user_existing_in_db():
    session = get_session()
    registration_mock = create_autospec(
        register_candidate, side_effect=DataExistsException
    )
    with pytest.raises(DataExistsException):
        registration_mock(session, USER_TEST_LOGIC_DATA)


def test_cannot_connect_to_db():
    def raise_db_connection_error():
        raise DatabaseError("Cannot connect to db")

    session = get_session()
    user_rep = RegisterUserRepository(session)
    user_rep.create_user = MagicMock(side_effect=raise_db_connection_error)
    with pytest.raises(DatabaseError):
        assert user_rep.create_user() == DatabaseError("Cannot connect to db")


@freeze_time(datetime.utcnow())
def test_register_user_successful(client):
    user_input = {
        "email": USER_EMAIL,
        "username": USER_USERNAME,
        "firstname": USER_FIRSTNAME,
        "surname": USER_SURNAME,
        "password": USER_PASSWORD,
        "repeat_password": USER_PASSWORD,
    }
    expected_response = {
        "email": USER_EMAIL,
        "username": USER_USERNAME,
        "firstname": USER_FIRSTNAME,
        "surname": USER_SURNAME,
        "registation_date": datetime.utcnow().isoformat() + "Z",
    }

    response = client.post("/my/registration", json=user_input)

    current_reponse = response.json
    user_id = current_reponse.pop("user_id")
    assert user_id > 0
    assert current_reponse == expected_response
    assert response.status_code == 201


def test_register_user_invalid_data(client):
    user_invalid_data = {
        "email": "candid!at$etestcom",
        "surname": "",
        "firstname": "",
        "username": "",
        "password": RANDOM_USER.password,
        "repeat_password": RANDOM_USER.password,
    }
    user_invalid_data_validation = {
        "username": ["ensure this value has at least 4 characters"],
        "firstname": ["ensure this value has at least 1 characters"],
        "surname": ["ensure this value has at least 1 characters"],
        "email": ["value is not a valid email address"],
    }
    response = client.post("/my/registration", json=user_invalid_data)
    assert response.json == user_invalid_data_validation
    assert response.status_code == 400


def test_register_user_missing_data(client):
    test_user_invalid = {
        "email": RANDOM_USER.email,
        "firstname": RANDOM_USER.firstname,
        "surname": RANDOM_USER.surname,
        "password": RANDOM_USER.password,
        "repeat_password": RANDOM_USER.password,
    }
    response = client.post("/my/registration", json=test_user_invalid)
    assert response.json == {"username": ["field required"]}
    assert response.status_code == 400


@pytest.mark.parametrize(
    "password,expected_validation",
    [
        (
            "1234567890123",
            [
                PASSWORD_WITHOUT_UPPER_CASE,
                PASSWORD_WITHOUT_LOWER_CASE,
                PASSWORD_WITHOUT_SPECIAL_CHAR,
            ],
        ),
        ("abc123!Z", [PASSWORD_TOO_SHORT]),
        (
            "abcedefghijKLMO",
            [PASSWORD_MISSING_REQUIRED_NUMBER, PASSWORD_WITHOUT_SPECIAL_CHAR],
        ),
        (
            "!@#$%^&*())(*%$)",
            [
                PASSWORD_WITHOUT_UPPER_CASE,
                PASSWORD_WITHOUT_LOWER_CASE,
                PASSWORD_MISSING_REQUIRED_NUMBER,
            ],
        ),
        (
            "",
            [PASSWORD_TOO_SHORT],
        ),
    ],
)
def test_register_user_invalid_password(password, expected_validation, client):
    user_data = {
        "email": RANDOM_USER.email,
        "username": RANDOM_USER.username,
        "firstname": RANDOM_USER.firstname,
        "surname": RANDOM_USER.surname,
        "password": password,
        "repeat_password": password,
    }
    response = client.post("/my/registration", json=user_data)
    assert response.json == {"password": expected_validation}
    assert response.status_code == 400


def test_password_and_repeat_password_not_match(client):
    user_input = {
        "email": USER_EMAIL,
        "username": USER_USERNAME,
        "firstname": USER_FIRSTNAME,
        "surname": USER_SURNAME,
        "password": USER_PASSWORD,
        "repeat_password": "abc",
    }
    response = client.post("/my/registration", json=user_input)
    assert response.json == {"password and repeat_password": ["values are not equal"]}
    assert response.status_code == 400


def test_register_candidate_returns_correct_data():
    session = get_session()
    register_candidate = MagicMock(return_value=NEW_USER)
    assert register_candidate(session, USER_TEST_LOGIC_DATA) == NEW_USER


def test_add_user_to_db(session):
    user = UserModel(
        email="test_email@test_xxx.pl",
        firstname="Anna",
        surname="Kovalska",
        username="akowalska",
        registration_date=datetime(2023, 7, 1),
    )
    session.add(user)
    session.flush()
    added_user = session.query(UserModel).filter(UserModel.email == user.email).first()
    assert added_user.email == user.email
    assert added_user.firstname == user.firstname
    assert added_user.surname == user.surname
    assert added_user.username == user.username
    assert added_user.registration_date == user.registration_date
