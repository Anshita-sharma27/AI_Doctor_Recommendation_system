import React from "react";

function Navbar({ title, subtitle }) {
  return (
    <div className="navbar-premium mb-4">
      <div>
        <h2 className="mb-1">{title}</h2>
        <p className="text-muted mb-0">{subtitle}</p>
      </div>
    </div>
  );
}

export default Navbar;