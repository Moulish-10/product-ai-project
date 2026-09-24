from fastapi import APIRouter , Depends, File, UploadFile, HTTPException
from PIL import Image, UnidentifiedImageError
from app.models.schemas import PredictionResponse
from app.services.inference_service import InferenceService
from app.utils.logger import get_logger
from functools import lru_cache
import time

router = APIRouter()

logger = get_logger(__name__)

ALLOWED_CONTENT_TYPE = {
      "image/jpg",
      "image/jpeg",
      "image/png",
      "image/webp"
}

@lru_cache
def get_inference_service() -> InferenceService:
    return InferenceService()


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    file: UploadFile = File(...),
    inference_service: InferenceService = Depends(get_inference_service),
    ):

        if file.content_type not in ALLOWED_CONTENT_TYPE:
              raise HTTPException(
                    status_code=400,
                    detail = "Unsupported image type. Use Jpg, Jpeg, png or webp"
              )

        try :
              
            image = Image.open(file.file)
            image.verify()

            file.file.seek(0)
            image = Image.open(file.file)

        except (UnidentifiedImageError, OSError):
              raise HTTPException(
                    status_code=400,
                    detail = "Uploaded file is not a valid image"
              )
        try:
            logger.info(
                "Prediction request received: %s",
                file.filename,
            )

            start_time = time.perf_counter()

            result = inference_service.predict(
                image=image,
                image_name=file.filename
            )

            elapsed_time = time.perf_counter() - start_time

            logger.info(
                "Prediction completed: %s | latency = %.4f seconds",
                file.filename,
                elapsed_time
            )

            return result
        
        except Exception:
            logger.exception(
                "Prediction failed: %s",
                file.filename,
            )

            raise HTTPException(
                status_code=500,
                detail="Prediction failed.",
            )