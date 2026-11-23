"""Erzeugt die statischen Seiten von Tangerine Motors.
Aufruf:  python3 _build/build.py   (aus dem Repo-Stammordner)
Inhalte und Zahlen stehen in _build/data.py."""
import os, html
from data import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = html.escape

def de(x, fmt):
    """Zahl im deutschen Format; nur der Zahlenteil wird umgestellt, die Einheit bleibt unverändert."""
    i = fmt.index("}") + 1
    num = fmt[:i].format(x).replace(",", "X").replace(".", ",").replace("X", ".")
    return num + fmt[i:]

LOGO = ('<svg class="mark" viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="18" r="12" fill="#FF7A45"/>'
        '<circle cx="16" cy="18" r="12" fill="none" stroke="#12140F" stroke-opacity=".25" stroke-width="1"/>'
        '<path d="M16 6 C16 3 18 1.5 21 1.5 C22 4.5 20 7 16 7 Z" fill="#C5F442"/><path d="M16 6.5 V9" stroke="#12140F" stroke-width="1.6" stroke-linecap="round"/>'
        '<path d="M10 15 a7 7 0 0 1 5 -4" stroke="#fff" stroke-opacity=".55" stroke-width="1.6" fill="none" stroke-linecap="round"/></svg>')

NAV = [("index.html", "Start"), ("modelle.html", "Modelle"), ("unternehmen.html", "Unternehmen"),
       ("investor-relations.html", "Investor Relations"), ("presse.html", "Presse")]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400..700&family=DM+Sans:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">')

def page(fname, title, desc, body):
    nav = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == fname else ""}>{t}</a></li>' for h, t in NAV)
    nav += '<li><a class="cta" href="kontakt.html">Kontakt</a></li>'
    doc = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0D0E0C">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="skip" href="#main">Zum Inhalt springen</a>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Tangerine Motors – Startseite">{LOGO}<span>Tangerine Motors</span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Menü</button>
    <nav aria-label="Hauptnavigation"><ul class="nav" id="nav">{nav}</ul></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="cols">
      <div class="stack">
        <a class="brand" href="index.html">{LOGO}<span>Tangerine Motors</span></a>
        <p class="small">{e(COMPANY['claim'])} Low Cost, Family, Eco-Friendly und Image – in zwei Regionen.</p>
      </div>
      <div><p class="label">Modelle</p><ul>{''.join(f'<li><a href="modelle.html#{m["id"]}">{e(m["name"])}</a></li>' for m in MODELS)}</ul></div>
      <div><p class="label">Investoren</p><ul><li><a href="investor-relations.html#kennzahlen">Kennzahlen</a></li><li><a href="investor-relations.html#segmente">Segmente</a></li><li><a href="investor-relations.html#kalender">Finanzkalender</a></li><li><a href="investor-relations.html#berichte">Berichte</a></li></ul></div>
      <div><p class="label">Unternehmen</p><ul><li><a href="unternehmen.html">Strategie</a></li><li><a href="unternehmen.html#vorstand">Vorstand</a></li><li><a href="presse.html">Presse</a></li><li><a href="kontakt.html">Kontakt</a></li></ul></div>
    </div>
    <div class="legal"><span>© 2026 Tangerine Motors · <a href="impressum.html">Impressum</a> · <a href="impressum.html#datenschutz">Datenschutz</a></span><span>Fiktives Unternehmen (Customer Value Challenge). Alle Kennzahlen sind Beispielwerte.</span></div>
  </div>
