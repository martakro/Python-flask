from datetime import datetime
from typing import Optional

from models.register_user.register_user_base import RegisterUserBase


class RegisterUserResponse(RegisterUserBase):
    """
    Holds user data
    """

    registration_date: Optional[datetime] = None
    user_id: Optional[int] = None
