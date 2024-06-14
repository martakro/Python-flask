from sqlalchemy import Column, DateTime, Integer, String

from db.models.base import Base


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    registration_date = Column(DateTime, nullable=False)
