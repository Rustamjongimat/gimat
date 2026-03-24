"""
GIMAT — FastAPI Main Application
Gidrologik Intellektual Monitoring va Axborot Tizimi
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database import engine, SessionLocal, Base
from .routers import rivers, stations, forecast, alerts, auth, export, reports, ws, admin
from .seed_data import seed_database
import os

# Create all tables
Base.metadata.create_all(bind=engine)

# Static files directory
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")

app = FastAPI(
    title="GIMAT API",
    description="Gidrologik Intellektual Monitoring va Axborot Tizimi — RESTful API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(rivers.router)
app.include_router(stations.router)
app.include_router(forecast.router)
app.include_router(alerts.router)
app.include_router(auth.router)
app.include_router(export.router)
app.include_router(reports.router)
app.include_router(ws.router)
app.include_router(admin.router)

# Mount static files (CSS, JS, images)
if os.path.exists(os.path.join(FRONTEND_DIR, "static")):
    app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_DIR, "static")), name="static")
if os.path.exists(os.path.join(FRONTEND_DIR, "geojson")):
    app.mount("/geojson", StaticFiles(directory=os.path.join(FRONTEND_DIR, "geojson")), name="geojson")


@app.on_event("startup")
def on_startup():
    """Seed database on first start"""
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


# ─── Frontend page routes ───
@app.get("/sw.js", include_in_schema=False)
def serve_sw():
    return FileResponse(os.path.join(FRONTEND_DIR, "sw.js"), media_type="application/javascript")

@app.get("/", include_in_schema=False)
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.get("/dashboard", include_in_schema=False)
def serve_dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, "dashboard.html"))


@app.get("/forecast", include_in_schema=False)
def serve_forecast():
    return FileResponse(os.path.join(FRONTEND_DIR, "forecast.html"))


@app.get("/alerts", include_in_schema=False)
def serve_alerts():
    return FileResponse(os.path.join(FRONTEND_DIR, "alerts.html"))


@app.get("/data", include_in_schema=False)
def serve_data():
    return FileResponse(os.path.join(FRONTEND_DIR, "data.html"))


@app.get("/login", include_in_schema=False)
def serve_login():
    return FileResponse(os.path.join(FRONTEND_DIR, "login.html"))


@app.get("/register", include_in_schema=False)
def serve_register():
    return FileResponse(os.path.join(FRONTEND_DIR, "register.html"))


@app.get("/profile", include_in_schema=False)
def serve_profile():
    return FileResponse(os.path.join(FRONTEND_DIR, "profile.html"))

@app.get("/reports", include_in_schema=False)
def serve_reports():
    return FileResponse(os.path.join(FRONTEND_DIR, "reports.html"))

@app.get("/admin", include_in_schema=False)
def serve_admin():
    return FileResponse(os.path.join(FRONTEND_DIR, "admin.html"))

# API info endpoints
@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "gimat-api"}
