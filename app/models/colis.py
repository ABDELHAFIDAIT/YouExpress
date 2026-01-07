from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as SqlEnum
from app.models.base import Base
from app.models.enums import StatutColis , EtatColis
from sqlalchemy.orm import relationship


class Colis(Base):
    __tablename__ = "colis"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=True)
    poids = Column(Float, nullable=False)
    ville_destination = Column(String, nullable=False)
    livreur_id = Column(Integer, ForeignKey("livreurs.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    expediteur_id = Column(Integer, ForeignKey("expediteurs.id", ondelete="CASCADE", onupdate="CASCADE") , nullable=False)
    destinataire_id = Column(Integer, ForeignKey("destinataires.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False)
    statut = Column(SqlEnum(StatutColis), default=StatutColis.CREE, nullable=False)
    etat = Column(SqlEnum(EtatColis), default=EtatColis.PENDING , nullable=False)
    
    historiques = relationship("Historique", cascade="all, delete-orphan", passive_deletes=True)

    
