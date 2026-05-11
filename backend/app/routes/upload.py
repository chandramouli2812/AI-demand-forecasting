from fastapi import APIRouter, UploadFile, File, BackgroundTasks
import pandas as pd
from app.services.preprocessing import preprocess
from app.services.model import train_model, DATA_CSV_PATH
from io import BytesIO

router = APIRouter()

@router.post("/upload")
async def upload(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents), engine="openpyxl")

    processed = preprocess(df)
    processed.to_csv(DATA_CSV_PATH, index=False)

    if background_tasks:
        background_tasks.add_task(train_model, processed)
        return {"message": "File uploaded & processed. Training started in background."}

    metadata = train_model(processed)
    return {"message": "File uploaded & processed", "metadata": metadata}


