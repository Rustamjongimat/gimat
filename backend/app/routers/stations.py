"""
GIMAT — Stations API Router
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/stations", tags=["Stations"])


@router.get("/", response_model=list[schemas.StationResponse])
def get_stations(
    river_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all monitoring stations"""
    query = db.query(models.Station)

    if river_id:
        query = query.filter(models.Station.river_id == river_id)
    if status:
        query = query.filter(models.Station.status == status)

    stations = query.all()
    result = []
    for station in stations:
        # Get latest discharge
        latest = db.query(models.HydroData).filter(
            models.HydroData.station_id == station.id
        ).order_by(models.HydroData.date.desc()).first()

        # Get active alert
        active_alert = db.query(models.Alert).filter(
            models.Alert.station_id == station.id,
            models.Alert.is_active == True
        ).order_by(models.Alert.sent_at.desc()).first()

        r = schemas.StationResponse(
            id=station.id,
            river_id=station.river_id,
            name=station.name,
            name_uz=station.name_uz,
            name_ru=station.name_ru,
            name_en=station.name_en,
            lat=station.lat,
            lon=station.lon,
            elevation=station.elevation,
            status=station.status,
            river_name=station.river.name if station.river else None,
            latest_discharge=latest.discharge if latest else None,
            alert_level=active_alert.level if active_alert else "normal"
        )
        result.append(r)
    return result
