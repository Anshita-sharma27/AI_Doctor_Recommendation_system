import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";

function ReportsPage() {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/reports")
      .then((res) => res.json())
      .then((data) => setReports(data || []))
      .catch(() => {});
  }, []);

  const handleDownloadPdf = (id) => {
    window.open(`http://127.0.0.1:5000/generate-pdf/${id}`, "_blank");
  };

  const handleExportExcel = () => {
    window.open("http://127.0.0.1:5000/export-excel", "_blank");
  };

  return (
    <div className="dashboard-layout">
      <Sidebar />

      <div className="dashboard-content">
        <div className="page-header reports-header">
          <div>
            <h1>Reports</h1>
            <p>Download PDF reports and export all records to Excel.</p>
          </div>

          <button className="primary-btn" onClick={handleExportExcel}>
            Export Excel
          </button>
        </div>

        <div className="table-card">
          <table>
            <thead>
              <tr>
                <th>Patient</th>
                <th>Disease</th>
                <th>Doctor</th>
                <th>Confidence</th>
                <th>Date</th>
                <th>PDF</th>
              </tr>
            </thead>
            <tbody>
              {reports.length > 0 ? (
                reports.map((item) => (
                  <tr key={item.id}>
                    <td>{item.patient_name}</td>
                    <td>{item.predicted_disease}</td>
                    <td>{item.predicted_doctor}</td>
                    <td>{item.confidence}%</td>
                    <td>{item.created_at}</td>
                    <td>
                      <button className="small-btn" onClick={() => handleDownloadPdf(item.id)}>
                        Download
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="6">No reports found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default ReportsPage;