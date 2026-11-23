"""Erzeugt alle Seiten von Tangerine Motors.
Aufruf (aus dem Repo-Stamm):
  python3 _build/extract.py "<Pfad>/Group Oragange All Data .xlsx"   # nur wenn sich die Excel ändert
  python3 _build/build.py
Zahlen: data/simulation.json (aus der Excel). Texte: _build/content.py."""
import os, json, html, csv
from content import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = html.escape
SIM = json.load(open(os.path.join(ROOT, "data/simulation.json"), encoding="utf-8"))
LINES = SIM["lines"]                    # ["Low Cost","Family","Eco","Image"]
R1, R2 = "Region 1", "Region 2"
FY, FYP = COMPANY["fy"], COMPANY["fy_period"]
MONO = open(os.path.join(ROOT, "_build/logo_mark.txt")).read()

def P(region, period):
    for p in SIM["regions"][region]:
        if p["period"] == period: return p
    return None

def b(region, period, key, i):
    p = P(region, period)
    if not p or key not in p["budget"]: return None
    return p["budget"][key][i]

def pct(v, nd=0):
    return "n. v." if v is None else f"{v*100:.{nd}f} %".replace(".", ",")

def n(v):
    return "n. v." if v is None else f"{v:,.0f}".replace(",", ".")

def offered(region, i):
    s = b(region, FYP, "sales", i); sh = b(region, FYP, "market_share", i)
    return not (s == 0 and (sh in (0, None)))

# ------------------------------------------------------------ Datenqualität automatisch prüfen
def data_quality():
    out = []
    for reg, ps in SIM["regions"].items():
        for a, c in zip(ps, ps[1:]):
            if a["budget"] == c["budget"]:
                out.append(f"{reg}: Mengen- und Marktdaten von Periode {c['period']} sind identisch mit Periode {a['period']} (möglicher Übertrag).")
            elif a["criteria"] == c["criteria"] and all(a["budget"].get(k) == c["budget"].get(k) for k in ("production", "sales", "market_share")):
                out.append(f"{reg}: Absatz, Produktion und Marktanteil von Periode {c['period']} sind identisch mit Periode {a['period']}.")
        for p in ps:
            for i, L in enumerate(LINES):
                s, sh, mv, pr = (p["budget"].get(k, [None]*4)[i] for k in ("sales", "market_share", "market_volume", "production"))
                if s is None and (pr or 0) > 0:
                    out.append(f"{reg}, Periode {p['period']}, {L}: Absatz fehlt in der Excel.")
                if mv is None and (s or 0) > 0:
                    out.append(f"{reg}, Periode {p['period']}, {L}: Marktvolumen fehlt in der Excel.")
                if s and mv and sh is not None:
                    implied = s / mv
                    if abs(implied - sh) > 0.05:
                        out.append(f"{reg}, Periode {p['period']}, {L}: Marktanteil laut Excel {pct(sh)}, rechnerisch aus Absatz/Marktvolumen {pct(implied)}.")
                if s and pr is not None and s > pr * 1.15 and p["period"] > 1:
                    out.append(f"{reg}, Periode {p['period']}, {L}: Absatz ({n(s)}) liegt deutlich über der Produktion ({n(pr)}) – Lagerabbau oder Eingabefehler.")
    return out + EXTRA_DQ

DQ = data_quality()

def dq_block():
    return (f'<details class="dq mt"><summary>Hinweise zur Datenqualität ({len(DQ)})</summary><ul>'
            + "".join(f"<li>{e(x)}</li>" for x in DQ) + f'</ul><p class="src">Quelle: {e(SIM["source"])}; Marktanteile wie in der Excel erfasst.</p></details>')

# ------------------------------------------------------------ Grundgerüst
NAV = [("index.html", "Start"), ("modelle.html", "Modelle"), ("unternehmen.html", "Unternehmen"),
       ("investoren.html", "Investor Relations"), ("presse.html", "Presse")]
IR_NAV = [("investoren.html", "Übersicht"), ("investoren-ergebnisse.html", "Ergebnisse & Präsentationen"),
          ("investoren-kennzahlen.html", "Kennzahlen"), ("investoren-aktionaere.html", "Aktie & Aktionäre"),
          ("investoren-governance.html", "Governance")]
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400..700&family=DM+Sans:wght@400;600&family=JetBrains+Mono:wght@400;600&family=Montserrat:wght@500&display=swap" rel="stylesheet">')

def brand():
    return (f'<a class="brand" href="index.html" aria-label="Tangerine Motors – Startseite">'
            f'<svg class="mark" viewBox="-4 -4 234 101" aria-hidden="true">{MONO}</svg><span class="div" aria-hidden="true"></span><span class="word">TANGERINE MOTORS</span></a>')

