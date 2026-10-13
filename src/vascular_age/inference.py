import json
import os
from functools import lru_cache
from pathlib import Path

import numpy as np
from keras.models import load_model


@lru_cache
def load_model_assets():
    model_dir_value = os.getenv("VASCULAR_AGE_MODEL_DIR")

    if not model_dir_value:
        raise RuntimeError(
            "VASCULAR_AGE_MODEL_DIR environment variable is not set."
        )

    model_dir = Path(model_dir_value)

    with (model_dir / "preprocessing.json").open(
        "r",
        encoding="utf-8",
    ) as file:
        metadata = json.load(file)

    model = load_model(
        model_dir / "model.keras",
        compile=False,
    )

    return model, metadata


def predict_age_category(waveform: list[float]) -> dict:
    model, metadata = load_model_assets()

    if metadata["kind"] != "mlp":
        raise RuntimeError(
            "The service currently supports only the MLP checkpoint."
        )

    expected_length = metadata["config"]["length"]

    if len(waveform) != expected_length:
        raise ValueError(
            f"Waveform must contain exactly {expected_length} samples."
        )

    x = np.asarray(
        [waveform],
        dtype=np.float32,
    )

    mean = metadata["x_scale"]["mean"]
    std = metadata["x_scale"]["std"]

    x = (x - mean) / std

    scores = model.predict(
        x,
        verbose=0,
    )[0]

    age_classes = metadata["age_classes"]

    predicted_index = int(np.argmax(scores))
    predicted_age = int(age_classes[predicted_index])

    return {
        "predicted_age_category": predicted_age,
        "scores": {
            str(age): float(score)
            for age, score in zip(age_classes, scores)
        },
        "model_status": metadata["status"],
    }
