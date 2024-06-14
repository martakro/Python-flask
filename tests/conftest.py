# pylint: disable=missing-function-docstring
import pytest
from db.create_db import get_session

from main import create_app


@pytest.fixture(scope="module")
def client():
    flask_app = create_app()
    with flask_app.app.test_client() as test_client:
        yield test_client


@pytest.fixture
def session():
    yield get_session()
