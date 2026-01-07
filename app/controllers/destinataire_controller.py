from sqlalchemy.orm import Session
from app.models import Destinataire
from app.schemas.user_schemas import DestinataireCreate 



class DestinatireController:
    def __init__(self , db: Session):
        self.db = db
        
        
    def create_destinataire(self , data: DestinataireCreate):
        destinataire = Destinataire(**data.model_dump())
        self.db.add(destinataire)
        self.db.commit()
        self.db.refresh(destinataire)
        return destinataire
    
    def get_destinataire_by_id(self, id: int):
        destinataire = (
            self.db.query(Destinataire)
            .filter(Destinataire.id == id)
            .first()
        )        
        return destinataire
    
    
    def get_all_destinataires(self):
        return self.db.query(Destinataire).all()