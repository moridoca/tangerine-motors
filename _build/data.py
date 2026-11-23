# Alle Inhalte und Kennzahlen der Website an einer Stelle.
# WICHTIG: Sämtliche Zahlen sind BEISPIELWERTE für das fiktive Unternehmen Tangerine Motors
# (Customer Value Challenge). Vor einer Präsentation durch die finalen Simulationswerte ersetzen.

COMPANY = {
    "name": "Tangerine Motors",
    "claim": "Vier Fahrzeuglinien. Eine Kapitalstrategie.",
    "mail_ir": "ir@tangerine-motors.example",
    "mail_info": "info@tangerine-motors.example",
    "mail_press": "presse@tangerine-motors.example",
    "start_period": "P4",
    "final_period": "P10",
}

PROFILE_KEYS = ["Design", "Performance", "Komfort", "Robustheit", "Größe", "Technologie", "Verbrauch", "Modellvielfalt", "Neuheit"]
MARKETING_KEYS = ["Händlernähe", "Kauferlebnis", "After-Sales", "Markenstärke"]

MODELS = [
    {
        "id": "clementine", "name": "Clementine", "line": "Low Cost", "car": "lowcost",
        "tagline": "Robust, geräumig, ehrlich kalkuliert.",
        "intro": "Der Clementine ist auf das reduziert, wofür seine Käufer bezahlen: Robustheit und Platz. Wenig Elektronik, viele Gleichteile, ein dichtes Händlernetz – so bleibt er Kostenführer.",
        "customer": "Preis und Lieferfähigkeit entscheiden, Marketing und Technik kaum. Gekauft wird aus praktischen Gründen.",
        "profile": [3, 3, 4, 8, 7, 3, 6, 3, 2],
        "marketing": [8, 4, 6, 3],
        "price": "ab 16.900 €",
        "role": "Kostenführer",
    },
    {
        "id": "grove", "name": "Grove", "line": "Family", "car": "family",
        "tagline": "Platz für alle. Verlässlich jeden Tag.",
        "intro": "Der Grove ist das Familienauto mit dem größten Ergebnisbeitrag im Haus. Stabile Ausstattung, stabiler Preis und ein Händler in der Nähe – für Kauf und Service.",
        "customer": "Mittlere Sensibilität für alle Kriterien. Markt in Region 1 schrumpft um rund 5 % pro Periode.",
        "profile": [6, 5, 7, 8, 9, 6, 6, 5, 5],
        "marketing": [8, 6, 7, 5],
        "price": "ab 27.400 €",
        "role": "Cash Cow",
    },
    {
        "id": "zest", "name": "Zest", "line": "Eco-Friendly", "car": "eco",
        "tagline": "Gebaut um den Verbrauch herum.",
        "intro": "Der Zest ist konsequent auf niedrigen Verbrauch und geringe CO₂-Emissionen ausgelegt. Weniger Leistung, mehr Technik – und mit wachsendem Volumen sinken die Stückkosten.",
        "customer": "Technik zählt am meisten, der Preis wenig. Am schnellsten wachsender Markt in Region 1 (+15 % pro Periode).",
        "profile": [5, 4, 5, 5, 4, 8, 10, 4, 7],
        "marketing": [6, 6, 6, 7],
        "price": "ab 31.900 €",
        "role": "Wachstumslinie",
    },
    {
        "id": "sanguine", "name": "Sanguine GT", "line": "Image", "car": "sport",
        "tagline": "Neuheit, Technik und Marke – mit Preis.",
        "intro": "Der Sanguine GT gibt dem Image-Kunden, was er sucht: Neuheit, Technologie und Markenstärke. Exklusiver Vertrieb und Premium-Service rechtfertigen den Preis.",
        "customer": "Technik und Marketing sind entscheidend, der Preis kaum. Teuerste Kapazität bei kaum Skaleneffekten.",
        "profile": [9, 9, 8, 7, 5, 9, 4, 7, 9],
        "marketing": [4, 9, 9, 9],
        "price": "ab 68.500 €",
        "role": "Preis- und Markenführer",
    },
]

