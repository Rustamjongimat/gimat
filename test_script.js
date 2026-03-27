
document.getElementById('app').innerHTML = `
  ${generateSidebar('reports')}
  <div class="main-content">
    ${generateHeader(t('nav_reports'), 'nav_reports')}
    <div class="page-content">
      
      <!-- Report Generator Form -->
      <div class="card mb-24 no-print">
        <div class="card-header">
          <h3 class="card-title">🖨️ Hisobot Parametrlari</h3>
          <button class="btn btn-danger btn-sm" onclick="window.print()" id="printBtn" style="display:none;">📄 PDF ga chop etish (Print)</button>
        </div>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:12px; align-items: end;">
          <div class="form-group" style="margin:0;">
            <label class="form-label">${t('river')}</label>
            <select class="form-select" id="report-river"></select>
          </div>
          <div class="form-group" style="margin:0;">
            <label class="form-label">Boshlanish</label>
            <input type="date" class="form-input" id="report-start" value="2023-01-01">
          </div>
          <div class="form-group" style="margin:0;">
            <label class="form-label">Tugash</label>
            <input type="date" class="form-input" id="report-end" value="2024-12-31">
          </div>
          <div class="form-group" style="margin:0;">
            <button class="btn btn-primary" style="width:100%;" onclick="generateReport()">Hisobot yaratish</button>
          </div>
        </div>
      </div>
      
      <!-- Built Report Display -->
      <div class="a4-wrapper" id="report-wrapper" style="display:none;">
        <div class="a4-page" id="printable-report">
          
          <div class="report-header">
            <h2>O'ZBEKISTON RESPUBLIKASI GIDROMETEOROLOGIYA XIZMATI</h2>
            <h3>Gidrologik Intellektual Monitoring (GIMAT) tizimi tahlili</h3>
          </div>
          
          <div class="report-title">
            <span id="rep-river-name">___</span> DARYOSI BO'YICHA RASMIY HISOBOT
          </div>
          
          <div class="report-info">
            <b>1. Tayyorlangan sana:</b> <span id="rep-today">___</span><br>
            <b>2. Tahlil davri:</b> <span id="rep-period">___</span><br>
            <b>3. Ma'sul stansiya hududi:</b> Kuzatuv tarmog'i bo'ylab umumlashtirilgan indikatorlar.<br>
            <b>4. Asosiy maqsad:</b> Daryo suv sathi va iqlim o'zgarishlarining miqdoriy tahlili.
          </div>
          
          <h4 style="margin-bottom:12px; font-size:15px;">5. Asosiy ko'rsatkichlar jadvali (Monitoring natijalari)</h4>
          <table class="report-table">
            <thead>
              <tr>
                <th>Ko'rsatkich</th>
                <th>O'rtacha qiymat</th>
                <th>Maksimum (Toshqin xavfi)</th>
                <th>Minimum (Qurg'oqchilik)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Oqim sarfi (m³/s)</td>
                <td id="rep-avg-disc">0</td>
                <td id="rep-max-disc">0</td>
                <td id="rep-min-disc">0</td>
              </tr>
              <tr>
                <td>Yog'ingarchilik (mm)</td>
                <td id="rep-avg-prec">0</td>
                <td id="rep-max-prec">0</td>
                <td id="rep-min-prec">0</td>
              </tr>
              <tr>
                <td>Harorat (°C)</td>
                <td id="rep-avg-temp">0</td>
                <td id="rep-max-temp">0</td>
                <td id="rep-min-temp">0</td>
              </tr>
            </tbody>
          </table>
          
          <h4 style="margin-bottom:12px; font-size:15px;">6. Suv sathi dinamikasi grafigi</h4>
          <div id="report-chart" style="width:100%; height:300px; border:1px solid #ccc; margin-bottom:24px;"></div>
          
          <div class="report-info">
            <b>Xulosa (Intellektual analiz):</b> <br>
            <span id="rep-conclusion">Yuqoridagi ma'lumotlar tahlil qilinganda...</span>
          </div>
          
          <div class="report-signatures">
            <div class="signature-block">
              Tayyorladi:<br>
              Analitik-operator / Tizim Dasturchisi<br>
              <div class="signature-line"></div>
            </div>
            <div class="signature-block">
              Tasdiqladi:<br>
              Bo'lim boshlig'i<br>
              <div class="signature-line"></div>
            </div>
          </div>
          
        </div>
      </div>

    </div>
  </div>
`;
initResponsive();

let rivers = [];

