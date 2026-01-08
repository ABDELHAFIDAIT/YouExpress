from sqlalchemy.orm import Session
from app.models.livreur import Livreur
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions import DatabaseError, BusinessRuleError, EntityNotFound
from app.schemas.user_schemas import (
    LivreurCreate
)

class LivreurController:
    def __init__(self , db: Session ):
        self.db = db
        
        
    def create_livreur(self , data :LivreurCreate):
        livreur = Livreur(**data.model_dump())
        
        try:
            self.db.add(livreur)
            self.db.commit()
            self.db.refresh(livreur)
            return livreur
            
        except IntegrityError as e:
            self.db.rollback()
            raise BusinessRuleError(f"Impossible de créer le livreur : Le numéro de téléphone '{data.telephone}' est déjà associé à un compte.")
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(f"Erreur lors de la création du livreur : {str(e)}")
    
    
    def get_livreur_by_id(self, id: int):
        livreur = (
            self.db.query(Livreur)
            .filter(Livreur.id == id)
            .first()
        )
        
        if not livreur:
            raise EntityNotFound(entity="Livreur", id=id)
        
        return livreur
    
    
    def get_all_livreurs(self):
        return self.db.query(Livreur).all()
    
    
    def get_livreur_zone(self , id: int):
        livreur = self.get_livreur_by_id(id)
        return livreur.zone_assigne
        