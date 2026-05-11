from fastapi import APIRouter, HTTPException
import pandas as pd
from app.services.insights import generate_insights
from app.services.model import DATA_CSV_PATH, get_available_products

router = APIRouter()

@router.get("/insights")
def get_insights(product: str = None):
    if not DATA_CSV_PATH.exists():
        raise HTTPException(status_code=404, detail="Upload dataset first")

    df = pd.read_csv(DATA_CSV_PATH, parse_dates=["ds"])
    if df.empty:
        raise HTTPException(status_code=400, detail="No data available")

    available_products = get_available_products(df)
    selected = product or (available_products[0] if available_products else "All Products")
    insights = generate_insights(df, selected)

    return {
        "insights": insights,
        "products": available_products,
        "selected_product": selected,
    }
