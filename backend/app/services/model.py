from pathlib import Path
import pickle
from statsmodels.tsa.arima.model import ARIMA

MODEL_PATH = Path(__file__).resolve().parent.parent / "data" / "model.pkl"

def train_model(df):
    model = ARIMA(df["y"], order=(5, 1, 0))
    model_fit = model.fit()

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model_fit, f)

    return "Model trained successfully"


def predict(days=7):
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model not trained yet")

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    forecast = model.forecast(steps=days)
    return forecast.tolist()
