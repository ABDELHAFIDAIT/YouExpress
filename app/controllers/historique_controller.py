from sqlalchemy.orm import Session
from app.models import Historique, Colis
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions import DatabaseError, BusinessRuleError, EntityNotFound

class HistoriqueController :
    
    def __init__(self, db:Session) :
        self.db = db
        self.table = Historique
    
    
    
    
    def get_historique_colis(self, id_colis:int) :
        try:
            colis_exists = self.db.query(Colis).filter(Colis.id == id_colis).first()
            
            if not colis_exists:
                raise EntityNotFound(entity="Colis", id=id_colis)

            historique = (
                self.db.query(self.table)
                .filter(self.table.id_colis == id_colis)
                .order_by(self.table.timestamp.desc())
                .all()
            )
            
            return historique

        except SQLAlchemyError as e:
            raise DatabaseError(f"Erreur lors de la lecture de l'historique : {str(e)}")