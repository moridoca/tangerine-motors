# Tangerine Motors – Website

Statische Unternehmenswebsite im Design der *Shareholders Presentation – Customer Value Challenge*
(Space Grotesk / DM Sans / JetBrains Mono, #0D0E0C · #0F2219 · Lime #C5F442 · Tangerine #FF7A45).

## Seiten
| Datei | Inhalt |
|---|---|
| `index.html` | Start: Hero, Modelle, Umsatzmix, IR-Teaser, Neuigkeiten |
| `modelle.html` | Produktabteilung: Clementine (Low Cost), Grove (Family), Zest (Eco-Friendly), Sanguine GT (Image) mit Produktprofil, Marketing, Vergleichstabelle |
| `unternehmen.html` | Strategie, Meilensteine, Nachhaltigkeit, Vorstand |
| `investor-relations.html` | Sechs Ranking-Kriterien, Aktie/EBIT-Verlauf, Segmente, Equity Story, Finanzkalender, Berichte, IR-Kontakt |
| `presse.html` | Meldungen, Mediathek, Pressekontakt |
| `kontakt.html` | Kontaktformular (öffnet E-Mail-Programm, speichert nichts) |
| `impressum.html` | Impressum & Datenschutz (Platzhalter) |

## Inhalte ändern
Alle Texte, Modelle und Kennzahlen stehen in `_build/data.py`. Danach neu erzeugen:

```bash
python3 _build/build.py
```

## Hinweis
Fiktives Unternehmen. **Alle Kennzahlen, Preise und Produktwerte sind Beispielwerte** und vor der
Präsentation durch die finalen Simulationswerte zu ersetzen. Impressum-Angaben sind Platzhalter;
die E-Mail-Adressen nutzen die reservierte Domain `.example`.

## Veröffentlichen
Reines HTML/CSS/JS ohne Build-Abhängigkeiten – läuft auf GitHub Pages (Branch `main`, Ordner `/`).
