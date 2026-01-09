from fastapi import APIRouter, Depends , status , HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers.expediteur_controller import ExpediteurController
from app.schemas.user_schemas import (
    ExpediteurCreate,
    ExpediteurRead
)



router = APIRouter(
    prefix="/expediteurs",
    tags=["Expediteurs"]
)


@router.post(
    "/",
    response_model = ExpediteurRead,
    status_code=status.HTTP_201_CREATED
)

def create_expediteur(
    payload: ExpediteurCreate,
    db: Session = Depends(get_db)
):
    controller = ExpediteurController(db)
    return controller.create_expediteur(payload)





@router.get(
    "/{expediteur_id}",
    response_model = ExpediteurRead
)
def get_expediteur_by_id(
    expediteur_id: int,
    db: Session = Depends(get_db)
):
    controller = ExpediteurController(db)
    expediteur = controller.get_expediteur_by_id(expediteur_id)
    if not expediteur:
        raise HTTPException(
            status_code=404,
            detail="Expediteur non trouvée"
        )
        
    return expediteur



@router.get(
    "/",
    response_model = list[ExpediteurRead]
)
def get_all_gestionnaires(
    db : Session = Depends(get_db)
):
    controller = ExpediteurController(db)
    return controller.get_all_expediteurs()



@router.post("/seed/", status_code=status.HTTP_201_CREATED)
def seed_expediteurs(db: Session = Depends(get_db)):
    controller = ExpediteurController(db)
    controller.seed_expediteurs()
    return {"message": "Seed des expediteurs terminé"}