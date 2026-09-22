from fastapi import APIRouter , Depends, File, UploadFile
from PIL import Image
from app.models.schemas import (
    PredictionRequest,
    PredictionResponse,
)
from app.services.inference_service import InferenceService


router = APIRouter()

def get_inference_service() -> InferenceService:
    return InferenceService()


@router.post("/predict", response_model=PredictionResponse)
async def predict(file : UploadFile = File(...)):

        image = Image.open(file.file)

        inference_service = get_inference_service()

        return inference_service.predict(file.filename)