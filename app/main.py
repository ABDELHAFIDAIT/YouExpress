from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine
from app.models.base import Base
import logging

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


@app.get("/health")
def api_health():
    return {"status": "ok", "message": "YouExpress API est en cours d'éxécution !"}