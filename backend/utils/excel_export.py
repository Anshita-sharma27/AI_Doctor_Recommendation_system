import pandas as pd

def export_reports_to_excel(reports, file_path):
    if not reports:
        df = pd.DataFrame(columns=[
            "id", "patient_name", "patient_email", "predicted_disease",
            "predicted_doctor", "specialization", "confidence", "created_at"
        ])
    else:
        df = pd.DataFrame(reports)

    df.to_excel(file_path, index=False)