def page(fname, title, desc, body, section=None):
    cur = "investoren.html" if fname.startswith("investoren") else fname
    nav = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{t}</a></li>' for h, t in NAV)
    nav += '<li><a class="cta" href="kontakt.html">Kontakt</a></li>'
    sub = ""
    if fname.startswith("investoren"):
        sub = ('<nav class="subnav" aria-label="Investor Relations"><div class="wrap"><span class="tag">Investor Relations</span>'
               + "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == fname else ""}>{t}</a>' for h, t in IR_NAV) + "</div></nav>")
    doc = f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1280">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#F7F0E4">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<a class="skip" href="#main">Zum Inhalt springen</a>
<header class="site-head">
  <div class="wrap">
    {brand()}
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Menü</button>
    <nav aria-label="Hauptnavigation"><ul class="nav" id="nav">{nav}</ul></nav>
  </div>
</header>
{sub}
<main id="main">
{body}
</main>
<footer class="site-foot">
  <div class="wrap">
    <div class="cols">
      <div class="stack">{brand()}<p class="small" style="color:#C9B49C">Vier Fahrzeuglinien in zwei Regionen: Low Cost, Family, Eco-Friendly und Image.</p></div>
      <div><p class="label">Modelle</p><ul>{''.join(f'<li><a href="modelle.html#{m["id"]}">{e(m["name"])}</a></li>' for m in LINE_META)}</ul></div>
      <div><p class="label">Investor Relations</p><ul>{''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in IR_NAV)}</ul></div>
      <div><p class="label">Unternehmen</p><ul><li><a href="unternehmen.html">Strategie</a></li><li><a href="investoren-governance.html">Vorstand</a></li><li><a href="presse.html">Presse</a></li><li><a href="kontakt.html">Kontakt</a></li></ul></div>
    </div>
    <div class="legal"><span>© 2026 Tangerine Motors · <a href="impressum.html">Impressum</a> · <a href="impressum.html#datenschutz">Datenschutz</a></span><span>Simulationsunternehmen der Customer Value Challenge · Daten: {e(SIM["source"])}</span></div>
  </div>
</footer>
<script src="assets/data.js"></script>
<script src="assets/site.js"></script>
</body>
</html>
"""
    open(os.path.join(ROOT, fname), "w", encoding="utf-8").write(doc)

def car(kind, alt, cls="car"):
    return f'<img class="{cls}" src="assets/cars/{kind}.svg" alt="{e(alt)}" loading="lazy" width="260" height="91">'

def series(region, key):
    ps = SIM["regions"][region]
    return {"periods": [f"P{p['period']}" for p in ps],
            "series": [{"name": LINES[i], "values": [p["budget"].get(key, [None]*4)[i] for p in ps]} for i in range(4)]}

def write_data_js():
    D = {"lines": LINES, "meta": [{"key": m["key"], "name": m["name"], "id": m["id"]} for m in LINE_META],
         "crit": SIM["criteria"], "critDe": CRIT_DE, "eng": ENGINEERING, "mkt": MARKETING, "fy": FY, "fyPeriod": FYP,
         "regions": SIM["regions"],
         "charts": {
             "sales-r1": series(R1, "sales"), "sales-r2": series(R2, "sales"),
             "share-r1": series(R1, "market_share"), "share-r2": series(R2, "market_share"),
             "volume-r1": series(R1, "market_volume"), "volume-r2": series(R2, "market_volume"),
             "bi": {"periods": BUSINESS_INDEX["periods"], "series": [{"name": "Region 1", "values": BUSINESS_INDEX["Region 1"]}, {"name": "Region 2", "values": BUSINESS_INDEX["Region 2"]}]},
         }}
    open(os.path.join(ROOT, "assets/data.js"), "w", encoding="utf-8").write("window.TM=" + json.dumps(D, ensure_ascii=False) + ";")

def write_csv():
    path = os.path.join(ROOT, "data/tangerine-motors-operative-daten.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Region", "Periode", "Linie", "Absatz", "Produktion", "Export", "Marktvolumen", "Marktanteil %"] + SIM["criteria"])
        for reg, ps in SIM["regions"].items():
            for p in ps:
                for i, L in enumerate(LINES):
                    g = lambda k: p["budget"].get(k, [None]*4)[i]
                    sh = g("market_share")
                    w.writerow([reg, p["period"], L, g("sales"), g("production"), g("exported"), g("market_volume"),
                                None if sh is None else round(sh*100, 1)] + [p["criteria"].get(c, [None]*4)[i] for c in SIM["criteria"]])

# ------------------------------------------------------------ gemeinsame Bausteine
def totals(region, period, key="sales"):
    vals = [b(region, period, key, i) for i in range(4)]
    return None if any(v is None for v in vals) else sum(vals), vals

def chart(cid, title, label, toggles=None, unit="", note=""):
    tg = ""
    if toggles:
        tg = '<div class="seg-toggle" role="group" aria-label="Region wählen">' + "".join(
            f'<button type="button" aria-pressed="{"true" if i == 0 else "false"}" data-chart="{cid}" data-key="{k}">{t}</button>' for i, (k, t) in enumerate(toggles)) + "</div>"
    first = toggles[0][0] if toggles else cid
    return (f'<div class="chart"><div class="chart-head"><div><p class="label">{e(label)}</p><h3>{e(title)}</h3></div>{tg}</div>'
            f'<div class="fig" id="{cid}" data-key="{first}" data-unit="{unit}" role="img" aria-label="{e(title)}"></div><div class="legend" id="{cid}-legend"></div>'
            + (f'<p class="src">{note}</p>' if note else "") + '</div>')

def fy_card(compact=False):
    return f"""<div class="result">
  <div class="cover"><div><p class="label" style="color:#C9B49C">Ergebnisse · Customer Value Challenge</p><p class="fy">{FY}</p></div>
    <div><h3>FY26 Präsentation</h3><p class="small" style="color:#C9B49C">Shareholders Presentation: Strategie, Zahlen, vier Fahrzeuglinien und Ausblick.</p></div></div>
  <div class="body">
    <p class="label">Veröffentlicht 23.11.2026</p>
    <div class="dlrow"><span>FY26 Präsentation</span><a class="dl btn" href="assets/ir/FY26-Praesentation.pdf" download>PDF ↓</a></div>
    <div class="dlrow"><span>FY26 Präsentation (PowerPoint)</span><a class="dl btn ghost" href="assets/ir/FY26-Praesentation.pptx" download>PPTX ↓</a></div>
    <div class="dlrow"><span>Operative Daten P1–P{FYP} (CSV)</span><a class="dl btn ghost" href="data/tangerine-motors-operative-daten.csv" download>CSV ↓</a></div>
    {'' if compact else '<p class="small">Die Präsentation enthält noch Platzhalter für Finanzkennzahlen, die nicht in den Simulationsdaten vorliegen.</p>'}
  </div>
