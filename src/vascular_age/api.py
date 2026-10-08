from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from vascular_age.preprocessing import validate_age


app = FastAPI(
    title="Vascular Age ML Service",
    version="0.1.0",
)


class AgeRequest(BaseModel):
    age: float


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/validate-age")
def validate_age_endpoint(request: AgeRequest):
    try:
        validated_age = validate_age(request.age)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return {
        "age": validated_age,
        "valid": True,
    }