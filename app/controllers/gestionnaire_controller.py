from sqlalchemy.orm import Session
from app.models import Gestionnaire
from app.schemas.user_schemas import AdminCreate
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions import DatabaseError, BusinessRuleError, EntityNotFound
import logging


logger = logging.getLogger("YouExpress")

class GestionnaireController:
    def __init__(self , db: Session):
        self.db = db
        
        
    def create_gestionnaire(self , data : AdminCreate):
        admin = Gestionnaire(**data.model_dump())
        
        try :
            self.db.add(admin)
            self.db.commit()
            self.db.refresh(admin)
            return admin
        
        except IntegrityError as e :
            self.db.rollback()
            raise BusinessRuleError(f"Impossible de créer le compte : Cet email {data.email} est probablement déjà utilisé.")
        
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(f"Erreur lors de la création de gestionnaire : {str(e)}")
    
    
    
    def get_gestionnaire_by_id(self, id: int):
        gestionnaire = (
            self.db.query(Gestionnaire)
            .filter(Gestionnaire.id == id)
            .first()
        )
        
        if not gestionnaire:
            raise EntityNotFound(entity="Gestionnaire", id=id)
        
        return gestionnaire
    
    
    def get_all_gestionnaires(self):
        return self.db.query(Gestionnaire).all()
    
    
    def seed_gestionnaire(self):
        try:
            existing = self.db.query(Gestionnaire).filter_by(nom="Admin", prenom="Admin").first()
            
            if not existing:
                logger.info("Table Gestionnaires vide ou Admin manquant. Création de l'admin...")
                
                admin = Gestionnaire(
                    nom="Admin",
                    prenom="Admin",
                    telephone="+212522000000"
                )
                
                self.db.add(admin)
                self.db.commit()
                logger.info("Gestionnaire 'Admin Admin  ' créé avec succès.")
            else:
                logger.info("Le gestionnaire existe déjà. Seeding ignoré.")
                
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Erreur lors du seeding du gestionnaire : {str(e)}")