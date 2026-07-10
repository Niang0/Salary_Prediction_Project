import pytest
from fastapi.testclient import TestClient
from api.main import app

# On initialise le client de test FastAPI
client = TestClient(app)

def test_read_root():
    """Vérifie que la racine de l'API répond correctement."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_prediction_endpoint():
    """Vérifie que la route de prédiction reçoit le JSON et renvoie un salaire."""
    # Correction du payload avec les clés exactes attendues par ton schéma Pydantic
    payload = {
        "age": 30,
        "experience": 5,
        "finance": 0,
        "it": 1,
        "rh": 0
    }
    
    # On simule la requête POST
    response = client.post("/predict", json=payload)
    
    # Assertions réajustées avec ta clé de réponse réelle
    assert response.status_code == 200
    data = response.json()
    assert "predicted_salary" in data
    assert isinstance(data["predicted_salary"], (int, float))
    