async function init() {
  rivers = await apiGet('/api/rivers') || [];
  const select = document.getElementById('report-river');
  select.innerHTML = rivers.map(r => {
    const name = r[`name_${currentLang}`] || r.name;
    return `<option value="${r.id}">${name}</option>`;
  }).join('');
  
  const today = new Date().toISOString().split('T')[0];
  document.getElementById('rep-today').textContent = today;
}

async function generateReport() {
  const btn = event.target;
  const original = btn.textContent;
  btn.textContent = "Kuting...";
  btn.disabled = true;
  
  try {
    const riverId = document.getElementById('report-river').value;
    const start = document.getElementById('report-start').value;
    const end = document.getElementById('report-end').value;
    
    // Fetch data
    let url = `/api/rivers/${riverId}/data?limit=5000`;
    if (start) url += `&start_date=${start}`;
    if (end) url += `&end_date=${end}`;
    
    const data = await apiGet(url) || [];
    if (data.length === 0) {
      alert("Bu davr uchun ma'lumot topilmadi.");
      return;
    }
    
    // Calculate Stats
    const discharges = data.map(d => d.discharge).filter(v => v != null);
    const precips = data.map(d => d.precipitation).filter(v => v != null);
    const temps = data.map(d => d.temperature).filter(v => v != null);
    
    const calc = (arr) => {
      if(arr.length === 0) return {avg:0, max:0, min:0};
      return {
        avg: (arr.reduce((a,b)=>a+b,0)/arr.length).toFixed(2),
        max: Math.max(...arr).toFixed(2),
        min: Math.min(...arr).toFixed(2)
      };
    };
    
    const dStats = calc(discharges);
    const pStats = calc(precips);
    const tStats = calc(temps);
    
    // Populate simple texts
    const riverObj = rivers.find(r => r.id == riverId);
    const riverName = riverObj ? (riverObj[`name_${currentLang}`] || riverObj.name) : '---';
    document.getElementById('rep-river-name').textContent = riverName.toUpperCase();
    document.getElementById('rep-period').textContent = `${start} dan ${end} gacha`;
    
    document.getElementById('rep-avg-disc').textContent = dStats.avg;
    document.getElementById('rep-max-disc').textContent = dStats.max;
    document.getElementById('rep-min-disc').textContent = dStats.min;
    
    document.getElementById('rep-avg-prec').textContent = pStats.avg;
    document.getElementById('rep-max-prec').textContent = pStats.max;
    document.getElementById('rep-min-prec').textContent = pStats.min;
    
    document.getElementById('rep-avg-temp').textContent = tStats.avg;
    document.getElementById('rep-max-temp').textContent = tStats.max;
    document.getElementById('rep-min-temp').textContent = tStats.min;
    
    let conclusion = `Tahlil davomida jami ${data.length} kunlik real ma'lumotlar o'rganildi. `;
    if (dStats.max > dStats.avg * 2) {
      conclusion += `O'rtacha suv sarfi doimiy bo'lsa-da (${dStats.avg} m³/s), davr ichida ${dStats.max} m³/s gacha xavfli maksimal oqish tasdiqlandi. Bu toshqin xavfini keltirib chiqarishi mumkin bo'lgan jiddiy burilishdir.`;
    } else {
      conclusion += `Daryo deyarli uzluksiz sokin rejimda oqmoqda. Suv sathining xavfli ko'tarilishi yoki favquloddagi qurg'oqchilik anomal holda kuzatilmadi.`;
    }
    document.getElementById('rep-conclusion').textContent = conclusion;
    
    // Plot Chart
    data.sort((a,b) => new Date(a.date) - new Date(b.date));
    const dates = data.map(d => d.date.split('T')[0]);
    const values = data.map(d => d.discharge);
    
    // We strictly define layout for light print format
    const trace = { x: dates, y: values, type: 'scatter', mode: 'lines', line: { color: '#2563EB', width: 2 }};
    const layout = {
      margin: { t: 20, r: 20, b: 40, l: 50 },
      paper_bgcolor: 'white',
      plot_bgcolor: 'white',
      font: { color: 'black' },
      xaxis: { gridcolor: '#e5e7eb' },
      yaxis: { gridcolor: '#e5e7eb', title: 'Oqim sarfi (m³/s)' },
      showlegend: false
    };
    
    Plotly.newPlot('report-chart', [trace], layout, {staticPlot: true});
    
    // Show UI
    document.getElementById('report-wrapper').style.display = 'flex';
    document.getElementById('printBtn').style.display = 'inline-block';
    
  } catch(err) {
    alert("Xatolik: " + err.message);
  } finally {
    btn.textContent = original;
    btn.disabled = false;
  }
}

init();

