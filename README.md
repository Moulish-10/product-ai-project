# SteelVision AI

A production-oriented AI inference API built with FastAPI, YOLO11n, PostgreSQL, SQLAlchemy, Alembic, Docker, and GitHub Actions.

## Overview

This project demonstrates an end-to-end AI application workflow:

```text
Image
  ↓
FastAPI API
  ↓
Request Validation
  ↓
YOLO11n Inference
  ↓
Prediction Results
  ↓
PostgreSQL
  ↓
API Response

The application provides object detection through a REST API and stores prediction and detection results in PostgreSQL.

Tech Stack
Python 3.11
FastAPI
YOLO11n / Ultralytics
PostgreSQL
SQLAlchemy
Alembic
Pydantic
Docker
Docker Compose
Pytest
Git
GitHub Actions
Architecture
                    ┌─────────────────┐
                    │     Client      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    FastAPI      │
                    │   REST API      │
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
                                │  predictions    │
                                │  detections     │
                                └─────────────────┘
Project Structure
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
├── tests/
│
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── alembic.ini
├── requirements.txt
└── yolo11n.pt
API Endpoints
Health Check
GET /health

Checks whether the API is running.

Example:

{
  "status": "Healthy"
}
Object Prediction
POST /predict

Upload an image and receive YOLO object detection results.

Example response:

{
  "message": "Prediction completed",
  "image_name": "image.jpg",
  "model_version": "yolo11n",
  "image_width": 1920,
  "image_height": 1080,
  "detection_count": 3,
  "inference_time_ms": 209.53,
  "detections": []
}
Prediction History
GET /predictions

Returns previously stored prediction records.

Prediction Details
GET /predictions/{prediction_id}

Returns a specific prediction and its associated detections.

Running the Project with Docker

Build and start the application:

docker compose up -d --build

Check running containers:

docker compose ps

View API logs:

docker logs steelvision-api

The API is available at:

http://localhost:8000

Interactive Swagger documentation:

http://localhost:8000/docs
Database

PostgreSQL runs as a Docker service.

The application stores prediction information in two main tables.

predictions

Stores information about each prediction request:

Prediction ID
Request ID
Image name
Model version
Detection count
Inference time
Creation timestamp
detections

Stores individual detected objects:

Detection ID
Prediction ID
Class name
Confidence
Bounding box coordinates
Database Migrations

Alembic is used to manage database schema migrations.

Apply migrations manually:

alembic upgrade head

Check the current migration:

alembic current

The Docker container automatically runs:

alembic upgrade head

during startup before starting the FastAPI application.

Testing

Run the test suite:

pytest -q

The tests cover API health, prediction functionality, prediction history, prediction details, and error scenarios.

Request Tracing

Each HTTP request receives a unique request ID.

The request ID is:

Returned through the X-Request-ID response header
Included in application logs
Stored with prediction records

This allows a prediction request to be traced across the API, logs, inference process, and database.

Error Handling

The API provides structured error handling for unexpected application failures.

Prediction database operations use transactions so that failed requests do not leave incomplete prediction records.

Docker

The application is containerized using Docker.

The Docker setup includes:

FastAPI application
YOLO11n model
PostgreSQL database
Automatic Alembic migrations
Health checks
Non-root application user

Docker Compose manages the API and PostgreSQL services.

Continuous Integration

GitHub Actions automatically runs the test suite when code is pushed to the repository or submitted through a pull request.

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
Development Workflow
Develop
   ↓
Run Tests
   ↓
Build / Run Docker
   ↓
Test API
   ↓
Git Commit
   ↓
Git Push
   ↓
GitHub Actions
   ↓
Automated Tests
Learning Objectives

This project was created as a practical learning project to understand the production lifecycle of an AI application.

Key concepts covered:

AI model serving
REST API development
FastAPI
Object detection
Separating API and inference logic
PostgreSQL integration
SQLAlchemy ORM
Database migrations with Alembic
Docker containerization
Docker Compose
Environment-based configuration
Request tracing
Application logging
Error handling
Database transactions
Automated testing
Git and GitHub
Continuous Integration with GitHub Actions
Future Improvements

Possible future improvements include:

Authentication and authorization
Model version management
Cloud deployment
Prometheus/Grafana monitoring
Model performance monitoring
Automated model retraining
Object storage for uploaded images
Docker image publishing through CI/CD
Production deployment
Status

The current version provides a complete learning-oriented AI inference pipeline with:

FastAPI
YOLO11n
PostgreSQL
SQLAlchemy
Alembic
Docker
Automated database migrations
Request tracing
Logging
Error handling
Automated tests
GitHub Actions CI