</div>"""

# ------------------------------------------------------------ Startseite
def build_index():
    t1, v1 = totals(R1, FYP); t1s, _ = totals(R1, 1)
    best = max(range(4), key=lambda i: b(R1, FYP, "market_share", i) or 0)
    best_share = b(R1, FYP, "market_share", best)
    lm = {m["key"]: m for m in LINE_META}
    eco_g = b(R1, FYP, "sales", 2) / b(R1, 1, "sales", 2) - 1
    ticker = [
        ("Absatz Region 1", n(t1), f"{FY} · +{pct(t1/t1s-1)} ggü. P1"),
        (f"Marktanteil {lm[LINES[best]]['name']}", pct(best_share), "Region 1 · höchster Anteil"),
        ("Marktanteil Grove", pct(b(R2, FYP, "market_share", 1)), "Region 2"),
        ("Absatz Zest", n(b(R1, FYP, "sales", 2)), f"Region 1 · +{pct(eco_g)} ggü. P1"),
    ]
    tick = "".join(f'<div class="item"><p class="label">{e(a)}</p><p class="val">{e(v)}</p><p class="small">{e(c)}</p></div>' for a, v, c in ticker)
    cards = ""
    for i, m in enumerate(LINE_META):
        s1 = pct(b(R1, FYP, "market_share", i)); s2 = pct(b(R2, FYP, "market_share", i)) if offered(R2, i) else "nicht angeboten"
        cards += f'''<a class="model-card" href="modelle.html#{m["id"]}"><p class="label">{e({"Eco": "Eco-Friendly"}.get(m["key"], m["key"]))} · {e(m["role"])}</p><h3>{e(m["name"])}</h3>{car(m["car"], m["name"] + ", Seitenansicht")}
<p class="small">{e(m["tagline"])}</p><p class="more">Marktanteil {FY}: R1 {s1} · R2 {s2} →</p></a>'''
    bar = "".join(f'<div class="seg{" on" if i == 2 else ""}" style="flex:{v}">{pct(v/t1)}<span>{e(LINE_META[i]["name"])}</span></div>' for i, v in enumerate(v1))
    under = "".join(f'<div class="item" style="flex:{v}"><h3 style="font-size:18px">{e(LINE_META[i]["name"])}</h3><p class="small">{n(v)} Einheiten</p></div>' for i, v in enumerate(v1))
    body = f"""
<section class="hero">
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <p class="eyebrow">{FY} · Customer Value Challenge</p>
        <h1>Vier Linien.<br>Ein Portfolio.</h1>
        <p class="sub">Kapital in die Wachstumslinien: Zest führt in Region 1 mit {pct(best_share)} Marktanteil, Grove hält in Region 2 {pct(b(R2, FYP, "market_share", 1))}.</p>
        <div class="actions"><a class="btn" href="modelle.html">Modelle entdecken</a><a class="btn ghost" href="investoren.html">Investor Relations</a></div>
      </div>
      <div><img class="car" src="assets/cars/coupe.svg" alt="Sanguine GT, Seitenansicht" width="520" height="182"><div class="road" aria-hidden="true"></div></div>
    </div>
    <div class="ticker">{tick}</div>
  </div>
</section>

<section class="paper">
  <div class="wrap">
    <p class="eyebrow">Modelle</p>
    <h2>Für jeden Kunden genau das, wofür er kauft</h2>
    <div class="models">{cards}</div>
  </div>
</section>

<section>
  <div class="wrap">
    <p class="eyebrow">Portfolio {FY}</p>
    <h2>Zest ist die größte Linie in Region 1: {pct(v1[2]/t1)} des Absatzes</h2>
    <div class="bar" role="img" aria-label="Absatzanteile je Linie, Region 1, {FY}">{bar}</div>
    <div class="under">{under}</div>
    <p class="src">Absatz Region 1, Periode {FYP} · Quelle: {e(SIM['source'])}</p>
  </div>
</section>

<section class="orange">
  <div class="wrap row" style="align-items:center">
    <div style="flex:2 1 420px"><p class="eyebrow">Investor Relations</p><h2 style="margin-bottom:0">Die FY26 Präsentation ist online</h2>
      <p class="sub">Strategie, Kennzahlen und die vier Fahrzeuglinien – mit allen operativen Daten zum Download.</p></div>
    <div style="flex:0 0 auto"><a class="btn" href="investoren-ergebnisse.html">Zur FY26 Präsentation →</a></div>
  </div>
</section>"""
    page("index.html", "Tangerine Motors", "Tangerine Motors: Clementine, Grove, Zest und Sanguine GT. Modelle, Unternehmen und Investor Relations.", body)

# ------------------------------------------------------------ Modelle
def build_models():
    tabs = "".join(f'<a class="btn ghost" href="#{m["id"]}">{e(m["name"])}</a>' for m in LINE_META)
    blocks = ""
    for i, m in enumerate(LINE_META):
        blocks += f"""
