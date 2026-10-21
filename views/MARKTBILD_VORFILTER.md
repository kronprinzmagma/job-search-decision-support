# MARKTBILD — auf Listenebene aussortiert

*Erzeugt von `scripts/marktbild.py` aus `data/screening_log.json`. Nicht von Hand bearbeiten.*

Diese Datei enthält jede Anzeige, die das Screening gesehen und **ohne Volltext** aussortiert hat. Auf Listenebene dürfen nur Firmen-Ausschluss, Vermittler, Beratung/Agentur, Distanz laut Ortstabelle, Junior/Praktikum, Engineering- und Entwicklerrollen, offensichtliche Nicht-Rollen und physische Produkte entscheiden (`spec/SWEEP.md`, «Listenebene»). Die im Volltext geprüften Fälle stehen in `MARKTBILD_VOLLTEXT.md`, ihre Anzeigen als `<id>--anzeige--<erfasst>.md` im jeweiligen Fall-Ordner.

Dieselben Daten als CSV zum Weiterrechnen: `data/marktbild_vorfilter.csv` (Semikolon-getrennt).

## Überblick

| Kategorie | Anzahl | Anteil |
|---|---:|---:|
| Kein Produktmandat (Nicht-Rolle, Betrieb, Support) | 564 | 34 % |
| Engineering / Entwicklung / Architektur | 417 | 25 % |
| Physisches Produktmanagement | 159 | 9 % |
| Vermittler / Personalberatung | 130 | 8 % |
| Junior / Praktikum / Lehrstelle | 128 | 7 % |
| Beratung / Agentur | 123 | 7 % |
| Firmen-Ausschluss der Persona | 61 | 3 % |
| Distanz | 40 | 2 % |
| **Total** | **1622** | |

## Woher das Rauschen kommt

| Kanal | auf Listenebene weg |
|---|---:|
| portal | 1178 |
| netzwerk-suche | 374 |
| netzwerk-empfehlung | 43 |
| behoerdenportal | 17 |
| zielportal | 10 |

## Firmen mit drei oder mehr aussortierten Anzeigen

*Wer oft auftaucht, sucht viel — auch wenn diesmal nichts passte. Kandidaten für die Zielportal-Liste.*

| Firma | Anzeigen |
|---|---:|
| Amberlin Versicherung AG | 76 |
| Veltrima Gesundheitsdienste AG | 75 |
| Tuskora Lebensmittel AG | 69 |
| Jobvera Staffing AG | 67 |
| Fendrix Analytics AG | 65 |
| Talentbrücke Personal AG | 63 |
| Pixavo Agentur GmbH | 63 |
| Trellin Immobilien AG | 61 |
| Mastrova Industrie AG | 61 |
| Spielora Gaming AG | 61 |
| Sanuvia Health AG | 60 |
| Kandora Consulting AG | 60 |
| Kalvit Software AG | 58 |
| Lernovi Bildung AG | 57 |
| Quendor Versicherungen AG | 56 |
| Brivana Privatbank AG | 55 |
| Sorvik Logistik AG | 55 |
| Vendaro Retail AG | 54 |
| Hovald Bau AG | 53 |
| Cirrova Cloud AG | 53 |
| Pelvio Mobility AG | 52 |
| Kombira Versand AG | 50 |
| Telvaro Kommunikation AG | 50 |
| Quelvia Pharma AG | 49 |
| Ristra Finanztechnik AG | 49 |
| Varella Energie AG | 47 |
| Orvana Reisen AG | 46 |
| Mirvel Medien AG | 40 |
| Kantonale Verwaltung Altmark | 10 |
| Stadtverwaltung Nordtal | 7 |

## Alle Einträge nach Kategorie

### Kein Produktmandat (Nicht-Rolle, Betrieb, Support) (564)

