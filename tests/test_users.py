import pytest
from sqlalchemy.orm import Session
from app.controllers.gestionnaire_controller import GestionnaireController
from app.controllers.expediteur_controller import ExpediteurController
from app.controllers.destinataire_controller import DestinatireController
from app.controllers.livreur_controller import LivreurController
from app.schemas.user_schemas import (
    AdminCreate, 
    DestinataireCreate, 
    ExpediteurCreate,
    LivreurCreate
)
from app.exceptions import DatabaseError, BusinessRuleError, EntityNotFound



# Gestionnaire =====================================================================

def test_create_gestionnaire(db:Session) :
    controller = GestionnaireController(db)
    payload = AdminCreate(
        nom="Admin",
        prenom="Admin",
        telephone="0600000009"
    )
    
    admin = controller.create_gestionnaire(payload)
    
    assert admin.id is not None
    assert admin.prenom == "Admin"
    assert admin.nom == "Admin"
    assert admin.telephone == "0600000009"



def test_seed_gestionnaire(db: Session):
    controller = GestionnaireController(db)
    
    controller.seed_gestionnaire()
    admins = controller.get_all_gestionnaires()
    assert len(admins) == 1
    assert admins[0].nom == "Admin"
    
    


# Livreur ==========================================================================

def test_create_livreur_success(db: Session):
    controller = LivreurController(db)
    
    payload = LivreurCreate(
        nom="Saad",
        prenom="Saad",
        telephone="0699999999",
        vehicule="Moto",
        zone_assigne="Casa-Anfa"
    )
    
    livreur = controller.create_livreur(payload)
    assert livreur.id is not None
    assert livreur.vehicule == "Moto"
    assert livreur.zone_assigne == "Casa-Anfa"



def test_get_livreur_zone(db: Session):
    controller = LivreurController(db)
    
    payload = LivreurCreate(
        nom="Omar", 
        prenom="Omar", 
        telephone="0612345678", 
        vehicule="Camion", 
        zone_assigne="Rabat-Agdal"
    )
    
    livreur = controller.create_livreur(payload)
    zone = controller.get_livreur_zone(livreur.id)
    
    assert zone == "Rabat-Agdal"



def test_seed_livreurs(db: Session):
    controller = LivreurController(db)
    
    controller.seed_livreurs()
    
    livreurs = controller.get_all_livreurs()
    
    assert len(livreurs) >= 25
    assert livreurs[0].id is not None
    assert "Livreur" in livreurs[0].prenom
    



# Expediteur =====================================================================

def test_create_expediteur(db: Session):
    controller = ExpediteurController(db)
    
    payload = ExpediteurCreate(
        nom="Shoes",
        prenom="Top",
        telephone="0600000099",
        email="contact@top-shoes.com",
        adresse="Haut Founty, Agadir"
    )
    
    expediteur = controller.create_expediteur(payload)
    
    assert expediteur.id is not None
    assert expediteur.email == "contact@top-shoes.com"
    assert expediteur.adresse == "Haut Founty, Agadir"



def test_seed_expediteurs(db: Session):
    controller = ExpediteurController(db)
    
    controller.seed_expediteurs()
    
    expediteurs = controller.get_all_expediteurs()
    
    assert len(expediteurs) >= 5
    assert expediteurs[0].id is not None
    assert expediteurs[0].adresse == "12, Parc Industriel Sidi Maarouf, Casablanca"
    assert expediteurs[0].email == "contact@techmaroc.ma"




# Destinataire =====================================================================

def test_create_destinataire(db: Session):
    controller = DestinatireController(db)
    
    payload = DestinataireCreate(
        nom="Oussama",
        prenom="Oussama",
        telephone="+212600000088",
        email="oussama@gmail.com",
        adresse="Rue Hassan 2, Les Amicales, Agadir"
    )
    
    dest = controller.create_destinataire(payload)
    
    assert dest.id is not None
    assert dest.email == "oussama@gmail.com"



def test_seed_destinataires(db: Session):
    controller = DestinatireController(db)
    controller.seed_destinataires()
    
    destinataires = controller.get_all_destinataires()
    assert len(destinataires) >= 5