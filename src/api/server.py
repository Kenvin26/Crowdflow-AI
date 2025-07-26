from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from src.forecasting.forecast import train_and_forecast
from fastapi.responses import JSONResponse
import os

app = FastAPI()

@app.get("/metrics/latest")
def latest_metrics():
    metrics_path = "data/outputs/metrics.csv"
    if not os.path.exists(metrics_path):
        return JSONResponse({"detail": "No metrics available yet. Please upload and process a video."}, status_code=200)
    try:
        df = pd.read_csv(metrics_path)
        if df.empty:
            return JSONResponse({"detail": "Metrics file is empty. Please process a video."}, status_code=200)
        last = df.iloc[-1].to_dict()
        return last
    except Exception as e:
        return JSONResponse({"detail": f"Error reading metrics: {str(e)}"}, status_code=500)

class ForecastRequest(BaseModel):
    horizon: int = 6

@app.post("/forecast")
def forecast(req: ForecastRequest):
    pred, conf = train_and_forecast(horizon=req.horizon)
    return {
        "forecast": pred.to_json(),
        "conf": conf.to_json()
    } 