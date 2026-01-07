from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Création du moteur avec l'URL générée dans config.py
engine = create_engine(settings.DATABASE_URL)

# Configuration de la session (l'intermédiaire pour les requêtes)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dépendance pour FastAPI (à utiliser dans les Controllers/Routes)
# Elle ouvre une session, exécute la tâche, et la ferme obligatoirement après.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()