from fastapi import APIRouter, HTTPException
from app.services.model import predict

router = APIRouter()

@router.get("/predict")
def get_prediction(days: int = 7, product: str = None):
    try:
        payload = predict(product, days)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return {
        "data": [
            {"day": f"Day {i + 1}", "forecast": float(value)}
            for i, value in enumerate(payload["forecast"])
        ],
        "chart": payload["chart"],
        "inventory": payload["inventory"],
        "metrics": payload["metrics"],
        "metadata": payload["metadata"],
        "anomalies": payload["anomalies"],
        "history": payload["history"],
    }
