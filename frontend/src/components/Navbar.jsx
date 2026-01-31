import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import React from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
    const { logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    return (
        <div className="flex gap-4 items-center">
            <Link to="/dashboard" className="text-sm">
                Dashboard
            </Link>
            <Link to="/schedule" className="text-sm">
                Schedule
            </Link>
            <button
                onClick={handleLogout}
                className="text-sm bg-red-500 text-white px-3 py-1 rounded"
            >
                Logout
            </button>
        </div>

    );
}
