from enum import Enum

class StatutColis(str, Enum):
    CREE = "cree"
    COLLECTE = "collecte"
    EN_STOCK = "en_stock"
    EN_TRANSIT = "en_transit"
    LIVRE = "livre"



class EtatColis(str, Enum):
    REFUSED = "refused"
    PENDING = "pending"
    ACCEPTED = "accepted"
