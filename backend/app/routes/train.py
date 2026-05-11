import os
from fastapi import APIRouter, HTTPException
import pandas as pd
from app.services.model import train_model, DATA_CSV_PATH

router = APIRouter()

@router.post("/train")
def train():
    if not DATA_CSV_PATH.exists():
        raise HTTPException(status_code=400, detail="Upload dataset first")

    df = pd.read_csv(DATA_CSV_PATH, parse_dates=["ds"])
    metadata = train_model(df)

    return {"message": "Model trained successfully", "metadata": metadata}
