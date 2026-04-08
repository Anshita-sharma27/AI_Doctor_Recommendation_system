import React, { useEffect, useState } from "react";
import axios from "axios";
import API_BASE from "../api";

export default function AdminDashboard() {
  const [stats, setStats] = useState({
    total_patients: 0,
    total_reports: 0,
    total_doctors: 0,
    total_appointments: 0
  });

  useEffect(() => {
    axios.get(`${API_BASE}/dashboard-stats`)
      .then((res) => setStats(res.data))
      .catch(() => alert("Failed to load dashboard stats"));
  }, []);

  return (
    <div className="dashboard-page">
      <div className="dashboard-card">
        <h1>Admin Dashboard</h1>

        <div className="stats-grid">
          <div className="stat-box">Patients: {stats.total_patients}</div>
          <div className="stat-box">Reports: {stats.total_reports}</div>
          <div className="stat-box">Doctors: {stats.total_doctors}</div>
          <div className="stat-box">Appointments: {stats.total_appointments}</div>
        </div>
      </div>
    </div>
  );
}