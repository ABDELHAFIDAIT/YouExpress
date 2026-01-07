from sqlalchemy.orm import Session
from app.models import Zone
from app.schemas.logistics_schemas import ZoneCreate


class ZoneController:
    def __init__(self , db: Session):
        self.db = db
        
    def create_zone(self , data: ZoneCreate):
        zone = Zone(**data.model_dump())
        self.db.add(zone)
        self.db.commit()
        self.db.refresh(zone)
        return zone
    
    
    def get_zone_by_id(self , id: int):
        zone = (
            self.db.query(Zone)
            .filter(Zone.id == id)
            .first()
        )
        
        return zone
    
    def get_all_zones(self):
        return self.db.query(Zone).all()
    
        


