"""
GIMAT SQLAlchemy ORM Models
Matches TZ Section 4.3 Database Schema
"""
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean, JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class River(Base):
    __tablename__ = "rivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    name_uz = Column(String(100))
    name_ru = Column(String(100))
    name_en = Column(String(100))
    basin = Column(String(100))
    length_km = Column(Float)
    area_km2 = Column(Float)
    geojson = Column(Text)  # GeoJSON string for river path
    description = Column(Text)

    stations = relationship("Station", back_populates="river")
    forecasts = relationship("Forecast", back_populates="river")


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    river_id = Column(Integer, ForeignKey("rivers.id"), nullable=False)
    name = Column(String(100), nullable=False)
    name_uz = Column(String(100))
    name_ru = Column(String(100))
    name_en = Column(String(100))
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    elevation = Column(Float)
    status = Column(String(20), default="active")  # active, inactive, maintenance

    river = relationship("River", back_populates="stations")
    hydro_data = relationship("HydroData", back_populates="station")
    alerts = relationship("Alert", back_populates="station")


class HydroData(Base):
    __tablename__ = "hydro_data"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    discharge = Column(Float)        # m³/s — daryo oqimi
    precipitation = Column(Float)    # mm — yog'in
    temperature = Column(Float)      # °C — harorat
    snow_cover = Column(Float)       # % — qor qoplami
    evaporation = Column(Float)      # mm — bug'lanish

    station = relationship("Station", back_populates="hydro_data")


class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)
    river_id = Column(Integer, ForeignKey("rivers.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    months_ahead = Column(Integer, nullable=False)
    model_type = Column(String(20), default="hybrid")  # hybrid, lstm, hbv
    values = Column(JSON)           # predicted discharge values
    confidence_lower = Column(JSON)  # 95% CI lower bound
    confidence_upper = Column(JSON)  # 95% CI upper bound
    metrics = Column(JSON)          # {rmse, mae, nse, r2}

    river = relationship("River", back_populates="forecasts")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    level = Column(String(20), nullable=False)  # normal, warning, danger
    value = Column(Float)
    threshold = Column(Float)
    message = Column(Text)
    message_uz = Column(Text)
    message_ru = Column(Text)
    message_en = Column(Text)
    sent_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    station = relationship("Station", back_populates="alerts")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="user")  # super_admin, operator, researcher, user
    name = Column(String(100))
    lang = Column(String(5), default="uz")  # uz, ru, en
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    subscriptions = relationship("Subscription", back_populates="user")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    channels = Column(JSON)      # ["email", "telegram"]
    thresholds = Column(JSON)    # {"warning": 500, "danger": 800}

    user = relationship("User", back_populates="subscriptions")
