from enum import Enum

class StatutColis(str, Enum):
    CREE = "crée"
    COLLECTE = "collecte"
    EN_STOCK = "en_stock"
    EN_TRANSIT = "en_transit"
    LIVRE = "livré"



class EtatColis(str, Enum):
    REFUSED = "refused"
    PENDING = "pending"
    ACCEPTED = "accepted"
