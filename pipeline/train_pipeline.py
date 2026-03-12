import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime

from training.train_model import train_model
from registry.hash_utils import file_hash


MODEL_NAME = "spam_classifier"
VERSION = "1.0"

MODEL_DIR = Path("models")
REGISTRY_PATH = Path("model_registry.json")

DATASET_PATH = "data/spam.csv"
TRAINING_CODE_PATH = "training/train_model.py"


def compute_hash(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def update_registry(model_path, model_hash):

    registry = {}

    if REGISTRY_PATH.exists():
        with open(REGISTRY_PATH) as f:
            registry = json.load(f)

    # lineage hashes
    dataset_hash = file_hash(DATASET_PATH)
    code_hash = file_hash(TRAINING_CODE_PATH)

    print("Dataset SHA256:", dataset_hash)
    print("Training Code SHA256:", code_hash)

    registry[MODEL_NAME] = {
        "version": VERSION,
        "model_path": str(model_path),
        "model_sha256": model_hash,
        "dataset_sha256": dataset_hash,
        "training_code_sha256": code_hash,
        "created_at": datetime.utcnow().isoformat()
    }

    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)


def main():

    MODEL_DIR.mkdir(exist_ok=True)

    print("Training model...")

    model_file = train_model()

    versioned_path = MODEL_DIR / f"{MODEL_NAME}_v{VERSION}.pkl"

    shutil.move(model_file, versioned_path)

    print("Computing model hash...")

    model_hash = compute_hash(versioned_path)

    print("Model SHA256:", model_hash)

    print("Updating registry with lineage metadata...")

    update_registry(versioned_path, model_hash)

    print("Pipeline complete.")


if __name__ == "__main__":
    main()