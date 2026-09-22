
class InferenceService:

    def __init__(self):
        self.model_version = "v0.1.0"

    def predict(self, image_name : str) -> dict:
        return {
            "message" : "Prediction completed",
            "image_name" : image_name,
            "model_version" : self.model_version,
            "confidence" : 0.0
        }
