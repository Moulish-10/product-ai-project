from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app
from app.api.prediction import get_inference_service

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.models.prediction import Prediction
client = TestClient(app)


class MockInferenceService:
    def predict(self, image, image_name):
        return {
            "message": "Prediction completed",
            "image_name": image_name,
            "model_version": "test-model",
            "image_width": image.width,
            "image_height": image.height,
            "detection_count": 1,
            "inference_time_ms": 123.45,

            "detections": [
                {
                    "class_name": "cat",
                    "confidence": 0.95,
                    "bbox": {
                        "x1": 10.0,
                        "y1": 20.0,
                        "x2": 100.0,
                        "y2": 150.0,
                    },
                }
            ],
        }


def create_test_image():
    image = Image.new("RGB", (200, 200))

    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    return buffer


def test_predict_valid_image():

    app.dependency_overrides[get_inference_service] = (
        lambda: MockInferenceService()
    )
    
    app.dependency_overrides[get_db] = override_get_db

    image = create_test_image()

    response = client.post(
        "/predict",
        files={
            "file": (
                "test.jpg",
                image,
                "image/jpeg",
            )
        },
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Prediction completed"
    assert data["image_name"] == "test.jpg"
    assert data["model_version"] == "test-model"
    assert data["image_width"] == 200
    assert data["image_height"] == 200
    assert data["detection_count"] == 1

    assert len(data["detections"]) == 1

    detection = data["detections"][0]

    assert detection["class_name"] == "cat"
    assert detection["confidence"] == 0.95

    assert detection["bbox"]["x1"] == 10.0
    assert detection["bbox"]["y1"] == 20.0
    assert detection["bbox"]["x2"] == 100.0
    assert detection["bbox"]["y2"] == 150.0

def test_predict_invalid_image():

    response = client.post(
        "/predict",
        files={
            "file": (
                "test.jpg",
                b"this is not an image",
                "image/jpeg",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
    "Uploaded file is not a valid image"
    )

TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)

Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()
