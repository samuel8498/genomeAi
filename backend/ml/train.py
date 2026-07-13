from preprocess import load_and_preprocess

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score

import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = "../../dataset/data.csv"
LABEL_PATH = "../../dataset/labels.csv"

X_train, X_test, y_train, y_test = load_and_preprocess(
    DATA_PATH,
    LABEL_PATH
)

print("\nTraining Random Forest...\n")

rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

rf.fit(X_train, y_train)

rf_pred = rf.predict(X_test)

rf_accuracy = accuracy_score(y_test, rf_pred)

print("Random Forest Accuracy :", rf_accuracy)

print("\nTraining XGBoost...\n")

xgb = XGBClassifier(
    random_state=42,
    eval_metric="mlogloss"
)

xgb.fit(X_train, y_train)

xgb_pred = xgb.predict(X_test)

xgb_accuracy = accuracy_score(y_test, xgb_pred)

print("XGBoost Accuracy :", xgb_accuracy)

if rf_accuracy > xgb_accuracy:

    print("\nRandom Forest Selected")

    joblib.dump(rf, BASE_DIR / "model.pkl")

else:

    print("\nXGBoost Selected")

    joblib.dump(xgb, BASE_DIR / "model.pkl")

print("\nTraining Completed Successfully")