</footer>
<script src="assets/site.js"></script>
</body>
</html>
"""
    open(os.path.join(ROOT, fname), "w", encoding="utf-8").write(doc)

def car(kind, alt):
    return f'<img class="car" src="assets/cars/{kind}.svg" alt="{e(alt)}" loading="lazy" width="260" height="91">'

def kpi_tiles(n=6):
    out = []
    for k in KPIS[:n]:
        up = k["final"] > k["start"]
        good = up == (k["better"] == "up")
        chg = (k["final"] / k["start"] - 1) * 100
        out.append(f'<div class="item kpi"><p class="label">{e(k["label"])}</p><p class="big">{e(de(k["final"], k["fmt"]))}</p>'
                   f'<p class="small">Start {e(de(k["start"], k["fmt"]))} · <span class="delta{"" if good else " neg"}">{"+" if chg>0 else "−"}{de(abs(chg), "{:.0f}")} %</span></p></div>')
    return "".join(out)

def line_chart(series, unit, fmt, w=900, h=320, zero=False):
    pad_l, pad_r, pad_t, pad_b = 64, 24, 24, 44
    vals = [v for _, v in series]
    lo, hi = min(vals + ([0] if zero else [])), max(vals)
    span = hi - lo or 1
    lo -= span * 0.08; hi += span * 0.08
    X = lambda i: pad_l + i * (w - pad_l - pad_r) / (len(series) - 1)
    Y = lambda v: pad_t + (hi - v) * (h - pad_t - pad_b) / (hi - lo)
    grid = ""
    for t in range(5):
        v = lo + (hi - lo) * t / 4
        grid += f'<line x1="{pad_l}" x2="{w-pad_r}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="#23261F"/><text x="{pad_l-12}" y="{Y(v)+5:.1f}" text-anchor="end" fill="#777D72" font-family="JetBrains Mono, Courier New, monospace" font-size="13">{e(de(v, fmt))}</text>'
    if zero and lo < 0:
        grid += f'<line x1="{pad_l}" x2="{w-pad_r}" y1="{Y(0):.1f}" y2="{Y(0):.1f}" stroke="#5E7A1E" stroke-dasharray="4 4"/>'
    pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, (_, v) in enumerate(series))
    area = f"M{X(0):.1f},{h-pad_b} L" + " L".join(f"{X(i):.1f},{Y(v):.1f}" for i, (_, v) in enumerate(series)) + f" L{X(len(series)-1):.1f},{h-pad_b} Z"
    labels = "".join(f'<text x="{X(i):.1f}" y="{h-14}" text-anchor="middle" fill="#A4AA9F" font-family="JetBrains Mono, Courier New, monospace" font-size="13">{p}</text>' for i, (p, _) in enumerate(series))
    dots = "".join(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="{6 if i==len(series)-1 else 4}" fill="{"#C5F442" if v>=0 else "#FF7A45"}"><title>{p}: {e(de(v, fmt))} {unit}</title></circle>' for i, (p, v) in enumerate(series))
    lv = series[-1][1]
    end = f'<text x="{X(len(series)-1)-10:.1f}" y="{Y(lv)-14:.1f}" text-anchor="end" fill="#C5F442" font-family="JetBrains Mono, Courier New, monospace" font-size="16" font-weight="600">{e(de(lv, fmt))} {unit}</text>'
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Verlauf {series[0][0]} bis {series[-1][0]}">'
            f'<defs><linearGradient id="ga{unit[:1]}{w}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C5F442" stop-opacity=".22"/><stop offset="1" stop-color="#C5F442" stop-opacity="0"/></linearGradient></defs>'
            f'{grid}<path d="{area}" fill="url(#ga{unit[:1]}{w})"/><polyline points="{pts}" fill="none" stroke="#C5F442" stroke-width="3" stroke-linejoin="round"/>{dots}{labels}{end}</svg>')

def segment_bars(key, w=900):
    rows = SEGMENTS
    mx = max(r[key] for r in rows)
    bh, gap, lw = 46, 22, 190
    h = len(rows) * (bh + gap)
    out = ""
    for i, r in enumerate(rows):
        y = i * (bh + gap)
        bw = (w - lw - 140) * r[key] / mx
        out += (f'<text x="0" y="{y+20}" fill="#ECEEE8" font-family="Space Grotesk, Arial, sans-serif" font-size="19" font-weight="600">{e(r["model"])}</text>'
                f'<text x="0" y="{y+40}" fill="#A4AA9F" font-family="JetBrains Mono, Courier New, monospace" font-size="13">{e(r["line"].upper())}</text>'
                f'<rect x="{lw}" y="{y}" width="{w-lw-140}" height="{bh}" rx="23" fill="#1C2410"/>'
                f'<rect x="{lw}" y="{y}" width="{bw:.1f}" height="{bh}" rx="23" fill="#C5F442"/>'
                f'<text x="{w}" y="{y+29}" text-anchor="end" fill="#C5F442" font-family="JetBrains Mono, Courier New, monospace" font-size="18" font-weight="600">{r[key]} Mio. €</text>')
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{"Umsatz" if key=="revenue" else "EBIT"} je Fahrzeuglinie">{out}</svg>'

# ---------------------------------------------------------------- Startseite
def build_index():
    ticker = "".join(f'<div class="item"><p class="label">{e(k["label"])}</p><p class="val">{e(de(k["final"], k["fmt"]))}</p></div>' for k in KPIS[:4])
    cards = "".join(f'''<a class="model-card" href="modelle.html#{m["id"]}">
<p class="label">{e(m["line"])}</p><h3>{e(m["name"])}</h3>{car(m["car"], m["name"] + ", Seitenansicht")}
<p class="small">{e(m["tagline"])}</p><p class="more">{e(m["price"])} →</p></a>''' for m in MODELS)
    total = sum(s["revenue"] for s in SEGMENTS)
    bar = "".join(f'<div class="seg" style="flex:{s["revenue"]}">{round(s["revenue"]/total*100)} %<span>{e(s["line"])}</span></div>' for s in SEGMENTS)
    under = "".join(f'<div class="item" style="flex:{s["revenue"]}"><h3>{e(s["line"])}</h3><p class="small">{e(s["model"])}</p></div>' for s in SEGMENTS)
    news = "".join(f'<li><span class="date">{d}</span><span>{e(t)}</span><span class="tag">{e(c)}</span></li>' for d, c, t in NEWS)
    body = f"""
