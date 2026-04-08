import os
import json
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(BASE_DIR, "dataset", "cleaned_dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "doctor_model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")
ACCURACY_PATH = os.path.join(MODEL_DIR, "accuracy.json")

os.makedirs(MODEL_DIR, exist_ok=True)

if not os.path.exists(DATASET_PATH):
    print("❌ Dataset not found:", DATASET_PATH)
    exit()

print("📂 Loading dataset...")
df = pd.read_csv(DATASET_PATH)

if "prognosis" not in df.columns:
    print("❌ 'prognosis' column not found in dataset")
    exit()

# Features and target
X = df.drop("prognosis", axis=1)
y = df["prognosis"]

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# Train model
print("🤖 Training model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = round(accuracy_score(y_test, y_pred) * 100, 2)

# Save model
joblib.dump(model, MODEL_PATH)
joblib.dump(label_encoder, ENCODER_PATH)

with open(ACCURACY_PATH, "w") as f:
    json.dump({"accuracy": accuracy}, f)

print("✅ Model trained successfully")
print("📦 Saved model:", MODEL_PATH)
print("📦 Saved encoder:", ENCODER_PATH)
print("📊 Accuracy:", accuracy, "%")