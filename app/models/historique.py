from sqlalchemy import Column, Integer, DateTime, Enum as SAEnum, ForeignKey
from app.models.base import Base 
import enum
from datetime import datetime, timezone

class AncienStatut(str, enum.Enum) :
    CREE = "créé"
    COLLECTE = "collecté"
    EN_STOCK = "en stock"
    EN_TRANSIT = "en transit"


class NouveauStatut(str, enum.Enum) :
    COLLECTE = "collecté"
    EN_STOCK = "en stock"
    EN_TRANSIT = "en transit"
    LIVRE = "livré"



class Historique(Base) :
    __tablename__ = "historiques"
    
    id = Column(Integer, primary_key=True, index=True)
    id_colis = Column(Integer, ForeignKey("colis.id"), nullable=False)
    ancien_status = Column(SAEnum(AncienStatut), nullable=False)
    nouveau_status = Column(SAEnum(NouveauStatut), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))