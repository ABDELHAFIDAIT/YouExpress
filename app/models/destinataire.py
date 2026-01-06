from sqlalchemy import Column, String
from app.models.user_base import User

class Destinataire(User) :
    __tablename__ = 'destinataires'
    
    adresse = Column(String, nullable=False)
    email = Column(String, nullable=False)