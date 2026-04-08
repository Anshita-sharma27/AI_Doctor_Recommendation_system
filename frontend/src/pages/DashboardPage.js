import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";

function DashboardPage() {
  const user = JSON.parse(localStorage.getItem("user"));
  const [stats, setStats] = useState({
    total_patients: 0,
    total_reports: 0,
    total_doctors: 0,
    total_appointments: 0,
  });

  useEffect(() => {
    fetch("http://127.0.0.1:5000/dashboard-stats")
      .then((res) => res.json())
      .then((data) => {
        setStats(data);
      })
      .catch(() => {});
  }, []);

  return (
    <div className="dashboard-layout">
      <Sidebar />

      <div className="dashboard-content">
        <div className="top-header">
          <div>
            <h1>Welcome, {user?.name || "User"} 👋</h1>
            <p>Here’s your AI healthcare dashboard overview.</p>
          </div>
        </div>

        <div className="stats-grid">
          <div className="stat-box">
            <h4>Total Patients</h4>
            <h2>{stats.total_patients || 0}</h2>
          </div>
          <div className="stat-box">
            <h4>Total Reports</h4>
            <h2>{stats.total_reports || 0}</h2>
          </div>
          <div className="stat-box">
            <h4>Total Doctors</h4>
            <h2>{stats.total_doctors || 0}</h2>
          </div>
          <div className="stat-box">
            <h4>Appointments</h4>
            <h2>{stats.total_appointments || 0}</h2>
          </div>
        </div>

        <div className="dashboard-grid">
          <div className="dashboard-card big-card">
            <h3>Smart AI Prediction</h3>
            <p>
              Predict diseases using symptoms and get doctor recommendations
              instantly with confidence score.
            </p>
          </div>

          <div className="dashboard-card">
            <h3>User Profile</h3>
            <p><strong>Name:</strong> {user?.name || "N/A"}</p>
            <p><strong>Email:</strong> {user?.email || "N/A"}</p>
            <p><strong>Role:</strong> {user?.role || "patient"}</p>
          </div>

          <div className="dashboard-card">
            <h3>Appointments</h3>
            <p>Book appointments with specialist doctors easily.</p>
          </div>

          <div className="dashboard-card">
            <h3>Reports</h3>
            <p>Download PDF reports and view prediction history.</p>
          </div>

          <div className="dashboard-card">
            <h3>Doctors</h3>
            <p>Find recommended doctors based on your predicted disease.</p>
          </div>

          <div className="dashboard-card">
            <h3>System Status</h3>
            <p>Frontend and backend are connected successfully.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;