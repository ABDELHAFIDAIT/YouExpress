from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine
from app.models.base import Base
import logging
from app.routes.colis_routes import router as colis_router
from app.routes.destinataire_routes import router as destinataire_router
from app.routes.expediteur_routes import router as expediteur_router
from app.routes.gestionnaire_routes import router as gestionnaire_router
from app.routes.historique_routes import router as historique_router
from app.routes.livreur_routes import router as livreur_router
from app.routes.zone_routes import router as zone_router
from app.models import colis, zone, historique, livreur, expediteur, destinataire, gestionnaire



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("YouExpress")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Démarrage de YouExpress...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Connexion Base de données établie et tables vérifiées.")
    except Exception as e:
        logger.error(f"Erreur de connexion à la base de données : {e}")
    
    yield
    
    logger.info("Arrêt de YouExpress.")



app = FastAPI(title="YouExpress API", lifespan=lifespan)



app.include_router(colis_router)
app.include_router(destinataire_router)
app.include_router(expediteur_router)
app.include_router(gestionnaire_router)
app.include_router(historique_router)
app.include_router(livreur_router)
app.include_router(zone_router)



@app.get("/health")
def api_health():
    return {"status": "ok", "message": "YouExpress API est en cours d'éxécution !"}