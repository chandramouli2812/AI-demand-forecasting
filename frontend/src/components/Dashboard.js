import { useState, useEffect } from "react";
import { getPrediction, getInsights } from "../api";
import Charts from "./Charts";

function Dashboard() {
  const [products, setProducts] = useState(["All Products"]);
  const [selectedProduct, setSelectedProduct] = useState("All Products");
  const [chartData, setChartData] = useState([]);
  const [forecastData, setForecastData] = useState([]);
  const [insights, setInsights] = useState(null);
  const [inventory, setInventory] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [metadata, setMetadata] = useState(null);
  const [loading, setLoading] = useState(false);
  const [days, setDays] = useState(7);

  const loadInsights = async (product) => {
    try {
      const response = await getInsights(product);
      const { insights: insightPayload, products: availableProducts, selected_product } = response.data;
      setInsights(insightPayload);
      setProducts(availableProducts || ["All Products"]);
      setSelectedProduct(selected_product || product || "All Products");
    } catch (err) {
      console.error(err);
      setInsights(null);
    }
  };

  const loadPrediction = async (product, predictionDays = days) => {
    try {
      setLoading(true);
      const response = await getPrediction(predictionDays, product);
      setForecastData(response.data.data || []);
      setChartData(response.data.chart || []);
      setInventory(response.data.inventory || null);
      setMetrics(response.data.metrics || null);
      setMetadata(response.data.metadata || null);
    } catch (err) {
      console.error(err);
      alert("❌ Error fetching forecast data. Ensure the model is trained and the selected product exists.");
      setForecastData([]);
      setChartData([]);
      setInventory(null);
      setMetrics(null);
    } finally {
      setLoading(false);
    }
  };

  const refreshData = async (product, predictionDays) => {
    await loadInsights(product);
    await loadPrediction(product, predictionDays);
  };
  <button
  className="button secondary"
  onClick={() => refreshData(selectedProduct, days)}
  disabled={loading}
>
  {loading ? "Refreshing..." : "Refresh Data"}
</button>


  useEffect(() => {
    refreshData(selectedProduct, days);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (selectedProduct) {
      loadPrediction(selectedProduct, days);
      loadInsights(selectedProduct);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedProduct]);

  return (
    <div className="dashboard-panel">
      <div className="section-header">
        <div>
          <p className="section-eyebrow">Forecast Analytics</p>
          <h2>Demand & Inventory</h2>
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
          <label className="product-select-wrapper">
            <span>Product</span>
            <select
              value={selectedProduct}
              onChange={(e) => setSelectedProduct(e.target.value)}
            >
              {products.map((product) => (
                <option key={product} value={product}>
                  {product}
                </option>
              ))}
            </select>
          </label>
          <button className="button primary" onClick={() => loadPrediction(selectedProduct, days)} disabled={loading}>
            {loading ? "Loading..." : `Predict ${days} Days`}
          </button>
        </div>
      </div>

      <div className="kpi-grid">
        <div className="kpi-card">
          <span>Average Demand</span>
          <strong>{insights?.average_demand != null ? insights.average_demand.toFixed(2) : "—"}</strong>
        </div>
        <div className="kpi-card">
          <span>Demand Trend</span>
          <strong>{insights?.trend ?? "—"}</strong>
        </div>
        <div className="kpi-card">
          <span>Anomaly Count</span>
          <strong>{insights?.anomaly_count != null ? insights.anomaly_count : "—"}</strong>
        </div>
        <div className="kpi-card">
          <span>MAE</span>
          <strong>{metrics?.mae != null ? metrics.mae.toFixed(2) : "—"}</strong>
        </div>
        <div className="kpi-card">
          <span>RMSE</span>
          <strong>{metrics?.rmse != null ? metrics.rmse.toFixed(2) : "—"}</strong>
        </div>
        <div className="kpi-card">
          <span>MAPE</span>
          <strong>{metrics?.mape != null ? `${metrics.mape.toFixed(1)}%` : "—"}</strong>
        </div>
      </div>

      <div className="chart-card">
        <div className="chart-header">
          <div>
            <h3>Forecast vs Actual</h3>
            <p>Compare recent demand, forecast, and anomalies for the selected product.</p>
          </div>
        </div>
        <Charts data={chartData} />
      </div>

      <div className="analytics-grid">
        <section className="card smaller-card">
          <h3>Inventory Recommendations</h3>
          <div className="details-list">
            <p><strong>Reorder Point:</strong> {inventory?.reorder_point ?? "—"}</p>
            <p><strong>Safety Stock:</strong> {inventory?.safety_stock ?? "—"}</p>
            <p><strong>Suggested Reorder:</strong> {inventory?.suggested_reorder_quantity ?? "—"}</p>
            <p><strong>Target Stock:</strong> {inventory?.recommended_stock ?? "—"}</p>
          </div>
        </section>

        <section className="card smaller-card">
          <h3>Model Summary</h3>
          <div className="details-list">
            <p><strong>Last trained:</strong> {metadata?.last_trained ?? "—"}</p>
            <p><strong>Products trained:</strong> {metadata?.product_count ?? "—"}</p>
            <p><strong>Data points:</strong> {metadata?.dataset_size ?? "—"}</p>
          </div>
        </section>
      </div>

      {insights?.anomalies?.length > 0 && (
        <div className="details-card">
          <h3>Anomaly Highlights</h3>
          <p className="details-description">Detected spikes and drops in recent demand history.</p>
          <ul className="details-list">
            {insights.anomalies.map((point) => (
              <li key={point.ds}>
                <span>{point.ds}</span>
                <strong>{`${point.type.toUpperCase()} ${point.value} (z=${point.z_score})`}</strong>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
