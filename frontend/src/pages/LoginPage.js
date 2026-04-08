import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function LoginPage() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
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

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("user", JSON.stringify(data.user));
        setMessage("✅ Login successful");

        setTimeout(() => {
          navigate("/dashboard");
        }, 800);
      } else {
        setMessage("❌ " + (data.error || "Login failed"));
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
            Smart disease prediction, doctor recommendation, reports,
            and appointment booking — all in one healthcare dashboard.
          </p>
        </div>
      </div>

      <div className="auth-right">
        <div className="auth-card">
          <h2>Welcome Back 👋</h2>
          <p className="sub-text">Login to continue</p>

          {message && <div className="auth-message">{message}</div>}

          <form onSubmit={handleLogin}>
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
              {loading ? "Logging in..." : "Login"}
            </button>
          </form>

          <p className="bottom-text">
            Don’t have an account? <Link to="/register">Register Now</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;