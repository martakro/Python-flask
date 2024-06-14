from http import HTTPStatus
from typing import Any


def hello_world() -> tuple[dict[str, Any], HTTPStatus]:
    """
    Example method
    """
    return {"msg": "Hello World!"}, HTTPStatus.OK


def health() -> tuple[dict[str, Any], HTTPStatus]:
    """
    Health check
    """
    return {"msg": HTTPStatus.OK.phrase}, HTTPStatus.OK
