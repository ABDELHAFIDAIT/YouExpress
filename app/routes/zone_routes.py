from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers.zone_controller import ZoneController
from app.schemas.logistics_schemas import (
    ZoneCreate,
    ZoneOut
)



router = APIRouter(
    prefix="/zones",
    tags=["Zones"]
)



@router.post(
    "/",
    response_model=ZoneOut,
    status_code=status.HTTP_201_CREATED
)
def create_zone(
    payload: ZoneCreate,
    db: Session = Depends(get_db)
):
    controller = ZoneController(db)
    return controller.create_zone(payload)


@router.get(
    "/{zone_id}",
    response_model=ZoneOut
)
def get_zone_by_id(
    zone_id: int,
    db: Session = Depends(get_db)
):
    controller = ZoneController(db)
    zone = controller.get_zone_by_id(zone_id)

    if not zone:
        raise HTTPException(
            status_code=404,
            detail="Zone non trouvée"
        )

    return zone


@router.get(
    "/",
    response_model=list[ZoneOut]
)
def get_all_zones(db: Session = Depends(get_db)):
    controller = ZoneController(db)
    return controller.get_all_zones()




@router.post(
    "/seed/maroc",
    status_code=status.HTTP_201_CREATED
)
def seed_maroc_zones(db: Session = Depends(get_db)):
    controller = ZoneController(db)
    controller.seed_maroc_zones()
    return {"message": "Seed des zones marocaines terminé"}
