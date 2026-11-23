{
const D = window.TM || {};
const COLORS = ['#A08D79', '#2B1D14', '#D46A26', '#8C3B12'];
const fmtPct = v => v == null ? 'n. v.' : (Math.round(v * 1000) / 10).toString().replace('.', ',') + ' %';
const fmtNum = v => v == null ? 'n. v.' : Math.round(v).toLocaleString('de-DE');
const LINE_NAMES = (D.meta || []).map(m => m.name);

// ---------- Navigation
const navBtn = document.querySelector('.nav-toggle'), nav = document.getElementById('nav');
if (navBtn && nav) navBtn.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  navBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
});

// ---------- Liniendiagramme
function drawChart(el) {
  const key = el.dataset.key, cfg = D.charts && D.charts[key];
  if (!cfg) return;
  const isPct = el.dataset.unit === '%';
  const W = el.clientWidth, H = el.clientHeight, small = false;
  const pl = small ? 44 : 58, pr = 16, pt = 14, pb = 32;
  const named = cfg.series.map((s, i) => ({ ...s, label: key === 'bi' ? s.name : LINE_NAMES[i] || s.name, color: key === 'bi' ? (i ? '#D46A26' : '#2B1D14') : COLORS[i] }));
  // Linien ohne Angebot (nur Nullen) ausblenden
  const shown = named.filter(s => s.values.some(v => v != null && v !== 0));
  const vals = shown.flatMap(s => s.values).filter(v => v != null);
  let lo = key === 'bi' ? Math.min(...vals) : 0, hi = Math.max(...vals);
  if (key === 'bi') { const pad = (hi - lo) * 0.12; lo -= pad; hi += pad; } else hi *= 1.08;
  const n = cfg.periods.length;
  const X = i => pl + (n === 1 ? 0 : i * (W - pl - pr) / (n - 1));
  const Y = v => pt + (hi - v) * (H - pt - pb) / (hi - lo || 1);
  const fmtAxis = v => isPct ? Math.round(v * 100) + ' %' : key === 'bi' ? v.toFixed(2).replace('.', ',') : Math.round(v).toLocaleString('de-DE');
  let s = '';
  for (let t = 0; t <= 4; t++) {
    const v = lo + (hi - lo) * t / 4, y = Y(v);
    s += `<line x1="${pl}" x2="${W - pr}" y1="${y}" y2="${y}" stroke="#E2D2B9"/><text x="${pl - 8}" y="${y + 4}" text-anchor="end" font-size="12" fill="#7D6B5A" font-family="JetBrains Mono, monospace">${fmtAxis(v)}</text>`;
  }
  if (key === 'bi') { const y = Y(1); s += `<line x1="${pl}" x2="${W - pr}" y1="${y}" y2="${y}" stroke="#A08D79" stroke-dasharray="4 4"/>`; }
  cfg.periods.forEach((p, i) => { if (!small || i % 2 === 0 || i === n - 1) s += `<text x="${X(i)}" y="${H - 8}" text-anchor="middle" font-size="12" fill="#7D6B5A" font-family="JetBrains Mono, monospace">${p}</text>`; });
  shown.forEach(se => {
    let d = '', pen = false;
    se.values.forEach((v, i) => { if (v == null) { pen = false; return; } d += (pen ? 'L' : 'M') + X(i) + ',' + Y(v) + ' '; pen = true; });
    s += `<path d="${d}" fill="none" stroke="${se.color}" stroke-width="${se.color === '#D46A26' ? 3.5 : 2.5}" stroke-linejoin="round"/>`;
    se.values.forEach((v, i) => { if (v != null) s += `<circle cx="${X(i)}" cy="${Y(v)}" r="${i === n - 1 ? 5 : 3.5}" fill="${se.color}"><title>${se.label}, ${cfg.periods[i]}: ${isPct ? fmtPct(v) : key === 'bi' ? v.toString().replace('.', ',') : fmtNum(v)}</title></circle>`; });
  });
  el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" aria-hidden="true">${s}</svg>`;
  const lg = document.getElementById(el.id + '-legend');
  if (lg) lg.innerHTML = shown.map(se => {
    const last = [...se.values].reverse().find(v => v != null);
    return `<span><i style="background:${se.color}"></i>${se.label}: ${isPct ? fmtPct(last) : key === 'bi' ? String(last).replace('.', ',') : fmtNum(last)}</span>`;
  }).join('') + (named.length > shown.length ? `<span>${named.filter(x => !shown.includes(x)).map(x => x.label).join(', ')}: nicht angeboten</span>` : '');
}
const charts = document.querySelectorAll('.fig[data-key]');
const chartObserver = new ResizeObserver(entries => entries.forEach(en => drawChart(en.target)));
charts.forEach(c => chartObserver.observe(c));
document.querySelectorAll('button[data-chart]').forEach(btn => btn.addEventListener('click', () => {
  const el = document.getElementById(btn.dataset.chart);
  el.dataset.key = btn.dataset.key;
  btn.parentElement.querySelectorAll('button').forEach(o => o.setAttribute('aria-pressed', o === btn ? 'true' : 'false'));
  drawChart(el);
}));

