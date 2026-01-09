import pytest
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# 1. Imports des modèles (Basés sur vos fichiers)
from app.main import app
from app.models.base import Base
from app.models.zone import Zone
from app.models.expediteur import Expediteur
from app.models.destinataire import Destinataire
from app.models.livreur import Livreur
from app.models.colis import Colis
from app.models.historique import Historique
from app.models.gestionnaire import Gestionnaire

load_dotenv()

# 2. Configuration DB (Identique)
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST_TEST")
port = os.getenv("POSTGRES_PORT_TEST")
db_name = os.getenv("POSTGRES_DB_TEST")

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Fixtures Système
@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    from app.database import get_db
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()




@pytest.fixture
def zone(db):
    z = Zone(nom = "Zone Nord" , code_postal = "22844")
    db.add(z)
    db.commit()
    db.refresh(z)
    return z


@pytest.fixture
def livreur(db):
    l = Livreur(nom = "meskini" , prenom = "abir" , telephone = "0699112233" , vehicule = "bmw" , zone_assigne = "oujda")
    db.add(l)
    db.commit()
    db.refresh(l)
    return l 


@pytest.fixture
def expediteur(db):
    e = Expediteur(nom = "abdelhafid" , prenom = "ait el mokhtar" , telephone = "0699112233" , email = "abdelhafid@gmail.com" , adresse = "italy chari3 lmokhtar")
    db.add(e)
    db.commit()
    db.refresh(e)
    return e


@pytest.fixture
def destinataire(db):
    d = Destinataire(nom = "bouchra" , prenom = "miloudy" , telephone = "0699002233" , email = "bouchra@gmail.com" , adresse = "france chari3 lmiloudy")
    db.add(d)
    db.commit()
    db.refresh(d)
    return d






