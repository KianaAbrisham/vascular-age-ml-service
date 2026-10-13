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


def test_predict_success(monkeypatch):
    def fake_predict_age_category(waveform):
        return {
            "predicted_age_category": 35,
            "scores": {
                "25": 0.10,
                "35": 0.50,
                "45": 0.10,
                "55": 0.10,
                "65": 0.10,
                "75": 0.10,
            },
            "model_status": "test_model",
        }

    monkeypatch.setattr(
        "vascular_age.api.predict_age_category",
        fake_predict_age_category,
    )

    response = client.post(
        "/predict",
        json={"waveform": [0.1] * 512},
    )

    assert response.status_code == 200
    assert response.json()["predicted_age_category"] == 35
    assert response.json()["model_status"] == "test_model"


def test_predict_invalid_length(monkeypatch):
    def fake_predict_age_category(waveform):
        raise ValueError(
            "Waveform must contain exactly 512 samples."
        )

    monkeypatch.setattr(
        "vascular_age.api.predict_age_category",
        fake_predict_age_category,
    )

    response = client.post(
        "/predict",
        json={"waveform": [0.1] * 100},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Waveform must contain exactly 512 samples."
    )