<article class="model" id="{m['id']}" data-line="{i}">
  <div>
    <p class="eyebrow">{e({"Eco": "Eco-Friendly"}.get(m['key'], m['key']))} · {e(m['role'])}</p>
    <h2 style="margin-bottom:10px">{e(m['name'])}</h2>
    <p class="sub" style="margin-top:0">{e(m['tagline'])}</p>
    <p class="lead" style="margin-top:16px">{e(m['intro'])}</p>
    <div class="stage mt">{car(m['car'], m['name'] + ', Seitenansicht', 'x')}</div>
    <p class="small" style="margin-top:14px"><strong style="color:var(--ink)">Zielkunde:</strong> {e(m['customer'])}</p>
  </div>
  <div>
    <div class="share"><div><p class="label">Marktanteil <span data-f="reg"></span> · <span data-f="per"></span></p><p class="big" data-f="share">–</p></div>
      <div><p class="label">Absatz</p><p class="val" data-f="sales">–</p></div></div>
    <div class="blockhead"><p class="label">Engineering · Skala 0–10</p><p class="label" data-f="cmp"></p></div>
    <div class="profile" data-f="eng"></div>
    <div class="blockhead"><p class="label">Marketing · Skala 0–10</p></div>
    <div class="profile" data-f="mkt"></div>
    <p class="small" data-f="na" hidden style="margin-top:14px"></p>
  </div>
</article>"""
    per_btns = "".join(f'<button type="button" data-per="{p}" aria-pressed="{"true" if p == FYP else "false"}">P{p}</button>' for p in range(1, FYP + 1))
    # Vergleichstabelle FY Region 1
    head = "".join(f"<th>{e(m['name'])}</th>" for m in LINE_META)
    rows = ""
    p8 = P(R1, FYP)
    for c in SIM["criteria"]:
        vals = p8["criteria"][c]; mx = max(v for v in vals if v is not None)
        rows += f"<tr><td>{e(CRIT_DE[c])}</td>" + "".join(f'<td class="num{" hi" if v == mx else ""}">{"n. v." if v is None else int(v)}</td>' for v in vals) + "</tr>"
    rows += '<tr class="total"><td>Marktanteil</td>' + "".join(f"<td>{pct(v)}</td>" for v in p8["budget"]["market_share"]) + "</tr>"
    body = f"""
<section class="hero" style="padding-bottom:clamp(40px,5vw,72px)">
  <div class="wrap">
    <p class="eyebrow">Modelle</p>
    <h1>Vier Linien,<br>vier Kunden.</h1>
    <p class="sub">Jedes Modell ist auf die Kaufkriterien seines Segments ausgelegt. Alle Werte stammen aus unseren Entscheidungen in der Simulation.</p>
    <div class="actions">{tabs}</div>
  </div>
</section>
<section class="paper" style="padding-top:0;position:sticky;top:72px;z-index:30;padding-bottom:0;border-bottom:1px solid var(--line)">
  <div class="wrap controls" style="padding-top:12px;padding-bottom:12px">
    <div class="seg-toggle" role="group" aria-label="Region"><button type="button" data-reg="Region 1" aria-pressed="true">Region 1</button><button type="button" data-reg="Region 2" aria-pressed="false">Region 2</button></div>
    <div class="seg-toggle" role="group" aria-label="Periode" id="per-btns">{per_btns}</div>
    <span class="small">Veränderung ggü. erster Periode der Region</span>
  </div>
</section>
<section style="padding-top:0"><div class="wrap" id="models">{blocks}</div></section>
<section class="paper">
  <div class="wrap">
    <p class="eyebrow">Vergleich {FY}</p>
    <h2>Alle Linien im Profil, Region 1, Periode {FYP}</h2>
    <div class="table-wrap"><table><thead><tr><th>Kriterium</th>{head}</tr></thead><tbody>{rows}</tbody></table></div>
    <p class="src">Höchster Wert je Kriterium hervorgehoben · Quelle: {e(SIM['source'])}</p>
  </div>
</section>"""
    page("modelle.html", "Modelle – Tangerine Motors", "Clementine, Grove, Zest und Sanguine GT: Engineering, Marketing und Marktanteile je Region und Periode.", body)

# ------------------------------------------------------------ Unternehmen
def build_company():
    roles = "".join(f'<div class="card"><p class="label">{e({"Eco": "Eco-Friendly"}.get(m["key"], m["key"]))}</p><h3>{e(m["role"])}</h3>{car(m["car"], m["name"])}<p class="small">{e(m["name"])} · {e(m["tagline"])}</p></div>' for m in LINE_META)
    cons = P(R1, FYP)["criteria"]["Consumption / Pollution"]; cons1 = P(R1, 1)["criteria"]["Consumption / Pollution"]
    body = f"""
<section class="hero" style="padding-bottom:clamp(48px,6vw,96px)">
  <div class="wrap">
    <p class="eyebrow">Unternehmen</p>
    <h1>Ein Autohersteller,<br>der wie ein Investor denkt.</h1>
    <p class="sub">Tangerine Motors baut vier Fahrzeuglinien für vier klar getrennte Kundengruppen – und steuert sie wie ein Portfolio.</p>
  </div>
</section>
<section class="paper">
  <div class="wrap">
    <p class="eyebrow">Strategie</p>
    <h2>Jede Linie hat eine Rolle im Portfolio</h2>
    <div class="grid4">{roles}</div>
  </div>
