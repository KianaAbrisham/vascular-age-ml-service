from pydantic import BaseModel


class AgeRequest(BaseModel):
    age: float


class AgeResponse(BaseModel):
    age: float
    valid: bool


class HealthResponse(BaseModel):
    status: str