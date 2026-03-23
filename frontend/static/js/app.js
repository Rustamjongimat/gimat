/**
 * GIMAT — Shared JavaScript Utilities
 * API client, i18n, auth helpers
 */
// API_BASE: empty when same origin (Render), or set via meta tag for Vercel
const API_BASE = document.querySelector('meta[name="api-base"]')?.content || '';

// ─── Translations ───
const TRANSLATIONS = {
  uz: {
    app_name: 'GIMAT',
    app_subtitle: 'Gidrologik Monitoring',
    nav_map: 'Xarita',
    nav_dashboard: 'Dashboard',
    nav_forecast: 'AI Prognoz',
    nav_alerts: 'Ogohlantirishlar',
    nav_data: "Ma'lumotlar",
    nav_reports: 'Hisobotlar',
    nav_login: 'Kirish',
    nav_profile: 'Profil',
    nav_section_main: 'Asosiy',
    nav_section_analytics: 'Tahlillar',
    nav_section_account: 'Hisob',
    map_title: "Interaktiv Xarita",
    dashboard_title: 'Monitoring Dashboard',
    forecast_title: 'AI Prognoz',
    alerts_title: 'Ogohlantirishlar',
    data_title: "Ma'lumotlar",
    station: 'Stansiya',
    river: 'Daryo',
    discharge: 'Oqim (m³/s)',
    precipitation: "Yog'in (mm)",
    temperature: 'Harorat (°C)',
    snow_cover: 'Qor qoplami (%)',
    evaporation: "Bug'lanish (mm)",
    date: 'Sana',
    status: 'Holat',
    level_normal: 'Normal',
    level_warning: 'Ehtiyot',
    level_danger: 'Xavfli',
    months: ['Yan','Fev','Mar','Apr','May','Iyun','Iyul','Avg','Sen','Okt','Noy','Dek'],
    export_csv: 'CSV yuklab olish',
    export_excel: 'Excel yuklab olish',
    forecast_months: 'Prognoz muddati (oy)',
    run_forecast: 'Prognozni ishga tushirish',
    model_hybrid: 'Gibrid (LSTM+HBV)',
    model_lstm: 'LSTM',
    model_hbv: 'HBV',
    metrics: 'Metrikalar',
    confidence_interval: '95% ishonch oralig\'i',
    legend: 'Izoh',
    active_alerts: 'Faol ogohlantirishlar',
    period_1m: '1 oy',
    period_6m: '6 oy',
    period_1y: '1 yil',
    period_all: 'Barchasi',
    login: 'Kirish',
    register: "Ro'yxatdan o'tish",
    email: 'Email',
    password: 'Parol',
    name: 'Ism',
    loading: 'Yuklanmoqda...',
    no_data: "Ma'lumot topilmadi",
    avg: "O'rtacha",
    max: 'Maksimum',
    min: 'Minimum',
    std: 'Standart chetlanish',
    error: 'Xatolik yuz berdi'
  },
  ru: {
    app_name: 'ГИМАТ',
    app_subtitle: 'Гидрологический мониторинг',
    nav_map: 'Карта',
    nav_dashboard: 'Дашборд',
    nav_forecast: 'ИИ Прогноз',
    nav_alerts: 'Оповещения',
    nav_data: 'Данные',
    nav_reports: 'Отчёты',
    nav_login: 'Войти',
    nav_profile: 'Профиль',
    nav_section_main: 'Основное',
    nav_section_analytics: 'Аналитика',
    nav_section_account: 'Аккаунт',
    map_title: 'Интерактивная карта',
    dashboard_title: 'Панель мониторинга',
    forecast_title: 'ИИ Прогноз',
    alerts_title: 'Оповещения',
    data_title: 'Данные',
    station: 'Станция',
    river: 'Река',
    discharge: 'Расход (м³/с)',
    precipitation: 'Осадки (мм)',
    temperature: 'Температура (°C)',
    snow_cover: 'Снежный покров (%)',
    evaporation: 'Испарение (мм)',
    date: 'Дата',
    status: 'Статус',
    level_normal: 'Нормально',
    level_warning: 'Внимание',
    level_danger: 'Опасность',
    months: ['Янв','Фев','Мар','Апр','Май','Июн','Июл','Авг','Сен','Окт','Ноя','Дек'],
    export_csv: 'Скачать CSV',
    export_excel: 'Скачать Excel',
    forecast_months: 'Период прогноза (мес)',
    run_forecast: 'Запустить прогноз',
    model_hybrid: 'Гибрид (LSTM+HBV)',
    model_lstm: 'LSTM',
    model_hbv: 'HBV',
    metrics: 'Метрики',
    confidence_interval: '95% доверительный интервал',
    legend: 'Легенда',
    active_alerts: 'Активные оповещения',
    period_1m: '1 мес',
    period_6m: '6 мес',
    period_1y: '1 год',
    period_all: 'Все',
    login: 'Войти',
    register: 'Регистрация',
    email: 'Email',
    password: 'Пароль',
    name: 'Имя',
    loading: 'Загрузка...',
    no_data: 'Данные не найдены',
    avg: 'Среднее',
    max: 'Максимум',
    min: 'Минимум',
    std: 'Стандартное отклонение',
    error: 'Произошла ошибка'
  },
  en: {
    app_name: 'GIMAT',
    app_subtitle: 'Hydrological Monitoring',
    nav_map: 'Map',
    nav_dashboard: 'Dashboard',
    nav_forecast: 'AI Forecast',
    nav_alerts: 'Alerts',
    nav_data: 'Data',
    nav_reports: 'Reports',
    nav_login: 'Login',
    nav_profile: 'Profile',
    nav_section_main: 'Main',
    nav_section_analytics: 'Analytics',
    nav_section_account: 'Account',
    map_title: 'Interactive Map',
    dashboard_title: 'Monitoring Dashboard',
    forecast_title: 'AI Forecast',
    alerts_title: 'Alerts',
    data_title: 'Data',
    station: 'Station',
    river: 'River',
    discharge: 'Discharge (m³/s)',
    precipitation: 'Precipitation (mm)',
    temperature: 'Temperature (°C)',
    snow_cover: 'Snow Cover (%)',
    evaporation: 'Evaporation (mm)',
    date: 'Date',
    status: 'Status',
    level_normal: 'Normal',
    level_warning: 'Warning',
    level_danger: 'Danger',
    months: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    export_csv: 'Download CSV',
    export_excel: 'Download Excel',
    forecast_months: 'Forecast period (months)',
    run_forecast: 'Run Forecast',
    model_hybrid: 'Hybrid (LSTM+HBV)',
    model_lstm: 'LSTM',
    model_hbv: 'HBV',
    metrics: 'Metrics',
    confidence_interval: '95% Confidence Interval',
    legend: 'Legend',
    active_alerts: 'Active alerts',
    period_1m: '1 month',
    period_6m: '6 months',
    period_1y: '1 year',
    period_all: 'All',
    login: 'Login',
    register: 'Register',
    email: 'Email',
    password: 'Password',
    name: 'Name',
    loading: 'Loading...',
    no_data: 'No data found',
    avg: 'Average',
    max: 'Maximum',
    min: 'Minimum',
    std: 'Std Deviation',
    error: 'An error occurred'
  }
};

