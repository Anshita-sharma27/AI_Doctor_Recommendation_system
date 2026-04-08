import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";

function AppointmentPage() {
  const user = JSON.parse(localStorage.getItem("user"));

  const [formData, setFormData] = useState({
    doctor_name: "",
    specialization: "",
    appointment_date: "",
    notes: "",
  });

  const [appointments, setAppointments] = useState([]);
  const [message, setMessage] = useState("");

  const loadAppointments = () => {
    fetch(`http://127.0.0.1:5000/appointments?email=${user?.email}`)
      .then((res) => res.json())
      .then((data) => setAppointments(data || []))
      .catch(() => {});
  };

  useEffect(() => {
    loadAppointments();
  }, []);

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleBook = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:5000/appointments", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          patient_name: user?.name,
          patient_email: user?.email,
          ...formData,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("✅ Appointment booked successfully");
        setFormData({
          doctor_name: "",
          specialization: "",
          appointment_date: "",
          notes: "",
        });
        loadAppointments();
      } else {
        setMessage("❌ " + (data.error || "Booking failed"));
      }
    } catch {
      setMessage("❌ Backend not connected");
    }
  };

  return (
    <div className="dashboard-layout">
      <Sidebar />

      <div className="dashboard-content">
        <div className="page-header">
          <h1>Appointments</h1>
          <p>Book and manage your doctor appointments.</p>
        </div>

        {message && <div className="auth-message">{message}</div>}

        <div className="page-card">
          <form className="form-grid" onSubmit={handleBook}>
            <input type="text" name="doctor_name" placeholder="Doctor Name" value={formData.doctor_name} onChange={handleChange} required />
            <input type="text" name="specialization" placeholder="Specialization" value={formData.specialization} onChange={handleChange} required />
            <input type="date" name="appointment_date" value={formData.appointment_date} onChange={handleChange} required />
            <textarea name="notes" placeholder="Notes" value={formData.notes} onChange={handleChange}></textarea>
            <button className="primary-btn" type="submit">Book Appointment</button>
          </form>
        </div>

        <div className="table-card">
          <table>
            <thead>
              <tr>
                <th>Doctor</th>
                <th>Specialization</th>
                <th>Date</th>
                <th>Status</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              {appointments.length > 0 ? (
                appointments.map((item) => (
                  <tr key={item.id}>
                    <td>{item.doctor_name}</td>
                    <td>{item.specialization}</td>
                    <td>{item.appointment_date}</td>
                    <td>{item.status}</td>
                    <td>{item.notes || "-"}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5">No appointments found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default AppointmentPage;