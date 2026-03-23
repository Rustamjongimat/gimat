"""
GIMAT — Rivers API Router
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/rivers", tags=["Rivers"])


@router.get("/", response_model=list[schemas.RiverListResponse])
def get_rivers(db: Session = Depends(get_db)):
    """Get all rivers"""
    rivers = db.query(models.River).all()
    result = []
    for river in rivers:
        r = schemas.RiverListResponse(
            id=river.id,
            name=river.name,
            name_uz=river.name_uz,
            name_ru=river.name_ru,
            name_en=river.name_en,
            basin=river.basin,
            length_km=river.length_km,
            area_km2=river.area_km2,
            description=river.description,
            station_count=len(river.stations)
        )
        result.append(r)
    return result


@router.get("/{river_id}", response_model=schemas.RiverResponse)
def get_river(river_id: int, db: Session = Depends(get_db)):
    """Get single river with GeoJSON"""
    river = db.query(models.River).filter(models.River.id == river_id).first()
    if not river:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="River not found")
    return river


@router.get("/{river_id}/data", response_model=list[schemas.HydroDataResponse])
def get_river_data(
    river_id: int,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    limit: int = Query(500, le=5000),
    db: Session = Depends(get_db)
):
    """Get hydrological data for a river's stations"""
    from datetime import datetime as dt

    station_ids = db.query(models.Station.id).filter(
        models.Station.river_id == river_id
    ).all()
    station_ids = [s[0] for s in station_ids]

    query = db.query(models.HydroData).filter(
        models.HydroData.station_id.in_(station_ids)
    )

    if start_date:
        query = query.filter(models.HydroData.date >= dt.fromisoformat(start_date))
    if end_date:
        query = query.filter(models.HydroData.date <= dt.fromisoformat(end_date))

    return query.order_by(models.HydroData.date.desc()).limit(limit).all()