| Datum | Firma | Rolle | Ort | Kanal | Grund |
|---|---|---|---|---|---|
| 2025-03-03 | Cirrova Cloud AG | UX Designer Daten | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-03 | Fendrix Analytics AG | Projektleiter Digitalisierung Prozesse | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-03 | Fendrix Analytics AG | Scrum Master (80–100 %) | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-03 | Kalvit Software AG | Requirements Engineer Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-03 | Kalvit Software AG | Requirements Engineer | Zürich | zielportal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-03 | Lernovi Bildung AG | UX Designer Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-03 | Orvana Reisen AG | Scrum Master Daten | Luzern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-03 | Ristra Finanztechnik AG | Requirements Engineer Prozesse | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-03 | Sanuvia Health AG | Requirements Engineer (80–100 %) | Winterthur | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-03 | Trellin Immobilien AG | Requirements Engineer Plattform-Services | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-03 | Trellin Immobilien AG | Projektleiter Digitalisierung Prozesse | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-03 | Veltrima Gesundheitsdienste AG | Projektleiter Digitalisierung | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-03 | Vendaro Retail AG | Projektleiter Digitalisierung B2B | Zürich | netzwerk-empfehlung | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-04 | Brivana Privatbank AG | Business Analyst B2B | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-04 | Cirrova Cloud AG | Business Analyst Digital Channels | Schlieren | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-04 | Kalvit Software AG | UX Designer | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-04 | Kombira Versand AG | UX Designer Kundenerlebnis | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-04 | Lernovi Bildung AG | Projektleiter Digitalisierung | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-04 | Mirvel Medien AG | UX Designer Kundenerlebnis | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-04 | Orvana Reisen AG | Projektleiter Digitalisierung | Luzern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-04 | Quendor Versicherungen AG | Business Analyst Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-04 | Quendor Versicherungen AG | Business Analyst | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-04 | Varella Energie AG | UX Designer | Baden | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-04 | Veltrima Gesundheitsdienste AG | Projektleiter Digitalisierung Daten | St. Gallen | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-05 | Amberlin Versicherung AG | Business Analyst Plattform-Services | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-05 | Amberlin Versicherung AG | Requirements Engineer | Lausanne | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-05 | Brivana Privatbank AG | Requirements Engineer Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-05 | Fendrix Analytics AG | Projektleiter Digitalisierung Kundenerlebnis | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-05 | Mirvel Medien AG | Requirements Engineer | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-05 | Mirvel Medien AG | Scrum Master | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-05 | Ristra Finanztechnik AG | Scrum Master Plattform-Services | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-05 | Ristra Finanztechnik AG | UX Designer Plattform-Services | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-05 | Ristra Finanztechnik AG | Scrum Master (80–100 %) | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-05 | Sorvik Logistik AG | UX Designer (80–100 %) | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-05 | Sorvik Logistik AG | Business Analyst | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-05 | Trellin Immobilien AG | Requirements Engineer B2B | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-05 | Veltrima Gesundheitsdienste AG | Business Analyst Daten | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-05 | Vendaro Retail AG | Projektleiter Digitalisierung Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-06 | Amberlin Versicherung AG | UX Designer | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-06 | Fendrix Analytics AG | Scrum Master Prozesse | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-06 | Kantonale Verwaltung Altmark | Requirements Engineer | Aarau | behoerdenportal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-06 | Kantonale Verwaltung Altmark | Scrum Master Prozesse | Aarau | behoerdenportal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-06 | Kombira Versand AG | Business Analyst Kundenerlebnis | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-06 | Orvana Reisen AG | Business Analyst Prozesse | Luzern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-06 | Pelvio Mobility AG | UX Designer | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-06 | Quelvia Pharma AG | Projektleiter Digitalisierung | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-06 | Ristra Finanztechnik AG | UX Designer B2B | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-06 | Sanuvia Health AG | Business Analyst Digital Channels | Winterthur | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-06 | Sorvik Logistik AG | UX Designer B2B | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-06 | Telvaro Kommunikation AG | Scrum Master | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-06 | Varella Energie AG | Business Analyst | Baden | netzwerk-empfehlung | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-07 | Amberlin Versicherung AG | UX Designer Plattform-Services | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-07 | Brivana Privatbank AG | Business Analyst Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-07 | Quelvia Pharma AG | Business Analyst | Basel | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-07 | Telvaro Kommunikation AG | UX Designer | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-07 | Trellin Immobilien AG | Business Analyst | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-07 | Veltrima Gesundheitsdienste AG | UX Designer | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-10 | Brivana Privatbank AG | Scrum Master B2B | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-10 | Brivana Privatbank AG | Projektleiter Digitalisierung | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-10 | Fendrix Analytics AG | UX Designer Daten | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-10 | Fendrix Analytics AG | Requirements Engineer Kundenerlebnis | Baden | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-10 | Orvana Reisen AG | Scrum Master Plattform-Services | Luzern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-10 | Quelvia Pharma AG | Projektleiter Digitalisierung (80–100 %) | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-10 | Sanuvia Health AG | Projektleiter Digitalisierung Daten | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-10 | Trellin Immobilien AG | UX Designer Plattform-Services | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-10 | Veltrima Gesundheitsdienste AG | Projektleiter Digitalisierung Prozesse | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-10 | Veltrima Gesundheitsdienste AG | UX Designer Kundenerlebnis | St. Gallen | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-11 | Lernovi Bildung AG | Scrum Master B2B | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-11 | Pelvio Mobility AG | Projektleiter Digitalisierung | Bern | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-11 | Quendor Versicherungen AG | UX Designer Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-11 | Ristra Finanztechnik AG | Business Analyst | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-11 | Sorvik Logistik AG | Scrum Master Daten | Kloten | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-11 | Sorvik Logistik AG | Scrum Master | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-11 | Vendaro Retail AG | Business Analyst Plattform-Services | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-11 | Vendaro Retail AG | Scrum Master Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-12 | Cirrova Cloud AG | UX Designer Digital Channels | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-12 | Cirrova Cloud AG | Projektleiter Digitalisierung Digital Channels | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-12 | Kalvit Software AG | Requirements Engineer Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-12 | Lernovi Bildung AG | Scrum Master | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-12 | Mirvel Medien AG | UX Designer Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-12 | Mirvel Medien AG | Requirements Engineer Digital Channels | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-12 | Pelvio Mobility AG | Projektleiter Digitalisierung Prozesse | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-12 | Quelvia Pharma AG | Business Analyst Plattform-Services | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-12 | Ristra Finanztechnik AG | Business Analyst Plattform-Services | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-12 | Sorvik Logistik AG | Projektleiter Digitalisierung Kundenerlebnis | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-12 | Telvaro Kommunikation AG | Projektleiter Digitalisierung Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-12 | Telvaro Kommunikation AG | Business Analyst (80–100 %) | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-12 | Trellin Immobilien AG | Requirements Engineer Prozesse | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-12 | Trellin Immobilien AG | Scrum Master (80–100 %) | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-12 | Trellin Immobilien AG | UX Designer | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-12 | Veltrima Gesundheitsdienste AG | Scrum Master (80–100 %) | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-13 | Fendrix Analytics AG | UX Designer Kundenerlebnis | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-13 | Fendrix Analytics AG | Business Analyst | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-13 | Fendrix Analytics AG | Requirements Engineer Prozesse | Baden | netzwerk-empfehlung | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-13 | Kalvit Software AG | UX Designer Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-13 | Kalvit Software AG | UX Designer B2B | Zürich | netzwerk-empfehlung | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-13 | Kombira Versand AG | Business Analyst | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-13 | Kombira Versand AG | Scrum Master Prozesse | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-13 | Lernovi Bildung AG | UX Designer Kundenerlebnis | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-13 | Mirvel Medien AG | Projektleiter Digitalisierung | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-13 | Quendor Versicherungen AG | Scrum Master Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-13 | Sanuvia Health AG | Projektleiter Digitalisierung | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-13 | Sorvik Logistik AG | Requirements Engineer Plattform-Services | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-13 | Trellin Immobilien AG | UX Designer Digital Channels | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-13 | Varella Energie AG | Scrum Master | Baden | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-13 | Vendaro Retail AG | Requirements Engineer Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-13 | Vendaro Retail AG | Requirements Engineer | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-14 | Amberlin Versicherung AG | Projektleiter Digitalisierung (80–100 %) | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-14 | Brivana Privatbank AG | Business Analyst | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-14 | Brivana Privatbank AG | UX Designer (80–100 %) | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-14 | Cirrova Cloud AG | Requirements Engineer Plattform-Services | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-14 | Lernovi Bildung AG | Business Analyst | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-14 | Mirvel Medien AG | Business Analyst | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-14 | Sorvik Logistik AG | Scrum Master Kundenerlebnis | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-14 | Sorvik Logistik AG | Requirements Engineer Prozesse | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-17 | Cirrova Cloud AG | Business Analyst (80–100 %) | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-17 | Kalvit Software AG | Business Analyst | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-17 | Kombira Versand AG | Projektleiter Digitalisierung Daten | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-17 | Lernovi Bildung AG | Scrum Master Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-17 | Mirvel Medien AG | Scrum Master Kundenerlebnis | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-17 | Mirvel Medien AG | UX Designer | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-17 | Orvana Reisen AG | UX Designer | Luzern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-17 | Orvana Reisen AG | Business Analyst Digital Channels | Luzern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-17 | Pelvio Mobility AG | Business Analyst | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-17 | Pelvio Mobility AG | UX Designer Daten | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-17 | Quendor Versicherungen AG | Projektleiter Digitalisierung Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-17 | Quendor Versicherungen AG | UX Designer | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-17 | Sanuvia Health AG | Business Analyst | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-17 | Sanuvia Health AG | Scrum Master Daten | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-17 | Trellin Immobilien AG | UX Designer Prozesse | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-17 | Trellin Immobilien AG | Scrum Master | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-17 | Varella Energie AG | Scrum Master Prozesse | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-18 | Amberlin Versicherung AG | Requirements Engineer Digital Channels | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-18 | Amberlin Versicherung AG | Projektleiter Digitalisierung B2B | Lausanne | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-18 | Brivana Privatbank AG | Requirements Engineer Kundenerlebnis | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-18 | Cirrova Cloud AG | Requirements Engineer Prozesse | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-18 | Kalvit Software AG | UX Designer Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-18 | Pelvio Mobility AG | Scrum Master Prozesse | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-18 | Pelvio Mobility AG | Requirements Engineer Daten | Bern | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-18 | Quelvia Pharma AG | Requirements Engineer Daten | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-18 | Sanuvia Health AG | Requirements Engineer B2B | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-18 | Sanuvia Health AG | UX Designer (80–100 %) | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-18 | Telvaro Kommunikation AG | Projektleiter Digitalisierung | Zürich | netzwerk-empfehlung | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-18 | Trellin Immobilien AG | Scrum Master Plattform-Services | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-19 | Amberlin Versicherung AG | Scrum Master Plattform-Services | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-19 | Brivana Privatbank AG | Requirements Engineer Plattform-Services | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-19 | Brivana Privatbank AG | Requirements Engineer Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-19 | Fendrix Analytics AG | UX Designer Digital Channels | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-19 | Fendrix Analytics AG | Scrum Master Daten | Baden | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-19 | Lernovi Bildung AG | UX Designer | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-19 | Mirvel Medien AG | Scrum Master Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-19 | Mirvel Medien AG | Projektleiter Digitalisierung B2B | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-19 | Sanuvia Health AG | UX Designer Kundenerlebnis | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-19 | Stadtverwaltung Nordtal | Projektleiter Digitalisierung Digital Channels | Winterthur | behoerdenportal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-19 | Telvaro Kommunikation AG | UX Designer B2B | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-19 | Veltrima Gesundheitsdienste AG | Business Analyst | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-19 | Vendaro Retail AG | Scrum Master Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-20 | Brivana Privatbank AG | Requirements Engineer Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-20 | Brivana Privatbank AG | Scrum Master Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-20 | Fendrix Analytics AG | UX Designer | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-20 | Fendrix Analytics AG | Requirements Engineer (80–100 %) | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-20 | Kalvit Software AG | Requirements Engineer Prozesse | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-20 | Kalvit Software AG | Business Analyst Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-20 | Kalvit Software AG | Business Analyst (80–100 %) | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-20 | Kalvit Software AG | Scrum Master | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-20 | Lernovi Bildung AG | Scrum Master (80–100 %) | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-20 | Mirvel Medien AG | Requirements Engineer Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-20 | Mirvel Medien AG | UX Designer Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-20 | Quelvia Pharma AG | Scrum Master Digital Channels | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-20 | Sanuvia Health AG | Projektleiter Digitalisierung Digital Channels | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-20 | Varella Energie AG | Scrum Master (80–100 %) | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-20 | Veltrima Gesundheitsdienste AG | Requirements Engineer Kundenerlebnis | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-20 | Veltrima Gesundheitsdienste AG | Business Analyst Plattform-Services | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-20 | Vendaro Retail AG | Scrum Master | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Brivana Privatbank AG | UX Designer | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Brivana Privatbank AG | UX Designer Digital Channels | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Cirrova Cloud AG | UX Designer Kundenerlebnis | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Fendrix Analytics AG | Business Analyst B2B | Baden | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Lernovi Bildung AG | Business Analyst Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Orvana Reisen AG | Scrum Master Kundenerlebnis | Luzern | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Pelvio Mobility AG | Requirements Engineer B2B | Bern | zielportal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Pelvio Mobility AG | Business Analyst Plattform-Services | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Quendor Versicherungen AG | Projektleiter Digitalisierung | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Ristra Finanztechnik AG | Requirements Engineer B2B | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Ristra Finanztechnik AG | Projektleiter Digitalisierung Kundenerlebnis | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Sanuvia Health AG | Projektleiter Digitalisierung (80–100 %) | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Sanuvia Health AG | Business Analyst (80–100 %) | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Sorvik Logistik AG | Requirements Engineer | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Sorvik Logistik AG | Business Analyst (80–100 %) | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Trellin Immobilien AG | Projektleiter Digitalisierung Plattform-Services | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Varella Energie AG | UX Designer (80–100 %) | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Veltrima Gesundheitsdienste AG | Requirements Engineer Digital Channels | St. Gallen | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Veltrima Gesundheitsdienste AG | Scrum Master Digital Channels | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-21 | Vendaro Retail AG | Business Analyst | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-22 | Amberlin Versicherung AG | Business Analyst | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-22 | Kalvit Software AG | UX Designer Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-22 | Quendor Versicherungen AG | Requirements Engineer Kundenerlebnis | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-22 | Quendor Versicherungen AG | Scrum Master | Zürich | zielportal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-22 | Trellin Immobilien AG | UX Designer B2B | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-24 | Amberlin Versicherung AG | UX Designer Daten | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-24 | Cirrova Cloud AG | Business Analyst Daten | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-24 | Kombira Versand AG | UX Designer | Dübendorf | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-24 | Orvana Reisen AG | Business Analyst | Luzern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-24 | Quelvia Pharma AG | UX Designer | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-24 | Quelvia Pharma AG | UX Designer Digital Channels | Basel | netzwerk-empfehlung | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-24 | Quelvia Pharma AG | Projektleiter Digitalisierung Kundenerlebnis | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-24 | Sanuvia Health AG | UX Designer B2B | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-24 | Sorvik Logistik AG | Business Analyst B2B | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-24 | Veltrima Gesundheitsdienste AG | Requirements Engineer Daten | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-24 | Veltrima Gesundheitsdienste AG | UX Designer Digital Channels | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-25 | Amberlin Versicherung AG | Scrum Master Daten | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-25 | Brivana Privatbank AG | Business Analyst Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-25 | Cirrova Cloud AG | UX Designer | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-25 | Kombira Versand AG | Requirements Engineer Prozesse | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-25 | Kombira Versand AG | Scrum Master B2B | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-25 | Lernovi Bildung AG | UX Designer Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-25 | Quelvia Pharma AG | Scrum Master | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-25 | Quendor Versicherungen AG | UX Designer Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-25 | Ristra Finanztechnik AG | Requirements Engineer Digital Channels | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-25 | Ristra Finanztechnik AG | Scrum Master | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-25 | Sorvik Logistik AG | Scrum Master Digital Channels | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-25 | Telvaro Kommunikation AG | Business Analyst | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-25 | Varella Energie AG | Business Analyst B2B | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-25 | Veltrima Gesundheitsdienste AG | Projektleiter Digitalisierung Plattform-Services | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-25 | Vendaro Retail AG | Business Analyst Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Amberlin Versicherung AG | Projektleiter Digitalisierung | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Brivana Privatbank AG | Projektleiter Digitalisierung Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Brivana Privatbank AG | Projektleiter Digitalisierung (80–100 %) | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Kalvit Software AG | Business Analyst Kundenerlebnis | Zürich | zielportal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Kombira Versand AG | Requirements Engineer Plattform-Services | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Lernovi Bildung AG | Requirements Engineer Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Orvana Reisen AG | Scrum Master | Luzern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Pelvio Mobility AG | Projektleiter Digitalisierung Digital Channels | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Pelvio Mobility AG | UX Designer Kundenerlebnis | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Quelvia Pharma AG | Requirements Engineer Plattform-Services | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Quelvia Pharma AG | UX Designer (80–100 %) | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Sanuvia Health AG | Requirements Engineer Kundenerlebnis | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Sorvik Logistik AG | Requirements Engineer Kundenerlebnis | Kloten | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Sorvik Logistik AG | Projektleiter Digitalisierung Plattform-Services | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Telvaro Kommunikation AG | UX Designer Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Varella Energie AG | Scrum Master Digital Channels | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Veltrima Gesundheitsdienste AG | Requirements Engineer Plattform-Services | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Veltrima Gesundheitsdienste AG | UX Designer Prozesse | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Vendaro Retail AG | Projektleiter Digitalisierung | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-26 | Vendaro Retail AG | Projektleiter Digitalisierung Kundenerlebnis | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-27 | Cirrova Cloud AG | Projektleiter Digitalisierung (80–100 %) | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-27 | Fendrix Analytics AG | UX Designer (80–100 %) | Baden | netzwerk-empfehlung | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-27 | Kalvit Software AG | Scrum Master B2B | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-27 | Kalvit Software AG | UX Designer Kundenerlebnis | Zürich | zielportal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-27 | Kombira Versand AG | UX Designer (80–100 %) | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-27 | Pelvio Mobility AG | Scrum Master | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-27 | Quendor Versicherungen AG | Requirements Engineer Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-27 | Ristra Finanztechnik AG | Business Analyst (80–100 %) | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-27 | Sorvik Logistik AG | Projektleiter Digitalisierung Digital Channels | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-27 | Telvaro Kommunikation AG | UX Designer Plattform-Services | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-27 | Varella Energie AG | Requirements Engineer Kundenerlebnis | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-27 | Varella Energie AG | Requirements Engineer | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-27 | Varella Energie AG | Projektleiter Digitalisierung B2B | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-28 | Amberlin Versicherung AG | UX Designer Kundenerlebnis | Lausanne | netzwerk-empfehlung | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-28 | Brivana Privatbank AG | Requirements Engineer | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-28 | Fendrix Analytics AG | UX Designer Prozesse | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-28 | Pelvio Mobility AG | Requirements Engineer Kundenerlebnis | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-28 | Quendor Versicherungen AG | Business Analyst (80–100 %) | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-28 | Ristra Finanztechnik AG | Requirements Engineer Kundenerlebnis | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-28 | Ristra Finanztechnik AG | UX Designer Digital Channels | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-28 | Sanuvia Health AG | UX Designer | Winterthur | netzwerk-empfehlung | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-28 | Sanuvia Health AG | Business Analyst Kundenerlebnis | Winterthur | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-28 | Sorvik Logistik AG | Scrum Master Plattform-Services | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-28 | Varella Energie AG | Business Analyst Digital Channels | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-28 | Varella Energie AG | UX Designer Prozesse | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-28 | Veltrima Gesundheitsdienste AG | Scrum Master | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-29 | Sanuvia Health AG | Business Analyst B2B | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-29 | Veltrima Gesundheitsdienste AG | Projektleiter Digitalisierung Digital Channels | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-31 | Brivana Privatbank AG | Projektleiter Digitalisierung Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-31 | Cirrova Cloud AG | Projektleiter Digitalisierung Daten | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-31 | Kalvit Software AG | Scrum Master Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-31 | Kombira Versand AG | UX Designer Digital Channels | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-31 | Kombira Versand AG | Scrum Master Digital Channels | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-31 | Lernovi Bildung AG | Requirements Engineer Kundenerlebnis | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-31 | Mirvel Medien AG | UX Designer (80–100 %) | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-31 | Mirvel Medien AG | Scrum Master Daten | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-31 | Orvana Reisen AG | Business Analyst Plattform-Services | Luzern | netzwerk-empfehlung | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-31 | Orvana Reisen AG | Scrum Master Prozesse | Luzern | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-31 | Pelvio Mobility AG | Projektleiter Digitalisierung B2B | Bern | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-31 | Quelvia Pharma AG | Requirements Engineer (80–100 %) | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-31 | Quelvia Pharma AG | Scrum Master Daten | Basel | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-31 | Telvaro Kommunikation AG | Requirements Engineer | Zürich | netzwerk-empfehlung | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-31 | Trellin Immobilien AG | Business Analyst Plattform-Services | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-03-31 | Trellin Immobilien AG | Business Analyst (80–100 %) | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Amberlin Versicherung AG | Projektleiter Digitalisierung Digital Channels | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Brivana Privatbank AG | Business Analyst (80–100 %) | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Brivana Privatbank AG | Business Analyst Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Brivana Privatbank AG | Scrum Master | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Fendrix Analytics AG | Projektleiter Digitalisierung | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Kalvit Software AG | Projektleiter Digitalisierung Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Kalvit Software AG | Business Analyst Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Kalvit Software AG | Scrum Master Kundenerlebnis | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Lernovi Bildung AG | Requirements Engineer | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Mirvel Medien AG | Business Analyst (80–100 %) | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Mirvel Medien AG | Business Analyst Digital Channels | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Pelvio Mobility AG | Requirements Engineer | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Quendor Versicherungen AG | Projektleiter Digitalisierung Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Quendor Versicherungen AG | Requirements Engineer Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Ristra Finanztechnik AG | Projektleiter Digitalisierung Prozesse | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Sanuvia Health AG | UX Designer Digital Channels | Winterthur | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Sorvik Logistik AG | Projektleiter Digitalisierung | Kloten | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Telvaro Kommunikation AG | Scrum Master Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Telvaro Kommunikation AG | Scrum Master (80–100 %) | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-01 | Varella Energie AG | Requirements Engineer Prozesse | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-02 | Amberlin Versicherung AG | Requirements Engineer Daten | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-02 | Brivana Privatbank AG | Scrum Master (80–100 %) | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-02 | Cirrova Cloud AG | Requirements Engineer | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-02 | Cirrova Cloud AG | Scrum Master Digital Channels | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-02 | Cirrova Cloud AG | Business Analyst | Schlieren | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-02 | Kombira Versand AG | Requirements Engineer | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-02 | Lernovi Bildung AG | Business Analyst Kundenerlebnis | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-02 | Pelvio Mobility AG | Scrum Master (80–100 %) | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-02 | Quelvia Pharma AG | Requirements Engineer | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-02 | Quendor Versicherungen AG | Requirements Engineer | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-02 | Quendor Versicherungen AG | Business Analyst Kundenerlebnis | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-02 | Sorvik Logistik AG | UX Designer Kundenerlebnis | Kloten | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-02 | Telvaro Kommunikation AG | Projektleiter Digitalisierung (80–100 %) | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-02 | Trellin Immobilien AG | Business Analyst Digital Channels | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-02 | Trellin Immobilien AG | Scrum Master Prozesse | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-02 | Vendaro Retail AG | Scrum Master Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Amberlin Versicherung AG | Scrum Master | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Cirrova Cloud AG | Scrum Master Prozesse | Schlieren | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Fendrix Analytics AG | Business Analyst Kundenerlebnis | Baden | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Kalvit Software AG | Business Analyst Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Kalvit Software AG | Scrum Master Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Kombira Versand AG | Scrum Master Kundenerlebnis | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Lernovi Bildung AG | Business Analyst Plattform-Services | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Lernovi Bildung AG | Business Analyst (80–100 %) | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Orvana Reisen AG | Requirements Engineer Plattform-Services | Luzern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Quendor Versicherungen AG | UX Designer B2B | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Ristra Finanztechnik AG | Scrum Master Prozesse | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Sanuvia Health AG | Projektleiter Digitalisierung Prozesse | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Sorvik Logistik AG | Scrum Master (80–100 %) | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Telvaro Kommunikation AG | Requirements Engineer (80–100 %) | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Trellin Immobilien AG | Business Analyst Kundenerlebnis | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Veltrima Gesundheitsdienste AG | UX Designer (80–100 %) | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Veltrima Gesundheitsdienste AG | Business Analyst Prozesse | St. Gallen | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Vendaro Retail AG | Projektleiter Digitalisierung Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-03 | Vendaro Retail AG | Scrum Master Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-04 | Amberlin Versicherung AG | UX Designer B2B | Lausanne | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-04 | Brivana Privatbank AG | Business Analyst Kundenerlebnis | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-04 | Cirrova Cloud AG | Scrum Master | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-04 | Cirrova Cloud AG | Requirements Engineer Kundenerlebnis | Schlieren | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-04 | Ristra Finanztechnik AG | Requirements Engineer | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-04 | Sanuvia Health AG | Scrum Master Prozesse | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-04 | Sanuvia Health AG | UX Designer Plattform-Services | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-04 | Sanuvia Health AG | Scrum Master | Winterthur | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-04 | Telvaro Kommunikation AG | Requirements Engineer B2B | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-04 | Telvaro Kommunikation AG | Business Analyst B2B | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-05 | Sanuvia Health AG | Projektleiter Digitalisierung Plattform-Services | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-05 | Vendaro Retail AG | UX Designer Plattform-Services | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-07 | Fendrix Analytics AG | Scrum Master Digital Channels | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-07 | Fendrix Analytics AG | Projektleiter Digitalisierung Plattform-Services | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-07 | Kalvit Software AG | Scrum Master Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-07 | Kombira Versand AG | Requirements Engineer Kundenerlebnis | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-07 | Kombira Versand AG | Scrum Master | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-07 | Lernovi Bildung AG | Projektleiter Digitalisierung B2B | Zürich | netzwerk-empfehlung | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-07 | Mirvel Medien AG | Projektleiter Digitalisierung (80–100 %) | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-07 | Quendor Versicherungen AG | Scrum Master Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-07 | Quendor Versicherungen AG | Requirements Engineer Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-07 | Telvaro Kommunikation AG | Scrum Master Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-07 | Trellin Immobilien AG | Requirements Engineer | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-07 | Trellin Immobilien AG | Projektleiter Digitalisierung Kundenerlebnis | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-07 | Trellin Immobilien AG | Projektleiter Digitalisierung | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-07 | Varella Energie AG | Scrum Master B2B | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-07 | Vendaro Retail AG | Requirements Engineer Daten | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Amberlin Versicherung AG | UX Designer Digital Channels | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Amberlin Versicherung AG | Business Analyst Digital Channels | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Brivana Privatbank AG | Scrum Master Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Cirrova Cloud AG | Requirements Engineer Digital Channels | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Lernovi Bildung AG | Projektleiter Digitalisierung Kundenerlebnis | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Lernovi Bildung AG | UX Designer Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Mirvel Medien AG | Business Analyst Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Pelvio Mobility AG | UX Designer B2B | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Pelvio Mobility AG | Projektleiter Digitalisierung Daten | Bern | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Quelvia Pharma AG | Requirements Engineer B2B | Basel | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Quendor Versicherungen AG | Projektleiter Digitalisierung Kundenerlebnis | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Quendor Versicherungen AG | Scrum Master (80–100 %) | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Ristra Finanztechnik AG | Projektleiter Digitalisierung Digital Channels | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Ristra Finanztechnik AG | Scrum Master Digital Channels | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Trellin Immobilien AG | Requirements Engineer Digital Channels | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Veltrima Gesundheitsdienste AG | Scrum Master Plattform-Services | St. Gallen | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Veltrima Gesundheitsdienste AG | Scrum Master Daten | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-08 | Vendaro Retail AG | UX Designer | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-09 | Fendrix Analytics AG | Scrum Master | Baden | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-09 | Fendrix Analytics AG | Business Analyst Plattform-Services | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-09 | Kalvit Software AG | Projektleiter Digitalisierung | Zürich | zielportal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-09 | Kantonale Verwaltung Altmark | UX Designer Daten | Aarau | behoerdenportal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-09 | Lernovi Bildung AG | Scrum Master Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-09 | Orvana Reisen AG | Projektleiter Digitalisierung Kundenerlebnis | Luzern | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-09 | Orvana Reisen AG | Business Analyst (80–100 %) | Luzern | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-09 | Pelvio Mobility AG | Business Analyst (80–100 %) | Bern | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-09 | Telvaro Kommunikation AG | Projektleiter Digitalisierung Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-09 | Veltrima Gesundheitsdienste AG | Requirements Engineer | St. Gallen | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-09 | Vendaro Retail AG | Requirements Engineer B2B | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-09 | Vendaro Retail AG | Scrum Master (80–100 %) | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-09 | Vendaro Retail AG | Business Analyst Digital Channels | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-10 | Amberlin Versicherung AG | Scrum Master B2B | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-10 | Fendrix Analytics AG | UX Designer B2B | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-10 | Fendrix Analytics AG | Business Analyst Daten | Baden | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-10 | Kombira Versand AG | UX Designer Plattform-Services | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-10 | Lernovi Bildung AG | Requirements Engineer (80–100 %) | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-10 | Lernovi Bildung AG | Projektleiter Digitalisierung (80–100 %) | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-10 | Mirvel Medien AG | Business Analyst Kundenerlebnis | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-10 | Quelvia Pharma AG | Requirements Engineer Digital Channels | Basel | netzwerk-empfehlung | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-10 | Quendor Versicherungen AG | UX Designer Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-10 | Ristra Finanztechnik AG | Projektleiter Digitalisierung B2B | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-10 | Sorvik Logistik AG | UX Designer | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-10 | Sorvik Logistik AG | Business Analyst Kundenerlebnis | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-10 | Trellin Immobilien AG | Business Analyst Prozesse | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-10 | Vendaro Retail AG | Business Analyst B2B | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-11 | Brivana Privatbank AG | UX Designer Prozesse | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-11 | Kombira Versand AG | UX Designer Daten | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-11 | Lernovi Bildung AG | Projektleiter Digitalisierung Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-11 | Sorvik Logistik AG | Scrum Master B2B | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-11 | Sorvik Logistik AG | Requirements Engineer Digital Channels | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-11 | Trellin Immobilien AG | Scrum Master Daten | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-11 | Varella Energie AG | Scrum Master Plattform-Services | Baden | netzwerk-empfehlung | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-11 | Veltrima Gesundheitsdienste AG | Business Analyst Digital Channels | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-12 | Kantonale Verwaltung Altmark | Scrum Master | Aarau | behoerdenportal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-12 | Lernovi Bildung AG | Requirements Engineer B2B | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-12 | Orvana Reisen AG | Projektleiter Digitalisierung (80–100 %) | Luzern | netzwerk-empfehlung | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-12 | Pelvio Mobility AG | Business Analyst Daten | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-12 | Varella Energie AG | UX Designer Kundenerlebnis | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-12 | Varella Energie AG | Projektleiter Digitalisierung | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-12 | Vendaro Retail AG | Business Analyst Kundenerlebnis | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-12 | Vendaro Retail AG | Requirements Engineer (80–100 %) | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-14 | Fendrix Analytics AG | Requirements Engineer Digital Channels | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-14 | Fendrix Analytics AG | Requirements Engineer B2B | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-14 | Kalvit Software AG | Requirements Engineer (80–100 %) | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-14 | Kalvit Software AG | Projektleiter Digitalisierung (80–100 %) | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-14 | Kombira Versand AG | UX Designer B2B | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-14 | Orvana Reisen AG | Business Analyst B2B | Luzern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-14 | Pelvio Mobility AG | UX Designer (80–100 %) | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-14 | Quelvia Pharma AG | UX Designer Plattform-Services | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-14 | Quendor Versicherungen AG | Projektleiter Digitalisierung Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-14 | Ristra Finanztechnik AG | Requirements Engineer Daten | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-14 | Sanuvia Health AG | Projektleiter Digitalisierung Kundenerlebnis | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-14 | Stadtverwaltung Nordtal | Requirements Engineer | Winterthur | behoerdenportal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-14 | Telvaro Kommunikation AG | UX Designer Kundenerlebnis | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-14 | Varella Energie AG | Business Analyst Daten | Baden | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-14 | Vendaro Retail AG | Business Analyst (80–100 %) | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-15 | Amberlin Versicherung AG | UX Designer Prozesse | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-15 | Brivana Privatbank AG | Scrum Master Kundenerlebnis | Zürich | zielportal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-15 | Brivana Privatbank AG | UX Designer Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-15 | Fendrix Analytics AG | Projektleiter Digitalisierung B2B | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-15 | Orvana Reisen AG | UX Designer Kundenerlebnis | Luzern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-15 | Quelvia Pharma AG | Requirements Engineer Prozesse | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-15 | Quendor Versicherungen AG | Requirements Engineer (80–100 %) | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-15 | Telvaro Kommunikation AG | Business Analyst Prozesse | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-15 | Trellin Immobilien AG | UX Designer Kundenerlebnis | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-15 | Trellin Immobilien AG | Scrum Master Digital Channels | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-15 | Varella Energie AG | Business Analyst (80–100 %) | Baden | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-16 | Cirrova Cloud AG | Projektleiter Digitalisierung B2B | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-16 | Kalvit Software AG | Projektleiter Digitalisierung Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-16 | Kombira Versand AG | UX Designer Prozesse | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-16 | Orvana Reisen AG | Requirements Engineer Kundenerlebnis | Luzern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-16 | Orvana Reisen AG | Projektleiter Digitalisierung Daten | Luzern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-16 | Pelvio Mobility AG | Scrum Master Daten | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-16 | Quelvia Pharma AG | Business Analyst Daten | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-16 | Ristra Finanztechnik AG | Scrum Master B2B | Zug | netzwerk-empfehlung | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-16 | Ristra Finanztechnik AG | Business Analyst Prozesse | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-16 | Sanuvia Health AG | Requirements Engineer | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-16 | Sorvik Logistik AG | Projektleiter Digitalisierung (80–100 %) | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-16 | Sorvik Logistik AG | Business Analyst Prozesse | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-16 | Veltrima Gesundheitsdienste AG | Projektleiter Digitalisierung (80–100 %) | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-16 | Veltrima Gesundheitsdienste AG | UX Designer Daten | St. Gallen | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-17 | Amberlin Versicherung AG | Requirements Engineer Kundenerlebnis | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-17 | Fendrix Analytics AG | Business Analyst Prozesse | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-17 | Lernovi Bildung AG | UX Designer B2B | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-17 | Quelvia Pharma AG | Scrum Master Kundenerlebnis | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-17 | Sanuvia Health AG | Projektleiter Digitalisierung B2B | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-17 | Sanuvia Health AG | Business Analyst Daten | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-17 | Telvaro Kommunikation AG | UX Designer Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-17 | Vendaro Retail AG | Requirements Engineer Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-18 | Amberlin Versicherung AG | Requirements Engineer (80–100 %) | Lausanne | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-18 | Fendrix Analytics AG | Scrum Master B2B | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-18 | Kombira Versand AG | Projektleiter Digitalisierung Kundenerlebnis | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-18 | Orvana Reisen AG | Requirements Engineer | Luzern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-18 | Pelvio Mobility AG | Scrum Master B2B | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-18 | Pelvio Mobility AG | Scrum Master Kundenerlebnis | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-18 | Sanuvia Health AG | Requirements Engineer Prozesse | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-18 | Telvaro Kommunikation AG | Business Analyst Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-18 | Trellin Immobilien AG | Projektleiter Digitalisierung (80–100 %) | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-18 | Vendaro Retail AG | Business Analyst Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-18 | Vendaro Retail AG | UX Designer Daten | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-19 | Kombira Versand AG | Scrum Master (80–100 %) | Dübendorf | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-19 | Pelvio Mobility AG | Scrum Master Plattform-Services | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-21 | Cirrova Cloud AG | Scrum Master (80–100 %) | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-21 | Kalvit Software AG | Business Analyst B2B | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-21 | Kombira Versand AG | Projektleiter Digitalisierung B2B | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-21 | Orvana Reisen AG | Projektleiter Digitalisierung Plattform-Services | Luzern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-21 | Pelvio Mobility AG | Projektleiter Digitalisierung Plattform-Services | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-21 | Sanuvia Health AG | Scrum Master Kundenerlebnis | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-21 | Telvaro Kommunikation AG | Requirements Engineer Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-21 | Telvaro Kommunikation AG | Scrum Master B2B | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-21 | Trellin Immobilien AG | Projektleiter Digitalisierung Daten | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-21 | Trellin Immobilien AG | Requirements Engineer Daten | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-21 | Trellin Immobilien AG | Projektleiter Digitalisierung B2B | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-21 | Veltrima Gesundheitsdienste AG | Requirements Engineer (80–100 %) | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Amberlin Versicherung AG | Requirements Engineer B2B | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Brivana Privatbank AG | Business Analyst Plattform-Services | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Kalvit Software AG | Requirements Engineer B2B | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Lernovi Bildung AG | Business Analyst Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Lernovi Bildung AG | Scrum Master Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Lernovi Bildung AG | Requirements Engineer Digital Channels | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Orvana Reisen AG | UX Designer Plattform-Services | Luzern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Orvana Reisen AG | Requirements Engineer Daten | Luzern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Quelvia Pharma AG | Scrum Master Plattform-Services | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Quelvia Pharma AG | Projektleiter Digitalisierung Daten | Basel | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Ristra Finanztechnik AG | Business Analyst Kundenerlebnis | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Ristra Finanztechnik AG | Projektleiter Digitalisierung Daten | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Sorvik Logistik AG | Business Analyst Digital Channels | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Sorvik Logistik AG | UX Designer Daten | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Telvaro Kommunikation AG | UX Designer (80–100 %) | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Telvaro Kommunikation AG | Projektleiter Digitalisierung B2B | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Trellin Immobilien AG | Requirements Engineer (80–100 %) | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Varella Energie AG | Projektleiter Digitalisierung Daten | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Veltrima Gesundheitsdienste AG | Business Analyst (80–100 %) | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-22 | Veltrima Gesundheitsdienste AG | UX Designer Plattform-Services | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-23 | Amberlin Versicherung AG | Scrum Master Kundenerlebnis | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-23 | Cirrova Cloud AG | Scrum Master Kundenerlebnis | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-23 | Fendrix Analytics AG | Business Analyst Digital Channels | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-23 | Fendrix Analytics AG | Scrum Master Kundenerlebnis | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-23 | Lernovi Bildung AG | Requirements Engineer Daten | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-23 | Mirvel Medien AG | Scrum Master (80–100 %) | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-23 | Quendor Versicherungen AG | Projektleiter Digitalisierung (80–100 %) | Zürich | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-23 | Quendor Versicherungen AG | Scrum Master B2B | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-23 | Quendor Versicherungen AG | Requirements Engineer B2B | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-23 | Quendor Versicherungen AG | Scrum Master Digital Channels | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-23 | Ristra Finanztechnik AG | Projektleiter Digitalisierung Plattform-Services | Zug | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-23 | Sanuvia Health AG | Business Analyst Plattform-Services | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-23 | Sorvik Logistik AG | Business Analyst Plattform-Services | Kloten | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-23 | Veltrima Gesundheitsdienste AG | Requirements Engineer B2B | St. Gallen | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-23 | Veltrima Gesundheitsdienste AG | Projektleiter Digitalisierung B2B | St. Gallen | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-23 | Vendaro Retail AG | Projektleiter Digitalisierung Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-24 | Amberlin Versicherung AG | Projektleiter Digitalisierung Kundenerlebnis | Lausanne | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-24 | Brivana Privatbank AG | UX Designer Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-24 | Cirrova Cloud AG | Scrum Master Plattform-Services | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-24 | Cirrova Cloud AG | UX Designer Plattform-Services | Schlieren | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-24 | Cirrova Cloud AG | Projektleiter Digitalisierung | Schlieren | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-24 | Fendrix Analytics AG | Business Analyst (80–100 %) | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-24 | Kombira Versand AG | Projektleiter Digitalisierung | Dübendorf | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-24 | Pelvio Mobility AG | Requirements Engineer Prozesse | Bern | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-24 | Quendor Versicherungen AG | Scrum Master Kundenerlebnis | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-24 | Ristra Finanztechnik AG | Requirements Engineer (80–100 %) | Zug | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-24 | Sanuvia Health AG | Business Analyst Prozesse | Winterthur | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-24 | Varella Energie AG | UX Designer Daten | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-24 | Varella Energie AG | Scrum Master Daten | Baden | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-24 | Vendaro Retail AG | Projektleiter Digitalisierung Plattform-Services | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-25 | Amberlin Versicherung AG | Scrum Master (80–100 %) | Lausanne | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-25 | Amberlin Versicherung AG | Projektleiter Digitalisierung Plattform-Services | Lausanne | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-25 | Brivana Privatbank AG | Projektleiter Digitalisierung Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-25 | Fendrix Analytics AG | Scrum Master Plattform-Services | Baden | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-25 | Kalvit Software AG | Projektleiter Digitalisierung Prozesse | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-25 | Mirvel Medien AG | Business Analyst Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-25 | Sorvik Logistik AG | Projektleiter Digitalisierung Daten | Kloten | netzwerk-suche | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-25 | Telvaro Kommunikation AG | Business Analyst Daten | Zürich | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |
| 2025-04-25 | Veltrima Gesundheitsdienste AG | Scrum Master B2B | St. Gallen | portal | Nicht-Rolle: kein Produktmandat (Listenebene) |

