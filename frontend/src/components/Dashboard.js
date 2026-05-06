import { useState, useEffect } from "react";
import { getPrediction, getInsights } from "../api";
import Charts from "./Charts";

function Dashboard() {
  const [data, setData] = useState([]);
  const [insights, setInsights] = useState(null);
  const [loadingInsights, setLoadingInsights] = useState(false);
  const [loadingForecast, setLoadingForecast] = useState(false);
  const [days, setDays] = useState(7);

  const fetchPrediction = async (predictionDays = days) => {
    try {
      setLoadingForecast(true);
      const res = await getPrediction(predictionDays);
      const responseData = res.data.data;

      if (!Array.isArray(responseData) || responseData.length === 0) {
        alert("No forecast data available");
        return;
      }

      setData(responseData);
    } catch (err) {
      console.error(err);
      alert("❌ Error fetching prediction");
    } finally {
      setLoadingForecast(false);
    }
  };

  const fetchInsights = async () => {
    try {
      setLoadingInsights(true);
      const res = await getInsights();
      setInsights(res.data.insights);
    } catch (err) {
      console.error(err);
      setInsights(null);
    } finally {
      setLoadingInsights(false);
    }
  };

  useEffect(() => {
    fetchInsights();
  }, []);

  return (
    <div className="dashboard-panel">
      <div className="section-header">
        <div>
          <p className="section-eyebrow">Forecast Analytics</p>
          <h2>Live Insights</h2>
        </div>
        <div className="button-row">
          <label className="days-input-wrapper">
            <span>Days</span>
            <input
              className="days-input"
              type="number"
              min="1"
              max="30"
              value={days}
              onChange={(e) => setDays(Math.max(1, Number(e.target.value) || 1))}
            />
          </label>
          <button className="button primary" onClick={() => fetchPrediction(days)} disabled={loadingForecast}>
            {loadingForecast ? "Loading..." : `Predict ${days} Days`}
          </button>
          <button className="button secondary" onClick={fetchInsights} disabled={loadingInsights}>
            {loadingInsights ? "Refreshing..." : "Refresh Insights"}
          </button>
        </div>
      </div>

      <div className="kpi-grid">
        <div className="kpi-card">
          <span>Max Demand</span>
          <strong>{insights?.max_demand ?? "—"}</strong>
        </div>
        <div className="kpi-card">
          <span>Min Demand</span>
          <strong>{insights?.min_demand ?? "—"}</strong>
        </div>
        <div className="kpi-card">
          <span>Average Demand</span>
          <strong>{insights?.average_demand ? insights.average_demand.toFixed(2) : "—"}</strong>
        </div>
        <div className="kpi-card">
          <span>Trend</span>
          <strong>{insights?.trend ?? "—"}</strong>
        </div>
        <div className="kpi-card">
          <span>Percent Change</span>
          <strong>{insights?.percent_change != null ? `${insights.percent_change}%` : "—"}</strong>
        </div>
      </div>

      <div className="chart-card">
        <div className="chart-header">
          <div>
            <h3>7-day Forecast</h3>
            <p>Forecast values are generated from the latest trained model.</p>
          </div>
        </div>
        <Charts data={data} />
      </div>

      {data && data.length > 0 && (
        <div className="details-card">
          <h3>Forecast Details</h3>
          <p className="details-description">A quick view of the predicted demand for the next 7 days.</p>
          <ul className="details-list">
            {data.map((point) => (
              <li key={point.day}>
                <span>{point.day}</span>
                <strong>{Number(point.forecast).toFixed(2)}</strong>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