<section class="dark hero">
  <div class="wrap">
    <p class="eyebrow">Tangerine Motors</p>
    <h1>Vier Fahrzeuglinien.<br>Eine Kapitalstrategie.</h1>
    <p class="sub">Wir verschieben Kapital in die Wachstumslinien: Marktführer bei Eco-Friendly, Kostenführer bei Low Cost, Preisführer bei Image – finanziert vom Family-Segment.</p>
    <div class="actions"><a class="btn" href="modelle.html">Modelle entdecken</a><a class="btn ghost" href="investor-relations.html">Investor Relations</a></div>
    <img class="car" src="assets/cars/coupe.svg" alt="Sanguine GT, Seitenansicht" width="520" height="182">
    <div class="road" aria-hidden="true"></div>
    <div class="ticker">{ticker}</div>
    <p class="small" style="margin-top:18px">Periode {COMPANY['final_period']} · <span class="flag">Beispielwerte</span></p>
  </div>
</section>

<section>
  <div class="wrap">
    <p class="eyebrow">Modelle</p>
    <h2>Für jeden Kunden genau das, wofür er bezahlt</h2>
    <div class="models">{cards}</div>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <p class="eyebrow">Portfolio</p>
    <h2>Umsatzmix nach Fahrzeuglinie: {total} Mio. € in {COMPANY['final_period']}</h2>
    <div class="bar" role="img" aria-label="Umsatzanteile je Linie">{bar}</div>
    <div class="under">{under}</div>
    <div class="grid3 mt">
      <div class="item"><p class="label">Start / {COMPANY['start_period']}</p><h3>Sechs identische Unternehmen</h3><p class="small">Family und Image verdienten Geld, Low Cost und Eco-Friendly verloren Geld. Das gemeinsame EBIT der vier Linien war leicht negativ.</p></div>
      <div class="hl"><p class="label" style="color:var(--lime)">Unsere Strategie</p><h3>Kapital in die Wachstumslinien</h3><p class="small">Eco-Friendly zur Marktführerschaft, Low Cost zum Kostenführer, Image über den Preis wachsen lassen – Family als Cash Cow finanziert den Umbau.</p></div>
      <div class="item"><p class="label">Heute / {COMPANY['final_period']}</p><h3>EBIT {EBIT_SERIES[-1][1]} Mio. €, ROCE {de(KPIS[2]['final'], '{:.1f}')} %</h3><p class="small">Aus einem operativen Verlust wurde ein positives Ergebnis – trotz Fusion und Rezession.</p></div>
    </div>
  </div>
</section>

