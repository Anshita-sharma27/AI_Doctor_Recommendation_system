import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";

function DoctorsPage() {
  const [doctors, setDoctors] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/doctors")
      .then((res) => res.json())
      .then((data) => setDoctors(data || []))
      .catch(() => {});
  }, []);

  return (
    <div className="dashboard-layout">
      <Sidebar />

      <div className="dashboard-content">
        <div className="page-header">
          <h1>Doctors</h1>
          <p>Available specialist doctors in the system.</p>
        </div>

        <div className="doctor-grid">
          {doctors.length > 0 ? (
            doctors.map((doctor) => (
              <div className="doctor-card" key={doctor.id}>
                <h3>{doctor.name}</h3>
                <p><strong>Specialization:</strong> {doctor.specialization}</p>
                <p><strong>Hospital:</strong> {doctor.hospital || "N/A"}</p>
                <p><strong>Experience:</strong> {doctor.experience || "N/A"}</p>
                <p><strong>Fees:</strong> {doctor.fees || "N/A"}</p>
                <p>{doctor.description || "No description available."}</p>
              </div>
            ))
          ) : (
            <div className="page-card">
              <p>No doctors found.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default DoctorsPage;