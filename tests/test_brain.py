# tests/test_brain.py
import pytest
from unittest.mock import MagicMock, AsyncMock
from app.core.brain import RailNetworkBrain

@pytest.mark.asyncio
async def test_resolve_conflict_logic():
    # 1. Préparation du cerveau
    brain = RailNetworkBrain()
    
    # 2. Simulation (Mocking) de la mémoire vectorielle
    # On simule que Qdrant renvoie un cas passé réussi
    mock_hit = MagicMock()
    mock_hit.payload = {
        'resolution_pattern': {'headway_seconds': 180, 'platform_load': 0.5},
        'outcome_summary': 'Succès passé'
    }
    mock_hit.score = 0.95
    brain.vector_mem.retrieve_golden_runs = MagicMock(return_value=[mock_hit])

    # 3. Exécution du test
    conflict = MagicMock(conflict_id="test_123", spatial_footprint="Zone A")
    results = await brain.resolve_conflict(conflict, [0.1] * 384)

    # 4. Vérifications
    assert len(results) == 1
    assert results[0]['action']['headway_seconds'] == 180
    assert results[0]['confidence'] == 0.95