<section class="accent">
  <div class="wrap row" style="align-items:center">
    <div>
      <p class="eyebrow">Investor Relations</p>
      <p class="big">{de(KPIS[5]['final'], '{:.2f}')} €</p>
      <h2 style="margin-bottom:0">Aktienkurs {COMPANY['final_period']}, +{de((KPIS[5]['final']/KPIS[5]['start']-1)*100, '{:.0f}')} % seit {COMPANY['start_period']}</h2>
      <p class="sub">Verschuldungsgrad {LEVERAGE} % – unter unserer Grenze von 40 %. Dividende von {DIVIDEND} je Aktie vorgesehen.</p>
    </div>
    <div style="flex:0 0 auto"><a class="btn" href="investor-relations.html">Zu den Kennzahlen →</a></div>
  </div>
</section>

<section>
  <div class="wrap">
    <p class="eyebrow">Aktuelles</p>
    <h2>Neuigkeiten</h2>
    <ul class="list">{news}</ul>
    <div class="actions"><a class="btn ghost" href="presse.html">Alle Meldungen</a></div>
  </div>
</section>"""
    page("index.html", "Tangerine Motors – Vier Fahrzeuglinien. Eine Kapitalstrategie.",
         "Tangerine Motors: Low Cost, Family, Eco-Friendly und Image. Modelle, Unternehmen und Investor Relations.", body)

# ---------------------------------------------------------------- Modelle
def meter(label, v):
    return f'<div class="meter"><div class="top"><span class="small">{e(label)}</span><span class="num">{v}</span></div><div class="track"><div class="fill" style="width:{v*10}%"></div></div></div>'

def build_models():
    tabs = "".join(f'<a href="#{m["id"]}">{e(m["name"])}</a>' for m in MODELS)
    blocks = ""
    for m in MODELS:
        prof = "".join(meter(k, v) for k, v in zip(PROFILE_KEYS, m["profile"]))
        mk = "".join(f'<div class="pair"><span class="lead" style="font-size:17px">{e(k)}</span><span class="val">{v}</span></div>' for k, v in zip(MARKETING_KEYS, m["marketing"]))
        blocks += f"""
<article class="model" id="{m['id']}">
  <div>
    <p class="eyebrow">{e(m['line'])} · {e(m['role'])}</p>
    <h2 style="margin-bottom:14px">{e(m['name'])}</h2>
    <p class="sub" style="margin-top:0">{e(m['tagline'])}</p>
    <p class="lead" style="margin-top:20px">{e(m['intro'])}</p>
    <div class="stage mt"><img src="assets/cars/{m['car']}.svg" alt="{e(m['name'])}, Seitenansicht" width="260" height="91" loading="lazy"></div>
  </div>
  <div>
    <p class="label">Produktprofil · Skala 1–10 <span class="flag">Beispielwerte</span></p>
    <div class="profile">{prof}</div>
    <div class="hl mt"><p class="label" style="color:var(--lime);margin-bottom:6px">Marketing</p>{mk}</div>
    <p class="small" style="margin-top:18px"><strong style="color:var(--ink)">Zielkunde:</strong> {e(m['customer'])}</p>
    <div class="actions" style="margin-top:24px"><span class="val">{e(m['price'])}</span><a class="btn ghost" href="kontakt.html?thema=Vertrieb&amp;modell={e(m['name'])}">Probefahrt anfragen</a></div>
  </div>
</article>"""
    rows = "".join(f'<tr><td>{e(k)}</td>' + "".join(f'<td class="num">{m["profile"][i]}</td>' for m in MODELS) + "</tr>" for i, k in enumerate(PROFILE_KEYS))
    body = f"""
<section class="dark">
  <div class="wrap">
    <p class="eyebrow">Modelle</p>
    <h1>Vier Linien,<br>vier Kunden.</h1>
    <p class="sub">Jedes Modell ist auf die Kaufkriterien seines Segments ausgelegt – nicht mehr, nicht weniger.</p>
    <div class="actions tabs">{tabs}</div>
  </div>
</section>
<section style="padding-top:0"><div class="wrap">{blocks}</div></section>
<section class="dark">
  <div class="wrap">
    <p class="eyebrow">Vergleich</p>
    <h2>Alle Linien im Produktprofil</h2>
    <div class="table-wrap"><table>
      <thead><tr><th>Kriterium</th>{''.join(f'<th>{e(m["name"])}</th>' for m in MODELS)}</tr></thead>
      <tbody>{rows}<tr class="total"><td>Preis</td>{''.join(f'<td>{e(m["price"])}</td>' for m in MODELS)}</tr></tbody>
    </table></div>
    <p class="small" style="margin-top:16px">Skala 1–10 aus den Engineering-Entscheidungen der Simulation. <span class="flag">Beispielwerte</span></p>
  </div>
