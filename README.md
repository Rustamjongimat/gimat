# GIMAT — Gidrologik Intellektual Monitoring va Axborot Tizimi

🌊 **Gidrologik Intellektual Monitoring va Axborot Tizimi** — O'zbekiston daryolarining gidrologik ko'rsatkichlarini real vaqt rejimida kuzatuvchi zamonaviy veb-platforma.

## Xususiyatlar

- 🗺️ **Interaktiv xarita** — Leaflet.js bilan O'zbekiston daryolari va stansiyalari
- 📊 **Real-time dashboard** — Plotly.js bilan oqim, yog'in, harorat grafiklari  
- 🤖 **AI Prognoz** — LSTM+HBV gibrid neyron tarmoq modeli
- 🔔 **Toshqin ogohlantirish** — 3 darajali signal tizimi
- 🌍 **Ko'p tilli** — O'zbek, Rus, Ingliz
- 📥 **Ma'lumot eksport** — CSV/Excel

## Texnologiyalar

| Qism | Texnologiya |
|------|-------------|
| Backend | Python FastAPI |
| Database | SQLite (MVP) / PostgreSQL |
| Frontend | HTML5, CSS3, JavaScript |
| Xarita | Leaflet.js |
| Grafiklar | Plotly.js |
| AI Model | NumPy simulyatsiya |

## Ishga tushirish

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Brauzerda: **http://localhost:8000**

## API Docs

Swagger: **http://localhost:8000/api/docs**

## Muallif

**Nasridinov Rustamjon** — TATU, 2025
