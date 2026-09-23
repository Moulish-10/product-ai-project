from PIL import Image

from app.models.model import AIModel
from app.utils.image import prepare_image


class InferenceService:
    def __init__(self):
        self.model = AIModel()

    def predict(self, image: Image.Image, image_name: str) -> dict:

        image = prepare_image(image)

        prediction = self.model.predict(image)

        return {
            "message": "Prediction completed",
            "image_name": image_name,
            "model_version": self.model.model_version,
            "confidence": prediction["confidence"],
        }