from io import BytesIO
from urllib import response

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app
from app.api.prediction import get_inference_service

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.models.prediction import Prediction
from app.models.detection import Detection as DetectionModel
from app.models.schemas import BoundingBox, Detection

client = TestClient(app)


class MockInferenceService:
    def predict(self, image, image_name):
        return {
            "message": "Prediction completed",
            "image_name": image_name,
            "model_version": "test-model",
            "image_width": 200,
            "image_height": 200,
            "detection_count": 1,
            "inference_time_ms": 123.45,
            "detections": [
                Detection(
                    class_name="cat",
                    confidence=0.95,
                    bbox=BoundingBox(
                        x1=10,
                        y1=20,
                        x2=100,
                        y2=150,
                    ),
                )
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

def test_get_prediction_history():

    app.dependency_overrides[get_db] = override_get_db

    db = TestSessionLocal()

    prediction = Prediction(
        request_id="test-history-request",
        image_name="history.jpg",
        model_version="test-model",
        detection_count=1,
        inference_time_ms=50.0,
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    db.close()

    response = client.get("/predictions")

    app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert "predictions" in data
    assert "total" in data
    assert data["total"] >= 1

    item = data["predictions"][0]

    assert item["id"] == prediction.id
    assert item["image_name"] == "history.jpg"
    assert item["model_version"] == "test-model"
    assert item["detection_count"] == 1


def test_get_prediction_details():

    app.dependency_overrides[get_db] = override_get_db

    db = TestSessionLocal()

    prediction = Prediction(
        request_id="test-detail-request",
        image_name="detail.jpg",
        model_version="test-model",
        detection_count=1,
        inference_time_ms=75.0,
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    detection = DetectionModel(
        prediction_id=prediction.id,
        class_name="cat",
        confidence=0.95,
        x1=10.0,
        y1=20.0,
        x2=100.0,
        y2=150.0,
    )

    db.add(detection)
    db.commit()

    prediction_id = prediction.id

    db.close()

    response = client.get(
        f"/predictions/{prediction_id}"
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == prediction_id
    assert data["image_name"] == "detail.jpg"
    assert data["model_version"] == "test-model"
    assert data["detection_count"] == 1

    assert len(data["detections"]) == 1

    result_detection = data["detections"][0]

    assert result_detection["class_name"] == "cat"
    assert result_detection["confidence"] == 0.95

    assert result_detection["bbox"]["x1"] == 10.0
    assert result_detection["bbox"]["y1"] == 20.0
    assert result_detection["bbox"]["x2"] == 100.0
    assert result_detection["bbox"]["y2"] == 150.0

def test_get_prediction_not_found():

    app.dependency_overrides[get_db] = override_get_db

    response = client.get("/predictions/999999")

    app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json()["detail"] == "Prediction not found."