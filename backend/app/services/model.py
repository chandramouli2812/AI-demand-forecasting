import json
import pickle
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.arima.model import ARIMA

from app.db.database import SessionLocal
from app.db.models import ModelMetadata

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
MODEL_PATH = DATA_DIR / "models.pkl"
DATA_CSV_PATH = BASE_DIR / "processed.csv"
METADATA_KEY = "latest"


def _ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
        date_col = "Order Date"
    elif "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        date_col = "Date"
    elif "ds" in df.columns:
        df["ds"] = pd.to_datetime(df["ds"], errors="coerce")
        date_col = "ds"
    else:
        raise ValueError("Missing date column in uploaded file")

    if "Quantity" in df.columns:
        qty_col = "Quantity"
    elif "Sales" in df.columns:
        qty_col = "Sales"
    elif "y" in df.columns:
        qty_col = "y"
    else:
        raise ValueError("Missing quantity column in uploaded file")

    if "Product" in df.columns:
        prod_col = "Product"
    elif "Category" in df.columns:
        prod_col = "Category"
    else:
        prod_col = None

    df = df[[date_col, qty_col] + ([prod_col] if prod_col else [])].copy()
    df = df.dropna(subset=[date_col, qty_col])
    df["ds"] = pd.to_datetime(df[date_col], errors="coerce")
    df["y"] = pd.to_numeric(df[qty_col], errors="coerce").fillna(0)

    if prod_col:
        df["product"] = df[prod_col].fillna("Unknown").astype(str)
    else:
        df["product"] = "All Products"

    df = df.groupby(["ds", "product"], as_index=False)["y"].sum()
    df = df.sort_values(["product", "ds"]).reset_index(drop=True)
    return df[["ds", "product", "y"]]


def _compute_metrics(actual, predicted):
    if len(actual) != len(predicted) or len(actual) == 0:
        return {"mae": None, "rmse": None, "mape": None}

    actual = np.array(actual, dtype=float)
    predicted = np.array(predicted, dtype=float)
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    with np.errstate(divide="ignore", invalid="ignore"):
        mape = np.mean(np.abs((actual - predicted) / np.where(actual == 0, 1, actual))) * 100
    return {
        "mae": float(mae),
        "rmse": float(rmse),
        "mape": float(mape),
    }


def _fit_series(series: pd.Series):
    if len(series) < 4 or series.nunique() <= 1:
        return {"type": "mean", "value": float(series.mean()) if len(series) > 0 else 0.0}

    try:
        model = ARIMA(series, order=(1, 1, 1))
        model_fit = model.fit()
        return {"type": "arima", "model": model_fit}
    except Exception:
        return {"type": "mean", "value": float(series.mean())}


def _forecast_model(model_data, steps):
    if model_data["type"] == "arima":
        try:
            return model_data["model"].forecast(steps=steps).tolist()
        except Exception:
            return [float(model_data["model"].predicted_mean.iloc[-1])] * steps

    return [float(model_data.get("value", 0.0))] * max(steps, 1)


def _load_models():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model not trained yet")

    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def save_metadata(metadata: dict):
    session = SessionLocal()
    try:
        record = session.query(ModelMetadata).filter_by(key=METADATA_KEY).first()
        if record:
            record.value = json.dumps(metadata, default=str)
        else:
            record = ModelMetadata(key=METADATA_KEY, value=json.dumps(metadata, default=str))
            session.add(record)
        session.commit()
    finally:
        session.close()


def get_metadata() -> dict:
    session = SessionLocal()
    try:
        record = session.query(ModelMetadata).filter_by(key=METADATA_KEY).first()
        if not record:
            return {}
        return json.loads(record.value)
    finally:
        session.close()


def get_available_products(df: pd.DataFrame):
    if "product" not in df.columns:
        return ["All Products"]
    products = sorted(df["product"].astype(str).unique().tolist())
    if "All Products" not in products:
        products.insert(0, "All Products")
    return products


def get_historical_data(product: str = None, window_days: int = 30):
    if not DATA_CSV_PATH.exists():
        return pd.DataFrame(columns=["ds", "product", "y"])

    df = pd.read_csv(DATA_CSV_PATH, parse_dates=["ds"]) if DATA_CSV_PATH.exists() else pd.DataFrame()
    if df.empty:
        return df

    if product and product != "All Products":
        df = df[df["product"] == product]
    return df.sort_values("ds").tail(window_days).reset_index(drop=True)


def calculate_inventory_recommendations(history: pd.DataFrame, forecast: list, lead_time: int = 7):
    if history.empty:
        return {
            "recommended_stock": 0,
            "safety_stock": 0,
            "reorder_point": 0,
            "suggested_reorder_quantity": 0,
            "lead_time_days": lead_time,
        }

    recent = history.copy()
    recent["prev_diff"] = recent["y"].diff().fillna(0)
    avg_daily = float(recent["y"].tail(lead_time).mean() or recent["y"].mean() or 0)
    std_daily = float(recent["y"].diff().tail(lead_time).std(ddof=0) or recent["y"].diff().std(ddof=0) or 0)
    service_z = 1.65
    safety_stock = float(round(std_daily * np.sqrt(lead_time) * service_z, 2))
    reorder_point = int(round(avg_daily * lead_time + safety_stock))
    forecast_cover = float(np.mean(forecast[-lead_time:]) if len(forecast) >= lead_time else float(np.mean(forecast) or avg_daily))
    recommended_stock = max(reorder_point, int(round(forecast_cover * 1.1)))
    suggested_reorder_quantity = max(0, recommended_stock - int(round(avg_daily * 2)))

    return {
        "recommended_stock": recommended_stock,
        "safety_stock": int(round(safety_stock)),
        "reorder_point": reorder_point,
        "suggested_reorder_quantity": suggested_reorder_quantity,
        "lead_time_days": lead_time,
    }


