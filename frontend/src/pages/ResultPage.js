import React from "react";
import Sidebar from "../components/Sidebar";

function ResultPage() {
  const result = JSON.parse(localStorage.getItem("predictionResult"));

  if (!result) {
    return (
      <div className="dashboard-layout">
        <Sidebar />
        <div className="dashboard-content">
          <div className="page-card">
            <h2>No prediction result found.</h2>
            <p>Please go to Prediction page first.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-layout">
      <Sidebar />

      <div className="dashboard-content">
        <div className="page-header">
          <h1>Prediction Result</h1>
          <p>Your AI disease prediction and doctor recommendation.</p>
        </div>

        <div className="result-grid">
          <div className="result-card">
            <h3>Predicted Disease</h3>
            <p>{result.predicted_disease}</p>
          </div>

          <div className="result-card">
            <h3>Recommended Doctor</h3>
            <p>{result.doctor_name}</p>
          </div>

          <div className="result-card">
            <h3>Specialization</h3>
            <p>{result.specialization}</p>
          </div>

          <div className="result-card">
            <h3>Confidence</h3>
            <p>{result.confidence}%</p>
          </div>

          <div className="result-card">
            <h3>Hospital</h3>
            <p>{result.doctor_hospital || "N/A"}</p>
          </div>

          <div className="result-card">
            <h3>Experience</h3>
            <p>{result.doctor_experience || "N/A"}</p>
          </div>
        </div>

        <div className="page-card">
          <h3>Doctor Description</h3>
          <p>{result.doctor_description || "No doctor description available."}</p>
        </div>
      </div>
    </div>
  );
}

export default ResultPage;