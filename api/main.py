import json
import hashlib
import joblib
from fastapi import FastAPI

app = FastAPI()


def compute_hash(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def load_registry():

    with open("model_registry.json") as f:
        return json.load(f)


registry = load_registry()

model_info = registry["spam_classifier"]

MODEL_PATH = model_info["model_path"]
EXPECTED_HASH = model_info["sha256"]


def verify_model():

    current_hash = compute_hash(MODEL_PATH)

    if current_hash != EXPECTED_HASH:
        raise Exception("Model integrity verification failed")


verify_model()

model = joblib.load(MODEL_PATH)


@app.get("/")
def status():
    return {"status": "model verified", "version": model_info["version"]}


@app.post("/predict")
def predict(text: str):

    prediction = model.predict([text])[0]

    return {"prediction": prediction}