import "./App.css";
import Upload from "./components/Upload";
import Dashboard from "./components/Dashboard";

function App() {
  return (
    <div className="main-container">
      <header className="page-header">
        <div>
          <p className="eyebrow">AI Demand Forecasting</p>
          <h1>Demand Forecast Dashboard</h1>
          <p className="subtitle">
            Upload your dataset, train the model, and review accurate demand forecasts with actionable insights.
          </p>
        </div>
      </header>

      <div className="page-grid">
        <section className="card panel-card">
          <Upload />
        </section>

        <section className="card dashboard-card">
          <Dashboard />
        </section>
      </div>
    </div>
  );
}

export default App;