// ─── i18n ───
let currentLang = localStorage.getItem('gimat-lang') || 'uz';

function t(key) {
  return TRANSLATIONS[currentLang]?.[key] || TRANSLATIONS['en']?.[key] || key;
}

function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem('gimat-lang', lang);
  // Update all translatable elements
  document.querySelectorAll('[data-i18n]').forEach(el => {
    el.textContent = t(el.dataset.i18n);
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    el.placeholder = t(el.dataset.i18nPlaceholder);
  });
  // Update language selector
  const langSelect = document.getElementById('lang-select');
  if (langSelect) langSelect.value = currentLang;
}

// ─── API Client ───
async function apiGet(path) {
  try {
    const headers = {};
    const token = localStorage.getItem('gimat-token');
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const res = await fetch(`${API_BASE}${path}`, { headers });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error('API Error:', err);
    return null;
  }
}

async function apiPost(path, data) {
  try {
    const headers = { 'Content-Type': 'application/json' };
    const token = localStorage.getItem('gimat-token');
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const res = await fetch(`${API_BASE}${path}`, {
      method: 'POST',
      headers,
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || `HTTP ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.error('API Error:', err);
    throw err;
  }
}

// ─── Auth ───
function isLoggedIn() {
  return !!localStorage.getItem('gimat-token');
}

function getUser() {
  const user = localStorage.getItem('gimat-user');
  return user ? JSON.parse(user) : null;
}

function logout() {
  localStorage.removeItem('gimat-token');
  localStorage.removeItem('gimat-user');
  window.location.href = '/login';
}

// ─── Helpers ───
function formatNumber(n, decimals = 1) {
  if (n === null || n === undefined) return '—';
  return Number(n).toFixed(decimals);
}

function formatDate(dateStr) {
  if (!dateStr) return '—';
  const d = new Date(dateStr);
  return d.toLocaleDateString(currentLang === 'uz' ? 'uz-UZ' : currentLang === 'ru' ? 'ru-RU' : 'en-US');
}

function alertLevelClass(level) {
  switch (level) {
    case 'danger': return 'badge-danger';
    case 'warning': return 'badge-warning';
    default: return 'badge-normal';
  }
}

function alertLevelText(level) {
  switch (level) {
    case 'danger': return t('level_danger');
    case 'warning': return t('level_warning');
    default: return t('level_normal');
  }
}

// ─── Generate Sidebar HTML ───
function generateSidebar(activePage) {
  const user = getUser();
  return `
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-logo">
      <div class="logo-icon">🌊</div>
      <div>
        <h1>GIMAT</h1>
        <div class="version">v1.0 — TATU 2025</div>
      </div>
    </div>
    <nav class="sidebar-nav">
      <div class="nav-section">
        <div class="nav-section-title" data-i18n="nav_section_main">${t('nav_section_main')}</div>
        <a href="/" class="nav-link ${activePage === 'map' ? 'active' : ''}">
          <span class="icon">🗺️</span>
          <span data-i18n="nav_map">${t('nav_map')}</span>
        </a>
        <a href="/dashboard" class="nav-link ${activePage === 'dashboard' ? 'active' : ''}">
          <span class="icon">📊</span>
          <span data-i18n="nav_dashboard">${t('nav_dashboard')}</span>
        </a>
      </div>
      <div class="nav-section">
        <div class="nav-section-title" data-i18n="nav_section_analytics">${t('nav_section_analytics')}</div>
        <a href="/forecast" class="nav-link ${activePage === 'forecast' ? 'active' : ''}">
          <span class="icon">🤖</span>
          <span data-i18n="nav_forecast">${t('nav_forecast')}</span>
        </a>
        <a href="/alerts" class="nav-link ${activePage === 'alerts' ? 'active' : ''}">
          <span class="icon">🔔</span>
          <span data-i18n="nav_alerts">${t('nav_alerts')}</span>
          <span class="badge" id="alert-count">3</span>
        </a>
        <a href="/data" class="nav-link ${activePage === 'data' ? 'active' : ''}">
          <span class="icon">📁</span>
          <span data-i18n="nav_data">${t('nav_data')}</span>
        </a>
      </div>
      <div class="nav-section">
        <div class="nav-section-title" data-i18n="nav_section_account">${t('nav_section_account')}</div>
        ${user ? `
        <a href="/profile" class="nav-link ${activePage === 'profile' ? 'active' : ''}">
          <span class="icon">👤</span>
          <span data-i18n="nav_profile">${t('nav_profile')}</span>
        </a>
        <a href="#" onclick="logout()" class="nav-link">
          <span class="icon">🚪</span>
          <span>Chiqish</span>
        </a>
        ` : `
        <a href="/login" class="nav-link ${activePage === 'login' ? 'active' : ''}">
          <span class="icon">🔑</span>
          <span data-i18n="nav_login">${t('nav_login')}</span>
        </a>
        `}
      </div>
    </nav>
  </aside>`;
}

function generateHeader(pageTitle, pageTitleKey) {
  return `
  <header class="header">
    <div class="header-left">
      <button class="header-btn" id="menu-toggle" onclick="toggleSidebar()" style="display:none;">☰</button>
      <h2 data-i18n="${pageTitleKey}">${pageTitle}</h2>
    </div>
    <div class="header-right">
      <select class="lang-select" id="lang-select" onchange="setLanguage(this.value)">
        <option value="uz" ${currentLang === 'uz' ? 'selected' : ''}>🇺🇿 O'zbekcha</option>
        <option value="ru" ${currentLang === 'ru' ? 'selected' : ''}>🇷🇺 Русский</option>
        <option value="en" ${currentLang === 'en' ? 'selected' : ''}>🇬🇧 English</option>
      </select>
      <div class="header-btn" style="font-size: 11px; color: var(--text-muted);">
        <span style="display:inline-block;width:8px;height:8px;background:var(--success);border-radius:50%;"></span>
        Online
      </div>
    </div>
  </header>`;
}

function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}

// ─── Responsive sidebar ───
function initResponsive() {
  const checkWidth = () => {
    const btn = document.getElementById('menu-toggle');
    if (window.innerWidth <= 768) {
      if (btn) btn.style.display = 'flex';
    } else {
      if (btn) btn.style.display = 'none';
      const sidebar = document.getElementById('sidebar');
      if (sidebar) sidebar.classList.remove('open');
    }
  };
  window.addEventListener('resize', checkWidth);
  checkWidth();
}

// ─── Plotly dark theme ───
const PLOTLY_LAYOUT = {
  paper_bgcolor: 'rgba(0,0,0,0)',
  plot_bgcolor: 'rgba(0,0,0,0)',
  font: { family: 'Inter, sans-serif', color: '#94A3B8', size: 12 },
  margin: { t: 40, r: 20, b: 40, l: 60 },
  xaxis: {
    gridcolor: 'rgba(255,255,255,0.05)',
    linecolor: 'rgba(255,255,255,0.1)',
    zerolinecolor: 'rgba(255,255,255,0.05)'
  },
  yaxis: {
    gridcolor: 'rgba(255,255,255,0.05)',
    linecolor: 'rgba(255,255,255,0.1)',
    zerolinecolor: 'rgba(255,255,255,0.05)'
  },
  legend: { bgcolor: 'rgba(0,0,0,0)', font: { color: '#94A3B8' } },
  hoverlabel: { bgcolor: '#1A2332', bordercolor: '#334155', font: { color: '#F1F5F9', family: 'Inter' } }
};

const PLOTLY_CONFIG = { responsive: true, displayModeBar: false };
