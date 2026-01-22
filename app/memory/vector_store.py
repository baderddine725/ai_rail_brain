from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
class VectorMemory:
    # ... (init précédent)

    def update_resolution_quality(self, incident_id: str, actual_delay_recovery: float):
        """
        Met à jour le score de qualité d'une résolution dans la mémoire vectorielle.
        """
        # Calcul du score de performance (0.0 à 1.0)
        # Si la récupération réelle est proche de l'objectif, le score augmente.
        quality_score = self._calculate_score(actual_delay_recovery)

        self.client.set_payload(
            collection_name="rail_incidents",
            payload={"quality_score": quality_score, "is_golden_run": quality_score > 0.8},
            points=[incident_id]
        )

    def search_weighted_golden_runs(self, query_vector: list):
        """
        Recherche des cas similaires, mais privilégie les 'Golden Runs' (succès passés).
        """
        from qdrant_client.models import Filter, FieldCondition, MatchValue

        return self.client.search(
            collection_name="rail_incidents",
            query_vector=query_vector,
            query_filter=Filter(
                must=[FieldCondition(key="is_golden_run", match=MatchValue(value=True))]
            ),
            limit=3
        )

    def _calculate_score(self, recovery):
        # Logique interne de scoring métier
        return min(1.0, max(0.0, recovery / 60)) # Exemple basé sur 60min de récup max