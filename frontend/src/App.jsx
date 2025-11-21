import { useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Authentication from "./pages/Authentication.jsx";
import Dashboard from "./pages/Dashboard.jsx";

export default function App() {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("user");
    return saved ? JSON.parse(saved) : null;
  });

  return (
    <Routes>
        <Route path="/" element={
          user ? <Navigate to="/dashboard" /> : <Navigate to="/authentication" />
        }/>
      <Route path="/authentication" element={user ? <Navigate to="/dashboard" /> : <Authentication setUser={setUser} />} />
      <Route path="/dashboard" element={ user ? <Dashboard user={user} setUser={setUser} /> : <Navigate to="/authentication" />}/>
    </Routes>
  );
}
