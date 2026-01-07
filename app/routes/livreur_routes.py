from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers.livreur_controller import LivreurController
from app.schemas.user_schemas import (
    LivreurCreate,
    LivreurRead
)
from app.schemas.logistics_schemas import ZoneRead




@router.get("/{livreur_id}/zone", response_model=ZoneRead)
def get_livreur_zone(
    livreur_id: int,
    db: Session = Depends(get_db)
):
    controller = LivreurController(db)
    return controller.get_livreur_zone(livreur_id)
