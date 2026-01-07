from sqlalchemy.orm import Session
from app.models import Gestionnaire
from app.schemas.user_schemas import AdminCreate



class GestionnaireController:
    def __init__(self , db: Session):
        self.db = db
        
        
    def create_gestionnaire(self , data : AdminCreate):
        admin = Gestionnaire(**data.model_dump())
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return admin
    
    
    def get_gestionnaire_by_id(self, id: int):
        gestionnaire = (
            self.db.query(Gestionnaire)
            .filter(Gestionnaire.id == id)
            .first()
        )
        
        return gestionnaire
    
    
    def get_all_gestionnaires(self):
        return self.db.query(Gestionnaire).all()