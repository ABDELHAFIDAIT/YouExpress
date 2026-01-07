from sqlalchemy.orm import Session
from app.models import Expediteur
from app.schemas.user_schemas import ExpediteurCreate



class ExpediteurController:
    def __init__(self , db : Session):
        self.db = db
        
    def create_expediteur(self , data: ExpediteurCreate):
        expediteur = Expediteur(**data.model_dump())
        self.db.add(expediteur)
        self.db.commit()
        self.db.refresh(expediteur)
        return expediteur
    
    
    
    def get_expediteur_by_id(self , id: int):
        expediteur = (
            self.db.query(Expediteur)
            .filter(Expediteur.id == id)
            .first()
        )
        
        return expediteur
    
    def get_all_expediteurs(self):
        return self.db.query(Expediteur).all()