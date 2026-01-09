from sqlalchemy.orm import Session
from app.models import Zone
from app.schemas.logistics_schemas import ZoneCreate
import logging
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions import DatabaseError, BusinessRuleError, EntityNotFound


logger = logging.getLogger("YouExpress")


class ZoneController:
    def __init__(self , db: Session):
        self.db = db
        

    def create_zone(self , data: ZoneCreate):
        zone = Zone(**data.model_dump())
        
        try:
            self.db.add(zone)
            self.db.commit()
            self.db.refresh(zone)
            return zone
            
        except IntegrityError as e:
            self.db.rollback()
            raise BusinessRuleError(f"Impossible de créer la zone : Le nom '{data.nom}' ou le code postal '{data.code_postal}' existe déjà.")
            
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseError(f"Erreur lors de la création de la zone : {str(e)}")
    
    
    def get_zone_by_id(self , id: int):
        zone = (
            self.db.query(Zone)
            .filter(Zone.id == id)
            .first()
        )
        
        if not zone:
            raise EntityNotFound(entity="Zone", id=id)
        
        return zone
    
    
    def get_all_zones(self):
        return self.db.query(Zone).all()
        
        
    def seed_maroc_zones(self):
        try:
            existing_zone = self.db.query(Zone).first()
            
            if not existing_zone:
                logger.info("Table Zones vide. Insertion de 25 zones marocaines...")
                villes = [
                    {"nom": "Casablanca - Anfa", "code_postal": "20000"},
                    {"nom": "Casablanca - Maarif", "code_postal": "20100"},
                    {"nom": "Casablanca - Ain Sebaa", "code_postal": "20250"},
                    {"nom": "Casablanca - Sidi Bernoussi", "code_postal": "20600"},
                    {"nom": "Casablanca - Hay Mohammadi", "code_postal": "20300"},
                    
                    {"nom": "Rabat - Agdal", "code_postal": "10000"},
                    {"nom": "Rabat - Hay Riad", "code_postal": "10100"},
                    {"nom": "Rabat - Hassan", "code_postal": "10010"},
                    {"nom": "Rabat - Océan", "code_postal": "10040"},
                    {"nom": "Salé - Centre", "code_postal": "11000"},

                    {"nom": "Marrakech - Guéliz", "code_postal": "40000"},
                    {"nom": "Marrakech - Medina", "code_postal": "40030"},
                    {"nom": "Marrakech - Menara", "code_postal": "40160"},

                    {"nom": "Tanger - Centre", "code_postal": "90000"},
                    {"nom": "Tanger - Malabata", "code_postal": "90060"},
                    {"nom": "Tétouan - Centre", "code_postal": "93000"},

                    {"nom": "Fès - Ville Nouvelle", "code_postal": "30000"},
                    {"nom": "Fès - Medina", "code_postal": "30030"},
                    {"nom": "Meknès - Hamria", "code_postal": "50000"},

                    {"nom": "Agadir - Secteur Touristique", "code_postal": "80000"},
                    {"nom": "Agadir - Talborjt", "code_postal": "80020"},
                    {"nom": "Oujda - Centre", "code_postal": "60000"},
                    {"nom": "Kénitra - Centre", "code_postal": "14000"},
                    {"nom": "Mohammedia - Centre", "code_postal": "28810"},
                    {"nom": "El Jadida - Centre", "code_postal": "24000"}
                ]
                
                zones_to_create = [Zone(nom=v["nom"], code_postal=v["code_postal"]) for v in villes]
                
                self.db.add_all(zones_to_create) 
                self.db.commit()
                
                logger.info(f"{len(villes)} zones insérées avec succès.")
            else:
                logger.info("Les zones existent déjà. Seeding ignoré.")
                
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Erreur lors du seeding des zones : {str(e)}")
            
