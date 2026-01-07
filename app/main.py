from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine
from app.models.base import Base
import logging
from app.routes import (
    colis_routes,
    destinataire_routes,
    expediteur_routes,
    gestionnaire_routes,
    historique_routes,
    livreur_routes,
    zone_routes
)

# Configuration basique du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("YouExpress")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Au démarrage ---
    logger.info("Démarrage de YouExpress...")
    try:
        # C'est ici que la magie opère : SQLAlchemy crée les tables si elles n'existent pas
        Base.metadata.create_all(bind=engine)
        logger.info("Connexion Base de données établie et tables vérifiées.")
    except Exception as e:
        logger.error(f"Erreur de connexion à la base de données : {e}")
    
    yield
    
    # --- À l'arrêt ---
    logger.info("Arrêt de YouExpress.")



app = FastAPI(title="YouExpress API", lifespan=lifespan)



app.include_router(colis_routes)
app.include_router(destinataire_routes)
app.include_router(expediteur_routes)
app.include_router(gestionnaire_routes)
app.include_router(historique_routes)
app.include_router(livreur_routes)
app.include_router(zone_routes)



@app.get("/health")
def api_health():
    return {"status": "ok", "message": "YouExpress API est en cours d'éxécution !"}