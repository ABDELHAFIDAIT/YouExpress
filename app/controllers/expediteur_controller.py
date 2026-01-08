from sqlalchemy.orm import Session
from app.models import Expediteur
from app.schemas.user_schemas import ExpediteurCreate
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions import DatabaseError, BusinessRuleError, EntityNotFound


class ExpediteurController:
    def __init__(self , db : Session):
        self.db = db
        
    def create_expediteur(self , data: ExpediteurCreate):
        expediteur = Expediteur(**data.model_dump())
        
        try:
            self.db.add(expediteur)
            self.db.commit()
            self.db.refresh(expediteur)
            return expediteur
            
        except IntegrityError as e:
            self.db.rollback()
            raise BusinessRuleError(f"Impossible de créer le compte : L'email '{data.email}' est déjà utilisé.")
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(f"Erreur lors de la création de l'expéditeur : {str(e)}")
    
    
    
    def get_expediteur_by_id(self , id: int):
        expediteur = (
            self.db.query(Expediteur)
            .filter(Expediteur.id == id)
            .first()
        )
        
        if not expediteur:
            raise EntityNotFound(entity="Expediteur", id=id)
        
        return expediteur
    
    
    
    def get_all_expediteurs(self):
        return self.db.query(Expediteur).all()