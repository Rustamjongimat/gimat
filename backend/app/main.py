"""
GIMAT — FastAPI Main Application
Gidrologik Intellektual Monitoring va Axborot Tizimi
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse, Response
from .database import engine, SessionLocal, Base
from datetime import datetime
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


# ─── SEO: robots.txt ───
@app.get("/robots.txt", include_in_schema=False)
def serve_robots():
    content = """User-agent: *
Allow: /
Disallow: /admin
Disallow: /api/
Disallow: /profile

Sitemap: https://gimat.onrender.com/sitemap.xml
"""
    return PlainTextResponse(content=content.strip(), media_type="text/plain")


# ─── SEO: sitemap.xml ───
@app.get("/sitemap.xml", include_in_schema=False)
def serve_sitemap():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    pages = [
        {"loc": "/",          "priority": "1.0",  "changefreq": "daily"},
        {"loc": "/dashboard", "priority": "0.9",  "changefreq": "daily"},
        {"loc": "/forecast",  "priority": "0.8",  "changefreq": "daily"},
        {"loc": "/alerts",    "priority": "0.8",  "changefreq": "daily"},
        {"loc": "/data",      "priority": "0.7",  "changefreq": "weekly"},
        {"loc": "/reports",   "priority": "0.7",  "changefreq": "weekly"},
        {"loc": "/login",     "priority": "0.3",  "changefreq": "monthly"},
        {"loc": "/register",  "priority": "0.3",  "changefreq": "monthly"},
    ]
    base_url = "https://gimat.onrender.com"
    urls_xml = ""
    for p in pages:
        urls_xml += f"""
  <url>
    <loc>{base_url}{p['loc']}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{p['changefreq']}</changefreq>
    <priority>{p['priority']}</priority>
  </url>"""
    
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls_xml}
</urlset>"""
    return Response(content=xml.strip(), media_type="application/xml")


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
