# SteelVision AI

### AI-Powered Steel Surface Defect Detection System

SteelVision AI is an end-to-end computer vision system for automated detection of surface defects in steel materials.

The system combines a YOLO11n object detection model with a production-oriented FastAPI backend, PostgreSQL persistence, Docker Compose, Alembic migrations, automated testing, GitHub Actions CI, and a Streamlit web interface.

## 🎯 Problem

Manual inspection of steel surfaces can be time-consuming and inconsistent.

SteelVision AI automatically analyzes an uploaded image and detects surface defects using a trained YOLO11n object detection model.

The system returns:

- Detected defect classes
- Confidence scores
- Bounding boxes
- Number of detections
- Model version
- Inference latency

Prediction results are also persisted in PostgreSQL for traceability and historical analysis.

---

## 🏗️ System Architecture

```text
                         User
                          │
                          ▼
                 ┌─────────────────┐
                 │  Streamlit UI   │
                 │  Port 8501      │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │    FastAPI      │
                 │    REST API     │
                 │    Port 8000    │
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │ Request ID +    │
                 │ Validation      │
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │ Inference       │
                 │ Service         │
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │    YOLO11n      │
                 │ Object Detection│
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │ Detection       │
                 │ Results         │
                 └───────┬─┬───────┘
                         │ │
              ┌──────────┘ └──────────┐
              ▼                       ▼
      ┌─────────────────┐     ┌─────────────────┐
      │  API Response   │     │   PostgreSQL    │
      └─────────────────┘     │                 │
                              │ predictions     │
                              │ detections      │
                              └─────────────────┘

Docker Services
steelvision-api
       │
       ├── FastAPI
       ├── YOLO11n
       └── Alembic

steelvision-postgres
       │
       └── Prediction Database

steelvision-ui
       │
       └── Streamlit

🔍 Detected Defect Classes
The model detects six steel surface defect categories:
Class	Description
Crazing	Fine crack-like surface defects
Inclusion	Foreign material/inclusion defects
Patches	Irregular patch-like surface defects
Pitted Surface	Small pit/depression defects
Rolled-in Scale	Scale defects embedded during rolling
Scratches	Linear surface scratches


📊 Dataset
Dataset:
NEU-DET
Dataset source:
KeenForgeAI/NEU-DET-corrected
Dataset distribution used for the project:
Split	Images
Training	3,316
Validation	180
Test	180
Total	3,676


Total annotated bounding boxes:
4,177
🤖 Model
YOLO11n
The project uses YOLO11n for real-time object detection.
Training configuration:
Parameter	Value
Model	YOLO11n
Image Size	640 × 640
Epochs	50
Batch Size	16
Training GPU	NVIDIA T4
Number of Classes	6


Final model:
models/steel_defect_yolo11n_v1.pt

Model version:
steel-defect-yolo11n-v1

📈 Model Performance
Final test-set performance:
Metric	Result
Precision	71.83%
Recall	74.39%
mAP@50	77.98%
mAP@50-95	44.90%
Inference	~5.5 ms/image


The model was selected as the final baseline after comparing different image-size configurations.
An 832px experiment was evaluated but did not improve the overall detection performance sufficiently to justify the additional inference cost.
🖥️ Web Interface
SteelVision AI includes a Streamlit interface for interactive inspection.
The UI provides:
- Image upload
- Defect detection
- Bounding-box visualization
- Confidence scores
- Detection count
- Inference latency
- Model version
- Prediction history
- Request ID
- Timestamp
Run the UI with Docker Compose and open:
http://localhost:8501

⚙️ Technology Stack
Machine Learning
- Python 3.11
- YOLO11n
- Ultralytics
- PyTorch
- Computer Vision
Backend
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Alembic
Frontend
- Streamlit
- Pillow
- Requests
DevOps
- Docker
- Docker Compose
- Git
- GitHub
- GitHub Actions
Testing
- Pytest
📁 Project Structure
SteelVision-AI/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   ├── api/
│   │   ├── health.py
│   │   └── prediction.py
│   │
│   ├── models/
│   │   ├── model.py
│   │   ├── prediction.py
│   │   ├── detection.py
│   │   └── schemas.py
│   │
│   ├── services/
│   │   └── inference_service.py
│   │
│   ├── utils/
│   │   ├── image.py
│   │   └── logger.py
│   │
│   ├── config.py
│   ├── database.py
│   └── main.py
│
├── dataset/
│   ├── dataset.py
│   └── train_baseline.py
│
├── models/
│   └── steel_defect_yolo11n_v1.pt
│
├── tests/
│   ├── test_health.py
│   └── test_prediction.py
│
├── ui/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── alembic.ini
├── requirements.txt
└── README.md

🔌 API Endpoints
Health Check
GET /health

Example:
{
  "status": "healthy"
}

API Root
GET /

Example:
{
  "message": "SteelVision AI API is running",
  "version": "0.1.0"
}

Object Detection
POST /predict

Upload an image using multipart form data.
Example response:
{
  "message": "Prediction completed",
  "image_name": "crazing_20.jpg",
  "model_version": "steel-defect-yolo11n-v1",
  "image_width": 640,
  "image_height": 640,
  "detection_count": 2,
  "inference_time_ms": 201.7,
  "detections": []
}

Prediction History
GET /predictions

Returns previously stored prediction records.
Prediction Details
GET /predictions/{prediction_id}

Returns a specific prediction and its associated detections.
🗄️ Database
PostgreSQL stores prediction history.
predictions
Stores:
- Prediction ID
- Request ID
- Image name
- Model version
- Detection count
- Inference time
- Creation timestamp
detections
Stores:
- Detection ID
- Prediction ID
- Class name
- Confidence
- Bounding box coordinates
The relationship allows every prediction request to be traced to its individual detections.
🔄 Prediction Flow
Upload Image
     ↓
FastAPI
     ↓
Validate Image
     ↓
Generate Request ID
     ↓
YOLO11n Inference
     ↓
Extract Detections
     ↓
Calculate Inference Time
     ↓
Store Prediction
     ↓
Store Detections
     ↓
Return JSON Response

🔎 Request Tracing
Every API request receives a unique request ID.
The request ID is:
- Returned through the X-Request-ID response header
- Included in application logs
- Stored with prediction records
This makes it possible to trace a request across the API, inference process, logs, and database.
🗃️ Database Migrations
Alembic manages database schema migrations.
Apply migrations manually:
alembic upgrade head

Check the current migration:
alembic current

Docker automatically runs:
alembic upgrade head

before starting the API.
🐳 Running with Docker
Build and start the complete application:
docker compose up -d --build

Check containers:
docker compose ps

Expected services:
steelvision-api
steelvision-postgres
steelvision-ui

API
http://localhost:8000

Swagger Documentation
http://localhost:8000/docs

Streamlit UI
http://localhost:8501

API Logs
docker logs steelvision-api

Stop the application
docker compose down

🧪 Testing
Run the test suite:
pytest -q

Current test status:
6 passed

The tests cover:
- API health
- Prediction functionality
- Prediction history
- Prediction details
- Error scenarios
🔁 Continuous Integration
GitHub Actions runs the test suite automatically when changes are pushed or pull requests are created.
Git Push
   ↓
GitHub Actions
   ↓
Checkout Repository
   ↓
Setup Python 3.11
   ↓
Install Dependencies
   ↓
Run Pytest
   ↓
PASS / FAIL

🔐 Configuration
Environment-specific configuration is provided through environment variables.
Example:
MODEL_PATH=models/steel_defect_yolo11n_v1.pt
MODEL_VERSION=steel-defect-yolo11n-v1
CONFIDENCE_THRESHOLD=0.25
DATABASE_URL=postgresql+psycopg2://...

Secrets and local environment files should not be committed to Git.
🛠️ Development Workflow
Develop
   ↓
Run Tests
   ↓
Run Docker
   ↓
Test API
   ↓
Test UI
   ↓
Git Commit
   ↓
Git Push
   ↓
GitHub Actions
   ↓
Automated Tests

🎯 Engineering Concepts Demonstrated
This project demonstrates an end-to-end AI engineering workflow:
- Computer vision model development
- Object detection
- Model evaluation
- AI model serving
- REST API development
- Separation of inference and API layers
- PostgreSQL integration
- SQLAlchemy ORM
- Alembic database migrations
- Request tracing
- Structured logging
- Error handling
- Database transactions
- Docker containerization
- Docker Compose
- Streamlit application development
- Automated testing
- Git/GitHub workflow
- Continuous integration
🚀 Future Improvements
Potential production extensions include:
- Authentication and authorization
- Model version management
- Cloud deployment
- Prometheus/Grafana monitoring
- Model performance monitoring
- Automated model retraining
- Object storage for uploaded images
- CI/CD Docker image publishing
- Production reverse proxy and HTTPS
These are intentionally kept outside the current MVP to maintain a focused and maintainable architecture.
📌 Project Status
Completed MVP
SteelVision AI currently provides a complete end-to-end steel defect detection pipeline:
YOLO11n
   +
FastAPI
   +
PostgreSQL
   +
SQLAlchemy
   +
Alembic
   +
Docker
   +
Streamlit
   +
Pytest
   +
GitHub Actions

The system is designed as a practical demonstration of taking a computer vision model from training and evaluation to API serving, persistence, containerization, testing, and CI.