### Engineering / Entwicklung / Architektur (417)

| Datum | Firma | Rolle | Ort | Kanal | Grund |
|---|---|---|---|---|---|
| 2025-03-03 | Amberlin Versicherung AG | Data Engineer Digital Channels | Lausanne | portal | Engineering-/Entwicklerrolle |
| 2025-03-03 | Fendrix Analytics AG | Data Engineer Prozesse | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-03-03 | Kombira Versand AG | Data Engineer Digital Channels | Dübendorf | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-03 | Lernovi Bildung AG | Data Engineer B2B | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-03 | Lernovi Bildung AG | Software Engineer Backend | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-03 | Pelvio Mobility AG | Software Engineer Backend Kundenerlebnis | Bern | portal | Engineering-/Entwicklerrolle |
| 2025-03-03 | Quelvia Pharma AG | Solution Architect B2B | Basel | portal | Engineering-/Entwicklerrolle |
| 2025-03-03 | Varella Energie AG | Solution Architect Prozesse | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-03-04 | Amberlin Versicherung AG | Software Engineer Backend Prozesse | Lausanne | portal | Engineering-/Entwicklerrolle |
| 2025-03-04 | Brivana Privatbank AG | Software Engineer Backend B2B | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-04 | Cirrova Cloud AG | Data Engineer B2B | Schlieren | netzwerk-empfehlung | Engineering-/Entwicklerrolle |
| 2025-03-04 | Fendrix Analytics AG | Solution Architect B2B | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-03-04 | Hovald Bau AG | Data Engineer B2B | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-03-04 | Hovald Bau AG | Data Engineer | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-03-04 | Kalvit Software AG | Solution Architect Daten | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-04 | Kombira Versand AG | Software Engineer Backend (80–100 %) | Dübendorf | portal | Engineering-/Entwicklerrolle |
| 2025-03-04 | Lernovi Bildung AG | Data Engineer Prozesse | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-04 | Orvana Reisen AG | Software Engineer Backend Plattform-Services | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-03-04 | Quendor Versicherungen AG | Software Engineer Backend Digital Channels | Zürich | zielportal | Engineering-/Entwicklerrolle |
| 2025-03-04 | Trellin Immobilien AG | Solution Architect Plattform-Services | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-03-04 | Varella Energie AG | Software Engineer Backend | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-03-04 | Veltrima Gesundheitsdienste AG | Solution Architect | St. Gallen | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-04 | Veltrima Gesundheitsdienste AG | Solution Architect Kundenerlebnis | St. Gallen | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-04 | Veltrima Gesundheitsdienste AG | Solution Architect B2B | St. Gallen | netzwerk-empfehlung | Engineering-/Entwicklerrolle |
| 2025-03-04 | Vendaro Retail AG | Solution Architect | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-05 | Cirrova Cloud AG | Data Engineer Daten | Schlieren | portal | Engineering-/Entwicklerrolle |
| 2025-03-05 | Lernovi Bildung AG | Solution Architect | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-05 | Mirvel Medien AG | Data Engineer Prozesse | Zürich | netzwerk-empfehlung | Engineering-/Entwicklerrolle |
| 2025-03-05 | Orvana Reisen AG | Software Engineer Backend | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-03-05 | Orvana Reisen AG | Software Engineer Backend Digital Channels | Luzern | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-05 | Quelvia Pharma AG | Solution Architect | Basel | portal | Engineering-/Entwicklerrolle |
| 2025-03-05 | Ristra Finanztechnik AG | Solution Architect Daten | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-03-05 | Trellin Immobilien AG | Solution Architect (80–100 %) | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-03-05 | Veltrima Gesundheitsdienste AG | Solution Architect Digital Channels | St. Gallen | portal | Engineering-/Entwicklerrolle |
| 2025-03-05 | Veltrima Gesundheitsdienste AG | Software Engineer Backend | St. Gallen | portal | Engineering-/Entwicklerrolle |
| 2025-03-05 | Vendaro Retail AG | Data Engineer Prozesse | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-06 | Brivana Privatbank AG | Solution Architect | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-06 | Mastrova Industrie AG | Solution Architect | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-03-06 | Orvana Reisen AG | Solution Architect | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-03-06 | Orvana Reisen AG | Software Engineer Backend B2B | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-03-06 | Quendor Versicherungen AG | Software Engineer Backend | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-06 | Trellin Immobilien AG | Software Engineer Backend Prozesse | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-03-07 | Amberlin Versicherung AG | Software Engineer Backend Daten | Lausanne | portal | Engineering-/Entwicklerrolle |
| 2025-03-07 | Brivana Privatbank AG | Data Engineer B2B | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-07 | Cirrova Cloud AG | Solution Architect Prozesse | Schlieren | portal | Engineering-/Entwicklerrolle |
| 2025-03-07 | Kombira Versand AG | Data Engineer | Dübendorf | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-07 | Mastrova Industrie AG | Software Engineer Backend | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-03-07 | Mastrova Industrie AG | Data Engineer Daten | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-03-07 | Mirvel Medien AG | Software Engineer Backend Plattform-Services | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-07 | Quendor Versicherungen AG | Software Engineer Backend Kundenerlebnis | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-07 | Ristra Finanztechnik AG | Data Engineer Kundenerlebnis | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-03-07 | Telvaro Kommunikation AG | Solution Architect | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-07 | Telvaro Kommunikation AG | Solution Architect Digital Channels | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-10 | Amberlin Versicherung AG | Solution Architect (80–100 %) | Lausanne | portal | Engineering-/Entwicklerrolle |
| 2025-03-10 | Cirrova Cloud AG | Solution Architect Daten | Schlieren | portal | Engineering-/Entwicklerrolle |
| 2025-03-10 | Kalvit Software AG | Data Engineer Daten | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-10 | Kantonale Verwaltung Altmark | Solution Architect Daten | Aarau | behoerdenportal | Engineering-/Entwicklerrolle |
| 2025-03-10 | Lernovi Bildung AG | Data Engineer Daten | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-10 | Orvana Reisen AG | Data Engineer Digital Channels | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-03-10 | Trellin Immobilien AG | Software Engineer Backend | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-03-10 | Varella Energie AG | Software Engineer Backend Kundenerlebnis | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-03-11 | Brivana Privatbank AG | Data Engineer | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-11 | Kalvit Software AG | Software Engineer Backend (80–100 %) | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-11 | Lernovi Bildung AG | Software Engineer Backend Digital Channels | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-11 | Quelvia Pharma AG | Software Engineer Backend Prozesse | Basel | portal | Engineering-/Entwicklerrolle |
| 2025-03-11 | Ristra Finanztechnik AG | Data Engineer | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-03-11 | Sorvik Logistik AG | Solution Architect (80–100 %) | Kloten | portal | Engineering-/Entwicklerrolle |
| 2025-03-11 | Vendaro Retail AG | Software Engineer Backend Digital Channels | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-12 | Amberlin Versicherung AG | Solution Architect | Lausanne | portal | Engineering-/Entwicklerrolle |
| 2025-03-12 | Fendrix Analytics AG | Data Engineer | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-03-12 | Hovald Bau AG | Data Engineer Plattform-Services | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-03-12 | Kalvit Software AG | Data Engineer (80–100 %) | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-12 | Mastrova Industrie AG | Solution Architect Prozesse | Aarau | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-13 | Amberlin Versicherung AG | Data Engineer (80–100 %) | Lausanne | portal | Engineering-/Entwicklerrolle |
| 2025-03-13 | Amberlin Versicherung AG | Solution Architect Plattform-Services | Lausanne | portal | Engineering-/Entwicklerrolle |
| 2025-03-13 | Cirrova Cloud AG | Software Engineer Backend Prozesse | Schlieren | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-13 | Hovald Bau AG | Solution Architect B2B | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-03-13 | Kalvit Software AG | Solution Architect | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-13 | Mastrova Industrie AG | Solution Architect Digital Channels | Aarau | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-13 | Mirvel Medien AG | Data Engineer Plattform-Services | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-13 | Sanuvia Health AG | Solution Architect Daten | Winterthur | portal | Engineering-/Entwicklerrolle |
| 2025-03-13 | Telvaro Kommunikation AG | Software Engineer Backend | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-13 | Telvaro Kommunikation AG | Software Engineer Backend (80–100 %) | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-13 | Veltrima Gesundheitsdienste AG | Solution Architect (80–100 %) | St. Gallen | portal | Engineering-/Entwicklerrolle |
| 2025-03-14 | Hovald Bau AG | Data Engineer Digital Channels | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-03-14 | Orvana Reisen AG | Software Engineer Backend Kundenerlebnis | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-03-14 | Ristra Finanztechnik AG | Solution Architect | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-03-14 | Sorvik Logistik AG | Solution Architect | Kloten | portal | Engineering-/Entwicklerrolle |
| 2025-03-14 | Varella Energie AG | Data Engineer Digital Channels | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-03-14 | Vendaro Retail AG | Solution Architect Digital Channels | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-17 | Amberlin Versicherung AG | Solution Architect Daten | Lausanne | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-17 | Kalvit Software AG | Data Engineer Plattform-Services | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-17 | Lernovi Bildung AG | Solution Architect B2B | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-17 | Lernovi Bildung AG | Software Engineer Backend B2B | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-17 | Mirvel Medien AG | Data Engineer | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-17 | Pelvio Mobility AG | Data Engineer Daten | Bern | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-17 | Sorvik Logistik AG | Software Engineer Backend Kundenerlebnis | Kloten | portal | Engineering-/Entwicklerrolle |
| 2025-03-17 | Trellin Immobilien AG | Solution Architect Prozesse | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-03-17 | Trellin Immobilien AG | Data Engineer Plattform-Services | Zug | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-17 | Varella Energie AG | Software Engineer Backend Prozesse | Baden | zielportal | Engineering-/Entwicklerrolle |
| 2025-03-17 | Veltrima Gesundheitsdienste AG | Software Engineer Backend (80–100 %) | St. Gallen | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-18 | Amberlin Versicherung AG | Software Engineer Backend | Lausanne | portal | Engineering-/Entwicklerrolle |
| 2025-03-18 | Brivana Privatbank AG | Software Engineer Backend Plattform-Services | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-18 | Cirrova Cloud AG | Solution Architect | Schlieren | portal | Engineering-/Entwicklerrolle |
| 2025-03-18 | Cirrova Cloud AG | Software Engineer Backend Daten | Schlieren | portal | Engineering-/Entwicklerrolle |
| 2025-03-18 | Cirrova Cloud AG | Data Engineer | Schlieren | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-18 | Fendrix Analytics AG | Solution Architect Plattform-Services | Baden | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-18 | Kalvit Software AG | Solution Architect Prozesse | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-18 | Lernovi Bildung AG | Data Engineer | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-18 | Mirvel Medien AG | Solution Architect Kundenerlebnis | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-18 | Pelvio Mobility AG | Data Engineer (80–100 %) | Bern | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-18 | Pelvio Mobility AG | Software Engineer Backend Daten | Bern | portal | Engineering-/Entwicklerrolle |
| 2025-03-18 | Quendor Versicherungen AG | Solution Architect Prozesse | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-18 | Quendor Versicherungen AG | Data Engineer | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-18 | Sanuvia Health AG | Solution Architect | Winterthur | portal | Engineering-/Entwicklerrolle |
| 2025-03-18 | Sorvik Logistik AG | Software Engineer Backend | Kloten | portal | Engineering-/Entwicklerrolle |
| 2025-03-18 | Stadtverwaltung Nordtal | Software Engineer Backend Digital Channels | Winterthur | behoerdenportal | Engineering-/Entwicklerrolle |
| 2025-03-18 | Stadtverwaltung Nordtal | Solution Architect Digital Channels | Winterthur | behoerdenportal | Engineering-/Entwicklerrolle |
| 2025-03-19 | Cirrova Cloud AG | Software Engineer Backend Digital Channels | Schlieren | portal | Engineering-/Entwicklerrolle |
| 2025-03-19 | Fendrix Analytics AG | Solution Architect Prozesse | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-03-19 | Pelvio Mobility AG | Software Engineer Backend Plattform-Services | Bern | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-19 | Ristra Finanztechnik AG | Software Engineer Backend Plattform-Services | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-03-19 | Sanuvia Health AG | Software Engineer Backend Prozesse | Winterthur | portal | Engineering-/Entwicklerrolle |
| 2025-03-19 | Sorvik Logistik AG | Data Engineer Daten | Kloten | portal | Engineering-/Entwicklerrolle |
| 2025-03-19 | Vendaro Retail AG | Software Engineer Backend Plattform-Services | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-20 | Amberlin Versicherung AG | Software Engineer Backend Digital Channels | Lausanne | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-20 | Fendrix Analytics AG | Data Engineer Daten | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-03-20 | Kalvit Software AG | Software Engineer Backend | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-20 | Kalvit Software AG | Software Engineer Backend Digital Channels | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-20 | Kombira Versand AG | Solution Architect B2B | Dübendorf | portal | Engineering-/Entwicklerrolle |
| 2025-03-20 | Mastrova Industrie AG | Data Engineer (80–100 %) | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-03-20 | Sanuvia Health AG | Solution Architect Plattform-Services | Winterthur | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-20 | Tuskora Lebensmittel AG | Solution Architect Kundenerlebnis | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-03-21 | Kombira Versand AG | Software Engineer Backend | Dübendorf | portal | Engineering-/Entwicklerrolle |
| 2025-03-21 | Lernovi Bildung AG | Data Engineer Plattform-Services | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-21 | Mastrova Industrie AG | Data Engineer | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-03-21 | Mirvel Medien AG | Solution Architect Digital Channels | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-21 | Mirvel Medien AG | Software Engineer Backend | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-21 | Telvaro Kommunikation AG | Software Engineer Backend Kundenerlebnis | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-21 | Trellin Immobilien AG | Data Engineer Kundenerlebnis | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-03-21 | Varella Energie AG | Software Engineer Backend Digital Channels | Baden | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-21 | Vendaro Retail AG | Data Engineer | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-22 | Brivana Privatbank AG | Solution Architect Plattform-Services | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-24 | Brivana Privatbank AG | Data Engineer Daten | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-24 | Cirrova Cloud AG | Software Engineer Backend Kundenerlebnis | Schlieren | portal | Engineering-/Entwicklerrolle |
| 2025-03-24 | Fendrix Analytics AG | Solution Architect (80–100 %) | Baden | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-24 | Hovald Bau AG | Software Engineer Backend (80–100 %) | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-03-24 | Mastrova Industrie AG | Data Engineer Plattform-Services | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-03-24 | Orvana Reisen AG | Data Engineer Kundenerlebnis | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-03-24 | Quelvia Pharma AG | Data Engineer | Basel | portal | Engineering-/Entwicklerrolle |
| 2025-03-24 | Ristra Finanztechnik AG | Solution Architect Kundenerlebnis | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-03-24 | Sanuvia Health AG | Data Engineer Prozesse | Winterthur | netzwerk-empfehlung | Engineering-/Entwicklerrolle |
| 2025-03-24 | Tuskora Lebensmittel AG | Solution Architect Prozesse | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-03-24 | Tuskora Lebensmittel AG | Software Engineer Backend | Luzern | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-24 | Vendaro Retail AG | Solution Architect Prozesse | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-25 | Amberlin Versicherung AG | Software Engineer Backend Plattform-Services | Lausanne | portal | Engineering-/Entwicklerrolle |
| 2025-03-25 | Fendrix Analytics AG | Software Engineer Backend | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-03-25 | Kalvit Software AG | Software Engineer Backend Kundenerlebnis | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-25 | Kalvit Software AG | Solution Architect Kundenerlebnis | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-25 | Kombira Versand AG | Data Engineer Daten | Dübendorf | portal | Engineering-/Entwicklerrolle |
| 2025-03-25 | Kombira Versand AG | Software Engineer Backend Daten | Dübendorf | portal | Engineering-/Entwicklerrolle |
| 2025-03-25 | Mirvel Medien AG | Data Engineer Daten | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-25 | Quelvia Pharma AG | Software Engineer Backend B2B | Basel | portal | Engineering-/Entwicklerrolle |
| 2025-03-25 | Quelvia Pharma AG | Data Engineer Plattform-Services | Basel | portal | Engineering-/Entwicklerrolle |
| 2025-03-25 | Quelvia Pharma AG | Data Engineer (80–100 %) | Basel | portal | Engineering-/Entwicklerrolle |
| 2025-03-25 | Sanuvia Health AG | Software Engineer Backend Digital Channels | Winterthur | portal | Engineering-/Entwicklerrolle |
| 2025-03-25 | Stadtverwaltung Nordtal | Solution Architect | Winterthur | behoerdenportal | Engineering-/Entwicklerrolle |
| 2025-03-25 | Varella Energie AG | Solution Architect Kundenerlebnis | Baden | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-25 | Veltrima Gesundheitsdienste AG | Data Engineer Kundenerlebnis | St. Gallen | portal | Engineering-/Entwicklerrolle |
| 2025-03-25 | Veltrima Gesundheitsdienste AG | Software Engineer Backend Plattform-Services | St. Gallen | portal | Engineering-/Entwicklerrolle |
| 2025-03-25 | Veltrima Gesundheitsdienste AG | Data Engineer Digital Channels | St. Gallen | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-26 | Brivana Privatbank AG | Software Engineer Backend (80–100 %) | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-26 | Hovald Bau AG | Data Engineer Daten | Aarau | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-26 | Kalvit Software AG | Software Engineer Backend Daten | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-26 | Kalvit Software AG | Solution Architect Digital Channels | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-26 | Kombira Versand AG | Solution Architect Digital Channels | Dübendorf | portal | Engineering-/Entwicklerrolle |
| 2025-03-26 | Kombira Versand AG | Data Engineer B2B | Dübendorf | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-26 | Orvana Reisen AG | Solution Architect Digital Channels | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-03-26 | Orvana Reisen AG | Solution Architect B2B | Luzern | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-26 | Pelvio Mobility AG | Software Engineer Backend | Bern | portal | Engineering-/Entwicklerrolle |
| 2025-03-26 | Telvaro Kommunikation AG | Data Engineer Prozesse | Zürich | netzwerk-empfehlung | Engineering-/Entwicklerrolle |
| 2025-03-26 | Telvaro Kommunikation AG | Data Engineer | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-26 | Trellin Immobilien AG | Solution Architect | Zug | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-26 | Tuskora Lebensmittel AG | Data Engineer Daten | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-03-27 | Brivana Privatbank AG | Software Engineer Backend | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-27 | Cirrova Cloud AG | Data Engineer Kundenerlebnis | Schlieren | portal | Engineering-/Entwicklerrolle |
| 2025-03-27 | Cirrova Cloud AG | Software Engineer Backend B2B | Schlieren | portal | Engineering-/Entwicklerrolle |
| 2025-03-27 | Cirrova Cloud AG | Software Engineer Backend | Schlieren | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-27 | Hovald Bau AG | Solution Architect Daten | Aarau | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-27 | Kombira Versand AG | Solution Architect Daten | Dübendorf | portal | Engineering-/Entwicklerrolle |
| 2025-03-27 | Quelvia Pharma AG | Software Engineer Backend | Basel | portal | Engineering-/Entwicklerrolle |
| 2025-03-27 | Sorvik Logistik AG | Data Engineer Kundenerlebnis | Kloten | portal | Engineering-/Entwicklerrolle |
| 2025-03-27 | Trellin Immobilien AG | Software Engineer Backend Plattform-Services | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-03-27 | Tuskora Lebensmittel AG | Solution Architect Daten | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-03-27 | Varella Energie AG | Data Engineer | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-03-27 | Vendaro Retail AG | Software Engineer Backend (80–100 %) | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-28 | Amberlin Versicherung AG | Data Engineer | Lausanne | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-28 | Cirrova Cloud AG | Software Engineer Backend Plattform-Services | Schlieren | portal | Engineering-/Entwicklerrolle |
| 2025-03-28 | Hovald Bau AG | Solution Architect Prozesse | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-03-28 | Kombira Versand AG | Solution Architect Kundenerlebnis | Dübendorf | portal | Engineering-/Entwicklerrolle |
| 2025-03-28 | Lernovi Bildung AG | Software Engineer Backend Plattform-Services | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-28 | Pelvio Mobility AG | Software Engineer Backend B2B | Bern | portal | Engineering-/Entwicklerrolle |
| 2025-03-28 | Sanuvia Health AG | Solution Architect (80–100 %) | Winterthur | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-28 | Telvaro Kommunikation AG | Solution Architect B2B | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-28 | Trellin Immobilien AG | Software Engineer Backend (80–100 %) | Zug | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-28 | Tuskora Lebensmittel AG | Data Engineer | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-03-28 | Tuskora Lebensmittel AG | Software Engineer Backend Digital Channels | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-03-29 | Fendrix Analytics AG | Solution Architect Daten | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-03-31 | Hovald Bau AG | Software Engineer Backend Plattform-Services | Aarau | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-31 | Hovald Bau AG | Software Engineer Backend Kundenerlebnis | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-03-31 | Kantonale Verwaltung Altmark | Software Engineer Backend Digital Channels | Aarau | behoerdenportal | Engineering-/Entwicklerrolle |
| 2025-03-31 | Kombira Versand AG | Data Engineer Prozesse | Dübendorf | portal | Engineering-/Entwicklerrolle |
| 2025-03-31 | Lernovi Bildung AG | Data Engineer Digital Channels | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-31 | Lernovi Bildung AG | Software Engineer Backend Prozesse | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-31 | Orvana Reisen AG | Solution Architect Daten | Luzern | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-31 | Orvana Reisen AG | Solution Architect Kundenerlebnis | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-03-31 | Pelvio Mobility AG | Solution Architect Plattform-Services | Bern | portal | Engineering-/Entwicklerrolle |
| 2025-03-31 | Quelvia Pharma AG | Software Engineer Backend Digital Channels | Basel | portal | Engineering-/Entwicklerrolle |
| 2025-03-31 | Sanuvia Health AG | Software Engineer Backend B2B | Winterthur | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-03-31 | Veltrima Gesundheitsdienste AG | Software Engineer Backend Digital Channels | St. Gallen | portal | Engineering-/Entwicklerrolle |
| 2025-03-31 | Vendaro Retail AG | Solution Architect Plattform-Services | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-03-31 | Vendaro Retail AG | Software Engineer Backend Prozesse | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-01 | Amberlin Versicherung AG | Software Engineer Backend Kundenerlebnis | Lausanne | portal | Engineering-/Entwicklerrolle |
| 2025-04-01 | Amberlin Versicherung AG | Software Engineer Backend B2B | Lausanne | portal | Engineering-/Entwicklerrolle |
| 2025-04-01 | Fendrix Analytics AG | Data Engineer Kundenerlebnis | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-04-01 | Kalvit Software AG | Data Engineer | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-01 | Kalvit Software AG | Solution Architect (80–100 %) | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-01 | Kantonale Verwaltung Altmark | Software Engineer Backend Plattform-Services | Aarau | behoerdenportal | Engineering-/Entwicklerrolle |
| 2025-04-01 | Mirvel Medien AG | Solution Architect Prozesse | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-01 | Pelvio Mobility AG | Data Engineer | Bern | portal | Engineering-/Entwicklerrolle |
| 2025-04-01 | Quelvia Pharma AG | Solution Architect Plattform-Services | Basel | portal | Engineering-/Entwicklerrolle |
| 2025-04-01 | Sanuvia Health AG | Software Engineer Backend | Winterthur | portal | Engineering-/Entwicklerrolle |
| 2025-04-01 | Trellin Immobilien AG | Data Engineer Daten | Zug | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-01 | Tuskora Lebensmittel AG | Data Engineer Plattform-Services | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-04-01 | Varella Energie AG | Solution Architect Daten | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-04-01 | Varella Energie AG | Solution Architect | Baden | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-01 | Varella Energie AG | Data Engineer Plattform-Services | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-04-01 | Veltrima Gesundheitsdienste AG | Data Engineer Prozesse | St. Gallen | portal | Engineering-/Entwicklerrolle |
| 2025-04-01 | Vendaro Retail AG | Data Engineer Daten | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-02 | Fendrix Analytics AG | Solution Architect Digital Channels | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-04-02 | Mirvel Medien AG | Solution Architect (80–100 %) | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-02 | Pelvio Mobility AG | Data Engineer Prozesse | Bern | portal | Engineering-/Entwicklerrolle |
| 2025-04-02 | Quelvia Pharma AG | Software Engineer Backend Daten | Basel | portal | Engineering-/Entwicklerrolle |
| 2025-04-02 | Quendor Versicherungen AG | Solution Architect Kundenerlebnis | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-02 | Sorvik Logistik AG | Solution Architect Digital Channels | Kloten | portal | Engineering-/Entwicklerrolle |
| 2025-04-02 | Trellin Immobilien AG | Solution Architect Digital Channels | Zug | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-02 | Varella Energie AG | Data Engineer (80–100 %) | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-04-02 | Vendaro Retail AG | Data Engineer Digital Channels | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-03 | Brivana Privatbank AG | Data Engineer Prozesse | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-03 | Fendrix Analytics AG | Software Engineer Backend Digital Channels | Baden | netzwerk-empfehlung | Engineering-/Entwicklerrolle |
| 2025-04-03 | Pelvio Mobility AG | Software Engineer Backend (80–100 %) | Bern | portal | Engineering-/Entwicklerrolle |
| 2025-04-03 | Quendor Versicherungen AG | Solution Architect Plattform-Services | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-03 | Quendor Versicherungen AG | Software Engineer Backend B2B | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-03 | Sorvik Logistik AG | Software Engineer Backend Prozesse | Kloten | portal | Engineering-/Entwicklerrolle |
| 2025-04-03 | Sorvik Logistik AG | Software Engineer Backend Digital Channels | Kloten | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-04 | Mastrova Industrie AG | Software Engineer Backend Digital Channels | Aarau | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-04 | Quendor Versicherungen AG | Data Engineer Kundenerlebnis | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-04 | Quendor Versicherungen AG | Solution Architect | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-04 | Sanuvia Health AG | Software Engineer Backend Kundenerlebnis | Winterthur | portal | Engineering-/Entwicklerrolle |
| 2025-04-04 | Sanuvia Health AG | Data Engineer Digital Channels | Winterthur | portal | Engineering-/Entwicklerrolle |
| 2025-04-04 | Sorvik Logistik AG | Solution Architect Daten | Kloten | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-04 | Sorvik Logistik AG | Data Engineer | Kloten | portal | Engineering-/Entwicklerrolle |
| 2025-04-04 | Telvaro Kommunikation AG | Data Engineer Daten | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-04 | Vendaro Retail AG | Software Engineer Backend | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-05 | Sorvik Logistik AG | Data Engineer Digital Channels | Kloten | portal | Engineering-/Entwicklerrolle |
| 2025-04-07 | Brivana Privatbank AG | Data Engineer Plattform-Services | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-07 | Hovald Bau AG | Solution Architect | Aarau | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-07 | Hovald Bau AG | Data Engineer Kundenerlebnis | Aarau | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-07 | Kombira Versand AG | Software Engineer Backend Plattform-Services | Dübendorf | portal | Engineering-/Entwicklerrolle |
| 2025-04-07 | Quendor Versicherungen AG | Data Engineer Prozesse | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-07 | Quendor Versicherungen AG | Data Engineer B2B | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-07 | Sanuvia Health AG | Data Engineer | Winterthur | portal | Engineering-/Entwicklerrolle |
| 2025-04-07 | Telvaro Kommunikation AG | Software Engineer Backend B2B | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-07 | Trellin Immobilien AG | Solution Architect Kundenerlebnis | Zug | netzwerk-empfehlung | Engineering-/Entwicklerrolle |
| 2025-04-07 | Varella Energie AG | Software Engineer Backend B2B | Baden | zielportal | Engineering-/Entwicklerrolle |
| 2025-04-08 | Amberlin Versicherung AG | Solution Architect B2B | Lausanne | portal | Engineering-/Entwicklerrolle |
| 2025-04-08 | Brivana Privatbank AG | Data Engineer (80–100 %) | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-08 | Brivana Privatbank AG | Solution Architect B2B | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-08 | Fendrix Analytics AG | Software Engineer Backend B2B | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-04-08 | Hovald Bau AG | Software Engineer Backend B2B | Aarau | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-08 | Mastrova Industrie AG | Software Engineer Backend Prozesse | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-04-08 | Mastrova Industrie AG | Software Engineer Backend Plattform-Services | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-04-08 | Pelvio Mobility AG | Solution Architect Kundenerlebnis | Bern | portal | Engineering-/Entwicklerrolle |
| 2025-04-08 | Ristra Finanztechnik AG | Software Engineer Backend Digital Channels | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-04-08 | Trellin Immobilien AG | Data Engineer | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-04-08 | Trellin Immobilien AG | Data Engineer B2B | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-04-08 | Tuskora Lebensmittel AG | Software Engineer Backend Prozesse | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-04-09 | Amberlin Versicherung AG | Data Engineer B2B | Lausanne | portal | Engineering-/Entwicklerrolle |
| 2025-04-09 | Brivana Privatbank AG | Software Engineer Backend Daten | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-09 | Fendrix Analytics AG | Software Engineer Backend Prozesse | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-04-09 | Mirvel Medien AG | Software Engineer Backend Daten | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-09 | Quelvia Pharma AG | Software Engineer Backend (80–100 %) | Basel | portal | Engineering-/Entwicklerrolle |
| 2025-04-09 | Ristra Finanztechnik AG | Solution Architect Prozesse | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-04-09 | Ristra Finanztechnik AG | Data Engineer B2B | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-04-09 | Stadtverwaltung Nordtal | Software Engineer Backend | Winterthur | behoerdenportal | Engineering-/Entwicklerrolle |
| 2025-04-09 | Trellin Immobilien AG | Data Engineer Prozesse | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-04-09 | Tuskora Lebensmittel AG | Solution Architect Plattform-Services | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-04-09 | Varella Energie AG | Data Engineer Kundenerlebnis | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-04-09 | Veltrima Gesundheitsdienste AG | Software Engineer Backend Daten | St. Gallen | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-09 | Vendaro Retail AG | Data Engineer (80–100 %) | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-10 | Cirrova Cloud AG | Solution Architect Kundenerlebnis | Schlieren | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-10 | Fendrix Analytics AG | Data Engineer B2B | Baden | netzwerk-empfehlung | Engineering-/Entwicklerrolle |
| 2025-04-10 | Kalvit Software AG | Software Engineer Backend Prozesse | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-10 | Kantonale Verwaltung Altmark | Solution Architect Plattform-Services | Aarau | behoerdenportal | Engineering-/Entwicklerrolle |
| 2025-04-10 | Kombira Versand AG | Solution Architect Plattform-Services | Dübendorf | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-10 | Sorvik Logistik AG | Solution Architect Kundenerlebnis | Kloten | portal | Engineering-/Entwicklerrolle |
| 2025-04-10 | Trellin Immobilien AG | Software Engineer Backend Daten | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-04-10 | Veltrima Gesundheitsdienste AG | Data Engineer Plattform-Services | St. Gallen | portal | Engineering-/Entwicklerrolle |
| 2025-04-10 | Veltrima Gesundheitsdienste AG | Data Engineer B2B | St. Gallen | portal | Engineering-/Entwicklerrolle |
| 2025-04-10 | Veltrima Gesundheitsdienste AG | Software Engineer Backend Prozesse | St. Gallen | portal | Engineering-/Entwicklerrolle |
| 2025-04-11 | Cirrova Cloud AG | Data Engineer Prozesse | Schlieren | portal | Engineering-/Entwicklerrolle |
| 2025-04-11 | Fendrix Analytics AG | Data Engineer Plattform-Services | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-04-11 | Kalvit Software AG | Software Engineer Backend Plattform-Services | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-11 | Kalvit Software AG | Solution Architect B2B | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-11 | Lernovi Bildung AG | Data Engineer (80–100 %) | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-11 | Lernovi Bildung AG | Solution Architect (80–100 %) | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-11 | Pelvio Mobility AG | Solution Architect Digital Channels | Bern | portal | Engineering-/Entwicklerrolle |
| 2025-04-11 | Ristra Finanztechnik AG | Data Engineer (80–100 %) | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-04-11 | Sorvik Logistik AG | Solution Architect B2B | Kloten | portal | Engineering-/Entwicklerrolle |
| 2025-04-11 | Telvaro Kommunikation AG | Software Engineer Backend Digital Channels | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-11 | Telvaro Kommunikation AG | Data Engineer Digital Channels | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-11 | Veltrima Gesundheitsdienste AG | Data Engineer Daten | St. Gallen | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-12 | Trellin Immobilien AG | Software Engineer Backend B2B | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-04-12 | Tuskora Lebensmittel AG | Data Engineer Kundenerlebnis | Luzern | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-14 | Amberlin Versicherung AG | Solution Architect Kundenerlebnis | Lausanne | portal | Engineering-/Entwicklerrolle |
| 2025-04-14 | Cirrova Cloud AG | Data Engineer (80–100 %) | Schlieren | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-14 | Fendrix Analytics AG | Software Engineer Backend Plattform-Services | Baden | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-14 | Orvana Reisen AG | Data Engineer Plattform-Services | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-04-14 | Quelvia Pharma AG | Software Engineer Backend Plattform-Services | Basel | portal | Engineering-/Entwicklerrolle |
| 2025-04-14 | Ristra Finanztechnik AG | Software Engineer Backend Daten | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-04-14 | Sanuvia Health AG | Software Engineer Backend (80–100 %) | Winterthur | portal | Engineering-/Entwicklerrolle |
| 2025-04-14 | Sanuvia Health AG | Data Engineer Daten | Winterthur | portal | Engineering-/Entwicklerrolle |
| 2025-04-14 | Sorvik Logistik AG | Data Engineer (80–100 %) | Kloten | portal | Engineering-/Entwicklerrolle |
| 2025-04-14 | Trellin Immobilien AG | Data Engineer (80–100 %) | Zug | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-14 | Varella Energie AG | Data Engineer B2B | Baden | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-14 | Veltrima Gesundheitsdienste AG | Data Engineer | St. Gallen | portal | Engineering-/Entwicklerrolle |
| 2025-04-14 | Vendaro Retail AG | Data Engineer B2B | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-14 | Vendaro Retail AG | Software Engineer Backend Daten | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-14 | Vendaro Retail AG | Solution Architect (80–100 %) | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-14 | Vendaro Retail AG | Data Engineer Kundenerlebnis | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-15 | Hovald Bau AG | Solution Architect Digital Channels | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-04-15 | Kalvit Software AG | Software Engineer Backend B2B | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-15 | Kantonale Verwaltung Altmark | Software Engineer Backend Prozesse | Aarau | behoerdenportal | Engineering-/Entwicklerrolle |
| 2025-04-15 | Mirvel Medien AG | Solution Architect | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-15 | Quelvia Pharma AG | Data Engineer B2B | Basel | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-15 | Quendor Versicherungen AG | Data Engineer (80–100 %) | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-15 | Tuskora Lebensmittel AG | Software Engineer Backend Kundenerlebnis | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-04-15 | Tuskora Lebensmittel AG | Software Engineer Backend Daten | Luzern | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-16 | Hovald Bau AG | Software Engineer Backend | Aarau | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-16 | Kombira Versand AG | Solution Architect | Dübendorf | portal | Engineering-/Entwicklerrolle |
| 2025-04-16 | Mastrova Industrie AG | Software Engineer Backend B2B | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-04-16 | Orvana Reisen AG | Data Engineer Prozesse | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-04-16 | Telvaro Kommunikation AG | Solution Architect (80–100 %) | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-16 | Varella Energie AG | Solution Architect Digital Channels | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-04-17 | Cirrova Cloud AG | Solution Architect Digital Channels | Schlieren | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-17 | Cirrova Cloud AG | Data Engineer Plattform-Services | Schlieren | portal | Engineering-/Entwicklerrolle |
| 2025-04-17 | Fendrix Analytics AG | Data Engineer Digital Channels | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-04-17 | Kombira Versand AG | Solution Architect Prozesse | Dübendorf | portal | Engineering-/Entwicklerrolle |
| 2025-04-17 | Mirvel Medien AG | Data Engineer (80–100 %) | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-17 | Telvaro Kommunikation AG | Solution Architect Kundenerlebnis | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-17 | Tuskora Lebensmittel AG | Software Engineer Backend (80–100 %) | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-04-18 | Amberlin Versicherung AG | Solution Architect Prozesse | Lausanne | portal | Engineering-/Entwicklerrolle |
| 2025-04-18 | Brivana Privatbank AG | Solution Architect Prozesse | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-18 | Fendrix Analytics AG | Solution Architect | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-04-18 | Lernovi Bildung AG | Solution Architect Kundenerlebnis | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-18 | Mastrova Industrie AG | Solution Architect Daten | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-04-18 | Mastrova Industrie AG | Software Engineer Backend (80–100 %) | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-04-18 | Pelvio Mobility AG | Solution Architect | Bern | portal | Engineering-/Entwicklerrolle |
| 2025-04-18 | Quelvia Pharma AG | Solution Architect Digital Channels | Basel | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-18 | Quelvia Pharma AG | Data Engineer Daten | Basel | portal | Engineering-/Entwicklerrolle |
| 2025-04-18 | Quendor Versicherungen AG | Data Engineer Digital Channels | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-18 | Sanuvia Health AG | Solution Architect Prozesse | Winterthur | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-18 | Veltrima Gesundheitsdienste AG | Solution Architect Daten | St. Gallen | portal | Engineering-/Entwicklerrolle |
| 2025-04-18 | Veltrima Gesundheitsdienste AG | Software Engineer Backend Kundenerlebnis | St. Gallen | portal | Engineering-/Entwicklerrolle |
| 2025-04-19 | Cirrova Cloud AG | Software Engineer Backend (80–100 %) | Schlieren | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-19 | Kalvit Software AG | Data Engineer Kundenerlebnis | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-19 | Orvana Reisen AG | Software Engineer Backend (80–100 %) | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-04-19 | Sanuvia Health AG | Data Engineer (80–100 %) | Winterthur | portal | Engineering-/Entwicklerrolle |
| 2025-04-19 | Sanuvia Health AG | Software Engineer Backend Plattform-Services | Winterthur | portal | Engineering-/Entwicklerrolle |
| 2025-04-21 | Amberlin Versicherung AG | Data Engineer Prozesse | Lausanne | portal | Engineering-/Entwicklerrolle |
| 2025-04-21 | Mirvel Medien AG | Solution Architect Daten | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-21 | Quendor Versicherungen AG | Solution Architect (80–100 %) | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-21 | Quendor Versicherungen AG | Software Engineer Backend Prozesse | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-21 | Varella Energie AG | Software Engineer Backend (80–100 %) | Baden | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-21 | Veltrima Gesundheitsdienste AG | Solution Architect Prozesse | St. Gallen | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-22 | Fendrix Analytics AG | Software Engineer Backend (80–100 %) | Baden | portal | Engineering-/Entwicklerrolle |
| 2025-04-22 | Fendrix Analytics AG | Software Engineer Backend Daten | Baden | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-22 | Lernovi Bildung AG | Software Engineer Backend Daten | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-22 | Mastrova Industrie AG | Data Engineer Prozesse | Aarau | portal | Engineering-/Entwicklerrolle |
| 2025-04-22 | Pelvio Mobility AG | Data Engineer Digital Channels | Bern | portal | Engineering-/Entwicklerrolle |
| 2025-04-22 | Pelvio Mobility AG | Data Engineer Plattform-Services | Bern | portal | Engineering-/Entwicklerrolle |
| 2025-04-22 | Sanuvia Health AG | Solution Architect Kundenerlebnis | Winterthur | portal | Engineering-/Entwicklerrolle |
| 2025-04-22 | Stadtverwaltung Nordtal | Solution Architect B2B | Winterthur | behoerdenportal | Engineering-/Entwicklerrolle |
| 2025-04-23 | Brivana Privatbank AG | Software Engineer Backend Kundenerlebnis | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-23 | Kantonale Verwaltung Altmark | Data Engineer Daten | Aarau | behoerdenportal | Engineering-/Entwicklerrolle |
| 2025-04-23 | Lernovi Bildung AG | Solution Architect Digital Channels | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-23 | Mirvel Medien AG | Software Engineer Backend Prozesse | Zürich | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-23 | Pelvio Mobility AG | Software Engineer Backend Digital Channels | Bern | portal | Engineering-/Entwicklerrolle |
| 2025-04-23 | Sanuvia Health AG | Solution Architect B2B | Winterthur | portal | Engineering-/Entwicklerrolle |
| 2025-04-23 | Telvaro Kommunikation AG | Software Engineer Backend Plattform-Services | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-23 | Telvaro Kommunikation AG | Data Engineer (80–100 %) | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-24 | Amberlin Versicherung AG | Data Engineer Kundenerlebnis | Lausanne | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-24 | Brivana Privatbank AG | Solution Architect (80–100 %) | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-24 | Kombira Versand AG | Software Engineer Backend B2B | Dübendorf | portal | Engineering-/Entwicklerrolle |
| 2025-04-24 | Kombira Versand AG | Data Engineer Plattform-Services | Dübendorf | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-24 | Lernovi Bildung AG | Solution Architect Daten | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-24 | Mirvel Medien AG | Solution Architect Plattform-Services | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-24 | Ristra Finanztechnik AG | Software Engineer Backend B2B | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-04-24 | Ristra Finanztechnik AG | Data Engineer Daten | Zug | portal | Engineering-/Entwicklerrolle |
| 2025-04-24 | Ristra Finanztechnik AG | Solution Architect Digital Channels | Zug | netzwerk-empfehlung | Engineering-/Entwicklerrolle |
| 2025-04-24 | Telvaro Kommunikation AG | Software Engineer Backend Daten | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-24 | Telvaro Kommunikation AG | Solution Architect Plattform-Services | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-24 | Tuskora Lebensmittel AG | Solution Architect (80–100 %) | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-04-24 | Varella Energie AG | Data Engineer Daten | Baden | netzwerk-suche | Engineering-/Entwicklerrolle |
| 2025-04-25 | Quendor Versicherungen AG | Solution Architect Daten | Zürich | portal | Engineering-/Entwicklerrolle |
| 2025-04-25 | Tuskora Lebensmittel AG | Solution Architect B2B | Luzern | portal | Engineering-/Entwicklerrolle |
| 2025-04-25 | Vendaro Retail AG | Solution Architect Daten | Zürich | portal | Engineering-/Entwicklerrolle |

