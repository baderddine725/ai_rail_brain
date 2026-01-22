from sentence_transformers import SentenceTransformer
import numpy as np

class RailEmbedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # Utilisation d'un modèle transformeur pour encoder le contexte textuel et opérationnel
        self.model = SentenceTransformer(model_name)

    def generate_context_vector(self, conflict_data: dict, context_text: str):
        """
        Crée un vecteur multimodal combinant les données brutes et le contexte textuel [cite : 47, 49].
        """
        # On concatène les informations clés pour créer une signature de l'incident
        features = f"Type: {conflict_data.get('type')} | Location: {conflict_data.get('location')} | {context_text}"
        embedding = self.model.encode(features)
        return embedding.tolist()