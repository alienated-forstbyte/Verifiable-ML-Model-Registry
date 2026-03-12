import pandas as pd
from sklearn.model_selection import train_test_split

def load_dataset():

    data = pd.read_csv(
        "data/spam.csv",
        encoding="latin-1"
    )

    data = data[["v1", "v2"]]
    data.columns = ["label", "message"]

    X = data["message"]
    y = data["label"]

    return train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )