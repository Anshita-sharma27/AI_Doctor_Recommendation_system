from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import json
import joblib
import pandas as pd
from datetime import datetime

from utils.doctor_mapping import doctor_mapping
from utils.pdf_generator import generate_pdf
from utils.excel_export import export_reports_to_excel

app = Flask(__name__)
CORS(app)

# -----------------------------
# BASE PATHS
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "database.db")
MODEL_PATH = os.path.join(BASE_DIR, "model", "doctor_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "model", "label_encoder.pkl")
ACCURACY_PATH = os.path.join(BASE_DIR, "model", "accuracy.json")
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "cleaned_dataset.csv")

REPORTS_DIR = os.path.join(BASE_DIR, "reports")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads", "doctors")
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

# -----------------------------
# Load model safely
# -----------------------------
model = None
label_encoder = None

try:
    if os.path.exists(MODEL_PATH) and os.path.exists(ENCODER_PATH):
        model = joblib.load(MODEL_PATH)
        label_encoder = joblib.load(ENCODER_PATH)
        print("✅ Model loaded successfully")
    else:
        print("⚠️ Model files not found")
except Exception as e:
    print("⚠️ Model load failed:", e)
    model = None
    label_encoder = None

# -----------------------------
# DB helper
# -----------------------------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------
# CREATE TABLES IF NOT EXIST
# -----------------------------
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'patient'
        )
    """)

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

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
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

    cur.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT,
            patient_email TEXT,
            doctor_name TEXT,
            specialization TEXT,
            appointment_date TEXT,
            notes TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

# -----------------------------
# Helper
# -----------------------------
def normalize_disease_name(name):
    return str(name).strip().lower()

# -----------------------------
# Root
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "AI Doctor Recommendation Backend Running",
        "database_path": DB_PATH
    })

# -----------------------------
# Register
# -----------------------------
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json(force=True)

        name = data.get("name", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "").strip()

        if not name or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE LOWER(email)=?", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            conn.close()
            return jsonify({"error": "Email already exists"}), 400

        cur.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (name, email, password, "patient"))

        conn.commit()
        conn.close()

        return jsonify({"message": "Registration successful"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Login
# -----------------------------
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(force=True)

        email = data.get("email", "").strip().lower()
        password = data.get("password", "").strip()

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE LOWER(email)=?", (email,))
        user = cur.fetchone()
        conn.close()

        if not user:
            return jsonify({"error": "User not found. Please register first."}), 404

        if user["password"] != password:
            return jsonify({"error": "Incorrect password"}), 401

        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Get doctors
# -----------------------------
@app.route("/doctors", methods=["GET"])
def get_doctors():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM doctors ORDER BY id DESC")
        doctors = [dict(row) for row in cur.fetchall()]
        conn.close()
        return jsonify(doctors)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Add doctor
# -----------------------------
@app.route("/doctors", methods=["POST"])
def add_doctor():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    specialization = data.get("specialization", "").strip()
    photo = data.get("photo", "").strip()
    description = data.get("description", "").strip()
    experience = data.get("experience", "").strip()
    fees = data.get("fees", "").strip()
    hospital = data.get("hospital", "").strip()
    disease_key = data.get("disease_key", "").strip().lower()

    if not name or not specialization:
        return jsonify({"error": "Doctor name and specialization are required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO doctors (
                name, specialization, photo, description,
                experience, fees, hospital, disease_key
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, specialization, photo, description, experience, fees, hospital, disease_key))
        conn.commit()
        conn.close()

        return jsonify({"message": "Doctor added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Update doctor
# -----------------------------
@app.route("/doctors/<int:doctor_id>", methods=["PUT"])
def update_doctor(doctor_id):
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    specialization = data.get("specialization", "").strip()
    photo = data.get("photo", "").strip()
    description = data.get("description", "").strip()
    experience = data.get("experience", "").strip()
    fees = data.get("fees", "").strip()
    hospital = data.get("hospital", "").strip()
    disease_key = data.get("disease_key", "").strip().lower()

    if not name or not specialization:
        return jsonify({"error": "Doctor name and specialization are required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE doctors
            SET name=?, specialization=?, photo=?, description=?,
                experience=?, fees=?, hospital=?, disease_key=?
            WHERE id=?
        """, (name, specialization, photo, description, experience, fees, hospital, disease_key, doctor_id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Doctor updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Delete doctor
# -----------------------------
@app.route("/doctors/<int:doctor_id>", methods=["DELETE"])
def delete_doctor(doctor_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM doctors WHERE id=?", (doctor_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Doctor deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Accuracy
# -----------------------------
@app.route("/accuracy", methods=["GET"])
def get_accuracy():
    try:
        if os.path.exists(ACCURACY_PATH):
            with open(ACCURACY_PATH, "r") as f:
                data = json.load(f)
            return jsonify(data)
        return jsonify({"accuracy": 0})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Symptoms
# -----------------------------
@app.route("/symptoms", methods=["GET"])
def get_symptoms():
    if not os.path.exists(DATASET_PATH):
        return jsonify({"error": "Cleaned dataset not found"}), 404

    try:
        df = pd.read_csv(DATASET_PATH)
        columns = [col for col in df.columns if col.lower() != "prognosis"]
        return jsonify({"symptoms": columns})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Prediction
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():
    global model, label_encoder

    if model is None or label_encoder is None:
        return jsonify({"error": "Model not trained yet or sklearn version mismatch"}), 500

    data = request.get_json(silent=True) or {}
    patient_name = data.get("patient_name", "").strip()
    patient_email = data.get("patient_email", "").strip().lower()
    symptoms = data.get("symptoms", {})

    if not patient_name:
        return jsonify({"error": "Patient name is required"}), 400

    if not isinstance(symptoms, dict) or len(symptoms) == 0:
        return jsonify({"error": "Symptoms data is required"}), 400

    try:
        if not os.path.exists(DATASET_PATH):
            return jsonify({"error": "Cleaned dataset not found"}), 500

        dataset_df = pd.read_csv(DATASET_PATH)
        feature_columns = [col for col in dataset_df.columns if col.lower() != "prognosis"]

        normalized_input = {}
        selected_count = 0

        for col in feature_columns:
            value = int(symptoms.get(col, 0))
            value = 1 if value == 1 else 0
            normalized_input[col] = value
            if value == 1:
                selected_count += 1

        if selected_count == 0:
            return jsonify({"error": "Please select at least one symptom"}), 400

        input_df = pd.DataFrame([normalized_input])
        input_df = input_df[feature_columns]

        prediction_encoded = model.predict(input_df)[0]
        probabilities = model.predict_proba(input_df)[0]
        confidence = round(float(max(probabilities)) * 100, 2)

        predicted_disease = label_encoder.inverse_transform([prediction_encoded])[0]
        disease_key = normalize_disease_name(predicted_disease)

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM doctors
            WHERE LOWER(disease_key)=?
            ORDER BY id ASC
            LIMIT 1
        """, (disease_key,))
        doctor_row = cur.fetchone()

        if doctor_row:
            doctor_name = doctor_row["name"]
            specialization = doctor_row["specialization"]
            doctor_photo = doctor_row["photo"]
            doctor_experience = doctor_row["experience"]
            doctor_fees = doctor_row["fees"]
            doctor_hospital = doctor_row["hospital"]
            doctor_description = doctor_row["description"]
        else:
            specialization, doctor_name = doctor_mapping.get(
                disease_key,
                ("General Physician", "Dr. Neha Kapoor")
            )
            doctor_photo = ""
            doctor_experience = ""
            doctor_fees = ""
            doctor_hospital = ""
            doctor_description = ""

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("""
            INSERT INTO reports (
                patient_name, patient_email, symptoms, predicted_disease,
                predicted_doctor, specialization, confidence, created_at, pdf_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_name,
            patient_email,
            json.dumps(normalized_input),
            predicted_disease,
            doctor_name,
            specialization,
            confidence,
            created_at,
            ""
        ))
        report_id = cur.lastrowid
        conn.commit()
        conn.close()

        return jsonify({
            "report_id": report_id,
            "patient_name": patient_name,
            "patient_email": patient_email,
            "predicted_disease": predicted_disease,
            "doctor_name": doctor_name,
            "specialization": specialization,
            "confidence": confidence,
            "probabilities": probabilities.tolist(),
            "selected_symptoms_count": selected_count,
            "doctor_photo": doctor_photo,
            "doctor_experience": doctor_experience,
            "doctor_fees": doctor_fees,
            "doctor_hospital": doctor_hospital,
            "doctor_description": doctor_description
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Prediction history
# -----------------------------
@app.route("/history/<email>", methods=["GET"])
def prediction_history(email):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM reports
            WHERE LOWER(patient_email)=?
            ORDER BY id DESC
        """, (email.strip().lower(),))
        reports = [dict(row) for row in cur.fetchall()]
        conn.close()
        return jsonify(reports)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Reports list
# -----------------------------
@app.route("/reports", methods=["GET"])
def get_reports():
    search = request.args.get("search", "").strip().lower()

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        if search:
            cur.execute("""
                SELECT * FROM reports
                WHERE LOWER(patient_name) LIKE ? 
                   OR LOWER(predicted_doctor) LIKE ?
                   OR LOWER(predicted_disease) LIKE ?
                   OR LOWER(specialization) LIKE ?
                ORDER BY id DESC
            """, (f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"))
        else:
            cur.execute("SELECT * FROM reports ORDER BY id DESC")

        reports = [dict(row) for row in cur.fetchall()]
        conn.close()
        return jsonify(reports)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Delete report
# -----------------------------
@app.route("/reports/<int:report_id>", methods=["DELETE"])
def delete_report(report_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT pdf_path FROM reports WHERE id=?", (report_id,))
        row = cur.fetchone()

        if row and row["pdf_path"] and os.path.exists(row["pdf_path"]):
            try:
                os.remove(row["pdf_path"])
            except:
                pass

        cur.execute("DELETE FROM reports WHERE id=?", (report_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Report deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Generate PDF
# -----------------------------
@app.route("/generate-pdf/<int:report_id>", methods=["GET"])
def generate_report_pdf(report_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM reports WHERE id=?", (report_id,))
        report = cur.fetchone()

        if not report:
            conn.close()
            return jsonify({"error": "Report not found"}), 404

        report = dict(report)
        pdf_path = os.path.join(REPORTS_DIR, f"report_{report_id}.pdf")

        try:
            symptoms_json = json.loads(report["symptoms"]) if report["symptoms"] else {}
            selected_symptoms = [k.replace("_", " ") for k, v in symptoms_json.items() if int(v) == 1]
            symptoms_text = ", ".join(selected_symptoms[:15]) if selected_symptoms else "N/A"
        except:
            symptoms_text = str(report["symptoms"])

        report_data = {
            "date": report["created_at"],
            "patient_name": report["patient_name"],
            "symptoms": symptoms_text,
            "doctor_name": report["predicted_doctor"],
            "specialization": report["specialization"],
            "predicted_disease": report["predicted_disease"],
            "confidence": report["confidence"]
        }

        logo_path = os.path.join(STATIC_DIR, "logo.png") if os.path.exists(os.path.join(STATIC_DIR, "logo.png")) else None

        generate_pdf(report_data, pdf_path, logo_path=logo_path)

        cur.execute("UPDATE reports SET pdf_path=? WHERE id=?", (pdf_path, report_id))
        conn.commit()
        conn.close()

        return send_file(pdf_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Export Excel
# -----------------------------
@app.route("/export-excel", methods=["GET"])
def export_excel():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM reports ORDER BY id DESC")
        reports = [dict(row) for row in cur.fetchall()]
        conn.close()

        file_path = os.path.join(REPORTS_DIR, "all_reports.xlsx")
        export_reports_to_excel(reports, file_path)

        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Appointments - Create
# -----------------------------
@app.route("/appointments", methods=["POST"])
def create_appointment():
    try:
        data = request.get_json(force=True)

        patient_name = data.get("patient_name", "").strip()
        patient_email = data.get("patient_email", "").strip().lower()
        doctor_name = data.get("doctor_name", "").strip()
        specialization = data.get("specialization", "").strip()
        appointment_date = data.get("appointment_date", "").strip()
        notes = data.get("notes", "").strip()

        if not patient_name or not patient_email or not doctor_name or not specialization or not appointment_date:
            return jsonify({"error": "All appointment fields are required"}), 400

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO appointments (
                patient_name, patient_email, doctor_name,
                specialization, appointment_date, notes, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_name,
            patient_email,
            doctor_name,
            specialization,
            appointment_date,
            notes,
            "Pending",
            created_at
        ))
        conn.commit()
        conn.close()

        return jsonify({"message": "Appointment request submitted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Appointments - Get all / by email
# -----------------------------
@app.route("/appointments", methods=["GET"])
def get_appointments():
    try:
        email = request.args.get("email", "").strip().lower()

        conn = get_db_connection()
        cur = conn.cursor()

        if email:
            cur.execute("""
                SELECT * FROM appointments
                WHERE LOWER(patient_email)=?
                ORDER BY id DESC
            """, (email,))
        else:
            cur.execute("SELECT * FROM appointments ORDER BY id DESC")

        appointments = [dict(row) for row in cur.fetchall()]
        conn.close()

        return jsonify(appointments)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Appointments - Update status
# -----------------------------
@app.route("/appointments/<int:appointment_id>", methods=["PUT"])
def update_appointment_status(appointment_id):
    try:
        data = request.get_json(force=True)
        status = data.get("status", "").strip()

        if status not in ["Pending", "Approved", "Rejected"]:
            return jsonify({"error": "Invalid status"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE appointments
            SET status=?
            WHERE id=?
        """, (status, appointment_id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Appointment status updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Dashboard analytics
# -----------------------------
@app.route("/dashboard-stats", methods=["GET"])
def dashboard_stats():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM users WHERE role='patient'")
        total_patients = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM reports")
        total_reports = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM doctors")
        total_doctors = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM appointments")
        total_appointments = cur.fetchone()[0]

        cur.execute("""
            SELECT substr(created_at, 1, 7) as month, COUNT(*) as count
            FROM reports
            GROUP BY month
            ORDER BY month
        """)
        monthly_data = [{"month": row[0], "count": row[1]} for row in cur.fetchall()]

        conn.close()

        return jsonify({
            "total_patients": total_patients,
            "total_reports": total_reports,
            "total_doctors": total_doctors,
            "total_appointments": total_appointments,
            "monthly_data": monthly_data
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# Serve doctor uploaded images
# -----------------------------
@app.route("/uploads/doctors/<filename>")
def uploaded_doctor_file(filename):
    return send_from_directory(UPLOADS_DIR, filename)

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    init_db()
    print("🚀 Backend starting...")
    print("📂 Using DB:", DB_PATH)
    app.run(debug=True)