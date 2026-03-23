"""
GIMAT — Data Export API Router
"""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime as dt
import io
import csv
from ..database import get_db
from .. import models

router = APIRouter(prefix="/api/export", tags=["Export"])


@router.get("/")
def export_data(
    station_id: Optional[int] = Query(None),
    river_id: Optional[int] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    format: str = Query("csv", regex="^(csv|xlsx)$"),
    db: Session = Depends(get_db)
):
    """Export hydrological data as CSV or Excel"""

    # Build query
    query = db.query(models.HydroData)

    if station_id:
        query = query.filter(models.HydroData.station_id == station_id)
    elif river_id:
        station_ids = db.query(models.Station.id).filter(
            models.Station.river_id == river_id
        ).all()
        station_ids = [s[0] for s in station_ids]
        query = query.filter(models.HydroData.station_id.in_(station_ids))

    if start_date:
        query = query.filter(models.HydroData.date >= dt.fromisoformat(start_date))
    if end_date:
        query = query.filter(models.HydroData.date <= dt.fromisoformat(end_date))

    data = query.order_by(models.HydroData.date).all()

    if format == "xlsx":
        return _export_excel(data, db)
    else:
        return _export_csv(data, db)


def _export_csv(data, db):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Station", "River", "Discharge (m³/s)", "Precipitation (mm)",
                      "Temperature (°C)", "Snow Cover (%)", "Evaporation (mm)"])

    for row in data:
        station = db.query(models.Station).filter(models.Station.id == row.station_id).first()
        river_name = station.river.name if station and station.river else ""
        station_name = station.name if station else ""
        writer.writerow([
            row.date.strftime("%Y-%m-%d") if row.date else "",
            station_name, river_name,
            row.discharge, row.precipitation,
            row.temperature, row.snow_cover, row.evaporation
        ])

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode("utf-8-sig")),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=gimat_data.csv"}
    )


def _export_excel(data, db):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "GIMAT Data"
    ws.append(["Date", "Station", "River", "Discharge (m³/s)", "Precipitation (mm)",
               "Temperature (°C)", "Snow Cover (%)", "Evaporation (mm)"])

    for row in data:
        station = db.query(models.Station).filter(models.Station.id == row.station_id).first()
        river_name = station.river.name if station and station.river else ""
        station_name = station.name if station else ""
        ws.append([
            row.date.strftime("%Y-%m-%d") if row.date else "",
            station_name, river_name,
            row.discharge, row.precipitation,
            row.temperature, row.snow_cover, row.evaporation
        ])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=gimat_data.xlsx"}
    )