</section>
<section>
  <div class="wrap">
    <p class="eyebrow">Meilensteine</p>
    <h2>Von sechs gleichen Unternehmen zu einem Hersteller in zwei Regionen</h2>
    <div class="grid3">
      <div class="item"><p class="big">P1</p><h3>Gleicher Start</h3><p class="small">Sechs identische Unternehmen, Marktanteile je Linie zwischen {pct(min(P(R1,1)['budget']['market_share']))} und {pct(max(P(R1,1)['budget']['market_share']))} in Region 1.</p></div>
      <div class="item"><p class="big">P{COMPANY['merger_period']}</p><h3>Fusion: Region 2</h3><p class="small">Mit der Fusion kam Region 2 hinzu. Dort sind wir mit Clementine, Grove und Sanguine GT vertreten; der Zest wird bisher nicht angeboten.</p></div>
      <div class="item"><p class="big">P{FYP}</p><h3>{FY}</h3><p class="small">Zest führt in Region 1 mit {pct(b(R1,FYP,'market_share',2))}, Grove hält in Region 2 {pct(b(R2,FYP,'market_share',1))}, Sanguine GT {pct(b(R2,FYP,'market_share',3))} im Image-Segment.</p></div>
    </div>
  </div>
</section>
<section class="dark">
  <div class="wrap grid2">
    <div><p class="eyebrow">Verbrauch & Emissionen</p><h2>Alle vier Linien auf Verbrauchsstufe {int(cons[0])} von 10</h2>
      <p class="lead">In Periode 1 lag die Stufe je nach Linie zwischen {int(min(cons1))} und {int(max(cons1))}; im {FY} erreichen Clementine, Grove, Zest und Sanguine GT in beiden Regionen den Höchstwert.</p>
      <p class="src" style="color:#A08D79">Kriterium „Consumption / Pollution“ · Quelle: {e(SIM['source'])}</p></div>
    <div><p class="eyebrow">Menschen</p><h2>Ein Team, sechs Verantwortungen</h2>
      <p class="lead">CEO, CFO und vier Linien-Direktoren entscheiden gemeinsam über Kapital, Kapazität und Produkt. <a href="investoren-governance.html" style="color:#FF9A57">Zum Vorstand</a></p></div>
  </div>
</section>"""
    page("unternehmen.html", "Unternehmen – Tangerine Motors", "Strategie, Meilensteine und Verantwortung bei Tangerine Motors.", body)

# ------------------------------------------------------------ Investor Relations
def ir_hero(title, sub):
    return f'<section class="hero" style="padding-bottom:clamp(40px,5vw,72px)"><div class="wrap"><p class="eyebrow">Investor Relations</p><h1>{title}</h1><p class="sub">{sub}</p></div></section>'

def build_ir_home():
    t1, _ = totals(R1, FYP); t1s, _ = totals(R1, 1)
    r2 = [b(R2, FYP, "sales", i) for i in range(4)]
    hl = [
        ("Absatz Region 1", n(t1), f"+{pct(t1/t1s-1)} ggü. P1"),
        ("Marktanteil Zest R1", pct(b(R1, FYP, "market_share", 2)), f"P1: {pct(b(R1, 1, 'market_share', 2))}"),
        ("Marktanteil Grove R2", pct(b(R2, FYP, "market_share", 1)), f"P{COMPANY['merger_period']}: {pct(b(R2, COMPANY['merger_period'], 'market_share', 1))}"),
        ("Marktanteil Sanguine GT R2", pct(b(R2, FYP, "market_share", 3)), "Image-Segment"),
    ]
    hls = "".join(f'<div class="item"><p class="label">{e(a)}</p><p class="big">{e(v)}</p><p class="small">{e(c)}</p></div>' for a, v, c in hl)
    cal = "".join(f'<li><span class="date">{d}</span><span>{e(t)}</span><span class="tag">{e(c)}</span></li>' for d, t, c in CALENDAR[:3])
    body = f"""
{ir_hero(f"{FY}: Wachstum<br>aus dem Portfolio.", "Informationen für Aktionäre, Analysten und Fremdkapitalgeber: Ergebnisse, Kennzahlen, Termine und Governance.")}
<section class="paper" style="padding-top:clamp(40px,5vw,72px)">
  <div class="wrap">
    <p class="eyebrow">Neueste Ergebnisse</p>
    <h2>FY26 Präsentation</h2>
    {fy_card(compact=True)}
  </div>
</section>
<section>
  <div class="wrap">
    <p class="eyebrow">Highlights {FY}</p>
    <h2>Operative Kennzahlen, Periode {FYP}</h2>
    <div class="grid4">{hls}</div>
    <p class="src">Region 2 Clementine: Absatz in Periode {FYP} nicht erfasst · Quelle: {e(SIM['source'])}</p>
    <div class="actions"><a class="btn ghost" href="investoren-kennzahlen.html">Alle Kennzahlen</a></div>
  </div>
</section>
<section class="paper">
  <div class="wrap grid2">
    <div><p class="eyebrow">Finanzkalender</p><h2>Nächste Termine</h2><ul class="list">{cal}</ul>
      <div class="actions"><a class="btn ghost" href="investoren-aktionaere.html#kalender">Vollständiger Kalender</a></div></div>
    <div><p class="eyebrow">Schnellzugriff</p><h2>Für Investoren</h2>
      <div class="grid2" style="gap:14px">
        {''.join(f'<a class="model-card" href="{h}" style="min-height:120px"><h3>{t}</h3><p class="more">Öffnen →</p></a>' for h, t in IR_NAV[1:])}
      </div></div>
  </div>
