import numpy as np
import pytest

from vascular_age import inference


class FakeModel:
    def predict(self, x, verbose=0):
        return np.array(
            [[0.10, 0.50, 0.10, 0.10, 0.10, 0.10]],
            dtype=np.float32,
        )


def fake_assets():
    model = FakeModel()

    metadata = {
        "kind": "mlp",
        "config": {
            "length": 512,
        },
        "x_scale": {
            "mean": 0.0,
            "std": 1.0,
        },
        "age_classes": [25, 35, 45, 55, 65, 75],
        "status": "test_model",
    }

    return model, metadata


def test_predict_age_category_success(monkeypatch):
    monkeypatch.setattr(
        inference,
        "load_model_assets",
        fake_assets,
    )

    waveform = [0.1] * 512

    result = inference.predict_age_category(waveform)

    assert result["predicted_age_category"] == 35
    assert result["scores"]["35"] == pytest.approx(0.50)
    assert result["model_status"] == "test_model"


def test_predict_age_category_invalid_length(monkeypatch):
    monkeypatch.setattr(
        inference,
        "load_model_assets",
        fake_assets,
    )

    waveform = [0.1] * 100

    with pytest.raises(
        ValueError,
        match="Waveform must contain exactly 512 samples.",
    ):
        inference.predict_age_category(waveform)
