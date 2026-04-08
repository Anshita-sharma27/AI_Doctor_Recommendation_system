import pandas as pd
import os

RAW_PATH = "dataset/raw_dataset.csv"
CLEAN_PATH = "dataset/cleaned_dataset.csv"

def clean_dataset():
    if not os.path.exists(RAW_PATH):
        print("❌ raw_dataset.csv not found inside dataset folder")
        return

    df = pd.read_csv(RAW_PATH)

    df.columns = [col.strip() for col in df.columns]
    df = df.drop_duplicates()
    df = df.fillna(0)

    if "prognosis" in df.columns:
        df["prognosis"] = df["prognosis"].astype(str).str.strip()

    os.makedirs("dataset", exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False)

    print("✅ Dataset cleaned successfully")
    print(f"📁 Saved to: {CLEAN_PATH}")

if __name__ == "__main__":
    clean_dataset()