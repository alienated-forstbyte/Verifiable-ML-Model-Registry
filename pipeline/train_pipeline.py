import json
import hashlib
import shutil
from pathlib import Path

from training.train_model import train_model

MODEL_NAME = "spam_classifier"
VERSION = "1.0"

MODEL_DIR = Path("models")
REGISTRY_PATH = Path("model_registry.json")


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

    registry[MODEL_NAME] = {
        "version": VERSION,
        "model_path": str(model_path),
        "sha256": model_hash
    }

    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=2)


def main():

    MODEL_DIR.mkdir(exist_ok=True)

    print("Training model...")

    model_file = train_model()

    versioned_path = MODEL_DIR / f"{MODEL_NAME}_v{VERSION}.pkl"

    shutil.move(model_file, versioned_path)

    print("Computing hash...")

    model_hash = compute_hash(versioned_path)

    print("Model SHA256:", model_hash)

    print("Updating registry...")

    update_registry(versioned_path, model_hash)

    print("Pipeline complete.")


if __name__ == "__main__":
    main()