def detect_anomalies(history: pd.DataFrame):
    if history.empty or len(history) < 3:
        return []

    values = history["y"].astype(float)
    mean = values.mean()
    std = values.std(ddof=0) or 1.0
    z_scores = ((values - mean) / std).round(2)

    anomalies = []
    for idx, z in enumerate(z_scores):
        if abs(z) >= 2.5:
            anomalies.append(
                {
                    "ds": history.iloc[idx]["ds"].strftime("%Y-%m-%d"),
                    "value": float(history.iloc[idx]["y"]),
                    "z_score": float(z),
                    "type": "spike" if z > 0 else "dip",
                }
            )
    return anomalies


def build_chart_payload(history: pd.DataFrame, forecast: list, days: int = 7):
    history = history.copy()
    history["day"] = history["ds"].dt.strftime("%Y-%m-%d")
    chart = [
        {"day": row["day"], "actual": float(row["y"])} for _, row in history.iterrows()
    ]

    if chart:
        last_date = history["ds"].max()
    else:
        last_date = pd.Timestamp.now()

    for offset, value in enumerate(forecast, start=1):
        next_date = last_date + pd.Timedelta(days=offset)
        chart.append({"day": next_date.strftime("%Y-%m-%d"), "forecast": float(value)})

    anomalies = detect_anomalies(history)
    anomaly_days = {a["ds"]: a["value"] for a in anomalies}
    for point in chart:
        if point["day"] in anomaly_days:
            point["anomaly"] = anomaly_days[point["day"]]
    return chart


def train_model(df: pd.DataFrame) -> dict:
    df = _normalize_dataframe(df)
    products = get_available_products(df)

    models = {}
    product_metrics = {}
    total_mae = []
    total_rmse = []
    total_mape = []

    for product in products:
        if product == "All Products":
            subset = df.copy()
        else:
            subset = df[df["product"] == product]

        series = subset.sort_values("ds")["y"].astype(float).reset_index(drop=True)
        if series.empty:
            continue

        train_series = series[:-7] if len(series) > 7 else series
        model_data = _fit_series(train_series)
        models[product] = model_data

        if len(series) > 1:
            forecast_steps = min(7, len(series))
            actual_test = series[-forecast_steps:]
            predicted_test = _forecast_model(model_data, forecast_steps)
            metrics = _compute_metrics(actual_test, predicted_test)
        else:
            metrics = _compute_metrics(series, [float(series.mean())] * len(series))

        product_metrics[product] = metrics
        if metrics["mae"] is not None:
            total_mae.append(metrics["mae"])
            total_rmse.append(metrics["rmse"])
            total_mape.append(metrics["mape"])

    _ensure_data_dir()
    with open(MODEL_PATH, "wb") as model_file:
        pickle.dump(models, model_file)

    metadata = {
        "last_trained": datetime.utcnow().isoformat() + "Z",
        "dataset_size": int(df.shape[0]),
        "product_count": int(len(products)),
        "products": products,
        "metrics": product_metrics,
        "average_mae": float(np.mean(total_mae)) if total_mae else None,
        "average_rmse": float(np.mean(total_rmse)) if total_rmse else None,
        "average_mape": float(np.mean(total_mape)) if total_mape else None,
    }
    save_metadata(metadata)
    return metadata


def predict(product: str = None, days: int = 7) -> dict:
    models = _load_models()
    if not DATA_CSV_PATH.exists():
        raise FileNotFoundError("No processed dataset available")

    df = pd.read_csv(DATA_CSV_PATH, parse_dates=["ds"])
    if df.empty:
        raise FileNotFoundError("No processed dataset available")

    if product and product != "All Products" and product not in df["product"].unique():
        raise ValueError(f"Product '{product}' not found in dataset")

    if product is None:
        product = "All Products"

    history = get_historical_data(product, window_days=60)
    if history.empty and product != "All Products":
        raise ValueError(f"No history available for '{product}'")

    model_key = product if product in models else "All Products"
    if model_key not in models:
        raise FileNotFoundError("Model not trained yet for selected product")

    forecast_values = _forecast_model(models[model_key], days)
    chart = build_chart_payload(history, forecast_values, days)
    inventory = calculate_inventory_recommendations(history, forecast_values)
    metadata = get_metadata()
    metrics = metadata.get("metrics", {}).get(product) or {}
    anomalies = detect_anomalies(history)
    history_payload = history.copy()
    if "ds" in history_payload.columns:
        history_payload["ds"] = history_payload["ds"].dt.strftime("%Y-%m-%d")

    return {
        "forecast": [float(value) for value in forecast_values],
        "chart": chart,
        "inventory": inventory,
        "metrics": metrics,
        "metadata": metadata,
        "anomalies": anomalies,
        "history": history_payload.to_dict(orient="records"),
    }
