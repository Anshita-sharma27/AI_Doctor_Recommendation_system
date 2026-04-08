import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# -----------------------------
# USERS TABLE
# -----------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'patient'
)
""")

# -----------------------------
# DOCTORS TABLE
# -----------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialization TEXT NOT NULL,
    photo TEXT,
    description TEXT,
    experience TEXT,
    fees TEXT,
    hospital TEXT,
    disease_key TEXT
)
""")

# -----------------------------
# REPORTS TABLE
# -----------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    patient_email TEXT,
    symptoms TEXT,
    predicted_disease TEXT,
    predicted_doctor TEXT,
    specialization TEXT,
    confidence REAL,
    created_at TEXT,
    pdf_path TEXT
)
""")

# -----------------------------
# APPOINTMENTS TABLE
# -----------------------------
cur.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT NOT NULL,
    patient_email TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    specialization TEXT NOT NULL,
    appointment_date TEXT NOT NULL,
    notes TEXT,
    status TEXT DEFAULT 'Pending',
    created_at TEXT
)
""")

conn.commit()
conn.close()

print("✅ Database setup completed successfully.")