import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function RegisterPage() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("✅ Registration successful");
        setTimeout(() => {
          navigate("/login");
        }, 1200);
      } else {
        setMessage("❌ " + (data.error || "Registration failed"));
      }
    } catch (error) {
      setMessage("❌ Backend not connected");
    }

    setLoading(false);
  };

  return (
    <div className="auth-page">
      <div className="auth-left">
        <div className="auth-left-content">
          <h1>AI Doctor Recommendation</h1>
          <p>
            Create your healthcare account and access smart prediction,
            doctor suggestions, reports, and appointments.
          </p>
        </div>
      </div>

      <div className="auth-right">
        <div className="auth-card">
          <h2>Create Account ✨</h2>
          <p className="sub-text">Register to continue</p>

          {message && <div className="auth-message">{message}</div>}

          <form onSubmit={handleRegister}>
            <label>Full Name</label>
            <input
              type="text"
              name="name"
              placeholder="Anshita Sharma"
              value={formData.name}
              onChange={handleChange}
              required
            />

            <label>Email</label>
            <input
              type="email"
              name="email"
              placeholder="anshita@gmail.com"
              value={formData.email}
              onChange={handleChange}
              required
            />

            <label>Password</label>
            <input
              type="password"
              name="password"
              placeholder="••••••"
              value={formData.password}
              onChange={handleChange}
              required
            />

            <button type="submit" disabled={loading}>
              {loading ? "Creating..." : "Register"}
            </button>
          </form>

          <p className="bottom-text">
            Already have an account? <Link to="/login">Login Now</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default RegisterPage;