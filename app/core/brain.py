from typing import List, Dict, Any
from .safety_gate import SafetyGate
from ..memory.vector_store import VectorMemory
from ..memory.graph_store import GraphMemory
from .conflict import Conflict # Assurez-vous que ce fichier existe ou commentez l'import si vous utilisez un dict

class RailNetworkBrain:
    def __init__(self):
        # Initialisation robuste : accepte que les DB soient absentes
        self.vector_mem = VectorMemory()
        
        # Correction ici : on passe bien les arguments attendus par GraphMemory
        self.graph_mem = GraphMemory("bolt://localhost:7687", "neo4j", "rail_password")
        
        self.safety = SafetyGate()

    async def resolve_conflict(self, current_conflict: Conflict, context_vector: List[float]):
        """Real-time decision loop"""
        
        # 1. Recall past 'Golden Runs'
        # Si Qdrant est éteint, retrieve_golden_runs renverra une liste vide grâce au correctif
        past_episodes = self.vector_mem.retrieve_golden_runs(context_vector)
        
        # 2. Extract resolution patterns
        proposals = []
        for episode in past_episodes:
            pattern = episode.payload.get('resolution_pattern', {})
            
            # 3. Apply Safety Gate (The AI Railway Tracks)
            if self.safety.validate(pattern):
                proposals.append({
                    "action": pattern,
                    "confidence": getattr(episode, 'score', 0.0),
                    "evidence": episode.payload.get('outcome_summary', 'No evidence') 
                })
        
        # Tri des propositions par confiance
        return sorted(proposals, key=lambda x: x['confidence'], reverse=True)

    async def learning_cycle(self, conflict_id: str, resolution_id: str, results: Dict[str, Any]):
        """
        Rôle : Consolide l'expérience acquise après une résolution.
        """
        print(f"Démarrage de l'apprentissage pour l'incident {conflict_id}...")
        
        # 1. Mise à jour du Graphe (Causalité physique et historique)
        self.graph_mem.link_conflict_to_resolution(conflict_id, resolution_id, results.get('impact_score', 0))
        
        # 2. Mise à jour du Vecteur (Optimisation de la recherche future)
        if hasattr(self.vector_mem, 'update_resolution_quality'):
             self.vector_mem.update_resolution_quality(conflict_id, results.get('delay_recovered', 0))
        
        print(f"Apprentissage terminé : L'incident {conflict_id} a enrichi la mémoire système.")