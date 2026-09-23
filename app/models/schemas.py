from pydantic import BaseModel

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
    detections: list[Detection]