from fastapi import FastAPI, HTTPException

from vascular_age.preprocessing import validate_age
from vascular_age.schemas import (
    AgeRequest,
    AgeResponse,
    HealthResponse,
    PredictionRequest,
    PredictionResponse,
)
from vascular_age.inference import predict_age_category

app = FastAPI(
    title="Vascular Age ML Service",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="healthy")


@app.post("/validate-age", response_model=AgeResponse)
def validate_age_endpoint(request: AgeRequest) -> AgeResponse:
    try:
        validated_age = validate_age(request.age)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return AgeResponse(
        age=validated_age,
        valid=True,
    )

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    try:
        result = predict_age_category(request.waveform)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return PredictionResponse(**result)
