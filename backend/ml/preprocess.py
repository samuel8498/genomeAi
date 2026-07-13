import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def load_and_preprocess(data_path, labels_path):

    data = pd.read_csv(data_path)
    labels = pd.read_csv(labels_path)

    print("Data Shape :", data.shape)
    print("Labels Shape :", labels.shape)

    # First column = Sample ID
    X = data.iloc[:, 1:]

    # Cancer labels
    y = labels.iloc[:, 1]

    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Save encoder
    joblib.dump(label_encoder, BASE_DIR / "label_encoder.pkl")

    # Scale features
    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    # Save scaler
    joblib.dump(scaler, BASE_DIR / "scaler.pkl")

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y_encoded,
        test_size=0.2,
        random_state=42,
        stratify=y_encoded
    )

    print("Training Samples :", len(X_train))
    print("Testing Samples :", len(X_test))

    return X_train, X_test, y_train, y_test