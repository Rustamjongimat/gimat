# -*- coding: utf-8 -*-
"""
GIMAT — Database Seed Data
Seeds Uzbekistan rivers, stations, and sample hydro data
"""
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import models
import json


def seed_database(db: Session):
    """Seed the database with initial data"""

    # Check if already seeded
    if db.query(models.River).count() > 0:
        print("Database already seeded, skipping...")
        return

    print("Seeding database...")

    # ─── 1. Rivers ───
    rivers_data = [
        {
            "name": "Amudaryo",
            "name_uz": "Amudaryo",
            "name_ru": "Амударья",
            "name_en": "Amu Darya",
            "basin": "Aral dengizi havzasi",
            "length_km": 2540,
            "area_km2": 309000,
            "description": "Markaziy Osiyoning eng katta daryosi"
        },
        {
            "name": "Sirdaryo",
            "name_uz": "Sirdaryo",
            "name_ru": "Сырдарья",
            "name_en": "Syr Darya",
            "basin": "Aral dengizi havzasi",
            "length_km": 2212,
            "area_km2": 219000,
            "description": "Markaziy Osiyoning ikkinchi yirik daryosi"
        },
        {
            "name": "Zarafshon",
            "name_uz": "Zarafshon",
            "name_ru": "Зарафшан",
            "name_en": "Zarafshan",
            "basin": "Zarafshon havzasi",
            "length_km": 877,
            "area_km2": 40400,
            "description": "Samarqand va Buxoro viloyatlarining asosiy suv manbai"
        },
        {
            "name": "Chirchiq",
            "name_uz": "Chirchiq",
            "name_ru": "Чирчик",
            "name_en": "Chirchik",
            "basin": "Sirdaryo havzasi",
            "length_km": 161,
            "area_km2": 14240,
            "description": "Toshkent viloyatining asosiy daryosi"
        },
        {
            "name": "Qashqadaryo",
            "name_uz": "Qashqadaryo",
            "name_ru": "Кашкадарья",
            "name_en": "Kashkadarya",
            "basin": "Qashqadaryo havzasi",
            "length_km": 378,
            "area_km2": 8780,
            "description": "Qashqadaryo viloyatining asosiy daryosi"
        },
        {
            "name": "Surxondaryo",
            "name_uz": "Surxondaryo",
            "name_ru": "Сурхандарья",
            "name_en": "Surkhandarya",
            "basin": "Amudaryo havzasi",
            "length_km": 175,
            "area_km2": 13500,
            "description": "Surxondaryo viloyatining asosiy daryosi"
        },
        {
            "name": "Naryn",
            "name_uz": "Naryn",
            "name_ru": "Нарын",
            "name_en": "Naryn",
            "basin": "Sirdaryo havzasi",
            "length_km": 807,
            "area_km2": 58370,
            "description": "Sirdaryo bosh irmoqlaridan biri"
        },
        {
            "name": "Angren",
            "name_uz": "Angren",
            "name_ru": "Ангрен",
            "name_en": "Angren",
            "basin": "Sirdaryo havzasi",
            "length_km": 185,
            "area_km2": 5680,
            "description": "Toshkent viloyatidagi daryo"
        },
        {
            "name": "Ohangaron",
            "name_uz": "Ohangaron",
            "name_ru": "Ахангаран",
            "name_en": "Akhangaran",
            "basin": "Sirdaryo havzasi",
            "length_km": 236,
            "area_km2": 7710,
            "description": "Chirchiq havzasiga yaqin daryo"
        },
        {
            "name": "Sangzor",
            "name_uz": "Sangzor",
            "name_ru": "Сангзар",
            "name_en": "Sangzar",
            "basin": "Sirdaryo havzasi",
            "length_km": 198,
            "area_km2": 3090,
            "description": "Jizzax viloyatidagi daryo"
        }
    ]

    river_objects = []
    for data in rivers_data:
        river = models.River(**data)
        db.add(river)
        river_objects.append(river)

    db.flush()

    # ─── 2. Stations ───
    stations_data = [
        # Amudaryo stations
        {"river_idx": 0, "name": "Termiz", "name_uz": "Termiz stansiyasi", "name_ru": "Термез", "name_en": "Termez", "lat": 37.2247, "lon": 67.2783, "elevation": 302},
        {"river_idx": 0, "name": "Tuyamuyun", "name_uz": "To'yamuyun stansiyasi", "name_ru": "Туямуюн", "name_en": "Tuyamuyun", "lat": 41.7636, "lon": 60.6531, "elevation": 88},
        # Sirdaryo stations
        {"river_idx": 1, "name": "Bekobod", "name_uz": "Bekobod stansiyasi", "name_ru": "Бекабад", "name_en": "Bekabad", "lat": 40.2214, "lon": 69.2692, "elevation": 320},
        {"river_idx": 1, "name": "Xovos", "name_uz": "Xovos stansiyasi", "name_ru": "Ховос", "name_en": "Khovos", "lat": 40.5398, "lon": 68.7592, "elevation": 298},
        # Zarafshon stations (main focus for dissertation)
        {"river_idx": 2, "name": "Dupul", "name_uz": "Dupul stansiyasi", "name_ru": "Дупул", "name_en": "Dupul", "lat": 39.5167, "lon": 67.8500, "elevation": 750},
        {"river_idx": 2, "name": "Samarqand", "name_uz": "Samarqand stansiyasi", "name_ru": "Самарканд", "name_en": "Samarkand", "lat": 39.6547, "lon": 66.9597, "elevation": 710},
        {"river_idx": 2, "name": "Navbahor", "name_uz": "Navbahor stansiyasi", "name_ru": "Навбахор", "name_en": "Navbahor", "lat": 39.8983, "lon": 65.3489, "elevation": 370},
        # Chirchiq stations
        {"river_idx": 3, "name": "Xodjikeyt", "name_uz": "Xodjikent stansiyasi", "name_ru": "Ходжикент", "name_en": "Khodzhikent", "lat": 41.5117, "lon": 69.7117, "elevation": 880},
        {"river_idx": 3, "name": "Toshkent", "name_uz": "Toshkent stansiyasi", "name_ru": "Ташкент", "name_en": "Tashkent", "lat": 41.3111, "lon": 69.2797, "elevation": 420},
        # Qashqadaryo stations
        {"river_idx": 4, "name": "Varganza", "name_uz": "Varganza stansiyasi", "name_ru": "Варганза", "name_en": "Varganza", "lat": 38.9250, "lon": 66.8750, "elevation": 650},
        {"river_idx": 4, "name": "Qarshi", "name_uz": "Qarshi stansiyasi", "name_ru": "Карши", "name_en": "Karshi", "lat": 38.8611, "lon": 65.7983, "elevation": 372},
        # Surxondaryo stations
        {"river_idx": 5, "name": "Denov", "name_uz": "Denov stansiyasi", "name_ru": "Денау", "name_en": "Denau", "lat": 38.2711, "lon": 67.8936, "elevation": 520},
        # Naryn station
        {"river_idx": 6, "name": "Uchqo'rg'on", "name_uz": "Uchqo'rg'on stansiyasi", "name_ru": "Учкурган", "name_en": "Uchkurgan", "lat": 41.1186, "lon": 71.0358, "elevation": 450},
        # Angren station
        {"river_idx": 7, "name": "Angren shahri", "name_uz": "Angren stansiyasi", "name_ru": "Ангрен", "name_en": "Angren City", "lat": 41.0167, "lon": 70.1439, "elevation": 940},
        # Ohangaron station
        {"river_idx": 8, "name": "Ohangaron shahri", "name_uz": "Ohangaron stansiyasi", "name_ru": "Ахангаран", "name_en": "Akhangaran City", "lat": 41.0656, "lon": 69.6386, "elevation": 420},
        # Sangzor station
        {"river_idx": 9, "name": "Jizzax", "name_uz": "Jizzax stansiyasi", "name_ru": "Джизак", "name_en": "Jizzakh", "lat": 40.1158, "lon": 67.8422, "elevation": 350},
    ]

    station_objects = []
    for data in stations_data:
        river_idx = data.pop("river_idx")
        station = models.Station(river_id=river_objects[river_idx].id, **data)
        db.add(station)
        station_objects.append(station)

    db.flush()

    # ─── 3. Hydro Data (2+ years for Zarafshon) ───
    print("Generating hydro data...")

    # Monthly patterns per river (approximate discharge m3/s)
    river_patterns = {
        0: {"base": [1200, 1100, 1300, 2500, 4200, 5800, 5000, 3200, 1800, 1400, 1250, 1200], "std_f": 0.15},  # Amudaryo
        1: {"base": [400, 380, 500, 1200, 2000, 2500, 2100, 1300, 700, 500, 420, 400], "std_f": 0.12},  # Sirdaryo
        2: {"base": [45, 42, 55, 120, 250, 380, 320, 180, 95, 65, 52, 47], "std_f": 0.15},  # Zarafshon
        3: {"base": [80, 75, 100, 200, 380, 450, 400, 280, 150, 100, 85, 80], "std_f": 0.12},  # Chirchiq
        4: {"base": [15, 12, 20, 65, 120, 85, 45, 25, 18, 15, 14, 14], "std_f": 0.20},  # Qashqadaryo
        5: {"base": [30, 25, 45, 90, 160, 130, 80, 50, 35, 30, 28, 28], "std_f": 0.18},  # Surxondaryo
        6: {"base": [250, 230, 300, 700, 1200, 1500, 1300, 800, 450, 320, 270, 250], "std_f": 0.12},  # Naryn
        7: {"base": [20, 18, 25, 55, 100, 120, 95, 60, 35, 25, 22, 20], "std_f": 0.18},  # Angren
        8: {"base": [35, 30, 45, 85, 150, 180, 140, 90, 55, 40, 36, 35], "std_f": 0.15},  # Ohangaron
        9: {"base": [8, 7, 12, 35, 60, 45, 25, 15, 10, 8, 8, 8], "std_f": 0.22},  # Sangzor
    }

    np.random.seed(42)
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2024, 12, 31)

    for station in station_objects:
        # Find river index
        river_idx = next(
            i for i, r in enumerate(river_objects) if r.id == station.river_id
        )
        pattern = river_patterns.get(river_idx, river_patterns[2])

        current = start_date
        while current <= end_date:
            month_idx = current.month - 1
            base_discharge = pattern["base"][month_idx]
            std = base_discharge * pattern["std_f"]

            discharge = max(0, np.random.normal(base_discharge, std))
            precipitation = max(0, np.random.normal(
                [25, 30, 35, 45, 40, 15, 8, 5, 10, 20, 25, 28][month_idx],
                [8, 10, 12, 15, 12, 5, 3, 2, 4, 8, 10, 10][month_idx]
            ))
            temperature = np.random.normal(
                [1, 4, 10, 16, 22, 28, 31, 29, 23, 15, 8, 3][month_idx],
                [2, 2, 3, 3, 3, 2, 2, 2, 3, 3, 2, 2][month_idx]
            )
            snow_cover = max(0, min(100, np.random.normal(
                [60, 55, 40, 20, 5, 0, 0, 0, 2, 15, 35, 55][month_idx],
                [15, 15, 12, 8, 3, 0, 0, 0, 2, 5, 10, 15][month_idx]
            )))
            evaporation = max(0, np.random.normal(
                [10, 15, 25, 40, 55, 70, 75, 65, 45, 30, 18, 12][month_idx],
                [3, 4, 6, 8, 10, 12, 12, 10, 8, 6, 4, 3][month_idx]
            ))

            hydro = models.HydroData(
                station_id=station.id,
                date=current,
                discharge=round(discharge, 2),
                precipitation=round(precipitation, 2),
                temperature=round(temperature, 2),
                snow_cover=round(snow_cover, 2),
                evaporation=round(evaporation, 2)
            )
            db.add(hydro)

            # Move to next month
            if current.month == 12:
                current = datetime(current.year + 1, 1, 1)
            else:
                current = datetime(current.year, current.month + 1, 1)

    db.flush()

    # ─── 4. Sample Alerts ───
    alert_data = [
        {
            "station_idx": 4, "level": "danger", "value": 420.5, "threshold": 380,
            "message": "Zarafshon daryosida toshqin xavfi!",
            "message_uz": "Zarafshon daryosida toshqin xavfi! Oqim 420.5 m³/s (chegara: 380 m³/s)",
            "message_ru": "Опасность наводнения на реке Зарафшан! Расход 420.5 м³/с (порог: 380 м³/с)",
            "message_en": "Flood danger on Zarafshan river! Discharge 420.5 m³/s (threshold: 380 m³/s)",
            "is_active": True
        },
        {
            "station_idx": 5, "level": "warning", "value": 210.3, "threshold": 200,
            "message": "Zarafshon — Samarqand stansiyasida ehtiyot signal",
            "message_uz": "Zarafshon — Samarqand stansiyasida oqim ortib bormoqda (210.3 m³/s)",
            "message_ru": "Зарафшан — Самарканд: повышение расхода воды (210.3 м³/с)",
            "message_en": "Zarafshan — Samarkand station: rising discharge (210.3 m³/s)",
            "is_active": True
        },
        {
            "station_idx": 0, "level": "warning", "value": 5200.0, "threshold": 5000,
            "message": "Amudaryo — Termiz stansiyasida ehtiyot signal",
            "message_uz": "Amudaryo — Termiz stansiyasida oqim yuqori (5200 m³/s)",
            "message_ru": "Амударья — Термез: повышенный расход (5200 м³/с)",
            "message_en": "Amu Darya — Termez: elevated discharge (5200 m³/s)",
            "is_active": True
        },
        {
            "station_idx": 2, "level": "normal", "value": 350.0, "threshold": 500,
            "message": "Sirdaryo — Bekobod stansiyasi normal holatda",
            "message_uz": "Sirdaryo — Bekobod stansiyasi normal holatda (350 m³/s)",
            "message_ru": "Сырдарья — Бекабад: нормальное состояние (350 м³/с)",
            "message_en": "Syr Darya — Bekabad station: normal condition (350 m³/s)",
            "is_active": False
        },
    ]

    for data in alert_data:
        station_idx = data.pop("station_idx")
        alert = models.Alert(
            station_id=station_objects[station_idx].id,
            sent_at=datetime.utcnow() - timedelta(hours=np.random.randint(1, 72)),
            **data
        )
        db.add(alert)
        
    # Check if admin user exists, if not create one
    admin_exist = db.query(models.User).filter(models.User.email == "admin@gimat.uz").first()
    if not admin_exist:
        import bcrypt
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw("admin123".encode("utf-8"), salt).decode("utf-8")
        admin = models.User(
            email="admin@gimat.uz",
            hashed_password=hashed,
            name="Super Admin",
            role="super_admin"
        )
        db.add(admin)

    db.commit()
    print(f"Seeded: {len(rivers_data)} rivers, {len(stations_data)} stations, alerts, admin user, and hydro data.")
