from sqlalchemy import Column, Integer, DateTime, Enum as SAEnum, ForeignKey
from app.models.base import Base 
import enum
from app.models.enums import StatutColis  

from datetime import datetime, timezone

class AncienStatut(str, enum.Enum) :
    CREE = "cree"
    COLLECTE = "collecte"
    EN_STOCK = "en stock"
    EN_TRANSIT = "en transit"


class NouveauStatut(str, enum.Enum) :
    COLLECTE = "collecte"
    EN_STOCK = "en stock"
    EN_TRANSIT = "en transit"
    LIVRE = "livre"



class Historique(Base) :
    __tablename__ = "historiques"
    
    id = Column(Integer, primary_key=True, index=True)
    id_colis = Column(Integer, ForeignKey("colis.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    ancien_status = Column(SAEnum(StatutColis), nullable=False)  
    nouveau_status = Column(SAEnum(StatutColis), nullable=False)  
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))