from sqlalchemy.orm import Session
from app.models.colis import Colis
from app.models.zone import Zone
from app.models.expediteur import Expediteur
from app.models.livreur import Livreur
from app.models.destinataire import Destinataire
from app.models.enums import StatutColis, EtatColis
from app.schemas.logistics_schemas import ColisCreateExpediteur, ColisCreateGestionnaire, ColisUpdate, ColisUpdateStatut
from app.controllers.historique_controller import HistoriqueController



class ColisController :
    def __init__(self, db:Session) :
        self.db = db
        self.table = Colis
        self.historique_ctrl = HistoriqueController(db)
    
    
    def get_all(self) :
        colis = self.db \
            .query(
                self.table.id,
                self.table.description,
                self.table.poids,
                self.table.ville_destination,
                self.table.statut,
                self.table.etat,
                
                Zone.nom.label("nom_zone"), 
                (Expediteur.nom + " " + Expediteur.prenom).label("expediteur"),
                (Destinataire.nom + " " + Destinataire.prenom).label("destinataire"),
                (Livreur.nom + " " + Livreur.prenom).label("livreur")
            ) \
            .join(Zone, self.table.zone_id == Zone.id) \
            .join(Expediteur, self.table.expediteur_id == Expediteur.id) \
            .join(Destinataire, self.table.destinataire_id == Destinataire.id) \
            .outerjoin(Livreur, self.table.livreur_id == Livreur.id) \
            .all()
        return colis
    
    
    def get_by_id(self, id_colis:int) :
        colis = self.db \
            .query(
                self.table.id,
                self.table.description,
                self.table.poids,
                self.table.ville_destination,
                self.table.statut,
                self.table.etat,
                
                Zone.nom.label("nom_zone"), 
                (Expediteur.nom + " " + Expediteur.prenom).label("expediteur"),
                (Destinataire.nom + " " + Destinataire.prenom).label("destinataire"),
                (Livreur.nom + " " + Livreur.prenom).label("livreur")
            ) \
            .join(Zone, self.table.zone_id == Zone.id) \
            .join(Expediteur, self.table.expediteur_id == Expediteur.id) \
            .join(Destinataire, self.table.destinataire_id == Destinataire.id) \
            .outerjoin(Livreur, self.table.livreur_id == Livreur.id) \
            .filter(self.table.id == id_colis) \
            .first()
        
        return colis
    
    
    def create_by_expediteur(self, data:ColisCreateExpediteur) :
        colis_data = data.model_dump()
        
        colis_data["statut"] = StatutColis.CREE
        colis_data["etat"] = EtatColis.PENDING
        
        new_colis = self.table(**colis_data)
        
        self.db.add(new_colis)
        self.db.commit()
        self.db.refresh(new_colis)
        
        return new_colis
    
    
    def create_by_gestionnaire(self, data:ColisCreateGestionnaire) :
        colis_data = data.model_dump()
        
        colis_data["statut"] = StatutColis.CREE
        colis_data["etat"] = EtatColis.ACCEPTED
        
        new_colis = self.table(**colis_data)
        
        self.db.add(new_colis)
        self.db.commit()
        self.db.refresh(new_colis)
        
        return new_colis
    
    
    def update_status(self, id_colis:int, statut_data:ColisUpdateStatut) :
        colis = self.get_by_id(id_colis)
        
        if not colis:
            return None
        
        new_statut = statut_data.statut
        
        if new_statut["statut"] != colis.statut :
            self.historique_ctrl.create_historique(
                id_colis=id_colis, 
                ancien_status=colis.statut.value, 
                nouveau_status=new_statut.value
            )
            
            colis.statut = new_statut
            self.db.commit()
            self.db.refresh(colis)
        
        return colis
    
    
    def update(self, id_colis:int, update_data:ColisUpdate) :
        colis = self.get_by_id(id_colis)
        
        if not colis:
            return None
        
        new_data = update_data.model_dump(exclude_unset=True)
        
        for key, value in new_data.items():
            setattr(colis, key, value)
        
        self.db.commit()
        self.db.refresh(colis)
        
        return colis
    
    
    def delete(self, id_colis:int) :
        colis = self.get_by_id(id_colis)
        
        if not colis :
            return None
        
        self.db.delete(colis)
        self.db.commit()
        
        return colis
    
    
    def validate(self, id_colis:int) :
        colis = colis = self.get_by_id(id_colis)
        
        if not colis :
            return None
        
        colis.etat = EtatColis.ACCEPTED
        
        self.db.commit()
        self.db.refresh(colis)
        
        return colis
    
    
    def filter_by_zone(self, zone_name:str) :
        colis = self.db \
            .query(
                self.table.id,
                self.table.description,
                self.table.poids,
                self.table.ville_destination,
                self.table.statut,
                self.table.etat,
                
                Zone.nom.label("nom_zone"), 
                (Expediteur.nom + " " + Expediteur.prenom).label("expediteur"),
                (Destinataire.nom + " " + Destinataire.prenom).label("destinataire"),
                (Livreur.nom + " " + Livreur.prenom).label("livreur")
            ) \
            .join(Zone, self.table.zone_id == Zone.id) \
            .join(Expediteur, self.table.expediteur_id == Expediteur.id) \
            .join(Destinataire, self.table.destinataire_id == Destinataire.id) \
            .outerjoin(Livreur, self.table.livreur_id == Livreur.id) \
            .filter(Zone.nom.ilike(f"%{zone_name}%")) \
            .all()
        
        return colis
    
    
    def filter_by_statut(self, statut:str) :
        colis = self.db \
            .query(
                self.table.id,
                self.table.description,
                self.table.poids,
                self.table.ville_destination,
                self.table.statut,
                self.table.etat,
                
                Zone.nom.label("nom_zone"), 
                (Expediteur.nom + " " + Expediteur.prenom).label("expediteur"),
                (Destinataire.nom + " " + Destinataire.prenom).label("destinataire"),
                (Livreur.nom + " " + Livreur.prenom).label("livreur")
            ) \
            .join(Zone, self.table.zone_id == Zone.id) \
            .join(Expediteur, self.table.expediteur_id == Expediteur.id) \
            .join(Destinataire, self.table.destinataire_id == Destinataire.id) \
            .outerjoin(Livreur, self.table.livreur_id == Livreur.id) \
            .filter(self.table.statut == statut) \
            .all()
        
        return colis
    
    
    def get_for_expediteur(self, id_expediteur:int) :
        colis = self.db \
            .query(
                self.table.id,
                self.table.description,
                self.table.poids,
                self.table.ville_destination,
                self.table.statut,
                self.table.etat,
                
                Zone.nom.label("nom_zone"), 
                (Livreur.nom + " " + Livreur.prenom).label("livreur"),
                (Destinataire.nom + " " + Destinataire.prenom).label("destinataire")
            ) \
            .join(Zone, self.table.zone_id == Zone.id) \
            .join(Livreur, self.table.livreur_id == Livreur.id) \
            .join(Destinataire, self.table.destinataire_id == Destinataire.id) \
            .filter(self.table.expediteur_id == id_expediteur) \
            .all()
        
        return colis
    
    
    def get_for_livreur(self, id_livreur:int) :
        colis = self.db \
            .query(
                self.table.id,
                self.table.description,
                self.table.poids,
                self.table.ville_destination,
                self.table.statut,
                self.table.etat,
                
                Zone.nom.label("nom_zone"), 
                (Expediteur.nom + " " + Expediteur.prenom).label("expediteur"),
                (Destinataire.nom + " " + Destinataire.prenom).label("destinataire")
            ) \
            .join(Zone, self.table.zone_id == Zone.id) \
            .join(Expediteur, self.table.expediteur_id == Expediteur.id) \
            .join(Destinataire, self.table.destinataire_id == Destinataire.id) \
            .filter(self.table.livreur_id == id_livreur) \
            .all()
        
        return colis
    
    
    def get_for_destinataire(self, id_destinataire:int) :
        colis = self.db \
            .query(
                self.table.id,
                self.table.description,
                self.table.poids,
                self.table.ville_destination,
                self.table.statut,
                self.table.etat,
                
                Zone.nom.label("nom_zone"), 
                (Expediteur.nom + " " + Expediteur.prenom).label("expediteur"),
                (Livreur.nom + " " + Livreur.prenom).label("livreur")
            ) \
            .join(Zone, self.table.zone_id == Zone.id) \
            .join(Expediteur, self.table.expediteur_id == Expediteur.id) \
            .join(Livreur, self.table.livreur_id == Livreur.id) \
            .filter(self.table.destinataire_id == id_destinataire, self.table.etat == EtatColis.ACCEPTED) \
            .all()
        
        return colis


