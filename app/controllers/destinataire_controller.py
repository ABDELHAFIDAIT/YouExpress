from sqlalchemy.orm import Session
from app.models import Destinataire
from app.schemas.user_schemas import DestinataireCreate
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions import DatabaseError, BusinessRuleError, EntityNotFound
import logging

logger = logging.getLogger("YouExpress")


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
    
    
    def seed_destinataires(self):
        try:
            if self.db.query(Destinataire).count() == 0:
                logger.info("Table Destinataires vide. Insertion de 5 clients...")
                
                data = [
                    {
                        "nom": "Benali", "prenom": "Omar", 
                        "telephone": "+212661111111", "email": "omar.benali@gmail.com", 
                        "adresse": "Apt 4, Imm 12, Bd Zerktouni, Casablanca"
                    },
                    {
                        "nom": "El Amrani", "prenom": "Sarah", 
                        "telephone": "+212662222222", "email": "sarah.elamrani@yahoo.fr", 
                        "adresse": "Villa 14, Hay Riad, Rabat"
                    },
                    {
                        "nom": "Tazi", "prenom": "Mehdi", 
                        "telephone": "+212663333333", "email": "mehdi.tazi@hotmail.com", 
                        "adresse": "Derb Dabachi, N 45, Marrakech Medina"
                    },
                    {
                        "nom": "Ouazzani", "prenom": "Fatima", 
                        "telephone": "+212664444444", "email": "fatima.ouazzani@gmail.com", 
                        "adresse": "Rue Velasquez, Tanger Centre"
                    },
                    {
                        "nom": "Chraibi", "prenom": "Driss", 
                        "telephone": "+212665555555", "email": "driss.chraibi@menara.ma", 
                        "adresse": "Avenue des FAR, Fès Ville Nouvelle"
                    }
                ]
                
                destinataires = [Destinataire(**d) for d in data]
                
                self.db.add_all(destinataires)
                self.db.commit()
                logger.info("5 Destinataires insérés avec succès.")
            else:
                logger.info("Des destinataires existent déjà. Seeding ignoré.")
                
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Erreur lors du seeding des destinataires : {str(e)}")