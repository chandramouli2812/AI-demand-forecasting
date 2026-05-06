from fastapi import APIRouter, HTTPException
import os
import pandas as pd
from app.services.insights import generate_insights

router = APIRouter()

DATA_PATH = "processed.csv"

@router.get("/insights")
def get_insights():
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=404, detail="Upload dataset first")

    df = pd.read_csv(DATA_PATH)
    if df.empty:
        raise HTTPException(status_code=400, detail="No data available")

    insights = generate_insights(df)
    return {"insights": insights}
