# tests/test_integration_db.py
import pytest
from app.memory.graph_store import GraphMemory
from app.memory.vector_store import VectorMemory

# Ce test sera ignoré si les DB ne sont pas là, c'est une bonne pratique
try:
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 7687))
    DB_AVAILABLE = True
    s.close()
except:
    DB_AVAILABLE = False

@pytest.mark.skipif(not DB_AVAILABLE, reason="Bases de données non accessibles")
def test_real_neo4j_connection():
    # Connexion réelle
    graph = GraphMemory("bolt://localhost:7687", "neo4j", "rail_password")
    
    # On vérifie qu'on peut récupérer la Gare du Nord créée par le script d'init
    with graph.driver.session() as session:
        result = session.run("MATCH (s:Station {name: 'Gare du Nord'}) RETURN s").single()
        assert result is not None
        assert result['s']['id'] == 'ST_A'

@pytest.mark.skipif(not DB_AVAILABLE, reason="Bases de données non accessibles")
def test_real_qdrant_search():
    # Connexion réelle
    vm = VectorMemory(host="localhost", port=6333)
    
    # On cherche un vecteur proche de [0.1, 0.1...] (notre Cas 1)
    query_vector = [0.1] * 384
    results = vm.retrieve_golden_runs(query_vector, limit=1)
    
    assert len(results) > 0
    # On vérifie qu'on a bien retrouvé le payload injecté
    assert results[0].payload['type'] == "headway_conflict"