import json

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


def test_predict_age_category_rejects_non_mlp(monkeypatch):
    def fake_non_mlp_assets():
        model, metadata = fake_assets()
        metadata["kind"] = "cnn1d"
        return model, metadata

    monkeypatch.setattr(
        inference,
        "load_model_assets",
        fake_non_mlp_assets,
    )

    waveform = [0.1] * 512

    with pytest.raises(
        RuntimeError,
        match="The service currently supports only the MLP checkpoint.",
    ):
        inference.predict_age_category(waveform)


def test_load_model_assets(monkeypatch, tmp_path):
    metadata = {
        "kind": "mlp",
        "config": {
            "length": 512,
        },
    }

    metadata_path = tmp_path / "preprocessing.json"
    metadata_path.write_text(
        json.dumps(metadata),
        encoding="utf-8",
    )

    fake_model = object()

    def fake_load_model(path, compile=False):
        assert path == tmp_path / "model.keras"
        assert compile is False
        return fake_model

    monkeypatch.setenv(
        "VASCULAR_AGE_MODEL_DIR",
        str(tmp_path),
    )

    monkeypatch.setattr(
        inference,
        "load_model",
        fake_load_model,
    )

    inference.load_model_assets.cache_clear()

    model, loaded_metadata = inference.load_model_assets()

    assert model is fake_model
    assert loaded_metadata == metadata

    inference.load_model_assets.cache_clear()


def test_load_model_assets_requires_model_dir(monkeypatch):
    monkeypatch.delenv(
        "VASCULAR_AGE_MODEL_DIR",
        raising=False,
    )

    inference.load_model_assets.cache_clear()

    with pytest.raises(
        RuntimeError,
        match="VASCULAR_AGE_MODEL_DIR environment variable is not set.",
    ):
        inference.load_model_assets()

    inference.load_model_assets.cache_clear()
