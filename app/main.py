from fastapi import FastAPI

app = FastAPI(
    title = "Product AI API",
    description = "Production oriented AI inference service",
    version = "0.1.0"
)

@app.get("/")
def root():
    return{
        "message" : "Product AI API is running",
        "version" : "0.1.0"
    }

@app.get("/health")
def health():
    return {
        "status" : "Healthy"
    }