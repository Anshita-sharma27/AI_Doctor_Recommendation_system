import pandas as pd
import joblib
import json
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

DATA_PATH = "dataset/cleaned_dataset.csv"
MODEL_DIR = "model"

def train_model():
    if not os.path.exists(DATA_PATH):
        print("❌ cleaned_dataset.csv not found. Run clean_dataset.py first.")
        return

    df = pd.read_csv(DATA_PATH)

    if df.empty:
        print("❌ Dataset is empty.")
        return

    if "prognosis" not in df.columns:
        print("❌ 'prognosis' column not found in dataset.")
        return

    X = df.drop("prognosis", axis=1)
    y = df["prognosis"]

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(model, os.path.join(MODEL_DIR, "doctor_model.pkl"))
    joblib.dump(label_encoder, os.path.join(MODEL_DIR, "label_encoder.pkl"))

    with open(os.path.join(MODEL_DIR, "accuracy.json"), "w") as f:
        json.dump({
            "accuracy": round(accuracy * 100, 2)
        }, f, indent=4)

    print("✅ Model trained successfully")
    print(f"🎯 Accuracy: {round(accuracy * 100, 2)}%")

if __name__ == "__main__":
    train_model()