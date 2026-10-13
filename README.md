\## Project Structure



```text

vascular-age-ml-service/

├── src/

│   └── vascular\_age/

│       ├── api.py

│       ├── inference.py

│       ├── preprocessing.py

│       ├── schemas.py

│       └── \_\_init\_\_.py

├── tests/

│   ├── test\_api.py

│   ├── test\_inference.py

│   └── test\_preprocessing.py

├── data/

├── models/

├── notebooks/

├── pyproject.toml

└── README.md



API Endpoints

Method	Endpoint	Purpose

GET	/health	Check service availability

POST	/validate-age	Validate a numeric age input

POST	/predict	Run age-category inference on a PPG waveform





Prediction Flow

PPG waveform

&#x20;   ↓

POST /predict

&#x20;   ↓

Pydantic request validation

&#x20;   ↓

Inference preprocessing

&#x20;   ↓

Saved Keras model

&#x20;   ↓

Six output scores

&#x20;   ↓

Predicted age category

&#x20;   ↓

JSON response



Installation

Python 3.10 or newer is required.

Create and activate a virtual environment:

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1



Install the project and development dependencies:

python -m pip install -e ".\[dev]"



Model Configuration

The service does not hard-code a local model path.

Instead, set the VASCULAR\_AGE\_MODEL\_DIR environment variable to a directory containing:

model.keras

preprocessing.json



Example in Windows PowerShell:

$env:VASCULAR\_AGE\_MODEL\_DIR = "C:\\path\\to\\saved\\model"



The service currently expects an MLP checkpoint whose preprocessing metadata defines the required waveform length and age classes.

Run the API

Start the development server:

python -m uvicorn vascular\_age.api:app --reload



Then open the interactive API documentation:

http://127.0.0.1:8000/docs



Prediction Request

The /predict endpoint expects JSON containing a waveform:

{

&#x20; "waveform": \[0.12, 0.15, 0.18]

}



The actual number of samples must match the length stored in the checkpoint metadata. The current demo checkpoint expects exactly 512 samples.

A successful response has the following structure:

{

&#x20; "predicted\_age\_category": 35,

&#x20; "scores": {

&#x20;   "25": 0.18,

&#x20;   "35": 0.32,

&#x20;   "45": 0.04,

&#x20;   "55": 0.19,

&#x20;   "65": 0.06,

&#x20;   "75": 0.20

&#x20; },

&#x20; "model\_status": "artificial\_data\_software\_check"

}



If the waveform length is invalid, the API returns an HTTP 400 response with a descriptive error message.

Testing

Run the full automated test suite with:

python -m pytest -v



The tests cover preprocessing validation, API behavior, prediction responses, invalid waveform handling, and inference logic.

The API tests use controlled mock predictions so they do not depend on a locally available model checkpoint. Inference logic is tested separately using a lightweight fake model.

Model Artifact

The model checkpoint is intentionally kept separate from the source-code repository.

The service loads the model at runtime from the directory specified by VASCULAR\_AGE\_MODEL\_DIR. This keeps machine-specific paths and generated model artifacts out of the application code.

Related Research Code

The model-training and benchmarking workflow is maintained separately:

https://github.com/KianaAbrisham/ppg-vascular-age-benchmark

The benchmark repository contains the training, evaluation, preprocessing, checkpoint, and prediction workflows used to produce compatible model artifacts.

Limitations

The current service supports only the MLP checkpoint path.

The demo checkpoint used during development was trained on artificial data for software validation. It must not be interpreted as evidence of clinical validity, biological-age estimation accuracy, or research-level model performance.

The current output represents one of six fixed age categories rather than a continuous vascular-age measurement.

Development Status

The current implementation includes:

\- FastAPI request and response schemas,

\- PPG waveform validation,

\- Keras checkpoint loading,

\- cached model initialization,

\- ML inference,

\- structured prediction responses,

\- HTTP error handling,

\- unit and API tests,

\- and local end-to-end API verification.
