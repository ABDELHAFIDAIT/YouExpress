from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.models.base import Base

class Colis(Base):
    __tablename__ = "colis"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=True)
    poids = Column(Float, nullable=False)
    ville_destination = Column(String, nullable=False)
    livreur_id = Column(Integer, ForeignKey("livreurs.id"), nullable=True)
    expediteur_id = Column(Integer, ForeignKey("expediteurs.id"), nullable=True)
    destinataire_id = Column(Integer, ForeignKey("destinataires.id"), nullable=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=True)
    
