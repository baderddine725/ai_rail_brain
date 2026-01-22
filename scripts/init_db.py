# scripts/init_db.py
import sys
import os

# Ajout de la racine au path pour importer 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.memory.graph_store import GraphMemory
from app.memory.vector_store import VectorMemory
from qdrant_client.models import PointStruct

def init_neo4j():
    print("🚂 Initialisation de Neo4j (Topologie)...")
    # Connexion (assurez-vous que le mot de passe correspond au docker-compose)
    graph = GraphMemory("bolt://localhost:7687", "neo4j", "rail_password")
    
    with graph.driver.session() as session:
        # Nettoyage préalable (ATTENTION : efface tout)
        session.run("MATCH (n) DETACH DELETE n")
        
        # Création d'une ligne simple : Gare A -> Gare B -> Gare C
        query = """
        CREATE (stA:Station {id: 'ST_A', name: 'Gare du Nord'})
        CREATE (stB:Station {id: 'ST_B', name: 'Gare Centrale'})
        CREATE (stC:Station {id: 'ST_C', name: 'Gare du Sud'})
        
        CREATE (stA)-[:CONNECTED_TO {distance_km: 10}]->(stB)
        CREATE (stB)-[:CONNECTED_TO {distance_km: 15}]->(stC)
        
        CREATE (t1:Train {id: 'TGV_001', status: 'ON_TIME'})
        CREATE (t1)-[:LOCATED_AT]->(stA)
        """
        session.run(query)
    print("✅ Neo4j prêt : 3 Gares, 1 Train.")

def init_qdrant():
    print("🧠 Initialisation de Qdrant (Mémoire Vectorielle)...")
    vm = VectorMemory(host="localhost", port=6333)
    
    # Création de faux vecteurs (Golden Runs)
    # Imaginons un vecteur de dimension 384 (standard pour all-MiniLM-L6-v2)
    vector_size = 384 
    
    # Cas 1 : Résolution réussie d'un conflit de 'Headway' (distance)
    fake_vector_1 = [0.1] * vector_size
    payload_1 = {
        "type": "headway_conflict",
        "resolution_pattern": {"headway_seconds": 180, "action": "slow_down"},
        "outcome_summary": "Retard absorbé en 5 min",
        "quality_score": 0.95,
        "is_golden_run": True
    }

    # Cas 2 : Résolution d'un problème de plateforme
    fake_vector_2 = [0.9] * vector_size
    payload_2 = {
        "type": "platform_conflict",
        "resolution_pattern": {"platform_change": "Track 3"},
        "outcome_summary": "Aucun retard",
        "quality_score": 0.98,
        "is_golden_run": True
    }

    vm.client.upsert(
        collection_name="rail_incidents",
        points=[
            PointStruct(id=1, vector=fake_vector_1, payload=payload_1),
            PointStruct(id=2, vector=fake_vector_2, payload=payload_2)
        ]
    )
    print("✅ Qdrant prêt : 2 Golden Runs injectés.")

if __name__ == "__main__":
    init_neo4j()
    init_qdrant()