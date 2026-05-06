from fastapi import APIRouter, HTTPException
from app.services.model import predict

router = APIRouter()

@router.get("/predict")
def get_prediction(days: int = 7):
    try:
        forecast = predict(days)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Model not trained yet")

    data = [
        {"day": f"Day {i + 1}", "forecast": float(value)}
        for i, value in enumerate(forecast)
    ]

    return {"data": data}
