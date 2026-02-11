import uuid
from fastapi import APIRouter, HTTPException, status
from app.models.event_schema import Event
from app.kafka_producer import KafkaProducerClient

router = APIRouter(prefix="/events", tags=["Events"])

producer = KafkaProducerClient()

@router.post("/", status_code=status.HTTP_201_CREATED)
def ingest_event(event: Event):
    if not event.event_id:
        event.event_id = str(uuid.uuid4())

    producer.send_event(
        topic="user_events_raw",
        key=event.user_id,
        event=event.model_dump(mode="json"),
    )

    return {
        "message": "Event ingested successfully",
        "event_id": event.event_id,
    }