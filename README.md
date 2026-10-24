# Vascular Age ML Service

[![Tests](https://github.com/KianaAbrisham/vascular-age-ml-service/actions/workflows/tests.yml/badge.svg)](https://github.com/KianaAbrisham/vascular-age-ml-service/actions/workflows/tests.yml)

A FastAPI-based machine learning service for serving age-category predictions from PPG waveforms.

The project demonstrates an end-to-end ML serving workflow: request validation, preprocessing, saved-model loading, inference, structured API responses, automated testing, containerization, and CI-based runtime verification.

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
├── .github/
│   └── workflows/
│       └── tests.yml
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
├── .dockerignore
├── Dockerfile
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

## Docker

Build the Docker image:

```powershell
docker build -t vascular-age-ml-service:0.1.0 .
```

Run the service with a saved model directory mounted read-only into the container:

```powershell
docker run -d --rm --name vascular-age-api -p 8000:8000 `
  --mount type=bind,source="C:\path\to\saved\model",target=/model,readonly `
  -e VASCULAR_AGE_MODEL_DIR=/model `
  vascular-age-ml-service:0.1.0
```

The mounted model directory must contain:

```text
model.keras
preprocessing.json
```

The model artifact remains outside the Docker image and is supplied at runtime through a read-only bind mount.

Check that the containerized API is running:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

A prediction request can then be sent to the containerized service:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:8000/predict `
  -ContentType "application/json" `
  -InFile .\request.json
```

Stop the container with:

```powershell
docker stop vascular-age-api
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

Run the test suite with statement and branch coverage:

```powershell
python -m pytest --cov=vascular_age --cov-branch --cov-report=term-missing --cov-fail-under=90 -v
```

The tests cover:

- age-input validation,
- API request and response behavior,
- valid and invalid prediction requests,
- fixed-length waveform validation,
- inference output handling,
- model-asset loading,
- unsupported checkpoint rejection,
- and predicted-class selection.

API tests use controlled mock predictions so they do not depend on a model file stored on one specific computer. Inference logic is tested separately with lightweight model substitutes and model-loading tests.

## Continuous Integration

GitHub Actions automatically:

- checks out the repository,
- sets up Python,
- installs the project and development dependencies,
- runs the automated test suite,
- measures statement and branch coverage,
- requires at least 90% test coverage,
- builds the Docker image,
- starts a container from that image,
- and verifies the `/health` endpoint.

This provides automated checks for both the Python application and the containerized runtime after each push.

## Model Artifact

The trained checkpoint is kept separate from this source-code repository.

At runtime, the application loads `model.keras` and `preprocessing.json` from the directory specified by `VASCULAR_AGE_MODEL_DIR`.

When Docker is used, the model directory can be supplied to the container through a read-only bind mount.

This avoids embedding machine-specific paths or generated model artifacts in the application code or Docker image.

## Related Research Code

The training and benchmarking workflow is maintained separately:

https://github.com/KianaAbrisham/ppg-vascular-age-benchmark

That repository contains the model-training, evaluation, preprocessing, checkpoint, and prediction workflows used to produce compatible model artifacts.

The software-serving workflow has also been verified locally using an MLP demo checkpoint produced by that repository and a 512-sample artificial PPG waveform.

## Limitations

The current service supports the MLP checkpoint path only.

The demo model used for software verification was trained on artificial data and must not be interpreted as evidence of clinical validity or research-level predictive performance.

The current output is one of six fixed age categories rather than a continuous biological or vascular-age measurement.

The saved demo checkpoint is used to verify software integration and model serving, not to establish predictive accuracy on patient or wearable data.

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
- statement and branch coverage checks,
- Docker image creation,
- runtime model mounting through a read-only bind mount,
- CI-based Docker build and container health verification,
- and local end-to-end prediction with a saved Keras checkpoint inside the Dockerized service.
