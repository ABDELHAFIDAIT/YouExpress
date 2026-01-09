from fastapi import APIRouter, Depends , status , HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers.gestionnaire_controller import GestionnaireController
from app.schemas.user_schemas import (
    AdminCreate,
    AdminRead
)



router = APIRouter(
    prefix="/gestionnaires",
    tags=["Gestionnaires"]
)



@router.post(
    "/",
    response_model = AdminRead,
    status_code=status.HTTP_201_CREATED
)

def create_gestionnaire(
    payload: AdminCreate,
    db: Session = Depends(get_db)
):
    controller = GestionnaireController(db)
    return controller.create_gestionnaire(payload)




@router.get(
    "/{gestionnaire_id}",
    response_model = AdminRead
)
def get_gestionnaire_by_id(
    gestionnaire_id: int,
    db: Session = Depends(get_db)
):
    controller = GestionnaireController(db)
    gestionnaire = controller.get_gestionnaire_by_id(gestionnaire_id)
    if not gestionnaire:
        raise HTTPException(
            status_code=404,
            detail="Gestionnaire non trouvée"
        )
        
    return gestionnaire




@router.get(
    "/",
    response_model = list[AdminRead]
)
def get_all_gestionnaires(
    db : Session = Depends(get_db)
):
    controller = GestionnaireController(db)
    return controller.get_all_gestionnaires()


@router.post("/seed/", status_code=status.HTTP_201_CREATED)
def seed_gestionnaires(db: Session = Depends(get_db)):
    controller = GestionnaireController(db)
    controller.seed_gestionnaire()
    return {"message": "Seed des gestionnaires terminé"}