from fastapi import APIRouter, Depends , status , HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers.livreur_controller import LivreurController
from app.schemas.user_schemas import (
    LivreurCreate,
    LivreurRead
)

router = APIRouter(
    prefix="/livreurs",
    tags=["Livreurs"]
)




@router.get("{livreur_id}/zone", response_model=LivreurRead)
def get_livreur_zone(
    livreur_id: int,
    db: Session = Depends(get_db)
):
    controller = LivreurController(db)
    return controller.get_livreur_zone(livreur_id)



@router.post(
    "/",
    response_model = LivreurRead,
    status_code=status.HTTP_201_CREATED
)
def create_livreur(
    payload : LivreurCreate,
    db : Session = Depends(get_db)
):
    controller = LivreurController(db)
    return controller.create_livreur(payload)


@router.get(
    "/{zone_id}",
    response_model = LivreurRead   
)
def get_livreur_by_id(
    livreur_id: int ,
    db : Session = Depends(get_db)
):
    controller = LivreurController(db)
    livreur = controller.get_livreur_by_id(livreur_id)
    
    if not livreur:
        raise HTTPException(
            status_code=404,
            detail="Livreur non trouvée"
        )
    return livreur


@router.get(
    "/",
    response_model = list[LivreurRead]
)
def get_all_livreurs(
    db : Session = Depends(get_db)
):
    controller = LivreurController(db)
    return controller.get_all_livreurs()



@router.post("/seed/", status_code=status.HTTP_201_CREATED)
def seed_livreurs(db: Session = Depends(get_db)):
    controller = LivreurController(db)
    controller.seed_livreurs()
    return {"message": "Seed des livreurs terminé"}