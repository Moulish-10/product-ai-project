from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.prediction import router as prediction_router

# Register SQLAlchemy models
from app.models.prediction import Prediction
from app.models.detection import Detection


app = FastAPI(
    title="Product AI API",
    description="Production-oriented AI inference service",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Product AI API is running",
        "version": "0.1.0",
    }


app.include_router(health_router)
app.include_router(prediction_router)