// ---------- Modellseite: Region und Periode
const modelsRoot = document.getElementById('models');
if (modelsRoot && D.regions) {
  let region = 'Region 1', period = D.fyPeriod;
  const regBtns = document.querySelectorAll('button[data-reg]'), perBtns = document.querySelectorAll('button[data-per]');
  const findP = (r, p) => D.regions[r].find(x => x.period === p);
  const meter = (label, v, base, mk) => {
    const has = v != null, dv = has && base != null ? v - base : null;
    const d = dv == null || dv === 0 ? '' : `<span class="d ${dv > 0 ? 'up' : 'dn'}">${dv > 0 ? '+' : '−'}${Math.abs(dv)}</span>`;
    return `<div class="meter${mk ? ' mk' : ''}"><div class="top"><span class="small">${label}</span><span class="num">${has ? v : 'n. v.'}${d}</span></div><div class="track"><div class="fill" style="width:${has ? v * 10 : 0}%"></div></div></div>`;
  };
  function render() {
    const rp = D.regions[region], first = rp[0].period;
    perBtns.forEach(b => { const p = +b.dataset.per; b.disabled = !findP(region, p); b.setAttribute('aria-pressed', p === period ? 'true' : 'false'); });
    const cur = findP(region, period), base = findP(region, first);
    modelsRoot.querySelectorAll('.model').forEach(art => {
      const i = +art.dataset.line, q = f => art.querySelector(`[data-f="${f}"]`);
      const sales = cur.budget.sales ? cur.budget.sales[i] : null, share = cur.budget.market_share ? cur.budget.market_share[i] : null;
      const off = !(sales === 0 && !share);
      q('reg').textContent = region; q('per').textContent = 'P' + period + (period === D.fyPeriod ? ' (' + D.fy + ')' : '');
      q('share').textContent = off ? fmtPct(share) : '–';
      q('sales').textContent = off ? fmtNum(sales) : '–';
      q('cmp').textContent = period === first ? '' : 'Δ ggü. P' + first;
      const crit = (list, mk) => list.map(c => meter(D.critDe[c], off ? cur.criteria[c][i] : null, period === first ? null : base.criteria[c][i], mk)).join('');
      q('eng').innerHTML = crit(D.eng, false); q('mkt').innerHTML = crit(D.mkt, true);
      const na = q('na'); na.hidden = off; na.textContent = off ? '' : `In ${region} wird der ${D.meta[i].name} in dieser Periode nicht angeboten.`;
    });
  }
  regBtns.forEach(b => b.addEventListener('click', () => {
    region = b.dataset.reg; regBtns.forEach(o => o.setAttribute('aria-pressed', o === b ? 'true' : 'false'));
    if (!findP(region, period)) period = D.fyPeriod;
    render();
  }));
  perBtns.forEach(b => b.addEventListener('click', () => { if (!b.disabled) { period = +b.dataset.per; render(); } }));
  render();
}

// ---------- Kontaktformular
const form = document.getElementById('contact');
if (form) {
  const params = new URLSearchParams(location.search), sel = form.querySelector('#thema');
  if (params.get('thema')) [...sel.options].forEach(o => { if (o.text === params.get('thema')) sel.value = o.text; });
  const to = { 'Investor Relations': 'ir', 'Presse': 'presse' };
  form.addEventListener('submit', ev => {
    ev.preventDefault();
    const notice = document.getElementById('notice');
    if (!form.checkValidity()) { notice.textContent = 'Bitte Name, gültige E-Mail und Nachricht angeben.'; return; }
    const box = (to[sel.value] || 'info') + '@tangerine-motors.example';
    const body = form.msg.value + '\n\n' + form.name.value + ' <' + form.mail.value + '>';
    location.href = 'mailto:' + box + '?subject=' + encodeURIComponent(sel.value + ' – Anfrage') + '&body=' + encodeURIComponent(body);
    notice.textContent = 'Ihr E-Mail-Programm wird geöffnet. Adresse: ' + box;
  });
}
}
