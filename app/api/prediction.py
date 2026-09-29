from functools import lru_cache
import time
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.prediction import Prediction
from app.models.schemas import PredictionResponse
from app.services.inference_service import InferenceService
from app.utils.logger import get_logger


router = APIRouter()

logger = get_logger(__name__)

ALLOWED_CONTENT_TYPES = {
    "image/jpg",
    "image/jpeg",
    "image/png",
    "image/webp",
}


@lru_cache
def get_inference_service() -> InferenceService:
    return InferenceService()


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Run object detection",
    description=(
        "Upload an image and run YOLO object detection. "
        "Supported formats: JPEG, PNG, and WEBP."
    ),
    responses={
        400: {
            "description": "Invalid or unsupported image."
        },
        500: {
            "description": "Prediction failed."
        },
    },
)
async def predict(
    file: UploadFile = File(...),
    inference_service: InferenceService = Depends(
        get_inference_service
    ),
    db: Session = Depends(get_db),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image type. Use JPG, JPEG, PNG, or WEBP.",
        )

    try:
        image = Image.open(file.file)
        image.verify()

        file.file.seek(0)
        image = Image.open(file.file)

    except (UnidentifiedImageError, OSError):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is not a valid image",
        )

    try:
        logger.info(
            "Prediction request received: %s",
            file.filename,
        )

        start_time = time.perf_counter()

        request_id = str(uuid.uuid4())

        result = inference_service.predict(
            image=image,
            image_name=file.filename,
        )

        prediction = Prediction(
            request_id=request_id,
            image_name=file.filename,
            model_version=result["model_version"],
            detection_count=result["detection_count"],
            inference_time_ms=result["inference_time_ms"],
        )

        db.add(prediction)
        db.commit()
        db.refresh(prediction)

        elapsed_time = time.perf_counter() - start_time

        logger.info(
            "Prediction completed: %s | latency = %.4f seconds",
            file.filename,
            elapsed_time,
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