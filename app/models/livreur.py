from sqlalchemy import Column, String
from app.models.user_base import User

class Livreur(User):
    __tablename__ = "livreurs"

    vehicule = Column(String, nullable=True)
    zone_assigne = Column(String, nullable=False)
    