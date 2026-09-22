from fastapi import APIRouter , Depends

from app.models.schemas import (
    PredictionRequest,
    PredictionResponse,
)
from app.services.inference_service import InferenceService


router = APIRouter()

def get_inference_service() -> InferenceService:
    return InferenceService()


@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest, 
            inference_service : InferenceService = Depends(get_inference_service),
              ):
    return inference_service.predict(request.image_name)