### Physisches Produktmanagement (159)

| Datum | Firma | Rolle | Ort | Kanal | Grund |
|---|---|---|---|---|---|
| 2025-03-03 | Hovald Bau AG | UX Designer | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-03 | Mastrova Industrie AG | Business Analyst | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-03 | Tuskora Lebensmittel AG | Product Manager Hardware Daten | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-04 | Tuskora Lebensmittel AG | Digital Product Lead Plattform-Services | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-04 | Tuskora Lebensmittel AG | UX Designer | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-05 | Hovald Bau AG | Requirements Engineer | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-05 | Lernovi Bildung AG | Product Manager Hardware Daten | Zürich | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-05 | Mastrova Industrie AG | Senior Product Manager | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-05 | Tuskora Lebensmittel AG | Product Manager Hardware B2B | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-05 | Tuskora Lebensmittel AG | Product Owner Self-Service Plattform-Services | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-06 | Mastrova Industrie AG | Scrum Master | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-06 | Mastrova Industrie AG | Scrum Master Plattform-Services | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-06 | Quelvia Pharma AG | Product Manager Hardware | Basel | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-06 | Sorvik Logistik AG | Product Manager Hardware (80–100 %) | Kloten | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-06 | Tuskora Lebensmittel AG | Projektleiter Digitalisierung | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-07 | Ristra Finanztechnik AG | Product Manager Hardware | Zug | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-10 | Mastrova Industrie AG | Product Owner Kundenportal (80–100 %) | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-10 | Tuskora Lebensmittel AG | Business Analyst | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-10 | Tuskora Lebensmittel AG | UX Designer B2B | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-11 | Hovald Bau AG | Scrum Master Plattform-Services | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-12 | Amberlin Versicherung AG | Product Manager Hardware Prozesse | Lausanne | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-12 | Mastrova Industrie AG | UX Designer (80–100 %) | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-13 | Hovald Bau AG | Requirements Engineer Daten | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-13 | Hovald Bau AG | Projektleiter Digitalisierung B2B | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-13 | Sanuvia Health AG | Product Manager Hardware Prozesse | Winterthur | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-14 | Hovald Bau AG | Product Owner Mobile App | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-14 | Mastrova Industrie AG | Business Analyst Daten | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-14 | Tuskora Lebensmittel AG | Business Analyst (80–100 %) | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-14 | Tuskora Lebensmittel AG | Requirements Engineer B2B | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-17 | Mastrova Industrie AG | Scrum Master (80–100 %) | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-17 | Orvana Reisen AG | Product Manager Hardware Digital Channels | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-18 | Tuskora Lebensmittel AG | Projektleiter Digitalisierung Plattform-Services | Luzern | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-18 | Tuskora Lebensmittel AG | Scrum Master Digital Channels | Luzern | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-18 | Tuskora Lebensmittel AG | Requirements Engineer Digital Channels | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-18 | Tuskora Lebensmittel AG | Projektleiter Digitalisierung Daten | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-18 | Tuskora Lebensmittel AG | Scrum Master (80–100 %) | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-19 | Brivana Privatbank AG | Product Manager Hardware Digital Channels | Zürich | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-19 | Hovald Bau AG | UX Designer Kundenerlebnis | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-19 | Mastrova Industrie AG | Product Manager Hardware B2B | Aarau | netzwerk-empfehlung | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-19 | Orvana Reisen AG | Product Manager Hardware B2B | Luzern | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-19 | Tuskora Lebensmittel AG | Product Manager Data Platform Kundenerlebnis | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-20 | Hovald Bau AG | Projektleiter Digitalisierung Plattform-Services | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-20 | Hovald Bau AG | UX Designer Digital Channels | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-20 | Mastrova Industrie AG | Scrum Master Digital Channels | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-20 | Mastrova Industrie AG | Projektleiter Digitalisierung Plattform-Services | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-21 | Hovald Bau AG | Scrum Master | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-21 | Mastrova Industrie AG | UX Designer Daten | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-21 | Quendor Versicherungen AG | Product Manager Hardware Daten | Zürich | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-22 | Tuskora Lebensmittel AG | Scrum Master | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-25 | Mastrova Industrie AG | UX Designer Digital Channels | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-25 | Mastrova Industrie AG | Business Analyst Kundenerlebnis | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-26 | Hovald Bau AG | Projektleiter Digitalisierung | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-26 | Orvana Reisen AG | Product Manager Hardware (80–100 %) | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-26 | Tuskora Lebensmittel AG | Business Analyst Prozesse | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-26 | Veltrima Gesundheitsdienste AG | Product Manager Hardware Daten | St. Gallen | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-27 | Hovald Bau AG | Senior Product Owner Kundenerlebnis | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-27 | Kombira Versand AG | Product Manager Hardware | Dübendorf | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-27 | Mastrova Industrie AG | Product Owner Kundenportal Prozesse | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-28 | Hovald Bau AG | UX Designer (80–100 %) | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-28 | Hovald Bau AG | Business Analyst | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-28 | Tuskora Lebensmittel AG | UX Designer Digital Channels | Luzern | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-28 | Tuskora Lebensmittel AG | Business Analyst Digital Channels | Luzern | netzwerk-empfehlung | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-31 | Lernovi Bildung AG | Product Manager Hardware | Zürich | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-31 | Mastrova Industrie AG | Projektleiter Digitalisierung Digital Channels | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-31 | Mastrova Industrie AG | Scrum Master Kundenerlebnis | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-31 | Mastrova Industrie AG | Requirements Engineer Plattform-Services | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-03-31 | Quelvia Pharma AG | Product Manager Hardware (80–100 %) | Basel | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-01 | Mastrova Industrie AG | Scrum Master Prozesse | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-01 | Tuskora Lebensmittel AG | Requirements Engineer | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-02 | Fendrix Analytics AG | Product Manager Hardware Digital Channels | Baden | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-02 | Fendrix Analytics AG | Product Manager Hardware (80–100 %) | Baden | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-02 | Hovald Bau AG | UX Designer Plattform-Services | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-02 | Hovald Bau AG | Senior Product Manager Daten | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-02 | Hovald Bau AG | Business Analyst Digital Channels | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-02 | Mastrova Industrie AG | Projektleiter Digitalisierung | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-02 | Tuskora Lebensmittel AG | Product Owner Kundenportal Digital Channels | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-03 | Mastrova Industrie AG | Product Manager Data Platform Kundenerlebnis | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-03 | Quendor Versicherungen AG | Product Manager Hardware (80–100 %) | Zürich | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-04 | Fendrix Analytics AG | Product Manager Hardware | Baden | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-04 | Hovald Bau AG | Requirements Engineer Prozesse | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-04 | Hovald Bau AG | Scrum Master B2B | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-04 | Lernovi Bildung AG | Product Manager Hardware Kundenerlebnis | Zürich | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-04 | Mastrova Industrie AG | Requirements Engineer B2B | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-04 | Mastrova Industrie AG | Requirements Engineer | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-04 | Mastrova Industrie AG | Business Analyst Prozesse | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-05 | Lernovi Bildung AG | Product Manager Hardware Digital Channels | Zürich | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-07 | Quendor Versicherungen AG | Product Manager Hardware Prozesse | Zürich | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-07 | Tuskora Lebensmittel AG | Projektleiter Digitalisierung Prozesse | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-08 | Hovald Bau AG | Business Analyst (80–100 %) | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-08 | Hovald Bau AG | Requirements Engineer Digital Channels | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-08 | Tuskora Lebensmittel AG | UX Designer Daten | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-08 | Tuskora Lebensmittel AG | Requirements Engineer Daten | Luzern | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-08 | Tuskora Lebensmittel AG | UX Designer Kundenerlebnis | Luzern | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-08 | Tuskora Lebensmittel AG | Product Manager Hardware (80–100 %) | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-09 | Hovald Bau AG | Scrum Master Daten | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-09 | Mastrova Industrie AG | Requirements Engineer Daten | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-09 | Mastrova Industrie AG | Business Analyst B2B | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-09 | Sanuvia Health AG | Product Manager Hardware Digital Channels | Winterthur | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-09 | Tuskora Lebensmittel AG | Requirements Engineer Plattform-Services | Luzern | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-09 | Tuskora Lebensmittel AG | Business Analyst B2B | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-09 | Tuskora Lebensmittel AG | Scrum Master Plattform-Services | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-09 | Tuskora Lebensmittel AG | Product Manager Hardware | Luzern | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-09 | Tuskora Lebensmittel AG | Business Analyst Kundenerlebnis | Luzern | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-10 | Hovald Bau AG | Business Analyst Daten | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-10 | Mastrova Industrie AG | Requirements Engineer (80–100 %) | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-10 | Mastrova Industrie AG | Product Manager Data Platform | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-10 | Mastrova Industrie AG | UX Designer Prozesse | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-11 | Hovald Bau AG | Product Manager KI-Anwendungen | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-11 | Sanuvia Health AG | Product Manager Hardware Daten | Winterthur | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-11 | Tuskora Lebensmittel AG | Projektleiter Digitalisierung Digital Channels | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-11 | Tuskora Lebensmittel AG | Product Manager KI-Anwendungen Digital Channels | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-12 | Pelvio Mobility AG | Product Manager Hardware (80–100 %) | Bern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-14 | Mastrova Industrie AG | Projektleiter Digitalisierung Kundenerlebnis | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-14 | Mastrova Industrie AG | Requirements Engineer Digital Channels | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-14 | Mastrova Industrie AG | Projektleiter Digitalisierung (80–100 %) | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-14 | Mastrova Industrie AG | UX Designer | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-14 | Mastrova Industrie AG | Scrum Master B2B | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-14 | Trellin Immobilien AG | Product Manager Hardware Kundenerlebnis | Zug | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-14 | Tuskora Lebensmittel AG | Product Manager Hardware Kundenerlebnis | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-14 | Varella Energie AG | Product Manager Hardware Plattform-Services | Baden | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-14 | Vendaro Retail AG | Product Manager Hardware Plattform-Services | Zürich | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-15 | Hovald Bau AG | Business Analyst B2B | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-15 | Mastrova Industrie AG | Projektleiter Digitalisierung Daten | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-15 | Trellin Immobilien AG | Product Manager Hardware Digital Channels | Zug | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-15 | Tuskora Lebensmittel AG | Projektleiter Digitalisierung B2B | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-15 | Tuskora Lebensmittel AG | Product Owner Mobile App B2B | Luzern | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-15 | Tuskora Lebensmittel AG | Scrum Master Kundenerlebnis | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-16 | Hovald Bau AG | Product Manager Hardware | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-16 | Hovald Bau AG | UX Designer B2B | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-16 | Tuskora Lebensmittel AG | Senior Product Owner | Luzern | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-16 | Tuskora Lebensmittel AG | Product Owner Self-Service Daten | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-16 | Tuskora Lebensmittel AG | Requirements Engineer Prozesse | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-17 | Amberlin Versicherung AG | Product Manager Hardware Plattform-Services | Lausanne | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-17 | Ristra Finanztechnik AG | Product Manager Hardware Prozesse | Zug | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-17 | Tuskora Lebensmittel AG | Scrum Master Daten | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-17 | Tuskora Lebensmittel AG | Lead Product Owner Plattform Kundenerlebnis | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-18 | Hovald Bau AG | Business Analyst Plattform-Services | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-18 | Hovald Bau AG | Projektleiter Digitalisierung Kundenerlebnis | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-18 | Kalvit Software AG | Product Manager Hardware | Zürich | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-18 | Kalvit Software AG | Product Manager Hardware Daten | Zürich | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-18 | Mastrova Industrie AG | Projektleiter Digitalisierung Prozesse | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-18 | Quelvia Pharma AG | Product Manager Hardware B2B | Basel | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-18 | Tuskora Lebensmittel AG | Product Manager Hardware Prozesse | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-18 | Tuskora Lebensmittel AG | Projektleiter Digitalisierung (80–100 %) | Luzern | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-21 | Cirrova Cloud AG | Product Manager Hardware B2B | Schlieren | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-21 | Hovald Bau AG | Product Owner Mobile App (80–100 %) | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-21 | Mastrova Industrie AG | Product Manager Data Platform B2B | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-21 | Orvana Reisen AG | Product Manager Hardware | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-21 | Tuskora Lebensmittel AG | Requirements Engineer (80–100 %) | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-23 | Cirrova Cloud AG | Product Manager Hardware (80–100 %) | Schlieren | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-23 | Kalvit Software AG | Product Manager Hardware (80–100 %) | Zürich | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-23 | Mastrova Industrie AG | Product Owner Kundenportal | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-23 | Tuskora Lebensmittel AG | Projektleiter Digitalisierung Kundenerlebnis | Luzern | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-24 | Hovald Bau AG | Scrum Master Prozesse | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-24 | Hovald Bau AG | Product Manager Hardware (80–100 %) | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-24 | Mastrova Industrie AG | Product Owner Self-Service | Aarau | portal | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-24 | Mastrova Industrie AG | Lead Product Owner Plattform B2B | Aarau | netzwerk-empfehlung | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-25 | Hovald Bau AG | Product Owner Kundenportal Prozesse | Aarau | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |
| 2025-04-25 | Tuskora Lebensmittel AG | UX Designer Plattform-Services | Luzern | netzwerk-suche | Physisches Produkt (Hardware, Maschinen, Lebensmittel) |

