import sys
import os

# --- LIGNES MAGIQUES POUR LE PATH ---
# On ajoute le dossier parent (racine du projet) au chemin de recherche Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# ------------------------------------

from fastapi.testclient import TestClient
from app.main import app  # Maintenant, il trouvera 'main'
client = TestClient(app)
def test_api_resolve_endpoint():
    # ... le reste de votre test ...
    payload = {
        "type": "headway_conflict",
        "severity": 3,
        "affected_trains": ["T1", "T2"],
        "spatial_footprint": "Gare Centrale",
        "temporal_window": {"start": "2023-10-27T10:00:00", "end": "2023-10-27T10:05:00"},
        # Champs requis par le schéma Pydantic Conflict
        "conflict_id": "test_cid_001",
        "content": {"reason": "signal_failure"}, 
        "location": "Track 4"
    }
    response = client.post("/resolve", json=payload)
    
    # Vérification de la réponse
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    
    try:
        response = client.post("/resolve", json=payload)
        # Si la DB n'est pas là, ça plantera peut-être avec une 500, 
        # mais au moins l'erreur "No module named main" aura disparu.
    except Exception:
       pass

