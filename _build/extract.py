"""Liest 'Group Oragange All Data .xlsx' (Blätter 'Region 1 ' und 'Region 2 ') und schreibt data/simulation.json.
Aufruf: python3 _build/extract.py "/pfad/Group Oragange All Data .xlsx"

Interpretation der Excel (bitte prüfen):
- Zeile 'Market Size' ist der Marktanteil (in Periode 6 heißt sie 'Market Share'); Werte 0–1 -> Prozent.
- 'Total Market Size' = Marktvolumen des Segments (Einheiten wie in der Simulation).
- 'Price' wird bewusst NICHT übernommen (keine Fahrzeugpreise auf der Website).
- Leere Zellen bleiben null (n. v.); Eco in Region 2 = 0 bedeutet: nicht angeboten.
"""
import json, os, re, sys
import openpyxl

LINES = ["Low Cost", "Family", "Eco", "Image"]
CRIT = ["Design", "Performance", "Comfort", "Robustness", "Size", "Technology", "Consumption / Pollution",
        "Models in Range", "Novelty", "Car Dealership Proximity", "Purchasing Experience", "After Sales Experience", "Brand Power"]
BUDGET = {"Total Market Size": "market_volume", "Market Size": "market_share", "Market Share": "market_share",
          "Production Volume": "production", "Exported": "exported", "Sales": "sales"}

def num(v):
    return None if v is None or v == "" else (round(float(v), 4) if isinstance(v, (int, float)) else None)

def parse(ws):
    periods, cur = [], None
    for row in ws.iter_rows(values_only=True):
        a = (str(row[0]).strip() if row[0] is not None else "")
        m = re.match(r"Periode\s*(\d+)", a)
        if m:
            cur = {"period": int(m.group(1)), "criteria": {}, "budget": {}}
            periods.append(cur); continue
        if cur is None or a.startswith("Zusätzliche"):
            if a.startswith("Zusätzliche"): cur = None
            continue
        if a in CRIT:
            cur["criteria"][a] = [num(x) for x in row[1:5]]
        lab = str(row[6]).strip() if len(row) > 6 and row[6] is not None else ""
        if lab in BUDGET:
            cur["budget"][BUDGET[lab]] = [num(x) for x in row[7:11]]
    return periods

def main(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    out = {"source": os.path.basename(path), "lines": LINES, "criteria": CRIT, "regions": {}}
    for ws in wb.worksheets:
        name = ws.title.strip()
        out["regions"][name] = parse(ws)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs(os.path.join(root, "data"), exist_ok=True)
    json.dump(out, open(os.path.join(root, "data/simulation.json"), "w"), ensure_ascii=False, indent=1)
    for r, ps in out["regions"].items():
        print(r, [p["period"] for p in ps])

if __name__ == "__main__":
    main(sys.argv[1])
