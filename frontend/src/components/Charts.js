import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Scatter,
  Legend,
} from "recharts";

function Charts({ data }) {
  if (!data || data.length === 0) {
    return <p>No data available</p>;
  }

  return (
    <div style={{ marginTop: "20px", width: "100%", height: 360 }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="actual" stroke="#8884d8" name="Actual" dot={false} />
          <Line type="monotone" dataKey="forecast" stroke="#82ca9d" name="Forecast" dot={false} />
          <Scatter data={data.filter((item) => item.anomaly != null)} dataKey="anomaly" fill="#ff4d4f" name="Anomaly" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default Charts;