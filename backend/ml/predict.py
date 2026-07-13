from pathlib import Path
import joblib
import pandas as pd

# -------------------------------------------------------
# Load trained model
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(BASE_DIR / "model.pkl")
scaler = joblib.load(BASE_DIR / "scaler.pkl")
label_encoder = joblib.load(BASE_DIR / "label_encoder.pkl")


def predict_cancer(csv_path):

    # Read uploaded CSV
    data = pd.read_csv(csv_path)

    # Number of features expected by the scaler
    expected_features = scaler.n_features_in_

    sample_names = None

    # -------------------------------------------------------
    # CASE 1:
    # File contains only gene columns
    # -------------------------------------------------------
    if data.shape[1] == expected_features:

        X = data

        sample_names = [
            f"Sample_{i+1}"
            for i in range(len(data))
        ]

    # -------------------------------------------------------
    # CASE 2:
    # File contains Sample ID + gene columns
    # -------------------------------------------------------
    elif data.shape[1] == expected_features + 1:

        sample_names = data.iloc[:, 0].astype(str)

        X = data.iloc[:, 1:]

    # -------------------------------------------------------
    # Wrong format
    # -------------------------------------------------------
    else:

        raise ValueError(
            f"""
Uploaded CSV has {data.shape[1]} columns.

Model expects

{expected_features} gene columns

OR

{expected_features + 1} columns
(SampleID + genes)
"""
        )

    # -------------------------------------------------------
    # Verify feature names
    # -------------------------------------------------------

    if hasattr(scaler, "feature_names_in_"):

        X = X.reindex(columns=scaler.feature_names_in_)

    # -------------------------------------------------------
    # Scale
    # -------------------------------------------------------

    X_scaled = scaler.transform(X)

    # -------------------------------------------------------
    # Predict
    # -------------------------------------------------------

    predictions = model.predict(X_scaled)

    probabilities = model.predict_proba(X_scaled)

    results = []

    for i in range(len(predictions)):

        cancer = label_encoder.inverse_transform(
            [predictions[i]]
        )[0]

        confidence = round(
            probabilities[i].max() * 100,
            2
        )

        results.append(
            {
                "sample": sample_names[i],
                "prediction": cancer,
                "confidence": confidence,
            }
        )

    return {
        "total_samples": len(results),
        "predictions": results,
    }