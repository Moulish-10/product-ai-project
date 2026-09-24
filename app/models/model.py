from ultralytics import YOLO
from app.config import settings

class AIModel:
    def __init__(self):
        self.model_version = settings.model_version
        self.model = YOLO(settings.model_path)

    def predict(self, image):
        results = self.model(
            image,
            conf = settings.confidence_threshold
            )
        return results