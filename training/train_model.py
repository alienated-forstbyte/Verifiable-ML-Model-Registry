import mlflow
import joblib
import hashlib

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from training.dataset_loader import load_dataset

from pathlib import Path

# fix for CI
mlflow.set_tracking_uri("file:./mlruns")
Path("mlruns").mkdir(exist_ok=True)
def hash_model(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def train_model():

    X_train, X_test, y_train, y_test = load_dataset()

    pipeline = Pipeline([
        ("vectorizer", CountVectorizer()),
        ("model", MultinomialNB())
    ])

    mlflow.start_run()

    pipeline.fit(X_train, y_train)

    model_path = "model.pkl"

    joblib.dump(pipeline, model_path)

    model_hash = hash_model(model_path)

    print("Model SHA256:", model_hash)

    mlflow.log_artifact(model_path)
    mlflow.log_param("model_sha256", model_hash)

    mlflow.end_run()

    print("Model trained, hashed, and logged.")

    return model_path


if __name__ == "__main__":
    train_model()