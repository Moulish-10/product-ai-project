from pydantic import BaseModel
from datetime import datetime

class HealthResponse(BaseModel):
    status : str

class PredictionRequest(BaseModel):
    image_name: str

class BoundingBox(BaseModel):
    x1 : float
    y1 : float
    x2 : float
    y2 : float

class Detection(BaseModel):
    class_name: str
    confidence: float
    bbox : BoundingBox


class PredictionResponse(BaseModel):
    message: str
    image_name: str
    model_version: str
    image_width: int
    image_height: int
    detection_count: int
    inference_time_ms : float
    detections: list[Detection]

class PredictionHistoryItem(BaseModel):
    id: int
    request_id: str
    image_name: str
    model_version: str
    detection_count: int
    inference_time_ms: float
    created_at: datetime


class PredictionHistoryResponse(BaseModel):
    predictions: list[PredictionHistoryItem]
    total: int

class PredictionDetailResponse(BaseModel):
    id: int
    request_id: str
    image_name: str
    model_version: str
    detection_count: int
    inference_time_ms: float
    created_at: datetime
    detections: list[Detection]