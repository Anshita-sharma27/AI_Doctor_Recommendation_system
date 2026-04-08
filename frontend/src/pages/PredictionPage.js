import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";

function PredictionPage() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user"));

  const [symptomsList, setSymptomsList] = useState([]);
  const [selectedSymptoms, setSelectedSymptoms] = useState({});
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:5000/symptoms")
      .then((res) => res.json())
      .then((data) => {
        if (data.symptoms) setSymptomsList(data.symptoms);
      })
      .catch(() => setMessage("❌ Failed to load symptoms"));
  }, []);

  const handleCheckbox = (symptom) => {
    setSelectedSymptoms((prev) => ({
      ...prev,
      [symptom]: prev[symptom] ? 0 : 1,
    }));
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          patient_name: user?.name || "Patient",
          patient_email: user?.email || "",
          symptoms: selectedSymptoms,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("predictionResult", JSON.stringify(data));
        navigate("/result");
      } else {
        setMessage("❌ " + (data.error || "Prediction failed"));
      }
    } catch (error) {
      setMessage("❌ Backend not connected");
    }

    setLoading(false);
  };

  return (
    <div className="dashboard-layout">
      <Sidebar />

      <div className="dashboard-content">
        <div className="page-header">
          <h1>Symptom Prediction</h1>
          <p>Select symptoms and get doctor recommendation instantly.</p>
        </div>

        {message && <div className="auth-message">{message}</div>}

        <div className="page-card">
          <form onSubmit={handlePredict}>
            <div className="symptoms-grid">
              {symptomsList.map((symptom, index) => (
                <label className="symptom-item" key={index}>
                  <input
                    type="checkbox"
                    checked={selectedSymptoms[symptom] === 1}
                    onChange={() => handleCheckbox(symptom)}
                  />
                  <span>{symptom.replaceAll("_", " ")}</span>
                </label>
              ))}
            </div>

            <button className="primary-btn" type="submit" disabled={loading}>
              {loading ? "Predicting..." : "Predict Now"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default PredictionPage;