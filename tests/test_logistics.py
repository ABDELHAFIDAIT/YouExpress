import pytest

from datetime import datetime
from app.controllers.colis_controller import ColisController , HistoriqueController
from app.controllers.zone_controller import ZoneController
from app.models import Colis , Historique , Zone
from app.models.enums import StatutColis , EtatColis
from app.schemas.logistics_schemas import (
    ColisCreateExpediteur,
    ColisCreateGestionnaire,
    ColisUpdate,
    ColisUpdateStatut,
    ZoneCreate
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



def test_get_colis_by_id(db , zone , expediteur , destinataire):
    controller = ColisController(db)
    data = ColisCreateExpediteur(
        description="colis test",
        poids=2,
        ville_destination="Paroujdais",
        zone_id=zone.id,
        expediteur_id=expediteur.id,
        destinataire_id=destinataire.id
    )
    colis = controller.create_by_expediteur(data)
    result = controller.get_by_id(colis.id)

    assert result is not None
    assert result.id == colis.id
    
    
    
def test_update_colis(db , zone , expediteur , destinataire):
    controller = ColisController(db)
    data = ColisCreateExpediteur(
        description="anceienne",
        poids=2,
        ville_destination="oujda",
        zone_id=zone.id,
        expediteur_id=expediteur.id,
        destinataire_id=destinataire.id
    )
    colis = controller.create_by_expediteur(data)
    update_data = ColisUpdate(description="nouvelle data")
    updated = controller.update(colis.id , update_data)
    assert updated.description == "nouvelle data"
    
    
    
    
def test_validate_colis(db , zone , expediteur , destinataire):
    controller = ColisController(db)
    colis = controller.create_by_expediteur(
        ColisCreateExpediteur(
            description="validation",
            poids=1,
            ville_destination="oujda",
            zone_id=zone.id,
            expediteur_id=expediteur.id,
            destinataire_id=destinataire.id
        )
    )
    
    validated = controller.validate(colis.id)
    assert validated.etat == EtatColis.ACCEPTED





def test_delete_colis(db, zone, expediteur, destinataire):
    controller = ColisController(db)

    colis = controller.create_by_expediteur(
        ColisCreateExpediteur(
            description="deleting",
            poids=2,
            ville_destination="oujda",
            zone_id=zone.id,
            expediteur_id=expediteur.id,
            destinataire_id=destinataire.id
        )
    )

    deleted = controller.delete(colis.id)
    assert deleted is not None
    assert db.query(Colis).filter(Colis.id == colis.id).first() is None





def test_get_all_colis(db, zone , expediteur , destinataire):
    controller = ColisController(db)
    colis = controller.create_by_expediteur(
        ColisCreateExpediteur(
            description="get all",
            poids=2,
            ville_destination="oujda",
            zone_id=zone.id,
            expediteur_id=expediteur.id,
            destinataire_id=destinataire.id
        )
    )
    
    result = controller.get_all()
    assert len(result) == 1
    

@pytest.fixture
def colis_controller(db):
    controller = ColisController(db)
    controller.historique_ctrl.create_historique = lambda *args, **kwargs: None
    return controller


def test_update_status_colis(db, zone, expediteur, destinataire, colis_controller):
    colis = colis_controller.create_by_expediteur(
        ColisCreateExpediteur(
            description="Test statut",
            poids=2,
            ville_destination="Oujda",
            zone_id=zone.id,
            expediteur_id=expediteur.id,
            destinataire_id=destinataire.id
        )
    )
    
    statut_initial = colis.statut
    
    updated = colis_controller.update_status(
        colis.id,
        ColisUpdateStatut(statut=StatutColis.EN_STOCK)
    )
    
    assert updated.statut == StatutColis.EN_STOCK
    assert updated.statut != statut_initial
    assert updated.id == colis.id




def test_filter_by_zone(db, zone, expediteur, destinataire ):
    controller = ColisController(db)

    controller.create_by_expediteur(
        ColisCreateExpediteur(
            description="zone test",
            poids=1,
            ville_destination="oujda",
            zone_id=zone.id,
            expediteur_id=expediteur.id,
            destinataire_id=destinataire.id
        )
    )

    result = controller.filter_by_zone(zone.nom)
    assert len(result) == 1


def test_filter_by_statut(db, zone, expediteur, destinataire):
    controller = ColisController(db)

    colis = controller.create_by_expediteur(
        ColisCreateExpediteur(
            description="filtrage statut",
            poids=1,
            ville_destination="oujda",
            zone_id=zone.id,
            expediteur_id=expediteur.id,
            destinataire_id=destinataire.id
        )
    )

    result = controller.filter_by_statut(colis.statut)
    assert len(result) == 1
    assert result[0].id == colis.id
    
    
    
def test_get_for_expediteur(db, zone, expediteur, destinataire, livreur):
    controller = ColisController(db)

    colis = controller.create_by_expediteur(
        ColisCreateExpediteur(
            description="pour expediteur",
            poids=1,
            ville_destination="oujda",
            zone_id=zone.id,
            expediteur_id=expediteur.id,
            destinataire_id=destinataire.id
        )
    )

    result = controller.get_for_expediteur(expediteur.id)
    assert len(result) == 1
    assert result[0].id == colis.id



def test_get_for_livreur(db, zone, expediteur, destinataire, livreur):
    controller = ColisController(db)

    colis = controller.create_by_gestionnaire(
        ColisCreateGestionnaire(
            description="pour livreur",
            poids=2,
            ville_destination="oujda",
            zone_id=zone.id,
            expediteur_id=expediteur.id,
            destinataire_id=destinataire.id,
            livreur_id=livreur.id
        )
    )
    db.refresh(colis)
    print("DEBUG:", colis.id, colis.livreur_id)


    result = controller.get_for_livreur(livreur.id)

    assert len(result) == 1

    row = result[0]
    assert row.id == colis.id
    assert row.nom_zone == zone.nom
    assert row.expediteur == f"{expediteur.nom} {expediteur.prenom}"
    assert row.destinataire == f"{destinataire.nom} {destinataire.prenom}"








def test_get_historique_colis(db, zone, expediteur, destinataire):
    colis_controller = ColisController(db)
    historique_controller = HistoriqueController(db)
    
    colis = colis_controller.create_by_expediteur(
        ColisCreateExpediteur(
            description="test historique",
            poids=1,
            ville_destination="oujda",
            zone_id=zone.id,
            expediteur_id=expediteur.id,
            destinataire_id=destinataire.id
        )
    )
    
    historique1 = Historique(
        id_colis=colis.id,
        ancien_status=StatutColis.CREE.value, 
        nouveau_status=StatutColis.EN_STOCK.value,
        timestamp=datetime.now()
    )
    db.add(historique1)
    
    historique2 = Historique(
        id_colis=colis.id,
        ancien_status=StatutColis.EN_STOCK.value,
        nouveau_status=StatutColis.COLLECTE.value,
        timestamp=datetime.now()
    )
    db.add(historique2)
    db.commit()
    
    historique_list = historique_controller.get_historique_colis(colis.id)
    
    assert len(historique_list) == 2
    assert historique_list[0].nouveau_status == StatutColis.COLLECTE.value
    assert historique_list[1].nouveau_status == StatutColis.EN_STOCK.value
    assert all(h.id_colis == colis.id for h in historique_list)
    
    
def test_create_zone(db):
    controller = ZoneController(db)
    
    zone_data = ZoneCreate(
        nom="Casablanca - Anfa",
        code_postal="20000"
    )
    
    zone = controller.create_zone(zone_data)
    
    assert zone.id is not None
    assert zone.nom == "Casablanca - Anfa"
    assert zone.code_postal == "20000"
    assert db.query(Zone).count() == 1
    
    
    
def test_get_zone_by_id(db):
    controller = ZoneController(db)
    
    zone = controller.create_zone(
        ZoneCreate(nom="Fès - Ville Nouvelle", code_postal="30000")
    )
    
    retrieved_zone = controller.get_zone_by_id(zone.id)
    
    assert retrieved_zone.id == zone.id
    assert retrieved_zone.nom == "Fès - Ville Nouvelle"
    assert retrieved_zone.code_postal == "30000"
    
    
def test_get_all_zones(db):
    controller = ZoneController(db)
    
    zones_data = [
        ZoneCreate(nom="Tanger - Centre", code_postal="90000"),
        ZoneCreate(nom="Agadir - Talborjt", code_postal="80020"),
        ZoneCreate(nom="Oujda - Centre", code_postal="60000")
    ]
    
    for zone_data in zones_data:
        controller.create_zone(zone_data)
    
    all_zones = controller.get_all_zones()
    
    assert len(all_zones) == 3
    assert all(isinstance(z, Zone) for z in all_zones)
    
    noms = [z.nom for z in all_zones]
    assert "Tanger - Centre" in noms
    assert "Agadir - Talborjt" in noms
    assert "Oujda - Centre" in noms
    
    
    

def test_seed_maroc_zones(db):
    controller = ZoneController(db)
    assert db.query(Zone).count() == 0
    controller.seed_maroc_zones()
    assert db.query(Zone).count() == 25
    
    casablanca = db.query(Zone).filter(Zone.nom == "Casablanca - Anfa").first()
    assert casablanca is not None
    assert casablanca.code_postal == "20000"
    
    rabat = db.query(Zone).filter(Zone.nom == "Rabat - Agdal").first()
    assert rabat is not None
    assert rabat.code_postal == "10000"