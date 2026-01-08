from sqlalchemy import Column, String
from app.models.user_base import User

class Expediteur(User):
    __tablename__ = "expediteurs"

    adresse = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    