### Vermittler / Personalberatung (130)

| Datum | Firma | Rolle | Ort | Kanal | Grund |
|---|---|---|---|---|---|
| 2025-03-03 | Jobvera Staffing AG | UX Designer Daten | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-03 | Jobvera Staffing AG | Business Analyst Kundenerlebnis | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-03 | Jobvera Staffing AG | Scrum Master | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-03 | Talentbrücke Personal AG | Requirements Engineer | Zürich | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-04 | Talentbrücke Personal AG | Solution Architect | Zürich | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-05 | Jobvera Staffing AG | UX Designer Prozesse | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-05 | Jobvera Staffing AG | Requirements Engineer Plattform-Services | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-05 | Talentbrücke Personal AG | UX Designer B2B | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-05 | Talentbrücke Personal AG | Junior Product Owner Plattform-Services | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-06 | Jobvera Staffing AG | UX Designer Digital Channels | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-06 | Jobvera Staffing AG | Solution Architect B2B | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-06 | Talentbrücke Personal AG | Software Engineer Backend Digital Channels | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-06 | Talentbrücke Personal AG | Product Manager Hardware Plattform-Services | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-07 | Jobvera Staffing AG | Software Engineer Backend (80–100 %) | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-07 | Talentbrücke Personal AG | Requirements Engineer B2B | Zürich | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-10 | Jobvera Staffing AG | UX Designer B2B | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-10 | Jobvera Staffing AG | Projektleiter Digitalisierung (80–100 %) | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-11 | Jobvera Staffing AG | Scrum Master Plattform-Services | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-12 | Jobvera Staffing AG | Product Manager Data Platform (80–100 %) | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-12 | Talentbrücke Personal AG | Requirements Engineer Digital Channels | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-12 | Talentbrücke Personal AG | UX Designer Prozesse | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-13 | Jobvera Staffing AG | Data Engineer Kundenerlebnis | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-13 | Jobvera Staffing AG | Requirements Engineer | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-14 | Jobvera Staffing AG | Data Engineer | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-17 | Jobvera Staffing AG | Software Engineer Backend | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-17 | Jobvera Staffing AG | Product Owner Self-Service Daten | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-17 | Jobvera Staffing AG | Projektleiter Digitalisierung Daten | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-18 | Talentbrücke Personal AG | Digital Product Lead Prozesse | Zürich | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-18 | Talentbrücke Personal AG | UX Designer | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-19 | Jobvera Staffing AG | Requirements Engineer Kundenerlebnis | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-20 | Talentbrücke Personal AG | Scrum Master | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-21 | Jobvera Staffing AG | UX Designer Plattform-Services | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-21 | Talentbrücke Personal AG | Business Analyst | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-21 | Talentbrücke Personal AG | Product Owner Kundenportal | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-21 | Talentbrücke Personal AG | Product Manager Hardware B2B | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-21 | Talentbrücke Personal AG | Requirements Engineer Daten | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-21 | Talentbrücke Personal AG | Scrum Master B2B | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-22 | Talentbrücke Personal AG | Product Owner Mobile App Plattform-Services | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-24 | Jobvera Staffing AG | Data Engineer Plattform-Services | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-24 | Jobvera Staffing AG | Requirements Engineer Digital Channels | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-24 | Talentbrücke Personal AG | Requirements Engineer Kundenerlebnis | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-25 | Jobvera Staffing AG | Software Engineer Backend Daten | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-26 | Jobvera Staffing AG | Solution Architect (80–100 %) | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-26 | Talentbrücke Personal AG | Business Analyst Daten | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-27 | Jobvera Staffing AG | Data Engineer B2B | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-27 | Talentbrücke Personal AG | Business Analyst Kundenerlebnis | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-28 | Jobvera Staffing AG | UX Designer | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-28 | Jobvera Staffing AG | Software Engineer Backend Digital Channels | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-28 | Jobvera Staffing AG | Requirements Engineer Prozesse | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-28 | Talentbrücke Personal AG | Data Engineer B2B | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-29 | Jobvera Staffing AG | Scrum Master Daten | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-29 | Jobvera Staffing AG | Software Engineer Backend B2B | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-31 | Jobvera Staffing AG | Solution Architect Daten | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-31 | Talentbrücke Personal AG | UX Designer Daten | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-03-31 | Talentbrücke Personal AG | Projektleiter Digitalisierung Plattform-Services | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-01 | Jobvera Staffing AG | Praktikum Produktmanagement | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-01 | Jobvera Staffing AG | Junior Product Owner | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-01 | Jobvera Staffing AG | Product Owner Mobile App Daten | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-01 | Jobvera Staffing AG | Product Owner Mobile App B2B | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-01 | Jobvera Staffing AG | Product Manager Hardware Daten | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-01 | Talentbrücke Personal AG | Junior Product Owner | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-01 | Talentbrücke Personal AG | Praktikum Produktmanagement Daten | Zürich | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-01 | Talentbrücke Personal AG | Product Manager Hardware Daten | Zürich | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-03 | Jobvera Staffing AG | UX Designer (80–100 %) | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-03 | Jobvera Staffing AG | Data Engineer Prozesse | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-03 | Talentbrücke Personal AG | Solution Architect Prozesse | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-03 | Talentbrücke Personal AG | Scrum Master Daten | Zürich | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-03 | Talentbrücke Personal AG | Product Manager Hardware Kundenerlebnis | Zürich | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-03 | Talentbrücke Personal AG | Praktikum Produktmanagement | Zürich | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-03 | Talentbrücke Personal AG | Software Engineer Backend B2B | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-04 | Jobvera Staffing AG | Requirements Engineer (80–100 %) | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-04 | Talentbrücke Personal AG | Software Engineer Backend (80–100 %) | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-05 | Jobvera Staffing AG | Projektleiter Digitalisierung Digital Channels | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-07 | Jobvera Staffing AG | Projektleiter Digitalisierung Plattform-Services | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-07 | Jobvera Staffing AG | UX Designer Kundenerlebnis | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-08 | Jobvera Staffing AG | Business Analyst Plattform-Services | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-08 | Jobvera Staffing AG | Data Engineer Digital Channels | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-08 | Jobvera Staffing AG | Data Engineer Daten | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-08 | Jobvera Staffing AG | Solution Architect Plattform-Services | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-08 | Talentbrücke Personal AG | Lead Product Owner Plattform Digital Channels | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-08 | Talentbrücke Personal AG | Business Analyst Prozesse | Zürich | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-08 | Talentbrücke Personal AG | Solution Architect Digital Channels | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-08 | Talentbrücke Personal AG | Senior Product Manager Daten | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-09 | Jobvera Staffing AG | Data Engineer (80–100 %) | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-09 | Talentbrücke Personal AG | Software Engineer Backend | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-09 | Talentbrücke Personal AG | Business Analyst B2B | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-09 | Talentbrücke Personal AG | Scrum Master (80–100 %) | Zürich | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-10 | Jobvera Staffing AG | Product Manager Data Platform Kundenerlebnis | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-10 | Jobvera Staffing AG | Business Analyst | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-10 | Jobvera Staffing AG | Software Engineer Backend Plattform-Services | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-10 | Talentbrücke Personal AG | Solution Architect Kundenerlebnis | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-10 | Talentbrücke Personal AG | Scrum Master Kundenerlebnis | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-11 | Jobvera Staffing AG | Projektleiter Digitalisierung | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-11 | Jobvera Staffing AG | Product Manager Hardware (80–100 %) | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-11 | Jobvera Staffing AG | Scrum Master Kundenerlebnis | Zug | netzwerk-empfehlung | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-11 | Talentbrücke Personal AG | Praktikum Produktmanagement Prozesse | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-14 | Jobvera Staffing AG | Product Owner Mobile App (80–100 %) | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-14 | Jobvera Staffing AG | Software Engineer Backend Prozesse | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-14 | Talentbrücke Personal AG | Data Engineer | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-14 | Talentbrücke Personal AG | Projektleiter Digitalisierung | Zürich | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-15 | Jobvera Staffing AG | Product Manager KI-Anwendungen Prozesse | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-15 | Talentbrücke Personal AG | UX Designer (80–100 %) | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-16 | Talentbrücke Personal AG | Business Analyst Digital Channels | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-16 | Talentbrücke Personal AG | Solution Architect Plattform-Services | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-17 | Jobvera Staffing AG | Solution Architect | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-17 | Jobvera Staffing AG | Scrum Master Prozesse | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-17 | Jobvera Staffing AG | Junior Product Owner Daten | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-17 | Talentbrücke Personal AG | Data Engineer Kundenerlebnis | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-18 | Jobvera Staffing AG | Praktikum Produktmanagement Daten | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-18 | Jobvera Staffing AG | Scrum Master B2B | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-18 | Talentbrücke Personal AG | Requirements Engineer Plattform-Services | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-18 | Talentbrücke Personal AG | Software Engineer Backend Plattform-Services | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-18 | Talentbrücke Personal AG | UX Designer Digital Channels | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-19 | Talentbrücke Personal AG | Junior Product Owner Kundenerlebnis | Zürich | netzwerk-empfehlung | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-21 | Jobvera Staffing AG | Product Owner Payments Kundenerlebnis | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-21 | Talentbrücke Personal AG | Product Manager Data Platform Daten | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-22 | Jobvera Staffing AG | Business Analyst Digital Channels | Zug | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-22 | Talentbrücke Personal AG | Junior Product Owner (80–100 %) | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-22 | Talentbrücke Personal AG | Requirements Engineer (80–100 %) | Zürich | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-22 | Talentbrücke Personal AG | Praktikum Produktmanagement B2B | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-22 | Talentbrücke Personal AG | Scrum Master Digital Channels | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-23 | Jobvera Staffing AG | Senior Product Owner (80–100 %) | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-23 | Talentbrücke Personal AG | Product Manager Hardware Prozesse | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-23 | Talentbrücke Personal AG | Product Owner Mobile App Digital Channels | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-23 | Talentbrücke Personal AG | Product Owner Self-Service | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-23 | Talentbrücke Personal AG | Software Engineer Backend Prozesse | Zürich | netzwerk-suche | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-24 | Jobvera Staffing AG | Software Engineer Backend Kundenerlebnis | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-24 | Talentbrücke Personal AG | UX Designer Plattform-Services | Zürich | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-25 | Jobvera Staffing AG | Lead Product Owner Plattform Kundenerlebnis | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |
| 2025-04-25 | Jobvera Staffing AG | Product Owner Payments Plattform-Services | Zug | portal | Vermittler (Personalvermittlung, kein Arbeitgeber) |

