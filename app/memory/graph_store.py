from neo4j import GraphDatabase


class GraphMemory:
    def __init__(self, uri=None, user=None, password=None):
        """
        Initialise la connexion Neo4j.
        Accepte des arguments (contrairement à votre version actuelle) 
        et gère l'absence de serveur (pour les tests).
        """
        self.driver = None
        if uri and user and password:
            try:
                # On tente la connexion, mais on ne plante pas si ça échoue
                self.driver = GraphDatabase.driver(uri, auth=(user, password))
            except Exception as e:
                print(f"⚠️ Attention : Neo4j non accessible. Mode 'Mock' activé. ({e})")

    

    
    def detect_platform_conflicts(self, station_id: str, start_time: str, end_time: str):
        """
        Détecte si deux trains sont programmés sur la même plateforme 
        au même moment (Chevauchement temporel).
        """
        query = """
        MATCH (t1:Train)-[r1:ASSIGNED_TO]->(p:Platform {id: $p_id})
        MATCH (t2:Train)-[r2:ASSIGNED_TO]->(p)
        WHERE t1.id <> t2.id
          AND r1.start_time < $end_t 
          AND r1.end_time > $start_t
          AND r2.start_time < $end_t 
          AND r2.end_time > $start_t
        RETURN t1.id, t2.id, p.id, r1.start_time, r2.start_time
        """
        with self.driver.session() as session:
            return session.run(query, p_id=station_id, start_t=start_time, end_t=end_time).data()

    def trace_delay_causality(self, incident_id: str):
        """
        Remonte la chaîne de causalité pour expliquer l'origine d'un retard.
        """
        query = """
        MATCH (origin:Incident {id: $id})<-[:CAUSED_BY*1..5]-(ripple:Delay)
        RETURN ripple.train_id, ripple.delay_minutes, ripple.timestamp
        ORDER BY ripple.timestamp ASC
        """
        with self.driver.session() as session:
            return session.run(query, id=incident_id).data()