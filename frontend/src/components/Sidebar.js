import React from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";

function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("predictionResult");
    navigate("/login");
  };

  const isActive = (path) => location.pathname === path;

  return (
    <div className="sidebar">
      <div>
        <h2 className="logo">AI Doctor</h2>

        <div className="sidebar-links">
          <Link className={isActive("/dashboard") ? "active-link" : ""} to="/dashboard">🏠 Dashboard</Link>
          <Link className={isActive("/prediction") ? "active-link" : ""} to="/prediction">🩺 Prediction</Link>
          <Link className={isActive("/result") ? "active-link" : ""} to="/result">📋 Result</Link>
          <Link className={isActive("/history") ? "active-link" : ""} to="/history">🕘 History</Link>
          <Link className={isActive("/appointments") ? "active-link" : ""} to="/appointments">📅 Appointments</Link>
          <Link className={isActive("/doctors") ? "active-link" : ""} to="/doctors">👨‍⚕️ Doctors</Link>
          <Link className={isActive("/reports") ? "active-link" : ""} to="/reports">📊 Reports</Link>
        </div>
      </div>

      <button className="logout-btn" onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
}

export default Sidebar;