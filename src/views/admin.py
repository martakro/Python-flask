from flask import abort, request


def get_user(user_id: int):
    """
    Allows to view user account
    """

    print(user_id)
    abort(501)


def get_users():
    """
    Allows to view all users account
    """
    abort(501)


def add_user():
    """
    Allows to add user account
    """
    if request.method == "POST":
        abort(501)


def delete_user(user_id: int):
    """
    Allows to delete user s
    """

    print(user_id)

    abort(501)


def update_user_data(user_id: int):
    """
    Allows to update user data
    """

    print(user_id)
    abort(501)