</section>
<section class="orange" id="kontakt">
  <div class="wrap row" style="align-items:center">
    <div style="flex:2 1 420px"><p class="eyebrow">IR-Kontakt</p><h2 style="margin-bottom:0">Investor Relations Team</h2><p class="sub">{COMPANY['mail_ir']}</p></div>
    <div style="flex:0 0 auto"><a class="btn" href="kontakt.html?thema=Investor%20Relations">Nachricht senden →</a></div>
  </div>
</section>"""
    page("investoren.html", "Investor Relations – Tangerine Motors", "Investor Relations von Tangerine Motors: FY26 Präsentation, Kennzahlen, Finanzkalender und Governance.", body)

def build_ir_results():
    body = f"""
{ir_hero("Ergebnisse &amp;<br>Präsentationen.", "Präsentationen, Berichte und Daten zum Herunterladen.")}
<section class="paper" style="padding-top:clamp(40px,5vw,72px)">
  <div class="wrap">
    <p class="eyebrow">{FY}</p>
    <h2>FY26 Präsentation</h2>
    {fy_card()}
  </div>
</section>
<section>
  <div class="wrap">
    <p class="eyebrow">Archiv</p>
    <h2>Alle Veröffentlichungen</h2>
    <ul class="list">
      <li><span class="date">23.11.2026</span><span>FY26 Präsentation (Shareholders Presentation)</span><a class="dl" href="assets/ir/FY26-Praesentation.pdf" download>PDF ↓</a></li>
      <li><span class="date">23.11.2026</span><span>Operative Daten Periode 1–{FYP}, Region 1 und 2</span><a class="dl" href="data/tangerine-motors-operative-daten.csv" download>CSV ↓</a></li>
      <li><span class="date">Q1 2027</span><span>Geschäftsbericht FY26</span><span class="tag">In Vorbereitung</span></li>
    </ul>
  </div>
</section>"""
    page("investoren-ergebnisse.html", "Ergebnisse & Präsentationen – Tangerine Motors", "FY26 Präsentation und operative Daten von Tangerine Motors zum Download.", body)

def build_ir_kpis():
    # Tabelle FY je Region
    def fy_table(reg):
        rows = ""
        for i, m in enumerate(LINE_META):
            if not offered(reg, i):
                rows += f'<tr><td>{e(m["name"])}</td><td class="num na" colspan="5">nicht angeboten</td></tr>'; continue
            first = SIM["regions"][reg][0]["period"]
            rows += (f'<tr><td>{e(m["name"])} <span class="small">· {e(m["key"])}</span></td><td class="num">{pct(b(reg, FYP, "market_share", i))}</td>'
                     f'<td class="num">{pct(b(reg, first, "market_share", i))}</td><td class="num">{n(b(reg, FYP, "sales", i))}</td>'
                     f'<td class="num">{n(b(reg, FYP, "production", i))}</td><td class="num">{n(b(reg, FYP, "market_volume", i))}</td></tr>')
        first = SIM["regions"][reg][0]["period"]
        return (f'<div class="table-wrap"><table><thead><tr><th>Linie</th><th>Marktanteil P{FYP}</th><th>Marktanteil P{first}</th><th>Absatz</th><th>Produktion</th><th>Marktvolumen</th></tr></thead><tbody>{rows}</tbody></table></div>')
    opens = "".join(f'<div class="ph"><p class="phtitle">{e(k.upper())}</p><p class="small">Nicht in den Simulationsdaten – aus dem Ergebnisbericht ergänzen.</p></div>' for k in OPEN_KPIS)
    body = f"""
{ir_hero("Kennzahlen.", "Marktanteile, Absatz und Märkte je Fahrzeuglinie und Region – Periode 1 bis {}.".format(FYP))}
<section class="paper" style="padding-top:clamp(40px,5vw,72px)">
  <div class="wrap">
    <p class="eyebrow">Marktanteile</p>
    <h2>Zest wächst von {pct(b(R1,1,'market_share',2))} auf {pct(b(R1,FYP,'market_share',2))} in Region 1</h2>
    {chart("c-share", "Marktanteil je Linie", "In Prozent", [("share-r1", "Region 1"), ("share-r2", "Region 2")], "%", "Marktanteile wie in der Excel erfasst (Zeile „Market Size“/„Market Share“).")}
  </div>
</section>
<section>
  <div class="wrap">
    <div class="grid2">
      {chart("c-sales", "Absatz je Linie", "Einheiten", [("sales-r1", "Region 1"), ("sales-r2", "Region 2")])}
      {chart("c-vol", "Marktvolumen je Segment", "Einheiten", [("volume-r1", "Region 1"), ("volume-r2", "Region 2")])}
    </div>
  </div>
</section>
<section class="paper">
  <div class="wrap">
    <p class="eyebrow">{FY} im Detail</p>
    <h2>Periode {FYP} nach Region</h2>
    <h3>Region 1</h3>{fy_table(R1)}
    <h3 class="mt">Region 2 <span class="small">(seit Fusion, ab Periode {COMPANY['merger_period']})</span></h3>{fy_table(R2)}
    {dq_block()}
  </div>
