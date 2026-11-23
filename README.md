# Tangerine Motors – Website

Statische Website (Orange/Creme) für Tangerine Motors, das Simulationsunternehmen unseres Teams in der Customer Value Challenge.
Typografie aus der FY26-Präsentation (Space Grotesk, DM Sans, JetBrains Mono), Logo in Montserrat.

## Struktur
| Bereich | Dateien |
|---|---|
| Start | `index.html` |
| Modelle (Produkte) | `modelle.html` – Engineering- und Marketingwerte je Linie, Region und Periode, Marktanteil, Absatz |
| Unternehmen | `unternehmen.html` |
| **Investor Relations** | `investoren.html` (Übersicht), `investoren-ergebnisse.html` (FY26 Präsentation, Downloads), `investoren-kennzahlen.html` (Marktanteile in %, Absatz, Marktvolumen, Business Index, Datenhinweise), `investoren-aktionaere.html` (Aktie, HV, Dividende, Finanzkalender), `investoren-governance.html` |
| Presse, Kontakt, Impressum | `presse.html`, `kontakt.html`, `impressum.html` |

## Daten
- Alle Zahlen stammen aus **„Group Oragange All Data .xlsx“** → `data/simulation.json` (Extraktion: `_build/extract.py`).
- Keine Fahrzeugpreise auf der Website (Spalte „Price“ wird nicht übernommen).
- „Market Size“ in der Excel = Marktanteil (in Periode 6 als „Market Share“ beschriftet) → in Prozent dargestellt.
- FY26 = Periode 8 der Excel.
- Umsatz, EBIT, ROCE, Aktienkurs, CO₂, Mitarbeitermoral sind nicht in der Excel → auf der IR-Seite als offen markiert.
- Unstimmigkeiten in der Excel werden beim Build automatisch erkannt und auf der Kennzahlen-Seite unter „Hinweise zur Datenqualität“ gelistet.
- `data/tangerine-motors-operative-daten.csv` wird beim Build erzeugt (Download auf der IR-Seite).

## Aktualisieren
```bash
python3 _build/extract.py "/pfad/zu/Group Oragange All Data .xlsx"   # neue Excel einlesen
python3 _build/build.py                                               # Seiten neu erzeugen
```
Texte und Termine: `_build/content.py`. FY26 Präsentation: `assets/ir/FY26-Praesentation.pdf` / `.pptx` ersetzen.

## Veröffentlichen
Reines HTML/CSS/JS ohne Abhängigkeiten – läuft auf GitHub Pages (Branch `main`, Ordner `/`).
