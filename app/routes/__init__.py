from .zone_routes import router as zone_router

def include_routes(app):
    app.include_router(zone_router)
