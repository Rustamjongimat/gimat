# -*- coding: utf-8 -*-
"""
GIMAT — Reports API Router
Generates HTML/PDF reports for rivers
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..services.report_service import generate_report_html

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/{river_id}", response_class=HTMLResponse)
def get_river_report(
    river_id: int,
    db: Session = Depends(get_db)
):
    """Generate an HTML report for a specific river (printable as PDF via browser)"""
    river = db.query(models.River).filter(models.River.id == river_id).first()
    if not river:
        raise HTTPException(status_code=404, detail="River not found")

    stations = db.query(models.Station).filter(
        models.Station.river_id == river_id
    ).all()

    station_ids = [s.id for s in stations]

    hydro_data = db.query(models.HydroData).filter(
        models.HydroData.station_id.in_(station_ids)
    ).order_by(models.HydroData.date.desc()).limit(48).all()

    hydro_data.reverse()

    alerts = db.query(models.Alert).filter(
        models.Alert.station_id.in_(station_ids)
    ).order_by(models.Alert.sent_at.desc()).limit(20).all()

    river_name = river.name_uz or river.name

    html = generate_report_html(river_name, stations, hydro_data, alerts)
    return HTMLResponse(content=html)
