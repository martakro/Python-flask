from http import HTTPStatus


class DataExistsException(Exception):
    def __init__(self, message, *args, **kwargs):
        super().__init__(message)
        self.status_code = HTTPStatus.BAD_REQUEST.value
        self.message = message


class DataNotUniqueException(Exception):
    def __init__(self, message, *args, **kwargs):
        super().__init__(message)
        self.status_code = HTTPStatus.BAD_REQUEST.value
        self.message = message


class DatabaseError(Exception):
    def __init__(self, message, *args, **kwargs):
        super().__init__(message)
        self.status_code = HTTPStatus.BAD_REQUEST.value
        self.message = message
