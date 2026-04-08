import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import DashboardPage from "./pages/DashboardPage";
import PredictionPage from "./pages/PredictionPage";
import ResultPage from "./pages/ResultPage";
import PredictionHistoryPage from "./pages/PredictionHistoryPage";
import AppointmentPage from "./pages/AppointmentPage";
import DoctorsPage from "./pages/DoctorsPage";
import ReportsPage from "./pages/ReportsPage";

import "./index.css";

function App() {
  const user = JSON.parse(localStorage.getItem("user"));

  return (
    <Router>
      <Routes>
        <Route path="/" element={user ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/prediction" element={<PredictionPage />} />
        <Route path="/result" element={<ResultPage />} />
        <Route path="/history" element={<PredictionHistoryPage />} />
        <Route path="/appointments" element={<AppointmentPage />} />
        <Route path="/doctors" element={<DoctorsPage />} />
        <Route path="/reports" element={<ReportsPage />} />
      </Routes>
    </Router>
  );
}

export default App;