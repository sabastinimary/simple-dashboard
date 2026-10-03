from pathlib import Path
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from src.features.engineering import transform
from src.model import load, score, level

app = FastAPI(title="Network Anomaly Detection API")
MODEL = "models/model.joblib"

class Event(BaseModel):
    duration: float
    src_bytes: float
    dst_bytes: float
    packets: int
    failed_logins: int
    port: int
    protocol: str

@app.get("/")
def root():
    return {"service": "network-anomaly-detection", "status": "running"}

@app.post("/predict")
def predict(event: Event):
    if not Path(MODEL).exists():
        return {"error": "Model not found. Run: python -m src.pipeline"}

    df = pd.DataFrame([event.model_dump()])
    X = transform(df)
    risk = float(score(load(MODEL), X)[0])

    return {
        "risk_score": round(risk, 4),
        "risk_level": level(risk)
    }
