import React from "react";
import { Link } from "react-router-dom";

export default function HomePage() {
  const user = JSON.parse(localStorage.getItem("user"));

  return (
    <div className="dashboard-page">
      <div className="dashboard-card">
        <h1>Welcome, {user?.name || "Patient"} 👨‍⚕️</h1>
        <p>Your AI healthcare assistant dashboard</p>

        <div className="home-actions">
          <Link to="/predict" className="action-btn">Start Prediction</Link>
          <Link to="/history" className="action-btn">Prediction History</Link>
          <Link to="/appointments" className="action-btn">Appointments</Link>
        </div>
      </div>
    </div>
  );
}