</section>"""
    page("modelle.html", "Modelle – Tangerine Motors", "Clementine, Grove, Zest und Sanguine GT: die vier Fahrzeuglinien von Tangerine Motors.", body)

# ---------------------------------------------------------------- Investor Relations
def build_ir():
    seg_rows = ""
    tr, te = 0, 0
    for s in SEGMENTS:
        tr += s["revenue"]; te += s["ebit"]
        seg_rows += f'<tr><td>{e(s["model"])} <span class="small">· {e(s["line"])}</span></td><td class="num">{s["revenue"]}</td><td class="num">{s["ebit"]}</td><td class="num">{de(s["ebit"]/s["revenue"]*100, "{:.1f}")} %</td><td class="num">{de(s["revenue"]/sum(x["revenue"] for x in SEGMENTS)*100, "{:.0f}")} %</td></tr>'
    seg_rows += f'<tr class="total"><td>Konzern</td><td>{tr}</td><td>{te}</td><td>{de(te/tr*100, "{:.1f}")} %</td><td>100 %</td></tr>'
    cal = "".join(f'<li><span class="date">{d}</span><span>{e(t)}</span><span class="tag">{e(c)}</span></li>' for d, t, c in CALENDAR)
    reps = "".join(f'<li><span class="date">2026</span><span>{e(t)}</span><span class="tag">{e(f)}</span></li>' for t, f in REPORTS)
    body = f"""
<section class="dark">
  <div class="wrap">
    <p class="eyebrow">Investor Relations</p>
    <h1>Aus Verlust wurde<br>{EBIT_SERIES[-1][1]} Mio. € EBIT.</h1>
    <p class="sub">Wir haben Kapital von den reifen in die wachsenden Linien verschoben, die Fusion integriert und die Rezession ohne Kapitalerhöhung überstanden.</p>
    <div class="actions"><a class="btn" href="#kennzahlen">Kennzahlen</a><a class="btn ghost" href="#kalender">Finanzkalender</a><a class="btn ghost" href="mailto:{COMPANY['mail_ir']}">IR kontaktieren</a></div>
  </div>
</section>

<section id="kennzahlen">
  <div class="wrap">
    <p class="eyebrow">Kennzahlen / CFO</p>
    <h2>Die sechs Ranking-Kriterien, {COMPANY['start_period']} bis {COMPANY['final_period']}</h2>
    <div class="grid3">{kpi_tiles()}</div>
    <p class="small mt"><span class="flag">Beispielwerte</span> Platzhalter für die finalen Simulationswerte – zentral in <code>_build/data.py</code> zu pflegen.</p>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <div class="row">
      <div class="chart" style="flex:1 1 520px">
        <div class="chart-head"><div><p class="label">Verlauf</p><h3 id="chart-title">Aktienkurs</h3></div>
          <div class="seg-toggle" role="group" aria-label="Kennzahl wählen"><button type="button" aria-pressed="true" data-show="c-price" data-title="Aktienkurs">Aktie</button><button type="button" aria-pressed="false" data-show="c-ebit" data-title="EBIT">EBIT</button></div></div>
        <div id="c-price">{line_chart(SHARE_PRICE, "€", "{:.2f}")}</div>
        <div id="c-ebit" hidden>{line_chart(EBIT_SERIES, "Mio. €", "{:.0f}", zero=True)}</div>
      </div>
      <div class="col stack" style="flex:1 1 300px">
        <div class="hl"><p class="label" style="color:var(--lime)">Verschuldungsgrad</p><p class="big">{LEVERAGE} %</p><p class="small">Grenze laut Finanzpolitik: unter 40 %.</p></div>
        <div class="soft"><p class="label">Dividende je Aktie</p><p class="val">{DIVIDEND}</p><p class="small">Vorschlag an die Hauptversammlung – Wiederaufnahme nach der Rezession.</p></div>
      </div>
    </div>
  </div>
</section>

<section id="segmente">
  <div class="wrap">
    <p class="eyebrow">Segmente</p>
    <h2>Family finanziert den Umbau, Eco-Friendly trägt das Wachstum</h2>
    <div class="row">
      <div class="chart" style="flex:1 1 520px">
        <div class="chart-head"><div><p class="label">{COMPANY['final_period']} · Mio. €</p><h3 id="seg-title">Umsatz je Linie</h3></div>
          <div class="seg-toggle" role="group" aria-label="Kennzahl wählen"><button type="button" aria-pressed="true" data-show="s-rev" data-title="Umsatz je Linie">Umsatz</button><button type="button" aria-pressed="false" data-show="s-ebit" data-title="EBIT je Linie">EBIT</button></div></div>
        <div id="s-rev">{segment_bars("revenue")}</div>
        <div id="s-ebit" hidden>{segment_bars("ebit")}</div>
      </div>
      <div class="table-wrap" style="flex:1 1 440px"><table>
        <thead><tr><th>Linie</th><th>Umsatz</th><th>EBIT</th><th>Marge</th><th>Anteil</th></tr></thead>
        <tbody>{seg_rows}</tbody></table>
        <p class="small" style="margin-top:12px">Mio. €, Periode {COMPANY['final_period']}. Marge und Anteil berechnet. <span class="flag">Beispielwerte</span></p></div>
    </div>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <p class="eyebrow">Equity Story</p>
    <h2>Drei Prioritäten für die nächsten Perioden</h2>
    <div class="grid3">
      <div class="item"><p class="big">01</p><h3>Führung in Eco-Friendly</h3><p class="small">Kostenvorteil aus Volumen halten, die Baureihe in Region 2 ausrollen, beim Verbrauch vorn bleiben, wenn die Kraftstoffpreise steigen.</p></div>
      <div class="item"><p class="big">02</p><h3>Low Cost in Region 2 skalieren</h3><p class="small">Niedrigere Produktionskosten und 20 % Marktwachstum nutzen; Region 1 über Transfer beliefern.</p></div>
      <div class="item"><p class="big">03</p><h3>Wiederaufbau nach der Rezession</h3><p class="small">Kapazität dort zurückholen, wo die Nachfrage zurückkehrt, Verschuldung unter 40 % halten, Dividende wieder aufnehmen.</p></div>
    </div>
  </div>
</section>

<section id="kalender">
  <div class="wrap grid2">
    <div><p class="eyebrow">Finanzkalender</p><h2>Termine 2027</h2><ul class="list">{cal}</ul></div>
    <div id="berichte"><p class="eyebrow">Berichte & Präsentationen</p><h2>Publikationen</h2><ul class="list">{reps}</ul></div>
  </div>
</section>

<section class="accent">
  <div class="wrap row" style="align-items:center">
    <div><p class="eyebrow">IR-Kontakt</p><h2 style="margin-bottom:0">Fragen zur Aktie, zum Bericht oder zur Hauptversammlung?</h2><p class="sub">{COMPANY['mail_ir']}</p></div>
    <div style="flex:0 0 auto"><a class="btn" href="kontakt.html?thema=Investor%20Relations">Nachricht senden →</a></div>
  </div>
</section>"""
    page("investor-relations.html", "Investor Relations – Tangerine Motors",
         "Kennzahlen, Segmente, Equity Story, Finanzkalender und Berichte von Tangerine Motors.", body)

# ---------------------------------------------------------------- Unternehmen
def build_company():
    board = "".join(f'<div class="person"><div class="avatar" aria-hidden="true">{i}</div><p class="label">{e(r)}</p><h3>[Name]</h3><p class="small">{e(d)}</p></div>' for i, r, d in BOARD)
    body = f"""
<section class="dark">
  <div class="wrap">
    <p class="eyebrow">Unternehmen</p>
    <h1>Ein Autohersteller,<br>der wie ein Investor denkt.</h1>
    <p class="sub">Tangerine Motors baut vier Fahrzeuglinien für vier klar getrennte Kundengruppen – und steuert sie wie ein Portfolio.</p>
  </div>
</section>

<section>
  <div class="wrap">
    <p class="eyebrow">Strategie</p>
    <h2>Jede Linie hat eine Rolle im Portfolio</h2>
    <div class="grid4">{''.join(f'<div class="soft"><p class="label">{e(m["line"])}</p><h3>{e(m["role"])}</h3>{car(m["car"], m["name"])}<p class="small">{e(m["name"])} · {e(m["tagline"])}</p></div>' for m in MODELS)}</div>
  </div>
</section>

<section class="dark">
  <div class="wrap">
    <p class="eyebrow">Meilensteine</p>
    <h2>Fusion, Rezession, Neuausrichtung</h2>
    <div class="grid3">
      <div class="item"><p class="big">{COMPANY['start_period']}</p><h3>Ausgangslage</h3><p class="small">Sechs identische Unternehmen. Zwei Linien profitabel, zwei mit Verlust, Konzern-EBIT leicht negativ.</p></div>
      <div class="item"><p class="big">Fusion</p><h3>Zwei Regionen, ein Portfolio</h3><p class="small">Mit der Fusion kam Region 2 hinzu – mit niedrigeren Produktionskosten und schnell wachsendem Low-Cost-Markt.</p></div>
      <div class="item"><p class="big">Rezession</p><h3>Kapazität angepasst</h3><p class="small">Nachfrage brach ein. Wir haben Kapazität reduziert, Verschuldung begrenzt und die Wachstumslinien geschützt.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap grid2">
    <div>
      <p class="eyebrow">Nachhaltigkeit</p>
      <h2>CO₂ je Fahrzeug von {de(KPIS[3]['start'], '{:.0f}')} auf {de(KPIS[3]['final'], '{:.0f}')} g/km gesenkt</h2>
      <p class="lead">Treiber ist der wachsende Anteil des Zest am Absatz und der konsequente Fokus auf Verbrauch in allen Linien. <span class="flag">Beispielwerte</span></p>
    </div>
    <div>
      <p class="eyebrow">Menschen</p>
      <h2>Mitarbeitermoral bei {de(KPIS[4]['final'], '{:.0f}')} %</h2>
      <p class="lead">Investitionen in Qualifizierung und Qualität zahlen sich in Produktivität und Ausschussquote aus. Karriere bei Tangerine Motors: <a href="kontakt.html?thema=Karriere">Initiativbewerbung</a>.</p>
    </div>
  </div>
</section>

<section class="dark" id="vorstand">
  <div class="wrap">
    <p class="eyebrow">Vorstand</p>
    <h2>Sechs Verantwortliche, eine Strategie</h2>
    <div class="grid3">{board}</div>
  </div>
</section>"""
    page("unternehmen.html", "Unternehmen – Tangerine Motors", "Strategie, Meilensteine, Nachhaltigkeit und Vorstand von Tangerine Motors.", body)

# ---------------------------------------------------------------- Presse
def build_press():
    news = "".join(f'<li><span class="date">{d}</span><span><strong style="color:var(--ink)">{e(t)}</strong></span><span class="tag">{e(c)}</span></li>' for d, c, t in NEWS)
    body = f"""
<section class="dark">
  <div class="wrap">
    <p class="eyebrow">Presse</p>
    <h1>Meldungen &amp;<br>Medien.</h1>
    <p class="sub">Aktuelle Mitteilungen, Fahrzeugbilder und Kontakte für Journalistinnen und Journalisten.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <p class="eyebrow">Mitteilungen</p>
    <h2>Neueste Meldungen</h2>
    <ul class="list">{news}</ul>
  </div>
</section>
<section class="dark">
  <div class="wrap">
    <p class="eyebrow">Mediathek</p>
    <h2>Fahrzeugzeichnungen zum Download</h2>
    <div class="grid4">{''.join(f'<a class="model-card" href="assets/cars/{m["car"]}.svg" download><p class="label">{e(m["line"])}</p><h3>{e(m["name"])}</h3>{car(m["car"], m["name"])}<p class="more">SVG laden ↓</p></a>' for m in MODELS)}</div>
  </div>
</section>
<section class="accent">
  <div class="wrap row" style="align-items:center">
    <div><p class="eyebrow">Pressekontakt</p><h2 style="margin-bottom:0">{COMPANY['mail_press']}</h2></div>
    <div style="flex:0 0 auto"><a class="btn" href="kontakt.html?thema=Presse">Anfrage senden →</a></div>
  </div>
