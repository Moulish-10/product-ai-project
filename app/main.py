from fastapi import FastAPI
from pydantic import BaseModel
from app.api.prediction import router as prediction_router
from app.api.health import router as health_router 



app = FastAPI(
    title="Product AI API",
    description=(
        "Production-oriented computer vision inference API "
        "for object detection."
    ),
    version="0.1.0",
)

@app.get("/")
def root():
    return{
        "message" : "Product AI API is running",
        "version" : "0.1.0"
    }

app.include_router(health_router)
app.include_router(prediction_router)
