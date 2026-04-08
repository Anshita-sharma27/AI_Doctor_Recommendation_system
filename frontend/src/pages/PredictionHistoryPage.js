import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";

function PredictionHistoryPage() {
  const user = JSON.parse(localStorage.getItem("user"));
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/history/${user?.email}`)
      .then((res) => res.json())
      .then((data) => setHistory(data || []))
      .catch(() => {});
  }, [user]);

  return (
    <div className="dashboard-layout">
      <Sidebar />

      <div className="dashboard-content">
        <div className="page-header">
          <h1>Prediction History</h1>
          <p>Your previous prediction reports are listed below.</p>
        </div>

        <div className="table-card">
          <table>
            <thead>
              <tr>
                <th>Patient</th>
                <th>Disease</th>
                <th>Doctor</th>
                <th>Specialization</th>
                <th>Confidence</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {history.length > 0 ? (
                history.map((item) => (
                  <tr key={item.id}>
                    <td>{item.patient_name}</td>
                    <td>{item.predicted_disease}</td>
                    <td>{item.predicted_doctor}</td>
                    <td>{item.specialization}</td>
                    <td>{item.confidence}%</td>
                    <td>{item.created_at}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="6">No prediction history found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default PredictionHistoryPage;