

from sqlalchemy.orm import Session
from app.models.livreur import Livreur
from app.schemas.user_schemas import (
    LivreurCreate
)

class LivreurController:
    def __init__(self , db: Session ):
        self.db = db
        
        
    def create_livreur(self , data :LivreurCreate):
        livreur = Livreur(**data.model_dump())
        self.db.add(livreur)
        self.db.commit()
        self.db.refresh(livreur)
        return livreur
    
    def get_livreur_by_id(self, id: int):
        livreur = (
            self.db.query(Livreur)
            .filter(Livreur.id == id)
            .first()
        )
        return livreur
    
    
    def get_all_livreurs(self):
        return self.db.query(Livreur).all()
    
    
    def get_livreur_zone(self , id: int):
        livreur = (
            self.db.query(Livreur)
            .filter(Livreur.id == id)
            .first()
        )
        
        return livreur.zone_assigne
        