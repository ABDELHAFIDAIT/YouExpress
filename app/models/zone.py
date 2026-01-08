from sqlalchemy import String, Integer, Column
from app.models.base import Base

class Zone(Base) :
    __tablename__ = "zones"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False, unique=True)
    code_postal = Column(String, nullable=False, unique=True)