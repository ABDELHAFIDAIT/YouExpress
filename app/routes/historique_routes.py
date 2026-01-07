from fastapi import APIRouter, Depends , status , HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.controllers.historique_controller import HistoriqueController
from app.schemas.logistics_schemas import (
    HistoriqueOut,
)



router = APIRouter(
    prefix="/historique",
    tags=["Historique"]
)


@router.get(
    "/{colis_id}",
    response_model = HistoriqueOut
)
def get_historique_colis(
    colis_id: int,
    db: Session = Depends(get_db)
):
    controller = HistoriqueController(db)
    historique = controller.get_historique_colis(colis_id)
    
    if not historique:
        raise HTTPException(
            status_code=404,
            detail="Historique non trouvée"
        )
        
    return historique