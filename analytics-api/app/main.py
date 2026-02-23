from fastapi import FastAPI
from app.api.routes import health, metrics

app = FastAPI(
    title="Analytics API",
    version="1.0.0"
)

app.include_router(health.router)
app.include_router(metrics.router,tags=["Metrics"])