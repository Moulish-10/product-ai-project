from pydantic import BaseModel

class HealthResponse(BaseModel):
    status : str

class PredictionRequest(BaseModel):
    image_name: str


class PredictionResponse(BaseModel):
    message: str
    image_name: str
    model_version: str
    confidence: float