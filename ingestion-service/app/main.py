from fastapi import FastAPI
from app.routers import events
import logging
from pythonjsonlogger import jsonlogger

# Logging setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

app = FastAPI(
    title="User Analytics Ingestion Service",
    version="1.0.0",
    description="Receives user events and publishes them to Kafka",
)

# Register routers
app.include_router(events.router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
