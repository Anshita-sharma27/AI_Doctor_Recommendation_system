import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import API from "../api";

function HistoryPage() {
  const [reports, setReports] = useState([]);
  const user = JSON.parse(localStorage.getItem("user"));

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    const res = await API.get("/reports");
    setReports(res.data.filter(r => r.patient_name === user.name));
  };

  return (
    <div className="dashboard-layout">
      <Sidebar role="patient" />
      <div className="main-content">
        <Navbar title="Prediction History" />

        <div className="row">
          {reports.map(r => (
            <div className="col-md-4" key={r.id}>
              <div className="dashboard-card">
                <h5>{r.predicted_disease}</h5>
                <p>{r.predicted_doctor}</p>
                <p>{r.confidence}%</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default HistoryPage;