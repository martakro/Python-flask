from datetime import datetime
from typing import Optional

from db.repositories.models.user.user_model_base import UserModelBase


class UserModelOutput(UserModelBase):
    registration_date: Optional[datetime] = None
    user_id: Optional[int] = None
