from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum
from app.models.enums import StatutColis, EtatColis





# ZONES =========================================================
class ZoneBase(BaseModel):
    nom: str
    code_postal: str

class ZoneCreate(ZoneBase):
    pass

class ZoneOut(ZoneBase):
    id: int
    class Config:
        from_attributes = True







# COLIS =========================================================
class ColisBase(BaseModel):
    description: str
    poids: int
    ville_destination: str


class ColisCreateExpediteur(ColisBase):
    id_expediteur: int
    id_destinataire: int
    id_zone: int


class ColisCreateGestionnaire(ColisBase):
    id_expediteur: int
    id_destinataire: int
    id_zone: int


class ColisUpdate(BaseModel):
    description: Optional[str] = None
    poids: Optional[int] = None
    ville_destination: Optional[str] = None
    statut: Optional[StatutColis] = None
    etat: Optional[EtatColis] = None
    id_livreur: Optional[int] = None
    id_zone: Optional[int] = None


class ColisUpdateStatut(BaseModel) :
    statut : StatutColis


class ColisOut(ColisBase):
    id: int
    statut: str
    etat: str
    id_expediteur: int
    id_destinataire: int
    id_livreur: Optional[int] = None
    id_zone: Optional[int] = None
    
    class Config:
        from_attributes = True





# HISTORIQUE =========================================================
class HistoriqueOut(BaseModel):
    id: int
    id_colis: int
    ancien_status: str
    nouveau_status: str
    timestamp: datetime

    class Config:
        from_attributes = True