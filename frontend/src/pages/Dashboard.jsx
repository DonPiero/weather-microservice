import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";
import { useState } from "react";

export default function Dashboard({ user, setUser }) {
  const [city, setCity] = useState("");
  const [weather, setWeather] = useState(null);
  const [history, setHistory] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [selectedMetric, setSelectedMetric] = useState("temperature");

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem("user");
  };

  const handleLiveWeather = async () => {
    if (!city.trim()) {
      setError("Please enter a city name.");
      return;
    }
    setError("");
    setLoading(true);
    setWeather(null);
    setHistory(null);

    try {
      const response = await fetch("http://localhost:8000/weather/live", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${user.token}`,
        },
        body: JSON.stringify({ city_name: city }),
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || "Failed to fetch weather.");
      }

      const data = await response.json();
      setWeather(data);
    } catch (err) {
      console.error(err);
      setError("Unable to fetch live weather. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleHistoryWeather = async (start, end) => {
      if (!city.trim()) {
        setError("Please enter a city name.");
        return;
      }
      setError("");
      setLoading(true);
      setWeather(null);
      setHistory(null);

      try {
        const response = await fetch("http://localhost:8000/weather/history", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${user.token}`,
          },
          body: JSON.stringify({
            city_name: city,
            start_time: start,
            end_time: end,
          }),
        });

        if (!response.ok) {
          const text = await response.text();
          throw new Error(text || "Failed to fetch history.");
        }

        const data = await response.json();
        setHistory(data);
      } catch (err) {
        console.error(err);
        setError("Unable to fetch weather history. Please try again.");
      } finally {
        setLoading(false);
      }
    };

  return (
    <div className="app-container">
      <div className="card">
        <h1 className="center">Welcome to Weather Microservice</h1>

        <div
          className="actions"
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr 0.7fr",
            gap: "10px",
          }}
        >
          <input
            className="input"
            type="text"
            placeholder="What city are you interested in?"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            style={{
              gridColumn: "1 / span 3",
            }}
          />

          <button
            className="btn btn-primary"
            disabled={loading}
            onClick={handleLiveWeather}
          >
            Get Live Weather
          </button>
          <button
              className="btn btn-primary"
              disabled={loading}
              onClick={() => setShowDatePicker(true)}
          >
              Get Weather History
          </button>
          <button
            className="btn btn-danger"
            disabled={loading}
            onClick={handleLogout}
          >
            Logout
          </button>
        </div>

        {error && <p className="status error">{error}</p>}

        {weather && (
          <div className="weather-result center">
            <h1>{weather.city_name.charAt(0).toUpperCase() + weather.city_name.slice(1)}</h1>
            <div className="weather-details">
              <p><strong>Temperature:</strong> {weather.temperature} °C</p>
              <p><strong>Humidity:</strong> {weather.humidity}%</p>
              <p><strong>Conditions:</strong> {weather.weather_description}</p>
              {weather.wind_speed !== undefined && (
                <p><strong>Wind Speed:</strong> {weather.wind_speed} m/s</p>
              )}
              <p><strong>Recorded at:</strong> {new Date(weather.timestamp).toLocaleString()}</p>
            </div>
          </div>
        )}

        {showDatePicker && (
          <div className="modal-overlay">
            <div className="modal">
              <h2>Select Date Range</h2>

              <label>Start Date:</label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />

              <label>End Date:</label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />

              <div className="modal-actions">
                <button
                  className="btn btn-primary"
                  onClick={() => {
                    if (!startDate || !endDate) {
                      alert("Please select both dates!");
                      return;
                    }
                    setShowDatePicker(false);
                    handleHistoryWeather(startDate, endDate);
                  }}
                >
                  Confirm
                </button>
                <button className="btn btn-danger" onClick={() => setShowDatePicker(false)}>
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}

        {history && (
          <div className="weather-charts center">
            <div className="chart-header">
              <select
                id="metric-select"
                className="input"
                style={{ width: "200px", marginLeft: "10px" }}
                value={selectedMetric}
                onChange={(e) => setSelectedMetric(e.target.value)}
              >
                <option value="temperature">Temperature (°C)</option>
                <option value="humidity">Humidity (%)</option>
                <option value="wind_speed">Wind Speed (m/s)</option>
              </select>
            </div>

            <ResponsiveContainer width="90%" height={200}>
              <LineChart data={history.readings}>
                <CartesianGrid stroke="#ccc" />
                <XAxis
                  dataKey="timestamp"
                  tickFormatter={(t) =>
                    new Date(t).toLocaleDateString([], { month: "short", day: "numeric" })
                  }
                />
                <YAxis />
                <Tooltip
                  labelFormatter={(t) => new Date(t).toLocaleString()}
                  formatter={(value) =>
                    selectedMetric === "temperature"
                      ? [`${value} °C`, "Temperature"]
                      : selectedMetric === "humidity"
                      ? [`${value}%`, "Humidity"]
                      : [`${value} m/s`, "Wind Speed"]
                  }
                />
                <Line
                  type="monotone"
                  dataKey={selectedMetric}
                  stroke={
                    selectedMetric === "temperature"
                      ? "royalblue"
                      : selectedMetric === "humidity"
                      ? "green"
                      : "crimson"
                  }
                  strokeWidth={2}
                  dot={{ r: 3 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  );
}
