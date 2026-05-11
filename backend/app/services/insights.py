from app.services.model import detect_anomalies, get_available_products, get_metadata


def generate_insights(df, product=None):
    if df.empty or "y" not in df.columns:
        return {
            "max_demand": None,
            "min_demand": None,
            "average_demand": None,
            "median_demand": None,
            "total_demand": None,
            "demand_range": None,
            "volatility": None,
            "trend": "flat",
            "percent_change": None,
            "anomaly_count": 0,
            "anomalies": [],
            "model_metrics": {},
        }

    if product and product != "All Products":
        subset = df[df["product"] == product].sort_values("ds")
    else:
        subset = df.sort_values("ds")

    if subset.empty:
        return {
            "max_demand": None,
            "min_demand": None,
            "average_demand": None,
            "median_demand": None,
            "total_demand": None,
            "demand_range": None,
            "volatility": None,
            "trend": "flat",
            "percent_change": None,
            "anomaly_count": 0,
            "anomalies": [],
            "model_metrics": {},
        }

    y = subset["y"].dropna().astype(float)
    first = y.iloc[0]
    last = y.iloc[-1]
    percent_change = None
    if first != 0:
        percent_change = round(((last - first) / first) * 100, 2)

    trend = "flat"
    if last > first:
        trend = "increasing"
    elif last < first:
        trend = "decreasing"

    anomalies = detect_anomalies(subset)
    metadata = get_metadata()
    model_metrics = metadata.get("metrics", {}).get(product or "All Products", {})

    insights = {
        "max_demand": float(y.max()),
        "min_demand": float(y.min()),
        "average_demand": float(y.mean()),
        "median_demand": float(y.median()),
        "total_demand": float(y.sum()),
        "demand_range": float(y.max() - y.min()),
        "volatility": float(y.pct_change().std()) if len(y) > 1 else 0.0,
        "trend": trend,
        "percent_change": percent_change,
        "anomaly_count": len(anomalies),
        "anomalies": anomalies,
        "model_metrics": model_metrics,
    }
    return insights
