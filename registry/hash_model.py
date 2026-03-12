import hashlib

def hash_model(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


if __name__ == "__main__":
    path = "models/spam_classifier_v1.pkl"
    print(hash_model(path))