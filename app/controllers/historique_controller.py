from sqlalchemy.orm import Session
from app.models.historique import Historique


class HistoriqueController :
    
    def __init__(self, db:Session) :
        self.db = db
        self.table = Historique
    
    
    
    
    def get_historique_colis(self, id_colis:int) :
        historique = self.db \
            .query(self.table) \
            .filter(self.table.id_colis == id_colis) \
            .order_by(self.table.timestamp.desc()) \
            .all()
            
        return historique