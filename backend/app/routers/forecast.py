"""
GIMAT — AI Forecast API Router
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..services.forecast_service import generate_forecast

router = APIRouter(prefix="/api", tags=["Forecast"])


@router.get("/rivers/{river_id}/forecast", response_model=schemas.ForecastResponse)
def get_river_forecast(
    river_id: int,
    months_ahead: int = 6,
    db: Session = Depends(get_db)
):
    """Get latest forecast for a river"""
    # Check if forecast exists
    forecast = db.query(models.Forecast).filter(
        models.Forecast.river_id == river_id,
        models.Forecast.model_type == "hybrid"
    ).order_by(models.Forecast.created_at.desc()).first()

    if not forecast:
        # Generate new forecast
        forecast = generate_forecast(db, river_id, months_ahead, "hybrid")

    return forecast


@router.post("/forecast/custom", response_model=schemas.ModelComparisonResponse)
def custom_forecast(
    request: schemas.ForecastRequest,
    db: Session = Depends(get_db)
):
    """Generate custom forecast with user-provided parameters"""
    river = db.query(models.River).filter(models.River.id == request.river_id).first()
    if not river:
        raise HTTPException(status_code=404, detail="River not found")

    hybrid = generate_forecast(
        db, request.river_id, request.months_ahead, "hybrid",
        precip=request.precipitation, temp=request.temperature, snow=request.snow_cover
    )
    lstm = generate_forecast(
        db, request.river_id, request.months_ahead, "lstm",
        precip=request.precipitation, temp=request.temperature, snow=request.snow_cover
    )
    hbv = generate_forecast(
        db, request.river_id, request.months_ahead, "hbv",
        precip=request.precipitation, temp=request.temperature, snow=request.snow_cover
    )

    return schemas.ModelComparisonResponse(
        hybrid=schemas.ForecastResponse.model_validate(hybrid),
        lstm=schemas.ForecastResponse.model_validate(lstm),
        hbv=schemas.ForecastResponse.model_validate(hbv)
    )
