from fastapi import APIRouter, Depends , status , HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers.destinataire_controller import DestinatireController
from app.schemas.user_schemas import (
    DestinataireCreate,
    DestinataireRead
)



router = APIRouter(
    prefix="/destinataire",
    tags=["Destinataire"]
)


@router.post(
    "/",
    response_model = DestinataireRead,
    status_code=status.HTTP_201_CREATED
)

def create_expediteur(
    payload: DestinataireRead,
    db: Session = Depends(get_db)
):
    controller = DestinatireController(db)
    return controller.create_destinataire(payload)


@router.get(
    "/{destinataire_id}",
    response_model = DestinataireRead,
)
def get_destinataire_by_id(
    destinataire_id:int ,
    db: Session = Depends(get_db)
):
    controller = DestinatireController(db)
    destinataire = controller.get_destinataire_by_id(destinataire_id)
    if not destinataire:
        raise HTTPException(
            status_code=404,
            detail="Destinatire non trouvée"
        )
    return destinataire


@router.get(
    "/",
    response_model = DestinataireRead
)

def get_all_destinataires(
    db: Session =Depends(get_db),
):
    controller = DestinatireController(db)
    return controller.get_all_destinataires()
