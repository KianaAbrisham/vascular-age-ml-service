from fastapi.testclient import TestClient

from vascular_age.api import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_validate_age_success():
    response = client.post(
        "/validate-age",
        json={"age": 35},
    )

    assert response.status_code == 200
    assert response.json() == {
        "age": 35.0,
        "valid": True,
    }


def test_validate_age_out_of_range():
    response = client.post(
        "/validate-age",
        json={"age": 150},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Age must be between 0 and 120."


def test_validate_age_wrong_type():
    response = client.post(
        "/validate-age",
        json={"age": "hello"},
    )

    assert response.status_code == 422
