# -*- coding: utf-8 -*-
"""
GIMAT — Admin API Router
Handles manual data entry and real-time triggers via WebSockets
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from .. import models, schemas
from ..services.websocket_manager import manager
from .auth import get_current_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])


def verify_admin(current_user: models.User = Depends(get_current_user)):
    """Check if the user is an admin"""
    if current_user.role not in ["super_admin", "admin", "operator"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )
    return current_user


@router.post("/data", response_model=schemas.HydroDataResponse)
async def add_hydro_data(
    data: schemas.HydroDataCreate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(verify_admin)
):
    """Add new hydrological data manually and broadcast to clients"""
    
    # Check if station exists
    station = db.query(models.Station).filter(models.Station.id == data.station_id).first()
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")

    # Create new record
    new_data = models.HydroData(
        station_id=data.station_id,
        date=data.date,
        discharge=data.discharge,
        precipitation=data.precipitation,
        temperature=data.temperature,
        snow_cover=data.snow_cover,
        evaporation=data.evaporation
    )
    db.add(new_data)
    
    # Evaluate Alert level based on Discharge
    # E.g. Discharge > threshold P90/P95 (using hardcoded fallback for demo)
    alert_level = "normal"
    river_name = station.river.name if station.river else "Unknown"
    
    # Very basic demo thresholds for alerting logic based on river basin/size
    warning_threshold = 400
    danger_threshold = 600
    if river_name == "Amudaryo":
        warning_threshold, danger_threshold = 1500, 2000
    elif river_name == "Sirdaryo":
        warning_threshold, danger_threshold = 1000, 1500
    elif river_name == "Zarafshon":
        warning_threshold, danger_threshold = 150, 250
        
    if new_data.discharge:
        if new_data.discharge >= danger_threshold:
            alert_level = "danger"
        elif new_data.discharge >= warning_threshold:
            alert_level = "warning"
            
    # Update station status
    station.status = "active"
    
    new_alert = None
    if alert_level != "normal":
        # Create an alert
        new_alert = models.Alert(
            station_id=station.id,
            level=alert_level,
            value=new_data.discharge,
            threshold=danger_threshold if alert_level == "danger" else warning_threshold,
            message_uz=f"Diqqat! {station.name} stansiyasida suv sathi {alert_level} darajaga yetdi.",
            message_ru=f"Внимание! Уровень воды на станции {station.name} достиг уровня {alert_level}.",
            message_en=f"Attention! Water level at station {station.name} reached {alert_level} level.",
            sent_at=datetime.utcnow(),
            is_active=True
        )
        db.add(new_alert)

    db.commit()
    db.refresh(new_data)
    
    # Broadcast new data
    payload = schemas.HydroDataResponse.model_validate(new_data).model_dump()
    # Convert datetime to ISO string for JSON serialization
    payload["date"] = payload["date"].isoformat()
    await manager.broadcast("new_data", payload)

    # Broadcast new alert if created
    if new_alert:
        db.refresh(new_alert)
        alert_payload = {
            "id": new_alert.id,
            "station_id": station.id,
            "station_name": station.name,
            "river_name": river_name,
            "level": alert_level,
            "value": new_alert.value,
            "threshold": new_alert.threshold,
            "message": new_alert.message_uz,
            "is_active": True,
            "sent_at": new_alert.sent_at.isoformat()
        }
        await manager.broadcast("new_alert", alert_payload)

    return new_data

