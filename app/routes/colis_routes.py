from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.controllers.colis_controller import ColisController
from app.schemas.logistics_schemas import (ColisBase, ColisCreateExpediteur, ColisCreateGestionnaire, 
                                           ColisDetailOut, ColisOut, ColisUpdate, ColisUpdateStatut)



router = APIRouter(
    prefix="/colis",
    tags=["Colis"]
)




# GET avec ColisDetailOut =============================================

@router.get("/", response_model=List[ColisDetailOut])
def get_all_colis(db: Session=Depends(get_db)) :
    controller = ColisController(db)
    return controller.get_all()



@router.get("/{id_colis}", response_model=ColisDetailOut)
def get_colis(id_colis: int, db: Session=Depends(get_db)) :
    controller = ColisController(db)
    colis =  controller.get_by_id(id_colis)
    
    if not colis:
        raise HTTPException(status_code=404, detail="Colis Introuvable !")
    
    return colis



@router.get("/filter/zone/{zone_name}", response_model=List[ColisDetailOut])
def filter_by_zone(zone_name : str, db: Session = Depends(get_db)):
    controller = ColisController(db)
    return controller.filter_by_zone(zone_name)



@router.get("/filter/statut/{statut}", response_model=List[ColisDetailOut])
def filter_by_statut(statut : str, db: Session = Depends(get_db)):
    controller = ColisController(db)
    return controller.filter_by_statut(statut)


@router.get("/expediteur/{id_expediteur}", response_model=List[ColisDetailOut])
def get_colis_expediteur(id_expediteur: int, db: Session = Depends(get_db)) :
    controller = ColisController(db)
    return controller.get_for_expediteur(id_expediteur)



@router.get("/destinataire/{id_destinataire}", response_model=List[ColisDetailOut])
def get_colis_destinataire(id_destinataire: int, db: Session = Depends(get_db)) :
    controller = ColisController(db)
    return controller.get_for_destinataire(id_destinataire)


@router.get("/livreur/{id_livreur}", response_model=List[ColisDetailOut])
def get_colis_livreur(id_livreur: int, db: Session = Depends(get_db)) :
    controller = ColisController(db)
    return controller.get_for_livreur(id_livreur)










# POST | PUT | DELETE avec ColisOut ==========================================================


@router.post("/expediteur", response_model=ColisOut, status_code=status.HTTP_201_CREATED)
def create_demende_expediteur(colis_data:ColisCreateExpediteur, db: Session = Depends(get_db)) :
    controller = ColisController(db)
    return controller.create_by_expediteur(colis_data)



@router.post("/gestionnaire", response_model=ColisOut, status_code=status.HTTP_201_CREATED)
def create_demende_gestionnaire(colis_data:ColisCreateGestionnaire, db: Session = Depends(get_db)) :
    controller = ColisController(db)
    return controller.create_by_gestionnaire(colis_data)




@router.put("/{id_colis}/statut", response_model=ColisOut)
def update_colis_statut(id_colis : int, statut_data:ColisUpdateStatut, db: Session = Depends(get_db)) :
    controller = ColisController(db)
    updated_colis = controller.update_status(id_colis, statut_data)
    if not updated_colis:
        raise HTTPException(status_code=404, detail="Colis introuvable !")
    return updated_colis



@router.put("/{id_colis}", response_model=ColisOut)
def update_colis(id_colis: int, colis_data: ColisUpdateStatut, db: Session = Depends(get_db)) :
    controller = ColisController(db)
    updated_colis = controller.update_status(id_colis, colis_data)
    if not updated_colis:
        raise HTTPException(status_code=404, detail="Colis introuvable !")
    return updated_colis




@router.put("/{colis_id}/validate", response_model=ColisOut)
def validate_colis(colis_id: int, db: Session = Depends(get_db)):
    controller = ColisController(db)
    updated_colis = controller.validate(colis_id)
    if not updated_colis:
        raise HTTPException(status_code=404, detail="Colis introuvable !")
    return updated_colis




@router.delete("/{colis_id}", response_model=ColisOut)
def delete_colis(colis_id: int, db: Session = Depends(get_db)):
    controller = ColisController(db)
    deleted_colis = controller.delete(colis_id)
    if not deleted_colis:
        raise HTTPException(status_code=404, detail="Colis introuvable !")
    return deleted_colis