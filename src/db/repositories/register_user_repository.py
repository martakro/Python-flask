from datetime import datetime
from typing import Optional

from db.models.user_model import UserModel
from db.repositories.models.user.user_model_base import UserModelBase
from db.repositories.models.user.user_model_output import UserModelOutput


class RegisterUserRepository:
    def __init__(self, session) -> None:
        self.session = session

    def create_user(self, user: UserModelBase) -> UserModelOutput:
        """
        creates new user
        """
        user_mapped = UserModel(
            email=user.email,
            username=user.username,
            firstname=user.firstname,
            surname=user.surname,
            registration_date=datetime.utcnow(),
        )
        self.session.add(user_mapped)
        self.session.commit()
        return UserModelOutput(
            user_id=user_mapped.user_id,
            email=user.email,
            username=user.username,
            firstname=user.firstname,
            surname=user.surname,
            registration_date=datetime.utcnow(),
        )

    def get_user_by_email(self, user_email: str) -> Optional[UserModelOutput]:
        """
        Searches db via user email
        """
        user = (
            self.session.query(UserModel).filter(UserModel.email == user_email).first()
        )
        if not user:
            return None
        return UserModelOutput(
            user_id=user.user_id,
            email=user.email,
            firstname=user.firstname,
            surname=user.surname,
            username=user.username,
            registration_date=user.registration_date,
        )
