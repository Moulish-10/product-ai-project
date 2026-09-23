from ultralytics import YOLO

class AIModel:
    def __init__(self):
        self.model_version = "yolo11n"
        self.model = YOLO("yolo11n.pt")

    def predict(self, image):
        results = self.model(image)
        return results