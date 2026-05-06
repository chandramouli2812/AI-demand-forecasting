from fastapi import APIRouter, UploadFile, File
import pandas as pd
from app.services.preprocessing import preprocess
from io import BytesIO

router = APIRouter()

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()   # read file properly
    df = pd.read_excel(BytesIO(contents), engine="openpyxl")

    processed = preprocess(df)
    processed.to_csv("processed.csv", index=False)

    return {"message": "File uploaded & processed"}


