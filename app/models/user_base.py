from sqlalchemy import Column, Integer, String
from app.models.base import Base

class User(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    prenom = Column(String, nullable=False)
    nom = Column(String, nullable=False)
    telephone = Column(String, nullable=False)