import pytest
from fastapi import status
from sqlalchemy import text, inspect
import os

def test_read_root(client):
 
    response = client.get("/")
    assert response.status_code in [200, 404]

def test_docs_availability(client):
    response = client.get("/openapi.json")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "info" in data
    assert "YouExpress" in data["info"]["title"]

def test_database_connection(db):
    try:
        result = db.execute(text("SELECT 1"))
        assert result.scalar() == 1
    except Exception as e:
        pytest.fail(f"Impossible de se connecter à la base de données : {str(e)}")

def test_models_table_creation(db):
    engine = db.get_bind()
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    expected_tables = [
        "zones",
        "expediteurs",
        "destinataires",
        "livreurs",
        "gestionnaires",
        "colis",
        "historiques"
    ]


    for table in expected_tables:
        assert table in existing_tables, f"ERREUR : La table '{table}' manque dans la base de données !"

def test_environment_variables():
    db_name = os.getenv("POSTGRES_DB_TEST")
    assert db_name == "youexpress_test", "Attention : Vous ne semblez pas utiliser la base de test !"
