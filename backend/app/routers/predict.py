from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil

from ml.predict import predict_cancer

router = APIRouter(tags=["Prediction"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/predict")
async def predict(file: UploadFile = File(...)):

    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV file."
        )

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = predict_cancer(file_path)

    return result