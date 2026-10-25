
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MedGuard API",
    description=(
        "Educational medication safety prototype "
        "using synthetic patient profiles only."
    ),
    version="1.0.0",
)

# Temporary development configuration.
# Restrict origins before deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=False,
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
