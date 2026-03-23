# -*- coding: utf-8 -*-
"""
GIMAT — PDF Report Generator
Generates PDF reports for hydrological data
"""
from io import BytesIO
from datetime import datetime


def generate_report_html(river_name, station_data, hydro_data, alerts):
    """Generate an HTML report that can be rendered as PDF"""

    # Calculate stats
    discharges = [d.discharge for d in hydro_data if d.discharge is not None]
    avg_discharge = sum(discharges) / len(discharges) if discharges else 0
    max_discharge = max(discharges) if discharges else 0
    min_discharge = min(discharges) if discharges else 0

    active_alerts = [a for a in alerts if a.is_active]
    danger_count = len([a for a in alerts if a.level == 'danger'])
    warning_count = len([a for a in alerts if a.level == 'warning'])

    stations_html = ""
    for s in station_data:
        stations_html += f"""
        <tr>
            <td>{s.name}</td>
            <td>{s.lat:.4f}, {s.lon:.4f}</td>
            <td>{s.elevation or '-'} m</td>
            <td>{s.status or 'active'}</td>
        </tr>"""

    recent_data_html = ""
    for d in hydro_data[-12:]:
        date_str = d.date.strftime('%Y-%m') if isinstance(d.date, datetime) else str(d.date)[:7]
        recent_data_html += f"""
        <tr>
            <td>{date_str}</td>
            <td><strong>{d.discharge:.1f}</strong></td>
            <td>{d.precipitation:.1f}</td>
            <td>{d.temperature:.1f}</td>
            <td>{d.snow_cover:.1f}</td>
            <td>{d.evaporation:.1f}</td>
        </tr>"""

    alerts_html = ""
    for a in alerts[:10]:
        level_color = '#EF4444' if a.level == 'danger' else '#F59E0B' if a.level == 'warning' else '#22C55E'
        sent_str = a.sent_at.strftime('%Y-%m-%d %H:%M') if isinstance(a.sent_at, datetime) else str(a.sent_at)
        alerts_html += f"""
        <tr>
            <td><span style="color:{level_color};font-weight:bold;">{a.level.upper()}</span></td>
            <td>{a.value:.1f} m3/s</td>
            <td>{a.threshold:.1f} m3/s</td>
            <td>{sent_str}</td>
            <td>{'Faol' if a.is_active else 'Tugagan'}</td>
        </tr>"""

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; color: #1a1a2e; line-height: 1.6; }}
            h1 {{ color: #1B4F8A; border-bottom: 3px solid #1B4F8A; padding-bottom: 10px; }}
            h2 {{ color: #334155; margin-top: 30px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 13px; }}
            th, td {{ border: 1px solid #e2e8f0; padding: 8px 12px; text-align: left; }}
            th {{ background: #f1f5f9; font-weight: 600; color: #334155; }}
            tr:nth-child(even) {{ background: #f8fafc; }}
            .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 16px 0; }}
            .stat-card {{ background: #f1f5f9; padding: 16px; border-radius: 8px; text-align: center; }}
            .stat-value {{ font-size: 24px; font-weight: 700; color: #1B4F8A; }}
            .stat-label {{ font-size: 12px; color: #64748B; margin-top: 4px; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
            .logo {{ font-size: 28px; font-weight: 800; color: #1B4F8A; }}
            .meta {{ font-size: 12px; color: #64748B; }}
            .footer {{ margin-top: 40px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 11px; color: #94A3B8; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div>
                <div class="logo">GIMAT</div>
                <div style="font-size:14px;color:#64748B;">Gidrologik Intellektual Monitoring va Axborot Tizimi</div>
            </div>
            <div class="meta">
                <div>Hisobot sanasi: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
                <div>TATU — 2025</div>
            </div>
        </div>

        <h1>{river_name} — Gidrologik Hisobot</h1>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{avg_discharge:.1f}</div>
                <div class="stat-label">O'rtacha oqim (m3/s)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{max_discharge:.1f}</div>
                <div class="stat-label">Maksimal oqim (m3/s)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{min_discharge:.1f}</div>
                <div class="stat-label">Minimal oqim (m3/s)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(station_data)}</div>
                <div class="stat-label">Stansiyalar soni</div>
            </div>
        </div>

        <h2>Monitoring stansiyalari</h2>
        <table>
            <thead><tr><th>Nomi</th><th>Koordinatalar</th><th>Balandlik</th><th>Holat</th></tr></thead>
            <tbody>{stations_html}</tbody>
        </table>

        <h2>So'nggi 12 oylik ma'lumotlar</h2>
        <table>
            <thead><tr><th>Sana</th><th>Oqim (m3/s)</th><th>Yog'in (mm)</th><th>Harorat (C)</th><th>Qor (%)</th><th>Bug'lanish (mm)</th></tr></thead>
            <tbody>{recent_data_html}</tbody>
        </table>

        <h2>Ogohlantirishlar ({danger_count} xavfli, {warning_count} ehtiyot)</h2>
        <table>
            <thead><tr><th>Daraja</th><th>Qiymat</th><th>Chegara</th><th>Vaqt</th><th>Holat</th></tr></thead>
            <tbody>{alerts_html if alerts_html else '<tr><td colspan="5" style="text-align:center;color:#94A3B8;">Ogohlantirishlar yo`q</td></tr>'}</tbody>
        </table>

        <div class="footer">
            GIMAT v1.0 — Nasridinov Rustamjon — Toshkent Axborot Texnologiyalari Universiteti (TATU) 2025
        </div>
    </body>
    </html>
    """
    return html
