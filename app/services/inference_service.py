from PIL import Image

from app.models.model import AIModel
from app.models.schemas import Detection , BoundingBox
from app.utils.image import prepare_image

import time

class InferenceService:
    def __init__(self):
        self.model = AIModel()

    def predict(self, image: Image.Image, image_name: str) -> dict:

        image = prepare_image(image)

        width, height = image.size

        start_time = time.perf_counter()

        results = self.model.predict(image)

        inference_time = time.perf_counter() - start_time

        detections = []

        result = results[0]

        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            class_name = result.names[class_id]

            x1,y1,x2,y2 = box.xyxy[0].tolist()

            detections.append(
                Detection(
                    class_name=class_name,
                    confidence=confidence,
                    bbox = BoundingBox(
                        x1 = x1,
                        y1 = y1,
                        x2 = x2,
                        y2 = y2,
                    ),
                )
            )

        return {
            "message": "Prediction completed",
            "image_name": image_name,
            "model_version": self.model.model_version,
            "image_width": width,
            "image_height": height,
            "detection_count": len(detections),
            "inference_time_ms": round(inference_time * 1000, 2),
            "detections": detections,
        }