</section>
<section>
  <div class="wrap">
    <p class="eyebrow">Marktumfeld</p>
    <h2>Region 2 wächst stetig, Region 1 erholt sich nach der Rezession</h2>
    {chart("bi", "Business Index", "Index, 1,0 = Ausgangsniveau", None, "", "Quelle: Simulations-Screenshots vom 23.11.2026, Werte abgelesen; Nummerierung P4–P12 der Simulation.")}
  </div>
</section>
<section class="paper">
  <div class="wrap">
    <p class="eyebrow">Finanzkennzahlen</p>
    <h2>Diese Werte folgen mit dem Ergebnisbericht</h2>
    <div class="grid4">{opens}</div>
  </div>
</section>"""
    page("investoren-kennzahlen.html", "Kennzahlen – Investor Relations – Tangerine Motors", "Marktanteile, Absatz, Marktvolumen und Business Index von Tangerine Motors.", body)

def build_ir_share():
    cal = "".join(f'<li><span class="date">{d}</span><span>{e(t)}</span><span class="tag">{e(c)}</span></li>' for d, t, c in CALENDAR)
    body = f"""
{ir_hero("Aktie &amp;<br>Aktionäre.", "Aktieninformationen, Hauptversammlung, Dividendenpolitik und Finanzkalender.")}
<section class="paper" style="padding-top:clamp(40px,5vw,72px)">
  <div class="wrap">
    <p class="eyebrow">Die Aktie</p>
    <h2>Aktieninformationen</h2>
    <div class="grid3">
      <div class="ph"><p class="phtitle">AKTIENKURS</p><p class="small">Start- und Schlusskurs aus der Simulation ergänzen.</p></div>
      <div class="ph"><p class="phtitle">RANG AKTIENKURS</p><p class="small">Platz von sechs Unternehmen.</p></div>
      <div class="ph"><p class="phtitle">DIVIDENDE JE AKTIE</p><p class="small">Ausschüttung der letzten Periode.</p></div>
    </div>
  </div>
</section>
<section id="kalender">
  <div class="wrap">
    <p class="eyebrow">Finanzkalender</p>
    <h2>Termine</h2>
    <ul class="list">{cal}</ul>
    <p class="src">Termine ab 2027 vorläufig.</p>
  </div>
</section>
<section class="paper">
  <div class="wrap grid2">
    <div><p class="eyebrow">Hauptversammlung</p><h2>Ordentliche Hauptversammlung</h2><p class="lead">Einladung, Tagesordnung und Abstimmungsergebnisse werden hier veröffentlicht, sobald der Termin feststeht.</p></div>
    <div><p class="eyebrow">Dividendenpolitik</p><h2>Ausschüttung nach Kapitalbedarf</h2><p class="lead">Vorrang hat die Finanzierung der Wachstumslinien Eco-Friendly und Low Cost; ausgeschüttet wird, was darüber hinaus verdient wird.</p></div>
  </div>
</section>"""
    page("investoren-aktionaere.html", "Aktie & Aktionäre – Investor Relations – Tangerine Motors", "Aktie, Hauptversammlung, Dividendenpolitik und Finanzkalender von Tangerine Motors.", body)

def build_ir_gov():
    board = "".join(f'<div class="person card"><div class="avatar" aria-hidden="true">{i}</div><p class="label">{e(r)}</p><h3>Name folgt</h3><p class="small">{e(d)}</p></div>' for i, r, d in BOARD)
    body = f"""
{ir_hero("Governance.", "Wer bei Tangerine Motors entscheidet – und wofür.")}
<section class="paper" style="padding-top:clamp(40px,5vw,72px)">
  <div class="wrap">
    <p class="eyebrow">Vorstand & Direktoren</p>
    <h2>Sechs Verantwortliche, eine Strategie</h2>
    <div class="grid3">{board}</div>
  </div>
</section>
<section>
  <div class="wrap grid3">
    <div class="item"><h3>Kapitalallokation</h3><p class="small">Investitionen folgen der Rolle jeder Linie: Wachstumslinien erhalten Kapazität, die Cash Cow finanziert.</p></div>
    <div class="item"><h3>Linienverantwortung</h3><p class="small">Jeder Direktor verantwortet Engineering, Marketing und Produktion seiner Linie in beiden Regionen.</p></div>
    <div class="item"><h3>Transparenz</h3><p class="small">Operative Daten werden je Periode vollständig veröffentlicht, Datenlücken offen ausgewiesen.</p></div>
  </div>
</section>"""
    page("investoren-governance.html", "Governance – Investor Relations – Tangerine Motors", "Vorstand, Direktoren und Grundsätze der Unternehmensführung von Tangerine Motors.", body)

# ------------------------------------------------------------ Presse, Kontakt, Impressum
NEWS = lambda: [
    ("23.11.2026", "Investor Relations", "Tangerine Motors veröffentlicht die FY26 Präsentation"),
    ("23.11.2026", "Produkt", f"Zest erreicht {pct(b(R1,FYP,'market_share',2))} Marktanteil in Region 1"),
    ("23.11.2026", "Region 2", f"Grove steigert Marktanteil in Region 2 auf {pct(b(R2,FYP,'market_share',1))}"),
]

def build_press():
    news = "".join(f'<li><span class="date">{d}</span><span><strong style="color:var(--ink)">{e(t)}</strong></span><span class="tag">{e(c)}</span></li>' for d, c, t in NEWS())
    media = "".join(f'<a class="model-card" href="assets/cars/{m["car"]}.svg" download><p class="label">{e(m["key"])}</p><h3>{e(m["name"])}</h3>{car(m["car"], m["name"])}<p class="more">SVG ↓</p></a>' for m in LINE_META)
    body = f"""
{'<section class="hero" style="padding-bottom:clamp(40px,5vw,72px)"><div class="wrap"><p class="eyebrow">Presse</p><h1>Meldungen &amp;<br>Medien.</h1></div></section>'}
<section class="paper"><div class="wrap"><p class="eyebrow">Mitteilungen</p><h2>Neueste Meldungen</h2><ul class="list">{news}</ul></div></section>
<section><div class="wrap"><p class="eyebrow">Mediathek</p><h2>Logo und Fahrzeugzeichnungen</h2>
  <div class="models"><a class="model-card" href="assets/logo.svg" download><p class="label">Marke</p><h3>Logo</h3><img src="assets/logo.svg" alt="Tangerine-Motors-Logo" style="margin:24px 0"><p class="more">SVG ↓</p></a>{media}</div></div></section>
