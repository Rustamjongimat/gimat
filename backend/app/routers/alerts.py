"""
GIMAT — Alerts API Router
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])


@router.get("/", response_model=list[schemas.AlertResponse])
def get_alerts(
    level: Optional[str] = Query(None, description="Filter by level: normal, warning, danger"),
    station_id: Optional[int] = Query(None),
    is_active: Optional[bool] = Query(None),
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db)
):
    """Get alerts with optional filters"""
    query = db.query(models.Alert)

    if level:
        query = query.filter(models.Alert.level == level)
    if station_id:
        query = query.filter(models.Alert.station_id == station_id)
    if is_active is not None:
        query = query.filter(models.Alert.is_active == is_active)

    alerts = query.order_by(models.Alert.sent_at.desc()).limit(limit).all()

    result = []
    for alert in alerts:
        station = db.query(models.Station).filter(models.Station.id == alert.station_id).first()
        river_name = None
        station_name = None
        if station:
            station_name = station.name
            if station.river:
                river_name = station.river.name

        r = schemas.AlertResponse(
            id=alert.id,
            station_id=alert.station_id,
            station_name=station_name,
            river_name=river_name,
            level=alert.level,
            value=alert.value,
            threshold=alert.threshold,
            message=alert.message,
            message_uz=alert.message_uz,
            message_ru=alert.message_ru,
            message_en=alert.message_en,
            sent_at=alert.sent_at,
            is_active=alert.is_active
        )
        result.append(r)
    return result
