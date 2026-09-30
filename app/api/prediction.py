from functools import lru_cache
import time
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.prediction import Prediction
from app.models.schemas import (
    PredictionResponse,
    PredictionHistoryItem,
    PredictionHistoryResponse,
    PredictionDetailResponse,
    Detection as DetectionSchema,
)

from app.models.detection import Detection as DetectionModel
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
        

        start_time = time.perf_counter()

        request_id = str(uuid.uuid4())

        logger.info(
                    "Prediction request received: %s",
                    file.filename,
                    extra={"request_id": request_id},
                )
        
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
        db.flush()

        for detection in result["detections"]:
            db_detection = DetectionModel(
                prediction_id=prediction.id,
                class_name=detection.class_name,
                confidence=detection.confidence,
                x1=detection.bbox.x1,
                y1=detection.bbox.y1,
                x2=detection.bbox.x2,
                y2=detection.bbox.y2,
            )

            db.add(db_detection)

        db.commit()
        db.refresh(prediction)
        
        elapsed_time = time.perf_counter() - start_time

        logger.info(
            "Prediction completed: %s | latency = %.4f seconds",
            file.filename,
            elapsed_time,
            extra={"request_id": request_id},
        )

        return result

    except Exception:

        db.rollback()

        logger.exception(
            "Prediction failed: %s",
            file.filename,
            extra={"request_id": request_id},
    )

        raise HTTPException(
            status_code=500,
            detail="Prediction failed.",
        )

@router.get(
    "/predictions/{prediction_id}",
    response_model=PredictionDetailResponse,
    summary="Get prediction details",
    description="Return one prediction together with its detections.",
)
def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
):
    prediction = (
        db.query(Prediction)
        .filter(Prediction.id == prediction_id)
        .first()
    )

    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found.",
        )

    detections = [
        DetectionSchema(
            class_name=detection.class_name,
            confidence=detection.confidence,
            bbox={
                "x1": detection.x1,
                "y1": detection.y1,
                "x2": detection.x2,
                "y2": detection.y2,
            },
        )
        for detection in prediction.detections
    ]

    return PredictionDetailResponse(
        id=prediction.id,
        request_id=prediction.request_id,
        image_name=prediction.image_name,
        model_version=prediction.model_version,
        detection_count=prediction.detection_count,
        inference_time_ms=prediction.inference_time_ms,
        created_at=prediction.created_at,
        detections=detections,
    )

@router.get(
    "/predictions",
    response_model=PredictionHistoryResponse,
    summary="Get prediction history",
    description="Return previously stored prediction records.",
)
def get_predictions(
    db: Session = Depends(get_db),
):
    predictions = (
        db.query(Prediction)
        .order_by(Prediction.created_at.desc())
        .all()
    )

    items = [
        PredictionHistoryItem(
            id=item.id,
            request_id=item.request_id,
            image_name=item.image_name,
            model_version=item.model_version,
            detection_count=item.detection_count,
            inference_time_ms=item.inference_time_ms,
            created_at=item.created_at,
        )
        for item in predictions
    ]

    return PredictionHistoryResponse(
        predictions=items,
        total=len(items),
    )