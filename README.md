# Vascular Age ML Service

[![Tests](https://github.com/KianaAbrisham/vascular-age-ml-service/actions/workflows/tests.yml/badge.svg)](https://github.com/KianaAbrisham/vascular-age-ml-service/actions/workflows/tests.yml)

A FastAPI-based machine learning service for serving age-category predictions from PPG waveforms.

The project demonstrates an end-to-end ML serving workflow: request validation, preprocessing, saved-model loading, inference, structured API responses, and automated testing.

## Current Scope

The service currently supports an MLP checkpoint and returns:

- a predicted age category,
- six model output scores,
- and model-status metadata.

The supported age categories are:

`25, 35, 45, 55, 65, 75`

The demo checkpoint used during development was trained on artificial data for software-integration testing. Its outputs are not evidence of clinical or research performance.

## Project Structure

```text
vascular-age-ml-service/
├── src/
│   └── vascular_age/
│       ├── api.py
│       ├── inference.py
│       ├── preprocessing.py
│       ├── schemas.py
│       └── __init__.py
├── tests/
│   ├── test_api.py
│   ├── test_inference.py
│   └── test_preprocessing.py
├── data/
├── models/
├── notebooks/
├── pyproject.toml
└── README.md
```

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Check service availability |
| `POST` | `/validate-age` | Validate a numeric age input |
| `POST` | `/predict` | Run age-category inference on a PPG waveform |

## Prediction Flow

```text
PPG waveform
    ↓
POST /predict
    ↓
Pydantic validation
    ↓
Inference preprocessing
    ↓
Saved Keras model
    ↓
Six output scores
    ↓
Predicted age category
    ↓
JSON response
```

## Installation

Python 3.10 or newer is required.

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project and development dependencies:

```powershell
python -m pip install -e ".[dev]"
```

## Model Configuration

The model path is not hard-coded in the application.

Set the `VASCULAR_AGE_MODEL_DIR` environment variable to a directory containing:

```text
model.keras
preprocessing.json
```

Example in Windows PowerShell:

```powershell
$env:VASCULAR_AGE_MODEL_DIR = "C:\path\to\saved\model"
```

The service reads the preprocessing metadata associated with the saved checkpoint and currently accepts only an MLP checkpoint.

## Run the API

Start the development server:

```powershell
python -m uvicorn vascular_age.api:app --reload
```

Open the interactive FastAPI documentation at:

```text
http://127.0.0.1:8000/docs
```

## Prediction Request

The `/predict` endpoint expects JSON containing a waveform:

```json
{
  "waveform": [0.12, 0.15, 0.18]
}
```

The waveform length must match the length stored in the checkpoint metadata. The current demo checkpoint expects 512 samples.

A successful response has this structure:

```json
{
  "predicted_age_category": 35,
  "scores": {
    "25": 0.18,
    "35": 0.32,
    "45": 0.04,
    "55": 0.19,
    "65": 0.06,
    "75": 0.20
  },
  "model_status": "artificial_data_software_check"
}
```

An invalid waveform length returns HTTP `400` with a descriptive error message.

## Testing

Run the automated test suite with:

```powershell
python -m pytest -v
```

The tests cover:

- age-input validation,
- API request and response behavior,
- valid and invalid prediction requests,
- fixed-length waveform validation,
- inference output handling,
- and predicted-class selection.

API tests use controlled mock predictions so they do not depend on a model file stored on one specific computer. Inference logic is tested separately with a lightweight fake model.

## Model Artifact

The trained checkpoint is kept separate from this source-code repository.

At runtime, the application loads `model.keras` and `preprocessing.json` from the directory specified by `VASCULAR_AGE_MODEL_DIR`.

This avoids embedding machine-specific paths or generated model artifacts in the application code.

## Related Research Code

The training and benchmarking workflow is maintained separately:

https://github.com/KianaAbrisham/ppg-vascular-age-benchmark

That repository contains the model-training, evaluation, preprocessing, checkpoint, and prediction workflows used to produce compatible model artifacts.

## Limitations

The current service supports the MLP checkpoint path only.

The demo model used for software verification was trained on artificial data and must not be interpreted as evidence of clinical validity or research-level predictive performance.

The current output is one of six fixed age categories rather than a continuous biological or vascular-age measurement.

## Development Status

The current implementation includes:

- FastAPI request and response schemas,
- fixed-length waveform validation,
- Keras checkpoint loading,
- cached model loading,
- ML inference,
- structured JSON responses,
- controlled HTTP error handling,
- automated API and inference tests,
- and local end-to-end API verification.