<section class="orange"><div class="wrap row" style="align-items:center"><div style="flex:2 1 420px"><p class="eyebrow">Pressekontakt</p><h2 style="margin-bottom:0">{COMPANY['mail_press']}</h2></div>
  <div style="flex:0 0 auto"><a class="btn" href="kontakt.html?thema=Presse">Anfrage senden →</a></div></div></section>"""
    page("presse.html", "Presse – Tangerine Motors", "Pressemitteilungen, Logo und Fahrzeugzeichnungen von Tangerine Motors.", body)

def build_contact():
    opts = "".join(f"<option>{t}</option>" for t in ["Vertrieb", "Investor Relations", "Presse", "Karriere", "Sonstiges"])
    body = f"""
<section class="hero" style="padding-bottom:clamp(40px,5vw,72px)"><div class="wrap"><p class="eyebrow">Kontakt</p><h1>Sprechen Sie<br>mit uns.</h1></div></section>
<section class="paper"><div class="wrap row">
  <form class="card" id="contact" style="flex:1 1 520px" novalidate>
    <div class="field"><label class="label" for="thema">Thema</label><select id="thema" name="thema">{opts}</select></div>
    <div class="grid2" style="gap:0 20px"><div class="field"><label class="label" for="name">Name</label><input id="name" name="name" autocomplete="name" required></div>
    <div class="field"><label class="label" for="mail">E-Mail</label><input id="mail" name="mail" type="email" autocomplete="email" required></div></div>
    <div class="field"><label class="label" for="msg">Nachricht</label><textarea id="msg" name="msg" required></textarea></div>
    <button class="btn" type="submit">Nachricht vorbereiten</button>
    <p class="notice" id="notice" role="status"></p>
    <p class="small">Öffnet Ihr E-Mail-Programm; diese Website speichert keine Daten.</p>
  </form>
  <div class="stack" style="flex:1 1 300px">
    <div class="card hl"><p class="label">Investor Relations</p><p class="val" style="font-size:18px;white-space:normal">{COMPANY['mail_ir']}</p></div>
    <div class="card"><p class="label">Presse</p><p class="val" style="font-size:18px;white-space:normal">{COMPANY['mail_press']}</p></div>
    <div class="card"><p class="label">Allgemein & Vertrieb</p><p class="val" style="font-size:18px;white-space:normal">{COMPANY['mail_info']}</p></div>
  </div></div></section>"""
    page("kontakt.html", "Kontakt – Tangerine Motors", "Kontakt zu Vertrieb, Investor Relations, Presse und Karriere.", body)

def build_legal():
    body = """
<section class="hero" style="padding-bottom:clamp(40px,5vw,72px)"><div class="wrap"><p class="eyebrow">Rechtliches</p><h1>Impressum</h1></div></section>
<section class="paper"><div class="wrap grid2">
  <div class="ph"><p class="phtitle">ANGABEN GEMÄSS § 5 DDG</p><p class="small">Firma, Rechtsform · Anschrift · Vertretungsberechtigte · Registergericht und -nummer · USt-IdNr. · E-Mail – vor Veröffentlichung eintragen.</p></div>
  <div class="card"><p class="label">Hinweis</p><h3>Simulationsunternehmen</h3><p class="small">Tangerine Motors ist das Unternehmen unseres Teams in der Customer Value Challenge (Business Management Simulation Capstone, Fall Term 2026). Die operativen Daten stammen aus der Simulation.</p></div>
</div>
<div class="wrap mt" id="datenschutz"><p class="eyebrow">Datenschutz</p><h2>Datenschutzhinweise</h2>
  <p class="lead">Diese Website setzt keine Cookies und speichert keine Formulardaten. Schriften werden von Google Fonts geladen; dabei wird Ihre IP-Adresse an Google übertragen.</p>
  <div class="ph mt"><p class="phtitle">VERANTWORTLICHER / HOSTING</p><p class="small">Verantwortliche Stelle, Hosting-Anbieter, Rechtsgrundlagen und Betroffenenrechte – vor Veröffentlichung eintragen.</p></div>
</div></section>"""
    page("impressum.html", "Impressum & Datenschutz – Tangerine Motors", "Impressum und Datenschutzhinweise.", body)

if __name__ == "__main__":
    write_data_js(); write_csv()
    build_index(); build_models(); build_company()
    build_ir_home(); build_ir_results(); build_ir_kpis(); build_ir_share(); build_ir_gov()
    build_press(); build_contact(); build_legal()
    print("ok ·", len(DQ), "Datenhinweise")
    for x in DQ: print(" -", x)
