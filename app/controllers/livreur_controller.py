from sqlalchemy.orm import Session
from app.models.livreur import Livreur
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions import DatabaseError, BusinessRuleError, EntityNotFound
from app.schemas.user_schemas import (
    LivreurCreate
)
import logging


logger = logging.getLogger("YouExpress")

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
     
     
    def seed_livreurs(self):
        try:
            if self.db.query(Livreur).count() == 0:
                logger.info("Table Livreurs vide. Insertion de 25 livreurs (1 par zone)...")
                
                # Liste exacte de tes zones pour mapper 1 livreur par zone
                zones_assignees = [
                    "Casablanca - Anfa", "Casablanca - Maarif", "Casablanca - Ain Sebaa", 
                    "Casablanca - Sidi Bernoussi", "Casablanca - Hay Mohammadi",
                    "Rabat - Agdal", "Rabat - Hay Riad", "Rabat - Hassan", "Rabat - Océan",
                    "Salé - Centre", "Marrakech - Guéliz", "Marrakech - Medina", "Marrakech - Menara",
                    "Tanger - Centre", "Tanger - Malabata", "Tétouan - Centre",
                    "Fès - Ville Nouvelle", "Fès - Medina", "Meknès - Hamria",
                    "Agadir - Secteur Touristique", "Agadir - Talborjt",
                    "Oujda - Centre", "Kénitra - Centre", "Mohammedia - Centre", "El Jadida - Centre"
                ]

                # Liste de prénoms/noms pour varier
                noms = ["Alami", "Berrada", "Chaoui", "Daoudi", "El Fassi", "Fikri", "Ghazouani", "Hamdaoui", 
                        "Idrissi", "Jebari", "Kadiri", "Lahlou", "Mernissi", "Naciri", "Oukacha", "Qebbaj", 
                        "Rahmani", "Saidi", "Taleb", "Wahbi", "Yacoubi", "Ziane", "Benjelloun", "Sefrioui", "Kabbaj"]
                
                livreurs_to_create = []
                
                for i, zone_nom in enumerate(zones_assignees):
                    # Alternance des véhicules pour le réalisme
                    type_vehicule = "Moto" if i % 2 == 0 else "Partner"
                    if i % 5 == 0: type_vehicule = "Camionnette"

                    livreur = Livreur(
                        prenom=f"Livreur{i+1}", # Ex: Livreur1, Livreur2...
                        nom=noms[i],            # Ex: Alami, Berrada...
                        telephone=f"+212699{i:02d}0000", # Tel unique: +212699000000, +212699010000...
                        vehicule=type_vehicule,
                        zone_assigne=zone_nom  # Assignation stricte à la zone
                    )
                    livreurs_to_create.append(livreur)
                
                self.db.add_all(livreurs_to_create)
                self.db.commit()
                logger.info(f"{len(livreurs_to_create)} Livreurs insérés avec succès.")
            else:
                logger.info("Des livreurs existent déjà. Seeding ignoré.")
                
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Erreur lors du seeding des livreurs : {str(e)}")   