import json
from confluent_kafka import Consumer, KafkaError
from models.schemas import RailEvent

class StreamHandler:
    def __init__(self, bootstrap_servers: str, group_id: str):
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })

    def start_ingestion(self, topics: list, callback):
        self.consumer.subscribe(topics)
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None: continue
                if msg.error():
                    print(f"Erreur Kafka: {msg.error()}")
                    continue

                # Normalisation de la donnée brute en RailEvent [cite : 17, 102]
                data = json.loads(msg.value().decode('utf-8'))
                event = RailEvent(
                    modality=data.get('modality'),
                    content=data.get('content'),
                    location=data.get('location')
                )
                callback(event) # Envoi au Brain pour traitement
        finally:
            self.consumer.close()