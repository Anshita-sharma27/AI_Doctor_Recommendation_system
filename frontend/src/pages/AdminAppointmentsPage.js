import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import API from "../api";

function AdminAppointmentsPage() {
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    try {
      const res = await API.get("/appointments");
      setAppointments(res.data || []);
    } catch (error) {
      alert("Failed to load appointments");
    }
  };

  const updateStatus = async (id, status) => {
    try {
      await API.put(`/appointments/${id}`, { status });
      fetchAppointments();
    } catch (error) {
      alert("Status update failed");
    }
  };

  return (
    <div className="dashboard-layout">
      <Sidebar role="admin" />

      <div className="main-content">
        <Navbar
          title="Appointment Requests"
          subtitle="Manage patient appointment bookings"
        />

        <div className="dashboard-card">
          <div className="table-responsive">
            <table className="table align-middle">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Patient</th>
                  <th>Email</th>
                  <th>Doctor</th>
                  <th>Specialization</th>
                  <th>Date</th>
                  <th>Status</th>
                  <th>Notes</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {appointments.map((item, index) => (
                  <tr key={item.id}>
                    <td>{index + 1}</td>
                    <td>{item.patient_name}</td>
                    <td>{item.patient_email}</td>
                    <td>{item.doctor_name}</td>
                    <td>{item.specialization}</td>
                    <td>{item.appointment_date}</td>
                    <td>
                      <span
                        className={`badge ${
                          item.status === "Approved"
                            ? "bg-success"
                            : item.status === "Rejected"
                            ? "bg-danger"
                            : "bg-warning text-dark"
                        }`}
                      >
                        {item.status}
                      </span>
                    </td>
                    <td>{item.notes || "-"}</td>
                    <td>
                      <div className="d-flex gap-2 flex-wrap">
                        <button
                          className="btn btn-sm btn-success"
                          onClick={() => updateStatus(item.id, "Approved")}
                        >
                          Approve
                        </button>
                        <button
                          className="btn btn-sm btn-danger"
                          onClick={() => updateStatus(item.id, "Rejected")}
                        >
                          Reject
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {appointments.length === 0 && (
              <div className="text-center py-5">
                <h4>No appointment requests found</h4>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdminAppointmentsPage;