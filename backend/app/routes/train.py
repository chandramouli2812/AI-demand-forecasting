import os
from fastapi import APIRouter, HTTPException
import pandas as pd
from app.services.model import train_model, MODEL_PATH

router = APIRouter()

DATA_PATH = "processed.csv"

@router.post("/train")
def train():
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=400, detail="Upload dataset first")

    df = pd.read_csv(DATA_PATH)
    train_model(df)

    return {"message": "Model trained successfully", "model_path": str(MODEL_PATH)}
