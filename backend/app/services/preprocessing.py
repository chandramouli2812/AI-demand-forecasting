import pandas as pd


def preprocess(df):
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
        raise ValueError("Dataset must contain a date column named 'Order Date', 'Date', or 'ds'.")

    if "Quantity" in df.columns:
        qty_col = "Quantity"
    elif "Sales" in df.columns:
        qty_col = "Sales"
    elif "y" in df.columns:
        qty_col = "y"
    else:
        raise ValueError("Dataset must contain a quantity column named 'Quantity', 'Sales', or 'y'.")

    if "Product" in df.columns:
        prod_col = "Product"
    elif "Category" in df.columns:
        prod_col = "Category"
    else:
        prod_col = None

    df = df.dropna(subset=[date_col, qty_col]).copy()
    df["ds"] = pd.to_datetime(df[date_col], errors="coerce")
    df["y"] = pd.to_numeric(df[qty_col], errors="coerce").fillna(0)

    if prod_col:
        df["product"] = df[prod_col].fillna("Unknown").astype(str)
    else:
        df["product"] = "All Products"

    processed = (
        df.groupby(["ds", "product"], as_index=False)["y"]
        .sum()
        .sort_values(["product", "ds"])
        .reset_index(drop=True)
    )

    return processed[["ds", "product", "y"]]