### Junior / Praktikum / Lehrstelle (128)

| Datum | Firma | Rolle | Ort | Kanal | Grund |
|---|---|---|---|---|---|
| 2025-03-03 | Brivana Privatbank AG | Junior Product Owner | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-04 | Brivana Privatbank AG | Junior Product Owner Digital Channels | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-04 | Quelvia Pharma AG | Praktikum Produktmanagement (80–100 %) | Basel | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-04 | Quelvia Pharma AG | Junior Product Owner (80–100 %) | Basel | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-04 | Trellin Immobilien AG | Praktikum Produktmanagement | Zug | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-05 | Fendrix Analytics AG | Praktikum Produktmanagement (80–100 %) | Baden | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-05 | Kalvit Software AG | Junior Product Owner Kundenerlebnis | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-05 | Lernovi Bildung AG | Praktikum Produktmanagement Plattform-Services | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-06 | Cirrova Cloud AG | Praktikum Produktmanagement | Schlieren | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-07 | Amberlin Versicherung AG | Junior Product Owner | Lausanne | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-07 | Fendrix Analytics AG | Junior Product Owner Kundenerlebnis | Baden | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-10 | Fendrix Analytics AG | Junior Product Owner | Baden | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-12 | Fendrix Analytics AG | Praktikum Produktmanagement Daten | Baden | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-13 | Hovald Bau AG | Junior Product Owner Digital Channels | Aarau | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-13 | Quendor Versicherungen AG | Praktikum Produktmanagement B2B | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-13 | Tuskora Lebensmittel AG | Praktikum Produktmanagement Digital Channels | Luzern | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-13 | Varella Energie AG | Praktikum Produktmanagement Kundenerlebnis | Baden | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-14 | Sorvik Logistik AG | Junior Product Owner Plattform-Services | Kloten | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-14 | Trellin Immobilien AG | Praktikum Produktmanagement Prozesse | Zug | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-17 | Amberlin Versicherung AG | Praktikum Produktmanagement | Lausanne | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-17 | Kalvit Software AG | Praktikum Produktmanagement | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-17 | Mastrova Industrie AG | Junior Product Owner | Aarau | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-17 | Orvana Reisen AG | Junior Product Owner Digital Channels | Luzern | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-17 | Sanuvia Health AG | Junior Product Owner (80–100 %) | Winterthur | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-17 | Vendaro Retail AG | Praktikum Produktmanagement (80–100 %) | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-18 | Brivana Privatbank AG | Junior Product Owner Prozesse | Zürich | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-18 | Cirrova Cloud AG | Junior Product Owner Plattform-Services | Schlieren | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-18 | Lernovi Bildung AG | Praktikum Produktmanagement | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-18 | Varella Energie AG | Junior Product Owner | Baden | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-18 | Vendaro Retail AG | Junior Product Owner Prozesse | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-19 | Fendrix Analytics AG | Praktikum Produktmanagement Plattform-Services | Baden | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-19 | Kalvit Software AG | Junior Product Owner | Zürich | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-19 | Kalvit Software AG | Praktikum Produktmanagement Kundenerlebnis | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-19 | Trellin Immobilien AG | Junior Product Owner | Zug | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-20 | Lernovi Bildung AG | Junior Product Owner Digital Channels | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-20 | Tuskora Lebensmittel AG | Junior Product Owner Plattform-Services | Luzern | netzwerk-empfehlung | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-21 | Pelvio Mobility AG | Praktikum Produktmanagement Prozesse | Bern | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-21 | Sanuvia Health AG | Praktikum Produktmanagement Prozesse | Winterthur | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-21 | Sorvik Logistik AG | Junior Product Owner | Kloten | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-21 | Trellin Immobilien AG | Praktikum Produktmanagement (80–100 %) | Zug | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-24 | Kombira Versand AG | Praktikum Produktmanagement B2B | Dübendorf | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-24 | Veltrima Gesundheitsdienste AG | Praktikum Produktmanagement B2B | St. Gallen | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-25 | Varella Energie AG | Praktikum Produktmanagement | Baden | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-25 | Vendaro Retail AG | Praktikum Produktmanagement B2B | Zürich | netzwerk-empfehlung | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-26 | Fendrix Analytics AG | Junior Product Owner B2B | Baden | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-26 | Kombira Versand AG | Praktikum Produktmanagement | Dübendorf | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-26 | Lernovi Bildung AG | Junior Product Owner Prozesse | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-26 | Quelvia Pharma AG | Junior Product Owner B2B | Basel | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-26 | Quendor Versicherungen AG | Junior Product Owner B2B | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-27 | Mastrova Industrie AG | Praktikum Produktmanagement Daten | Aarau | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-27 | Orvana Reisen AG | Praktikum Produktmanagement | Luzern | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-27 | Quendor Versicherungen AG | Junior Product Owner Prozesse | Zürich | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-28 | Fendrix Analytics AG | Praktikum Produktmanagement | Baden | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-28 | Ristra Finanztechnik AG | Praktikum Produktmanagement (80–100 %) | Zug | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-28 | Telvaro Kommunikation AG | Praktikum Produktmanagement Daten | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-28 | Vendaro Retail AG | Junior Product Owner (80–100 %) | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-31 | Brivana Privatbank AG | Praktikum Produktmanagement | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-31 | Cirrova Cloud AG | Junior Product Owner Digital Channels | Schlieren | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-31 | Fendrix Analytics AG | Praktikum Produktmanagement Digital Channels | Baden | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-31 | Hovald Bau AG | Praktikum Produktmanagement Daten | Aarau | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-31 | Kombira Versand AG | Praktikum Produktmanagement Daten | Dübendorf | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-31 | Mastrova Industrie AG | Praktikum Produktmanagement | Aarau | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-03-31 | Orvana Reisen AG | Junior Product Owner Plattform-Services | Luzern | netzwerk-empfehlung | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-01 | Amberlin Versicherung AG | Praktikum Produktmanagement Prozesse | Lausanne | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-01 | Brivana Privatbank AG | Junior Product Owner Plattform-Services | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-01 | Kombira Versand AG | Praktikum Produktmanagement Kundenerlebnis | Dübendorf | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-01 | Kombira Versand AG | Junior Product Owner Kundenerlebnis | Dübendorf | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-01 | Pelvio Mobility AG | Junior Product Owner | Bern | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-01 | Quelvia Pharma AG | Junior Product Owner Kundenerlebnis | Basel | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-01 | Sanuvia Health AG | Praktikum Produktmanagement | Winterthur | netzwerk-empfehlung | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-01 | Tuskora Lebensmittel AG | Praktikum Produktmanagement Prozesse | Luzern | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-02 | Cirrova Cloud AG | Praktikum Produktmanagement Digital Channels | Schlieren | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-02 | Mastrova Industrie AG | Junior Product Owner B2B | Aarau | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-02 | Telvaro Kommunikation AG | Praktikum Produktmanagement | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-02 | Trellin Immobilien AG | Praktikum Produktmanagement Kundenerlebnis | Zug | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-03 | Cirrova Cloud AG | Junior Product Owner (80–100 %) | Schlieren | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-03 | Mastrova Industrie AG | Praktikum Produktmanagement Digital Channels | Aarau | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-03 | Ristra Finanztechnik AG | Junior Product Owner Digital Channels | Zug | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-03 | Sanuvia Health AG | Junior Product Owner | Winterthur | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-03 | Sorvik Logistik AG | Praktikum Produktmanagement (80–100 %) | Kloten | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-04 | Quelvia Pharma AG | Praktikum Produktmanagement | Basel | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-07 | Cirrova Cloud AG | Junior Product Owner | Schlieren | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-09 | Pelvio Mobility AG | Praktikum Produktmanagement B2B | Bern | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-09 | Ristra Finanztechnik AG | Junior Product Owner | Zug | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-10 | Orvana Reisen AG | Praktikum Produktmanagement Daten | Luzern | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-10 | Pelvio Mobility AG | Praktikum Produktmanagement Plattform-Services | Bern | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-10 | Ristra Finanztechnik AG | Praktikum Produktmanagement Kundenerlebnis | Zug | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-11 | Sanuvia Health AG | Praktikum Produktmanagement Daten | Winterthur | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-11 | Sorvik Logistik AG | Junior Product Owner Prozesse | Kloten | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-11 | Veltrima Gesundheitsdienste AG | Praktikum Produktmanagement Prozesse | St. Gallen | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-12 | Sorvik Logistik AG | Junior Product Owner Kundenerlebnis | Kloten | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-14 | Hovald Bau AG | Junior Product Owner Prozesse | Aarau | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-14 | Hovald Bau AG | Praktikum Produktmanagement Kundenerlebnis | Aarau | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-14 | Telvaro Kommunikation AG | Praktikum Produktmanagement (80–100 %) | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-15 | Kombira Versand AG | Praktikum Produktmanagement Digital Channels | Dübendorf | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-15 | Tuskora Lebensmittel AG | Junior Product Owner | Luzern | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-16 | Quendor Versicherungen AG | Praktikum Produktmanagement Prozesse | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-16 | Sorvik Logistik AG | Junior Product Owner B2B | Kloten | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-17 | Mirvel Medien AG | Junior Product Owner | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-17 | Sanuvia Health AG | Praktikum Produktmanagement B2B | Winterthur | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-18 | Kombira Versand AG | Junior Product Owner | Dübendorf | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-18 | Pelvio Mobility AG | Junior Product Owner B2B | Bern | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-18 | Quendor Versicherungen AG | Junior Product Owner Plattform-Services | Zürich | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-18 | Quendor Versicherungen AG | Praktikum Produktmanagement | Zürich | netzwerk-empfehlung | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-18 | Sanuvia Health AG | Junior Product Owner B2B | Winterthur | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-18 | Sorvik Logistik AG | Junior Product Owner Daten | Kloten | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-18 | Trellin Immobilien AG | Junior Product Owner (80–100 %) | Zug | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-18 | Varella Energie AG | Junior Product Owner Prozesse | Baden | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-21 | Telvaro Kommunikation AG | Praktikum Produktmanagement Plattform-Services | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-21 | Trellin Immobilien AG | Junior Product Owner Kundenerlebnis | Zug | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-22 | Kalvit Software AG | Praktikum Produktmanagement Daten | Zürich | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-22 | Pelvio Mobility AG | Junior Product Owner Daten | Bern | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-22 | Quelvia Pharma AG | Junior Product Owner Plattform-Services | Basel | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-22 | Quelvia Pharma AG | Praktikum Produktmanagement B2B | Basel | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-22 | Sorvik Logistik AG | Praktikum Produktmanagement Prozesse | Kloten | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-22 | Telvaro Kommunikation AG | Junior Product Owner | Zürich | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-22 | Tuskora Lebensmittel AG | Junior Product Owner B2B | Luzern | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-23 | Brivana Privatbank AG | Praktikum Produktmanagement Daten | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-23 | Pelvio Mobility AG | Junior Product Owner Kundenerlebnis | Bern | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-23 | Quendor Versicherungen AG | Junior Product Owner | Zürich | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-23 | Trellin Immobilien AG | Junior Product Owner Plattform-Services | Zug | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-23 | Veltrima Gesundheitsdienste AG | Praktikum Produktmanagement | St. Gallen | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-24 | Mastrova Industrie AG | Junior Product Owner Daten | Aarau | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-24 | Mirvel Medien AG | Praktikum Produktmanagement | Zürich | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-24 | Ristra Finanztechnik AG | Junior Product Owner Daten | Zug | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-25 | Ristra Finanztechnik AG | Praktikum Produktmanagement Daten | Zug | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-25 | Sorvik Logistik AG | Praktikum Produktmanagement Plattform-Services | Kloten | portal | Ausschluss 1 (Junior/Praktikum) |
| 2025-04-25 | Varella Energie AG | Junior Product Owner (80–100 %) | Baden | netzwerk-suche | Ausschluss 1 (Junior/Praktikum) |