</section>"""
    page("presse.html", "Presse – Tangerine Motors", "Pressemitteilungen, Mediathek und Pressekontakt von Tangerine Motors.", body)

# ---------------------------------------------------------------- Kontakt
def build_contact():
    opts = "".join(f"<option>{t}</option>" for t in ["Vertrieb", "Investor Relations", "Presse", "Karriere", "Sonstiges"])
    body = f"""
<section class="dark">
  <div class="wrap">
    <p class="eyebrow">Kontakt</p>
    <h1>Sprechen Sie<br>mit uns.</h1>
  </div>
</section>
<section>
  <div class="wrap row">
    <form class="soft" id="contact" style="flex:1 1 520px" novalidate>
      <div class="field"><label class="label" for="thema">Thema</label><select id="thema" name="thema">{opts}</select></div>
      <div class="grid2" style="gap:0 24px">
        <div class="field"><label class="label" for="name">Name</label><input id="name" name="name" autocomplete="name" required></div>
        <div class="field"><label class="label" for="mail">E-Mail</label><input id="mail" name="mail" type="email" autocomplete="email" required></div>
      </div>
      <div class="field"><label class="label" for="msg">Nachricht</label><textarea id="msg" name="msg" required></textarea></div>
      <button class="btn" type="submit">Nachricht vorbereiten</button>
      <p class="notice" id="notice" role="status"></p>
      <p class="small">Das Formular öffnet Ihr E-Mail-Programm; es werden keine Daten auf dieser Website gespeichert.</p>
    </form>
    <div class="stack" style="flex:1 1 300px">
      <div class="hl"><p class="label" style="color:var(--lime)">Investor Relations</p><p class="val" style="font-size:20px">{COMPANY['mail_ir']}</p></div>
      <div class="soft"><p class="label">Presse</p><p class="val" style="font-size:20px">{COMPANY['mail_press']}</p></div>
      <div class="soft"><p class="label">Allgemein &amp; Vertrieb</p><p class="val" style="font-size:20px">{COMPANY['mail_info']}</p></div>
    </div>
  </div>
</section>"""
    page("kontakt.html", "Kontakt – Tangerine Motors", "Kontakt zu Vertrieb, Investor Relations, Presse und Karriere bei Tangerine Motors.", body)

def build_legal():
    body = """
<section class="dark"><div class="wrap"><p class="eyebrow">Rechtliches</p><h1>Impressum</h1></div></section>
<section><div class="wrap grid2">
  <div class="ph"><p class="phtitle">ANGABEN GEMÄSS § 5 DDG</p><p class="small">[Firma, Rechtsform]<br>[Straße, Hausnummer]<br>[PLZ Ort]<br>Vertreten durch: [Name]<br>Registergericht / -nummer: [__]<br>USt-IdNr.: [__]<br>E-Mail: [__]</p></div>
  <div class="soft"><p class="label">Hinweis</p><h3>Fiktives Unternehmen</h3><p class="small">Tangerine Motors ist ein Simulationsunternehmen aus der Customer Value Challenge. Marken, Modelle und alle Kennzahlen auf dieser Website sind frei erfunden bzw. Beispielwerte. Vor einer öffentlichen Veröffentlichung sind die Pflichtangaben einzutragen.</p></div>
</div>
<div class="wrap mt" id="datenschutz"><p class="eyebrow">Datenschutz</p><h2>Datenschutzhinweise</h2>
  <p class="lead">Diese Website setzt keine Cookies und speichert keine Formulardaten. Schriften werden von Google Fonts geladen; dabei wird Ihre IP-Adresse an Google übertragen. Für einen datensparsamen Betrieb können die Schriften lokal eingebunden werden.</p>
  <div class="ph mt"><p class="phtitle">VERANTWORTLICHER / HOSTING</p><p class="small">[Verantwortliche Stelle, Kontakt, Hosting-Anbieter, Rechtsgrundlagen, Betroffenenrechte]</p></div>
</div></section>"""
    page("impressum.html", "Impressum & Datenschutz – Tangerine Motors", "Impressum und Datenschutzhinweise von Tangerine Motors.", body)

if __name__ == "__main__":
    build_index(); build_models(); build_ir(); build_company(); build_press(); build_contact(); build_legal()
    open(os.path.join(ROOT, "assets/favicon.svg"), "w").write(LOGO.replace('class="mark" ', 'xmlns="http://www.w3.org/2000/svg" ').replace(' aria-hidden="true"', ''))
    print("ok")
