import pytest


from app.controllers.colis_controller import ColisController
from app.models import Colis
from app.models.enums import StatutColis , EtatColis
from app.schemas.logistics_schemas import (
    ColisCreateExpediteur,
    ColisCreateGestionnaire,
    ColisUpdate,
    ColisUpdateStatut
)

def test_create_colis_by_expediteur(db, zone, expediteur, destinataire):
    controller = ColisController(db)

    data = ColisCreateExpediteur(
        description="Colis test",
        poids=2,
        ville_destination="Paris",
        zone_id=zone.id,
        expediteur_id=expediteur.id,
        destinataire_id=destinataire.id
    )

    colis = controller.create_by_expediteur(data)
    assert colis.id is not None
    assert colis.description == "Colis test"
    assert colis.statut == StatutColis.CREE
    assert colis.etat == EtatColis.PENDING
    assert db.query(Colis).count() == 1




def test_create_colis_by_gestionnaire(db , zone , expediteur , destinataire , livreur):
    controller = ColisController(db)
    
    data = ColisCreateGestionnaire(
        description="colis gestionnaire",
        poids = 4,
        ville_destination="oujda",
        zone_id = zone.id,
        expediteur_id=expediteur.id,
        destinataire_id=destinataire.id,
        livreur_id=livreur.id
    )
    
    colis = controller.create_by_gestionnaire(data)
    assert colis.etat == EtatColis.ACCEPTED
    assert colis.statut == StatutColis.CREE



# def test_get_colis_by_id(db , zone , expediteur , destinataire):
#     controller = ColisController(db)