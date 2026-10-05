from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.health import router as health_router
from app.api.prediction import router as prediction_router

# Register SQLAlchemy models
from app.models.prediction import Prediction
from app.models.detection import Detection

import uuid

from app.models.schemas import ErrorResponse

app = FastAPI(
    title="SteelVision AI API",
    description="Production-oriented AI inference service",
    version="0.1.0",
)

@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())

    request.state.request_id = request_id

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    return response

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    request_id = getattr(
        request.state,
        "request_id",
        None,
    )

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error.",
            request_id=request_id,
            status_code=500,
        ).model_dump(),
    )


@app.get("/")
def root():
    return {
        "message": "SteelVision AI API is running",
        "version": "0.1.0",
    }


app.include_router(health_router)
app.include_router(prediction_router)
