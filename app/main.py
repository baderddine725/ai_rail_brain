from fastapi import FastAPI, BackgroundTasks
from app.core.brain import RailNetworkBrain
from app.models.schemas import Conflict
from app.utils.embeddings import RailEmbedder
import uvicorn

app = FastAPI(title="AI Rail Network Brain")
brain = RailNetworkBrain()
embedder = RailEmbedder()


@app.on_event("startup")
async def startup_event():
    # Ici, on pourrait lancer le StreamHandler en tâche de fond [cite : 83]
    print("AI Rail Network Brain is Active - Memory Loaded.")
@app.post("/resolve")
async def handle_conflict(conflict: Conflict, background_tasks: BackgroundTasks):
    # 1. Phase de décision (Ultra rapide)
    context_vector = embedder.generate_context_vector(conflict.dict(), "")
    suggestions = await brain.resolve_conflict(conflict, context_vector)

    # 2. Simulation du résultat (Optionnel pour l'exemple)
    # Dans un vrai cas, 'results' proviendrait de l'observation réelle après 15-30 min
    fake_results = {"delay_recovered": 45, "impact_score": 0.9}

    # 3. Déclenchement de la boucle d'apprentissage en arrière-plan
    # Cela permet de répondre immédiatement à l'opérateur sans attendre les DB
    background_tasks.add_task(
        brain.learning_cycle, 
        conflict.conflict_id, 
        "res_123", 
        fake_results
    )

    return {
        "status": "decision_sent",
        "recommendations": suggestions,
        "learning_status": "background_processing"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)