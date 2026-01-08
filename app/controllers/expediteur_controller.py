from sqlalchemy.orm import Session
from app.models import Expediteur
from app.schemas.user_schemas import ExpediteurCreate
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions import DatabaseError, BusinessRuleError, EntityNotFound
import logging

logger = logging.getLogger("YouExpress")


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
    
    
    
    def seed_expediteurs(self):
        try:
            if self.db.query(Expediteur).count() == 0:
                logger.info("Table Expediteurs vide. Insertion de 5 expéditeurs...")
                
                data = [
                    {
                        "nom": "Société TechMaroc", "prenom": "Responsable Logistique", 
                        "telephone": "+212522998877", "email": "contact@techmaroc.ma", 
                        "adresse": "12, Parc Industriel Sidi Maarouf, Casablanca"
                    },
                    {
                        "nom": "Mode Caftan Lux", "prenom": "Khadija", 
                        "telephone": "+212535600000", "email": "commandes@caftanlux.ma", 
                        "adresse": "45 Rue des Mérinides, Fès"
                    },
                    {
                        "nom": "Bio Argan Atlas", "prenom": "Hassan", 
                        "telephone": "+212524303030", "email": "export@bioargan.ma", 
                        "adresse": "Km 5 Route de l'Ourika, Marrakech"
                    },
                    {
                        "nom": "Librairie Al Qalam", "prenom": "Youssef", 
                        "telephone": "+212537707070", "email": "info@alqalam.ma", 
                        "adresse": "22 Avenue Mohammed V, Rabat"
                    },
                    {
                        "nom": "Auto Pièces Nord", "prenom": "Said", 
                        "telephone": "+212539909090", "email": "service@autopieces.ma", 
                        "adresse": "Zone Franche, Tanger"
                    }
                ]
                
                expediteurs = [Expediteur(**d) for d in data]
                
                self.db.add_all(expediteurs)
                self.db.commit()
                logger.info("5 Expéditeurs insérés avec succès.")
            else:
                logger.info("Des expéditeurs existent déjà. Seeding ignoré.")
                
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Erreur lors du seeding des expéditeurs : {str(e)}")