
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints.patients import router as patients_router
from app.api.v1.endpoints.assessments import router as assessments_router
from app.api.v1.endpoints.ai import router as ai_router
from app.api.v1.endpoints.auth import router as auth_router


app = FastAPI(
    title="MedGuard API",
    description=(
        "Educational medication safety prototype "
        "using synthetic patient profiles only."
    ),
    version="1.0.0",
)


# Register API routers
app.include_router(patients_router, prefix="/api/v1")
app.include_router(assessments_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "MedGuard API",
    }


@app.get("/api/v1")
def api_information():
    return {
        "application": "MedGuard",
        "message": "Medication safety API is running",
        "data_policy": "Synthetic data only",
    }