### Beratung / Agentur (123)

| Datum | Firma | Rolle | Ort | Kanal | Grund |
|---|---|---|---|---|---|
| 2025-03-04 | Kandora Consulting AG | Junior Product Owner Prozesse | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-04 | Pixavo Agentur GmbH | UX Designer | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-04 | Pixavo Agentur GmbH | Requirements Engineer Prozesse | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-04 | Pixavo Agentur GmbH | Requirements Engineer B2B | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-04 | Pixavo Agentur GmbH | Scrum Master (80–100 %) | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-05 | Kandora Consulting AG | Solution Architect | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-05 | Pixavo Agentur GmbH | Projektleiter Digitalisierung Prozesse | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-05 | Pixavo Agentur GmbH | UX Designer Prozesse | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-05 | Pixavo Agentur GmbH | Solution Architect Kundenerlebnis | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-06 | Kandora Consulting AG | Business Analyst Kundenerlebnis | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-06 | Pixavo Agentur GmbH | Product Owner Self-Service | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-06 | Pixavo Agentur GmbH | Scrum Master Prozesse | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-07 | Kandora Consulting AG | Scrum Master (80–100 %) | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-10 | Pixavo Agentur GmbH | Business Analyst | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-11 | Pixavo Agentur GmbH | Data Engineer B2B | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-12 | Kandora Consulting AG | Product Manager Data Platform | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-12 | Pixavo Agentur GmbH | Software Engineer Backend Plattform-Services | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-12 | Pixavo Agentur GmbH | Software Engineer Backend (80–100 %) | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-13 | Kandora Consulting AG | Business Analyst (80–100 %) | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-13 | Kandora Consulting AG | Projektleiter Digitalisierung | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-13 | Kandora Consulting AG | Software Engineer Backend | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-13 | Pixavo Agentur GmbH | Junior Product Owner Prozesse | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-14 | Kandora Consulting AG | UX Designer | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-14 | Kandora Consulting AG | Projektleiter Digitalisierung Daten | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-14 | Kandora Consulting AG | Requirements Engineer Prozesse | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-14 | Pixavo Agentur GmbH | Product Manager KI-Anwendungen | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-18 | Kandora Consulting AG | Data Engineer | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-18 | Pixavo Agentur GmbH | Scrum Master Daten | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-18 | Pixavo Agentur GmbH | Solution Architect B2B | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-18 | Pixavo Agentur GmbH | Product Manager Hardware Plattform-Services | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-19 | Kandora Consulting AG | Business Analyst Plattform-Services | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-19 | Kandora Consulting AG | UX Designer Digital Channels | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-19 | Kandora Consulting AG | UX Designer (80–100 %) | Zürich | netzwerk-empfehlung | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-19 | Pixavo Agentur GmbH | Projektleiter Digitalisierung (80–100 %) | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-19 | Pixavo Agentur GmbH | Data Engineer | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-19 | Pixavo Agentur GmbH | Product Manager Hardware Prozesse | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-20 | Pixavo Agentur GmbH | Software Engineer Backend Kundenerlebnis | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-20 | Pixavo Agentur GmbH | Requirements Engineer Kundenerlebnis | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-21 | Kandora Consulting AG | Scrum Master Prozesse | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-21 | Kandora Consulting AG | Product Manager Data Platform Daten | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-21 | Kandora Consulting AG | Data Engineer (80–100 %) | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-21 | Pixavo Agentur GmbH | Solution Architect | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-21 | Pixavo Agentur GmbH | Junior Product Owner Digital Channels | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-22 | Kandora Consulting AG | Solution Architect Prozesse | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-24 | Kandora Consulting AG | Data Engineer Daten | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-24 | Kandora Consulting AG | Software Engineer Backend Daten | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-24 | Pixavo Agentur GmbH | Business Analyst Daten | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-25 | Pixavo Agentur GmbH | Data Engineer Plattform-Services | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-25 | Pixavo Agentur GmbH | Scrum Master | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-26 | Kandora Consulting AG | Solution Architect Plattform-Services | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-26 | Kandora Consulting AG | Business Analyst Prozesse | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-26 | Kandora Consulting AG | Product Owner Mobile App Digital Channels | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-26 | Pixavo Agentur GmbH | Software Engineer Backend Prozesse | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-27 | Kandora Consulting AG | Business Analyst | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-27 | Kandora Consulting AG | Product Owner Mobile App | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-27 | Kandora Consulting AG | Requirements Engineer Kundenerlebnis | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-27 | Pixavo Agentur GmbH | Requirements Engineer | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-28 | Pixavo Agentur GmbH | Product Manager Hardware | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-28 | Pixavo Agentur GmbH | UX Designer Plattform-Services | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-28 | Pixavo Agentur GmbH | UX Designer (80–100 %) | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-28 | Pixavo Agentur GmbH | Scrum Master Kundenerlebnis | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-31 | Pixavo Agentur GmbH | Lead Product Owner Plattform Kundenerlebnis | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-31 | Pixavo Agentur GmbH | Requirements Engineer Plattform-Services | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-03-31 | Pixavo Agentur GmbH | UX Designer Digital Channels | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-01 | Pixavo Agentur GmbH | Business Analyst B2B | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-02 | Kandora Consulting AG | Scrum Master Kundenerlebnis | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-02 | Kandora Consulting AG | UX Designer Plattform-Services | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-02 | Pixavo Agentur GmbH | Product Owner Mobile App (80–100 %) | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-03 | Pixavo Agentur GmbH | Business Analyst Digital Channels | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-03 | Pixavo Agentur GmbH | Projektleiter Digitalisierung Digital Channels | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-03 | Pixavo Agentur GmbH | Software Engineer Backend Digital Channels | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-04 | Kandora Consulting AG | Data Engineer Plattform-Services | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-04 | Kandora Consulting AG | Junior Product Owner | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-04 | Pixavo Agentur GmbH | Lead Product Owner Plattform Daten | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-05 | Kandora Consulting AG | Product Owner Kundenportal Prozesse | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-07 | Kandora Consulting AG | Requirements Engineer Plattform-Services | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-07 | Kandora Consulting AG | Scrum Master B2B | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-07 | Kandora Consulting AG | Product Manager Data Platform Digital Channels | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-07 | Kandora Consulting AG | Praktikum Produktmanagement Daten | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-07 | Pixavo Agentur GmbH | Requirements Engineer (80–100 %) | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-07 | Pixavo Agentur GmbH | Product Manager Hardware Daten | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-08 | Kandora Consulting AG | Software Engineer Backend (80–100 %) | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-09 | Kandora Consulting AG | Projektleiter Digitalisierung B2B | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-09 | Kandora Consulting AG | Software Engineer Backend Digital Channels | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-09 | Pixavo Agentur GmbH | Junior Product Owner | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-11 | Kandora Consulting AG | Business Analyst Digital Channels | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-11 | Pixavo Agentur GmbH | Requirements Engineer Digital Channels | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-12 | Kandora Consulting AG | Junior Product Owner Daten | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-14 | Kandora Consulting AG | Head of Product Digital Channels | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-14 | Kandora Consulting AG | Requirements Engineer Digital Channels | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-15 | Kandora Consulting AG | Product Owner Self-Service (80–100 %) | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-15 | Kandora Consulting AG | Junior Product Owner Kundenerlebnis | Zürich | netzwerk-empfehlung | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-15 | Pixavo Agentur GmbH | Senior Product Owner Kundenerlebnis | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-15 | Pixavo Agentur GmbH | Product Manager Data Platform Kundenerlebnis | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-16 | Kandora Consulting AG | Requirements Engineer | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-16 | Kandora Consulting AG | Data Engineer B2B | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-16 | Kandora Consulting AG | Business Analyst B2B | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-16 | Pixavo Agentur GmbH | Junior Product Owner Plattform-Services | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-16 | Pixavo Agentur GmbH | Software Engineer Backend | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-17 | Kandora Consulting AG | Praktikum Produktmanagement Digital Channels | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-18 | Kandora Consulting AG | Product Owner Kundenportal Kundenerlebnis | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-18 | Kandora Consulting AG | Praktikum Produktmanagement | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-18 | Pixavo Agentur GmbH | Product Manager Data Platform Digital Channels | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-18 | Pixavo Agentur GmbH | Projektleiter Digitalisierung | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-19 | Kandora Consulting AG | Senior Product Owner Daten | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-19 | Kandora Consulting AG | Projektleiter Digitalisierung Digital Channels | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-21 | Kandora Consulting AG | Lead Product Owner Plattform | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-21 | Kandora Consulting AG | Praktikum Produktmanagement B2B | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-21 | Pixavo Agentur GmbH | UX Designer B2B | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-21 | Pixavo Agentur GmbH | Product Owner Self-Service (80–100 %) | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-22 | Kandora Consulting AG | Product Manager Hardware B2B | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-22 | Pixavo Agentur GmbH | Data Engineer Prozesse | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-22 | Pixavo Agentur GmbH | Solution Architect Daten | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-22 | Pixavo Agentur GmbH | Requirements Engineer Daten | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-22 | Pixavo Agentur GmbH | Business Analyst Plattform-Services | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-23 | Pixavo Agentur GmbH | Business Analyst (80–100 %) | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-23 | Pixavo Agentur GmbH | Software Engineer Backend B2B | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-24 | Kandora Consulting AG | Software Engineer Backend Prozesse | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-24 | Kandora Consulting AG | Solution Architect Digital Channels | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-24 | Pixavo Agentur GmbH | UX Designer Daten | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-24 | Pixavo Agentur GmbH | Product Owner Mobile App | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-25 | Kandora Consulting AG | Senior Product Manager B2B | Zürich | portal | Ausschluss 4 (Beratung/Agentur) |
| 2025-04-25 | Kandora Consulting AG | Solution Architect (80–100 %) | Zürich | netzwerk-suche | Ausschluss 4 (Beratung/Agentur) |

