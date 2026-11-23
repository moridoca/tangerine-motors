# Redaktionelle Inhalte (Texte, Namen, Termine). Alle ZAHLEN kommen aus data/simulation.json (Excel).

COMPANY = {
    "name": "Tangerine Motors",
    "mail_ir": "ir@tangerine-motors.example",
    "mail_info": "info@tangerine-motors.example",
    "mail_press": "presse@tangerine-motors.example",
    "fy": "FY26",
    "fy_period": 8,          # FY26 = Periode 8 der Excel
    "first_period": 1,
    "merger_period": 5,      # Region 2 ab Periode 5 in der Excel
}

LINE_META = [
    {"key": "Low Cost", "id": "clementine", "name": "Clementine", "car": "lowcost", "role": "Kostenführer",
     "tagline": "Robust, geräumig, ehrlich kalkuliert.",
     "intro": "Der Clementine ist auf das reduziert, wofür seine Käufer zahlen: Robustheit und Platz. Wenig Elektronik, viele Gleichteile, Lieferfähigkeit vor Ausstattung.",
     "customer": "Preis und Lieferfähigkeit entscheiden, Marketing und Technik kaum. Gekauft wird aus praktischen Gründen."},
    {"key": "Family", "id": "grove", "name": "Grove", "car": "family", "role": "Cash Cow",
     "tagline": "Platz für alle. Verlässlich jeden Tag.",
     "intro": "Der Grove ist das Familienauto im Portfolio: stabile Ausstattung, Händler in der Nähe für Kauf und Service. Er finanziert den Ausbau der Wachstumslinien.",
     "customer": "Mittlere Sensibilität für alle Kriterien. Der Family-Markt in Region 1 schrumpft, in Region 2 wächst er."},
    {"key": "Eco", "id": "zest", "name": "Zest", "car": "eco", "role": "Wachstumslinie",
     "tagline": "Gebaut um den Verbrauch herum.",
     "intro": "Der Zest ist konsequent auf niedrigen Verbrauch und geringe Emissionen ausgelegt – weniger Leistung, mehr Technik. Mit wachsendem Volumen sinken die Stückkosten.",
     "customer": "Technik zählt am meisten. Am schnellsten wachsender Markt in Region 1; in Region 2 bisher nicht angeboten."},
    {"key": "Image", "id": "sanguine", "name": "Sanguine GT", "car": "sport", "role": "Markenführer",
     "tagline": "Neuheit, Technik und Marke.",
     "intro": "Der Sanguine GT gibt dem Image-Kunden, was er sucht: Performance, Technologie und Markenstärke – mit exklusivem Vertrieb und Premium-Service.",
     "customer": "Technik und Marketing sind entscheidend. Teuerste Kapazität bei kaum Skaleneffekten."},
]

CRIT_DE = {
    "Design": "Design", "Performance": "Performance", "Comfort": "Komfort", "Robustness": "Robustheit", "Size": "Größe",
    "Technology": "Technologie", "Consumption / Pollution": "Verbrauch / Emissionen", "Models in Range": "Modellvielfalt",
    "Novelty": "Neuheit", "Car Dealership Proximity": "Händlernähe", "Purchasing Experience": "Kauferlebnis",
    "After Sales Experience": "After-Sales", "Brand Power": "Markenstärke",
}
ENGINEERING = ["Design", "Performance", "Comfort", "Robustness", "Size", "Technology", "Consumption / Pollution", "Models in Range", "Novelty"]
MARKETING = ["Car Dealership Proximity", "Purchasing Experience", "After Sales Experience", "Brand Power"]

# Business Index aus den Simulations-Screenshots (23.11.2026, 18:06), Werte abgelesen; Nummerierung P4–P12 der Simulation
BUSINESS_INDEX = {
    "periods": ["P4", "P5", "P6", "P7", "P8", "P9", "P10", "P11", "P12"],
    "Region 1": [1.04, 1.05, 1.06, 1.08, 1.11, 1.05, 0.936, 1.05, 1.20],
    "Region 2": [1.00, 1.00, 1.00, 1.06, 1.12, 1.19, 1.26, 1.34, 1.42],
}

CALENDAR = [
    ("23.11.2026", "FY26 Präsentation – Shareholders Presentation, Customer Value Challenge", "Ergebnisse"),
    ("Q1 2027", "Geschäftsbericht FY26", "Bericht"),
    ("Q2 2027", "Ordentliche Hauptversammlung", "HV"),
    ("Q3 2027", "Halbjahresbericht H1 FY27", "Bericht"),
]

BOARD = [
    ("CEO", "Vorstandsvorsitz", "Strategie, Fusion, Kapitalallokation"),
    ("CFO", "Finanzvorstand", "Finanzen, HR & Qualität, Verschuldung"),
    ("LC", "Direktor Low Cost", "Clementine – Engineering, Marketing, Produktion"),
    ("FA", "Direktor Family", "Grove – Engineering, Marketing, Produktion"),
    ("EC", "Direktor Eco-Friendly", "Zest – Engineering, Marketing, Produktion"),
    ("IM", "Direktor Image", "Sanguine GT – Engineering, Marketing, Produktion"),
]

# Kennzahlen, die NICHT in der Excel stehen -> Platzhalter auf der IR-Seite
OPEN_KPIS = ["Umsatz", "EBIT", "ROCE", "Kum. Gewinnrücklagen", "Aktienkurs", "CO₂-Emissionen", "Mitarbeitermoral", "Verschuldungsgrad"]

# Manuell festgestellte Abweichung zwischen den beiden Excel-Dateien
EXTRA_DQ = [
    "Region 2, Periode 7, Low Cost: Absatz 362 laut „Group Orange All Data“, 287 laut „Group_5 Excel“ (Blatt Budget_v07); Marktanteil Family 28 % vs. 27 %. Die Website verwendet „All Data“.",
    "Der Business Index stammt aus Screenshots der Simulation (abgelesen) und nutzt deren Nummerierung P4–P12; die Excel zählt Periode 1–8.",
    "Umsatz, EBIT, ROCE, Aktienkurs, CO₂ und Mitarbeitermoral sind in den Excel-Dateien nicht enthalten und deshalb als offen markiert.",
]
