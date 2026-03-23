"""
GIMAT Pydantic Schemas
Request/Response validation models
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime


# ─── River Schemas ───
class RiverBase(BaseModel):
    name: str
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    basin: Optional[str] = None
    length_km: Optional[float] = None
    area_km2: Optional[float] = None
    description: Optional[str] = None

class RiverResponse(RiverBase):
    id: int
    geojson: Optional[str] = None
    class Config:
        from_attributes = True

class RiverListResponse(RiverBase):
    id: int
    station_count: Optional[int] = 0
    class Config:
        from_attributes = True


# ─── Station Schemas ───
class StationBase(BaseModel):
    name: str
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    lat: float
    lon: float
    elevation: Optional[float] = None
    status: Optional[str] = "active"

class StationResponse(StationBase):
    id: int
    river_id: int
    river_name: Optional[str] = None
    latest_discharge: Optional[float] = None
    alert_level: Optional[str] = "normal"
    class Config:
        from_attributes = True


# ─── HydroData Schemas ───
class HydroDataResponse(BaseModel):
    id: int
    station_id: int
    date: datetime
    discharge: Optional[float] = None
    precipitation: Optional[float] = None
    temperature: Optional[float] = None
    snow_cover: Optional[float] = None
    evaporation: Optional[float] = None
    class Config:
        from_attributes = True


# ─── Forecast Schemas ───
class ForecastRequest(BaseModel):
    river_id: int
    months_ahead: int = 6
    model_type: str = "hybrid"
    precipitation: Optional[float] = None
    temperature: Optional[float] = None
    snow_cover: Optional[float] = None

class ForecastResponse(BaseModel):
    id: int
    river_id: int
    created_at: datetime
    months_ahead: int
    model_type: str
    values: Optional[List[float]] = None
    confidence_lower: Optional[List[float]] = None
    confidence_upper: Optional[List[float]] = None
    metrics: Optional[Dict[str, float]] = None
    class Config:
        from_attributes = True

class ModelComparisonResponse(BaseModel):
    hybrid: ForecastResponse
    lstm: ForecastResponse
    hbv: ForecastResponse


# ─── Alert Schemas ───
class AlertResponse(BaseModel):
    id: int
    station_id: int
    station_name: Optional[str] = None
    river_name: Optional[str] = None
    level: str
    value: Optional[float] = None
    threshold: Optional[float] = None
    message: Optional[str] = None
    message_uz: Optional[str] = None
    message_ru: Optional[str] = None
    message_en: Optional[str] = None
    sent_at: Optional[datetime] = None
    is_active: bool = True
    class Config:
        from_attributes = True


# ─── Auth Schemas ───
class UserRegister(BaseModel):
    email: str
    password: str
    name: Optional[str] = None
    lang: Optional[str] = "uz"

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    name: Optional[str] = None
    lang: Optional[str] = "uz"
    is_active: bool = True
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ─── Export Schemas ───
class ExportRequest(BaseModel):
    station_id: Optional[int] = None
    river_id: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    format: str = "csv"  # csv, xlsx


# ─── Stats Schemas ───
class StatsResponse(BaseModel):
    mean: Optional[float] = None
    max: Optional[float] = None
    min: Optional[float] = None
    std: Optional[float] = None
    cv: Optional[float] = None
    count: int = 0