### Firmen-Ausschluss der Persona (61)

| Datum | Firma | Rolle | Ort | Kanal | Grund |
|---|---|---|---|---|---|
| 2025-03-04 | Spielora Gaming AG | UX Designer | Zürich | netzwerk-suche | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-07 | Spielora Gaming AG | Scrum Master Daten | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-07 | Spielora Gaming AG | Scrum Master Prozesse | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-11 | Spielora Gaming AG | Data Engineer Prozesse | Zürich | netzwerk-suche | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-11 | Spielora Gaming AG | Requirements Engineer Digital Channels | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-12 | Spielora Gaming AG | Praktikum Produktmanagement Plattform-Services | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-17 | Spielora Gaming AG | Product Owner Self-Service | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-17 | Spielora Gaming AG | Software Engineer Backend | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-18 | Spielora Gaming AG | Business Analyst Plattform-Services | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-18 | Spielora Gaming AG | Requirements Engineer | Zürich | netzwerk-suche | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-19 | Spielora Gaming AG | Senior Product Manager (80–100 %) | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-19 | Spielora Gaming AG | Data Engineer Digital Channels | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-19 | Spielora Gaming AG | Projektleiter Digitalisierung Prozesse | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-19 | Spielora Gaming AG | Product Owner Kundenportal | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-19 | Spielora Gaming AG | Solution Architect (80–100 %) | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-20 | Spielora Gaming AG | Data Engineer | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-21 | Spielora Gaming AG | Solution Architect | Zürich | netzwerk-suche | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-22 | Spielora Gaming AG | Product Manager Hardware Plattform-Services | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-22 | Spielora Gaming AG | Solution Architect Kundenerlebnis | Zürich | netzwerk-suche | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-22 | Spielora Gaming AG | Scrum Master (80–100 %) | Zürich | netzwerk-empfehlung | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-24 | Spielora Gaming AG | Praktikum Produktmanagement Kundenerlebnis | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-25 | Spielora Gaming AG | Business Analyst | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-25 | Spielora Gaming AG | Requirements Engineer Prozesse | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-26 | Spielora Gaming AG | Projektleiter Digitalisierung Kundenerlebnis | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-27 | Spielora Gaming AG | Requirements Engineer (80–100 %) | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-28 | Spielora Gaming AG | Product Manager Hardware Daten | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-28 | Spielora Gaming AG | Software Engineer Backend B2B | Zürich | netzwerk-suche | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-03-31 | Spielora Gaming AG | Scrum Master Digital Channels | Zürich | netzwerk-empfehlung | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-01 | Spielora Gaming AG | Business Analyst (80–100 %) | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-01 | Spielora Gaming AG | Junior Product Owner Digital Channels | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-01 | Spielora Gaming AG | Data Engineer B2B | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-01 | Spielora Gaming AG | Business Analyst Prozesse | Zürich | netzwerk-suche | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-02 | Spielora Gaming AG | UX Designer Daten | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-02 | Spielora Gaming AG | UX Designer (80–100 %) | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-03 | Spielora Gaming AG | Product Owner Mobile App B2B | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-03 | Spielora Gaming AG | Product Owner Self-Service B2B | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-03 | Spielora Gaming AG | Solution Architect Daten | Zürich | netzwerk-suche | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-03 | Spielora Gaming AG | Requirements Engineer Plattform-Services | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-04 | Spielora Gaming AG | Data Engineer (80–100 %) | Zürich | netzwerk-empfehlung | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-04 | Spielora Gaming AG | Solution Architect Prozesse | Zürich | netzwerk-suche | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-08 | Spielora Gaming AG | Junior Product Owner | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-08 | Spielora Gaming AG | Business Analyst B2B | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-10 | Spielora Gaming AG | UX Designer Prozesse | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-10 | Spielora Gaming AG | Business Analyst Kundenerlebnis | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-11 | Spielora Gaming AG | Software Engineer Backend Kundenerlebnis | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-14 | Spielora Gaming AG | Scrum Master | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-14 | Spielora Gaming AG | UX Designer Digital Channels | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-15 | Spielora Gaming AG | Product Owner Kundenportal Plattform-Services | Zürich | netzwerk-empfehlung | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-15 | Spielora Gaming AG | UX Designer B2B | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-17 | Spielora Gaming AG | Requirements Engineer B2B | Zürich | netzwerk-suche | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-18 | Spielora Gaming AG | Product Owner Payments B2B | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-19 | Spielora Gaming AG | Data Engineer Kundenerlebnis | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-21 | Spielora Gaming AG | Business Analyst Daten | Zürich | netzwerk-suche | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-22 | Spielora Gaming AG | Software Engineer Backend Digital Channels | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-23 | Spielora Gaming AG | Projektleiter Digitalisierung B2B | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-23 | Spielora Gaming AG | Software Engineer Backend Prozesse | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-24 | Spielora Gaming AG | Projektleiter Digitalisierung (80–100 %) | Zürich | netzwerk-suche | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-24 | Spielora Gaming AG | Requirements Engineer Daten | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-24 | Spielora Gaming AG | Product Owner Mobile App (80–100 %) | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-25 | Spielora Gaming AG | Business Analyst Digital Channels | Zürich | portal | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |
| 2025-04-25 | Spielora Gaming AG | Scrum Master Kundenerlebnis | Zürich | netzwerk-suche | Firmen-Ausschluss (Persona: keine Glücksspielbranche) |

### Distanz (40)

| Datum | Firma | Rolle | Ort | Kanal | Grund |
|---|---|---|---|---|---|
| 2025-03-03 | Amberlin Versicherung AG | Senior Product Manager Daten | Lausanne | netzwerk-suche | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-03-03 | Veltrima Gesundheitsdienste AG | Product Owner Self-Service | St. Gallen | portal | Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min. |
| 2025-03-04 | Amberlin Versicherung AG | Senior Product Owner | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-03-05 | Amberlin Versicherung AG | Product Owner Kundenportal Digital Channels | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-03-06 | Veltrima Gesundheitsdienste AG | Senior Product Manager | St. Gallen | netzwerk-suche | Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min. |
| 2025-03-07 | Amberlin Versicherung AG | Senior Product Manager | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-03-11 | Amberlin Versicherung AG | Product Owner Self-Service B2B | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-03-13 | Amberlin Versicherung AG | Product Owner Self-Service Plattform-Services | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-03-13 | Veltrima Gesundheitsdienste AG | Product Manager Data Platform Digital Channels | St. Gallen | netzwerk-suche | Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min. |
| 2025-03-18 | Amberlin Versicherung AG | Lead Product Owner Plattform Kundenerlebnis | Lausanne | netzwerk-suche | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-03-20 | Veltrima Gesundheitsdienste AG | Product Manager Data Platform Prozesse | St. Gallen | netzwerk-suche | Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min. |
| 2025-03-21 | Veltrima Gesundheitsdienste AG | Senior Product Owner | St. Gallen | netzwerk-suche | Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min. |
| 2025-03-24 | Amberlin Versicherung AG | Product Manager KI-Anwendungen Digital Channels | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-03-27 | Veltrima Gesundheitsdienste AG | Product Owner Mobile App B2B | St. Gallen | portal | Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min. |
| 2025-03-28 | Amberlin Versicherung AG | Lead Product Owner Plattform | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-03-31 | Amberlin Versicherung AG | Product Owner Mobile App | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-03-31 | Veltrima Gesundheitsdienste AG | Product Owner Mobile App | St. Gallen | netzwerk-suche | Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min. |
| 2025-04-02 | Amberlin Versicherung AG | Product Manager Data Platform | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-04-04 | Amberlin Versicherung AG | Product Owner Mobile App B2B | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-04-04 | Amberlin Versicherung AG | Product Owner Mobile App Digital Channels | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-04-04 | Amberlin Versicherung AG | Product Owner Self-Service Daten | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-04-05 | Amberlin Versicherung AG | Product Owner Self-Service Prozesse | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-04-05 | Veltrima Gesundheitsdienste AG | Senior Product Manager B2B | St. Gallen | netzwerk-empfehlung | Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min. |
| 2025-04-07 | Amberlin Versicherung AG | Product Owner Kundenportal B2B | Lausanne | netzwerk-suche | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-04-07 | Veltrima Gesundheitsdienste AG | Product Owner Kundenportal | St. Gallen | portal | Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min. |
| 2025-04-08 | Amberlin Versicherung AG | Product Owner Self-Service Digital Channels | Lausanne | netzwerk-suche | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-04-08 | Veltrima Gesundheitsdienste AG | Product Owner Kundenportal Kundenerlebnis | St. Gallen | netzwerk-empfehlung | Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min. |
| 2025-04-09 | Amberlin Versicherung AG | Lead Product Owner Plattform Daten | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-04-09 | Veltrima Gesundheitsdienste AG | Product Owner Self-Service (80–100 %) | St. Gallen | portal | Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min. |
| 2025-04-11 | Amberlin Versicherung AG | Senior Product Manager Digital Channels | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-04-14 | Amberlin Versicherung AG | Senior Product Manager B2B | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-04-16 | Amberlin Versicherung AG | Product Owner Mobile App Daten | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-04-17 | Veltrima Gesundheitsdienste AG | Senior Product Owner Digital Channels | St. Gallen | netzwerk-suche | Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min. |
| 2025-04-18 | Veltrima Gesundheitsdienste AG | Lead Product Owner Plattform B2B | St. Gallen | portal | Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min. |
| 2025-04-18 | Veltrima Gesundheitsdienste AG | Product Owner Mobile App Plattform-Services | St. Gallen | netzwerk-suche | Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min. |
| 2025-04-18 | Veltrima Gesundheitsdienste AG | Product Manager KI-Anwendungen B2B | St. Gallen | portal | Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min. |
| 2025-04-18 | Veltrima Gesundheitsdienste AG | Product Owner Kundenportal Digital Channels | St. Gallen | portal | Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min. |
| 2025-04-23 | Amberlin Versicherung AG | Product Manager Data Platform Prozesse | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |
| 2025-04-23 | Veltrima Gesundheitsdienste AG | Product Owner Self-Service Plattform-Services | St. Gallen | portal | Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min. |
| 2025-04-25 | Amberlin Versicherung AG | Senior Product Manager (80–100 %) | Lausanne | portal | Ausschluss 2 (Distanz): Lausanne, Pendelzeit 130 Min. |

