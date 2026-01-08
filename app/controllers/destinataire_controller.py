from sqlalchemy.orm import Session
from app.models import Destinataire
from app.schemas.user_schemas import DestinataireCreate
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions import DatabaseError, BusinessRuleError, EntityNotFound



class DestinatireController:
    def __init__(self , db: Session):
        self.db = db
        
        
    def create_destinataire(self , data: DestinataireCreate):
        
        destinataire = Destinataire(**data.model_dump())
        
        try:
            self.db.add(destinataire)
            self.db.commit()
            self.db.refresh(destinataire)
            return destinataire
            
        except IntegrityError as e:
            self.db.rollback()
            raise BusinessRuleError(f"Impossible de créer le destinataire : Cet email est probablement déjà utilisé.")
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(f"Erreur lors de la création du destinataire : {str(e)}")
        
    
    
    def get_destinataire_by_id(self, id: int):  
        destinataire = (
            self.db.query(Destinataire)
            .filter(Destinataire.id == id)
            .first()
        )
        
        if not destinataire:
            raise EntityNotFound(entity="Destinataire", id=id)
            
        return destinataire
    
    
    def get_all_destinataires(self):
        return self.db.query(Destinataire).all()