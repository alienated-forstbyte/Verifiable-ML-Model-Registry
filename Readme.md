Verifiable ML Model Registry

A secure MLOps pipeline for training, verifying, versioning, and deploying machine learning models with cryptographic integrity checks.

This project demonstrates how to build a production-style ML pipeline with:

automated model training

model integrity verification

lineage tracking

containerized deployment

CI/CD automation

model registry management

The system ensures that trained models cannot be tampered with without detection.

Architecture
Developer Push
      ↓
GitHub Actions CI/CD
      ↓
Training Pipeline
      ↓
Model Artifact
      ↓
Cryptographic Hash
      ↓
Model Registry (Lineage Tracking)
      ↓
Docker Image Build
      ↓
DockerHub Deployment
      ↓
FastAPI Inference Service
Key Features
Model Integrity Verification

Each trained model is hashed using SHA-256.

model.pkl
   ↓
SHA256 hash
   ↓
stored in model registry

At deployment time the hash is verified to ensure the model has not been modified.

Model Registry

The project maintains a registry file:

model_registry.json

Example:

{
  "spam_classifier": {
    "version": "1.0",
    "model_path": "models/spam_classifier_v1.0.pkl",
    "model_sha256": "...",
    "dataset_sha256": "...",
    "training_code_sha256": "...",
    "created_at": "2026-03-12T10:00:00Z"
  }
}

This provides full model lineage tracking.

Model Lineage Tracking

Each training run records:

model hash

dataset hash

training code hash

timestamp

version

This allows complete reproducibility of models.

CI/CD Pipeline

GitHub Actions automatically performs:

git push
   ↓
install dependencies
   ↓
run training pipeline
   ↓
generate model + hashes
   ↓
update registry
   ↓
build docker image
   ↓
push to DockerHub
Containerized Deployment

The inference API is packaged as a Docker container.

Run locally:

docker run -p 8000:8000 <dockerhub-username>/ml-secure-api

API documentation:

http://localhost:8000/docs
Project Structure
.
├── api/
│   └── main.py
│
├── training/
│   ├── train_model.py
│   └── dataset_loader.py
│
├── pipeline/
│   └── train_pipeline.py
│
├── registry/
│   └── hash_utils.py
│
├── models/
│
├── data/
│   └── spam.csv
│
├── model_registry.json
├── requirements.txt
├── Dockerfile
└── .github/workflows/ml_pipeline.yml
Running Locally
1 Install Dependencies
pip install -r requirements.txt
2 Run Training Pipeline
python -m pipeline.train_pipeline

This will:

train the model

compute hashes

update the registry

3 Run the API
uvicorn api.main:app --reload

Open:

http://localhost:8000/docs
Running with Docker

Build container:

docker build -t ml-secure-api .

Run container:

docker run -p 8000:8000 ml-secure-api
Example Prediction

Input:

free lottery win money now

Response:

{
  "prediction": "spam"
}
Security Model

The system verifies model integrity using cryptographic hashing.

Verification flow:

model file
   ↓
compute SHA256
   ↓
compare with registry
   ↓
load model if valid

If hashes do not match the API refuses to load the model.

Future Improvements

Potential extensions:

blockchain-based model registry

model drift detection

automated retraining

feature store integration

MLflow tracking server

Kubernetes deployment

Technologies Used

Python

Scikit-learn

FastAPI

MLflow

Docker

GitHub Actions

SHA256 Cryptographic Hashing

License

MIT License.

If you'd like, I can also help you add a clean architecture diagram and badges (CI status, DockerHub, license) so the README looks more professional and portfolio-ready.