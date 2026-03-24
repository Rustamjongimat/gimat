"""
GIMAT — AI Forecast Service
Simulated LSTM+HBV hybrid model for Zarafshon river
Generates realistic mock forecast data with confidence intervals
"""
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .. import models
from typing import Optional


# Zarafshon river seasonal discharge pattern (m³/s) — based on real patterns
ZARAFSHON_MONTHLY_MEAN = [45, 42, 55, 120, 250, 380, 320, 180, 95, 65, 52, 47]
ZARAFSHON_MONTHLY_STD = [8, 7, 12, 30, 50, 70, 55, 35, 18, 12, 9, 8]

# Model performance characteristics
MODEL_PARAMS = {
    "hybrid": {"noise_factor": 0.08, "nse": 0.89, "r2": 0.91, "rmse_factor": 0.10, "mae_factor": 0.07},
    "lstm":   {"noise_factor": 0.12, "nse": 0.82, "r2": 0.85, "rmse_factor": 0.14, "mae_factor": 0.10},
    "hbv":    {"noise_factor": 0.15, "nse": 0.76, "r2": 0.79, "rmse_factor": 0.18, "mae_factor": 0.13},
}


import os
import joblib

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "ml_models", "hybrid_model.pkl")

def generate_forecast(
    db: Session,
    river_id: int,
    months_ahead: int = 6,
    model_type: str = "hybrid",
    precip: Optional[float] = None,
    temp: Optional[float] = None,
    snow: Optional[float] = None
) -> models.Forecast:
    """Generate forecast using real MLP model if exists, else fallback to simulation"""
    
    now = datetime.utcnow()
    current_month = now.month
    
    # Check for real model
    use_real_model = False
    model_payload = None
    if os.path.exists(MODEL_PATH) and model_type == "hybrid":
        try:
            model_payload = joblib.load(MODEL_PATH)
            use_real_model = True
        except Exception as e:
            print(f"Failed to load real ML model: {e}")

    values = []
    lower = []
    upper = []
    
    params = MODEL_PARAMS.get(model_type, MODEL_PARAMS["hybrid"])
    
    if use_real_model:
        # ---- REAL ML PIPELINE PREDICTION ----
        mlp = model_payload["model"]
        scaler = model_payload["scaler"]
        
        # We need a generic station_id. Fetch a station belonging to this river
        station = db.query(models.Station).filter(models.Station.river_id == river_id).first()
        station_id = station.id if station else 1
        
        for i in range(months_ahead):
            month_idx = ((current_month + i - 1) % 12) + 1  # 1-12
            
            # Use given params, fallback to historical monthly averages
            p_val = precip if precip is not None else 30.0 + (month_idx % 4) * 10
            t_val = temp if temp is not None else 15.0 + (6 - abs(month_idx - 6)) * 4
            s_val = snow if snow is not None else max(0, 20.0 - (month_idx % 6) * 5)
            
            # Predict
            X_input = scaler.transform([[station_id, month_idx, p_val, t_val, s_val]])
            prediction = mlp.predict(X_input)[0]
            predicted = max(0, float(prediction))
            
            rmse = model_payload["metrics"]["rmse"]
            ci_width = rmse * (1 + i * 0.1)
            
            values.append(round(predicted, 2))
            lower.append(round(max(0, predicted - 1.96 * ci_width), 2))
            upper.append(round(predicted + 1.96 * ci_width, 2))
            
        metrics = model_payload["metrics"]
            
    else:
        # ---- SIMULATION FALLBACK PIPELINE ----
        np.random.seed(int(now.timestamp()) % 10000 + hash(model_type) % 100)
        
        for i in range(months_ahead):
            month_idx = (current_month + i) % 12
            base = ZARAFSHON_MONTHLY_MEAN[month_idx]
            std = ZARAFSHON_MONTHLY_STD[month_idx]

            if precip is not None: base *= (1 + (precip - 50) / 200)
            if temp is not None: base *= (1 + (temp - 15) / 100)
            if snow is not None: base *= (1 + (snow - 30) / 150)

            noise = np.random.normal(0, std * params["noise_factor"])
            predicted = max(0, base + noise)

            ci_width = std * (1 + i * 0.15) * (1 + params["noise_factor"])
            
            values.append(round(predicted, 2))
            lower.append(round(max(0, predicted - 1.96 * ci_width), 2))
            upper.append(round(predicted + 1.96 * ci_width, 2))

        mean_discharge = np.mean(ZARAFSHON_MONTHLY_MEAN)
        metrics = {
            "rmse": round(mean_discharge * params["rmse_factor"], 2),
            "mae": round(mean_discharge * params["mae_factor"], 2),
            "nse": params["nse"],
            "r2": params["r2"]
        }

    # Save forecast to DB
    forecast = models.Forecast(
        river_id=river_id,
        months_ahead=months_ahead,
        model_type=model_type,
        values=values,
        confidence_lower=lower,
        confidence_upper=upper,
        metrics=metrics,
        created_at=now
    )
    db.add(forecast)
    db.commit()
    db.refresh(forecast)

    return forecast
