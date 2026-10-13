from pydantic import BaseModel


class AgeRequest(BaseModel):
    age: float


class AgeResponse(BaseModel):
    age: float
    valid: bool


class HealthResponse(BaseModel):
    status: str


class PredictionRequest(BaseModel):
    waveform: list[float]


class PredictionResponse(BaseModel):
    predicted_age_category: int
    scores: dict[str, float]
    model_status: str
