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


def generate_forecast(
    db: Session,
    river_id: int,
    months_ahead: int = 6,
    model_type: str = "hybrid",
    precip: Optional[float] = None,
    temp: Optional[float] = None,
    snow: Optional[float] = None
) -> models.Forecast:
    """Generate a simulated forecast for a river"""

    params = MODEL_PARAMS.get(model_type, MODEL_PARAMS["hybrid"])
    now = datetime.utcnow()
    current_month = now.month

    # Generate predicted values
    np.random.seed(int(now.timestamp()) % 10000 + hash(model_type) % 100)

    values = []
    lower = []
    upper = []

    for i in range(months_ahead):
        month_idx = (current_month + i) % 12
        base = ZARAFSHON_MONTHLY_MEAN[month_idx]
        std = ZARAFSHON_MONTHLY_STD[month_idx]

        # Apply user parameter adjustments
        if precip is not None:
            base *= (1 + (precip - 50) / 200)  # precip effect
        if temp is not None:
            base *= (1 + (temp - 15) / 100)  # temp effect on snowmelt
        if snow is not None:
            base *= (1 + (snow - 30) / 150)  # snow cover effect

        # Add model-specific noise
        noise = np.random.normal(0, std * params["noise_factor"])
        predicted = max(0, base + noise)

        # Confidence intervals widen over time
        ci_width = std * (1 + i * 0.15) * (1 + params["noise_factor"])
        ci_lower = max(0, predicted - 1.96 * ci_width)
        ci_upper = predicted + 1.96 * ci_width

        values.append(round(predicted, 2))
        lower.append(round(ci_lower, 2))
        upper.append(round(ci_upper, 2))

    # Calculate metrics
    mean_discharge = np.mean(ZARAFSHON_MONTHLY_MEAN)
    rmse = round(mean_discharge * params["rmse_factor"], 2)
    mae = round(mean_discharge * params["mae_factor"], 2)

    metrics = {
        "rmse": rmse,
        "mae": mae,
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
