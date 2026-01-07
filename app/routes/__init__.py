from .zone_routes import router as zone_router
from .livreur_routes import router as livreur_route

def include_routes(app):
    app.include_router(zone_router)
    app.include_router(livreur_route)