# Sechs Ranking-Kriterien der Simulation: Start (P4) -> Final
KPIS = [
    {"label": "Umsatz", "start": 412, "final": 538, "fmt": "{:,.0f} Mio. €", "better": "up"},
    {"label": "Kum. Gewinnrücklagen", "start": 61, "final": 118, "fmt": "{:,.0f} Mio. €", "better": "up"},
    {"label": "ROCE", "start": 6.1, "final": 11.4, "fmt": "{:.1f} %", "better": "up"},
    {"label": "CO₂-Emissionen", "start": 142, "final": 109, "fmt": "{:.0f} g/km", "better": "down"},
    {"label": "Mitarbeitermoral", "start": 64, "final": 78, "fmt": "{:.0f} %", "better": "up"},
    {"label": "Aktienkurs", "start": 24.0, "final": 37.8, "fmt": "{:.2f} €", "better": "up"},
]

# Segmente in der finalen Periode, Mio. €
SEGMENTS = [
    {"line": "Low Cost", "model": "Clementine", "revenue": 118, "ebit": 9},
    {"line": "Family", "model": "Grove", "revenue": 176, "ebit": 31},
    {"line": "Eco-Friendly", "model": "Zest", "revenue": 149, "ebit": 14},
    {"line": "Image", "model": "Sanguine GT", "revenue": 95, "ebit": 22},
]

SHARE_PRICE = [("P4", 24.0), ("P5", 22.6), ("P6", 25.9), ("P7", 27.4), ("P8", 31.2), ("P9", 34.5), ("P10", 37.8)]
EBIT_SERIES = [("P4", -2), ("P5", -9), ("P6", 18), ("P7", 34), ("P8", 51), ("P9", 63), ("P10", 76)]

LEVERAGE = 34  # Verschuldungsgrad in %, Ziel < 40 %
DIVIDEND = "0,90 €"

CALENDAR = [
    ("18.03.2027", "Geschäftsbericht 2026 und Analystenkonferenz", "Bericht"),
    ("12.05.2027", "Quartalsmitteilung Q1 2027", "Bericht"),
    ("24.06.2027", "Ordentliche Hauptversammlung", "HV"),
    ("05.08.2027", "Halbjahresfinanzbericht 2027", "Bericht"),
    ("10.11.2027", "Quartalsmitteilung Q3 2027", "Bericht"),
]

REPORTS = [
    ("Geschäftsbericht 2026", "PDF · in Vorbereitung"),
    ("Shareholders Presentation – Customer Value Challenge", "Präsentation"),
    ("Quartalsmitteilung Q3 2026", "PDF · in Vorbereitung"),
    ("Finanzkalender 2027", "ICS · in Vorbereitung"),
]

BOARD = [
    ("CEO", "Vorstandsvorsitz", "Strategie, Fusion, Kapitalallokation"),
    ("CFO", "Finanzvorstand", "Finanzen, HR & Qualität, Verschuldung"),
    ("DLC", "Direktor Low Cost", "Clementine – Engineering, Marketing, Produktion"),
    ("DFA", "Direktor Family", "Grove – Engineering, Marketing, Produktion"),
    ("DEC", "Direktor Eco-Friendly", "Zest – Engineering, Marketing, Produktion"),
    ("DIM", "Direktor Image", "Sanguine GT – Engineering, Marketing, Produktion"),
]

NEWS = [
    ("23.11.2026", "Unternehmen", "Tangerine Motors präsentiert Ergebnis der Customer Value Challenge"),
    ("02.11.2026", "Produkt", "Zest: Verbrauch erneut gesenkt, Reichweite der Baureihe erweitert"),
    ("14.10.2026", "Investor Relations", "Verschuldungsgrad unter 40 % – Dividende wieder vorgesehen"),
]
