from kafka import KafkaProducer
import json
import logging

logger = logging.getLogger(__name__)


class KafkaProducerClient:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            key_serializer=lambda k: k.encode("utf-8"),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            acks="all",
            retries=3,
        )
        logger.info("Kafka Producer connected")

    def send_event(self, topic: str, key: str, event: dict):
        self.producer.send(
            topic=topic,
            key=key,
            value=event,
        )
        self.producer.flush()
