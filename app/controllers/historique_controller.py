from sqlalchemy.orm import Session
from app.models.historique import Historique


class HistoriqueController :
    
    def __init__(self, db:Session) :
        self.db = db
        self.table = Historique
    
    
    def create_historique(self, id_colis:int, ancien_status:str, nouveau_status:str) :
        new_hist = self.table(
            id_colis=id_colis,
            ancien_status = ancien_status,
            nouveau_status = nouveau_status
        )
        
        self.db.add(new_hist)
        self.db.commit()
        self.db.refresh(new_hist)
        
        return new_hist
    
    
    def get_historique_colis(self, id_colis:int) :
        historique = self.db \
            .query(self.table) \
            .filter(self.table.id_colis == id_colis) \
            .order_by(self.table.timestamp.desc()) \
            .all()
            
        return historique