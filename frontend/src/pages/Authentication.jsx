import { useState } from "react";

export default function Authentication({ setUser }) {
  const [mode, setMode] = useState("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const toggleMode = () => {
    setMode(mode === "login" ? "register" : "login");
    setError("");
    setEmail("");
    setPassword("");
    setConfirmPassword("");
  };

  async function handleSubmit(e) {
      e.preventDefault();
      setError("");
      setLoading(true);

      try {
        const endpoint =
          mode === "login"
            ? "http://localhost:8000/auth/login"
            : "http://localhost:8000/auth/register";

        if (mode === "register" && password !== confirmPassword) {
          setError("Passwords do not match.");
          setLoading(false);
          return;
        }

        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
          switch (response.status) {
            case 401:
              setError("Invalid credentials. Please try again.");
              break;
            case 409:
              setError("An account with this email already exists.");
              break;
            default:
              setError("Server error. Please try again later.");
          }
          setLoading(false);
          return;
        }

        const data = await response.json();

        const userData = { token: data.access_token };
        setUser(userData);
        localStorage.setItem("user", JSON.stringify(userData));
      } catch (err) {
        console.error(err);
        setError("Network error. Check your connection and try again.");
      } finally {
        setLoading(false);
      }
    }

  return (
    <div className="app-container">
      <div className="card">
        <h1 className="center">
          {mode === "login" ? "Connect to your account" : "Create an account"}
        </h1>

        <form className="form" onSubmit={handleSubmit}>
          <input
            className="input"
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            className="input"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {mode === "register" && (
            <input
              className="input"
              type="password"
              placeholder="Confirm Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          )}

          {error && (
            <p
              className={`status ${
                error.startsWith("Registration successful") ? "ok" : "error"
              }`}
            >
              {error}
            </p>
          )}

          <button className="btn btn-primary" type="submit" disabled={loading}>
            {loading
              ? "Processing..."
              : mode === "login"
              ? "Login"
              : "Register"}
          </button>
        </form>

        <p className="center muted bigger">
          {mode === "login" ? (
            <>
              Don’t have an account?{" "}
              <button className="btn btn-transparent" type="button" onClick={toggleMode}>
                Register
              </button>
            </>
          ) : (
            <>
              Already have an account?{" "}
              <button className="btn btn-transparent" type="button" onClick={toggleMode}>
                Login
              </button>
            </>
          )}
        </p>
      </div>
    </div>
  );
}
