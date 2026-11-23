# MARKTREPORT — was das Screening über den Markt sagt

**Generiert:** 2025-04-25 · `python3 scripts/marktreport.py` · **nicht von Hand editieren**
**Datenbasis:** 2276 gesichtete Anzeigen aus 2546 Abfrage-Läufen, 357 bewertete Fälle in der Pipeline.

Dieser Report beantwortet drei Fragen: **Warum kommen Stellen nicht in Frage? Welcher Kanal liefert? Was folgt daraus für Suche und Dossier?**

## 1 — Der Trichter

| Stufe | Anzahl | Anteil |
|---|---:|---:|
| Gesichtet (Listenebene) | 2276 | 100% |
| Volltext geprüft | 357 | 15% |
| Als Kandidat vorgelegt | 62 | 2% |
| Beworben (Versand erfolgt) | 32 | — |
| Einladung zum Gespräch | 12 | 37% der Bewerbungen |
| Absagen (davon ohne Gespräch) | 14 (9) | — |
| Angebote | 0 | — |

**Harte Zahl:** 32 Bewerbungen, 12 Einladungen, 9 Absagen schon nach der Dossierprüfung. Die Einladungsquote ist der eigentliche Engpass, nicht die Zahl der gefundenen Stellen. Ob das Raster sie vorhersagt: `python3 scripts/analyse_fit_v2.py`.

## 2 — Warum Stellen nicht in Frage kommen

### 2a Auf Listenebene (Vorfilter, ohne Volltext)

- **564×** Kein Produktmandat / falscher Rollentyp
- **417×** Engineering-/Entwicklerrolle
- **267×** Dublette (anderer Kanal)
- **159×** Physisches Produktmanagement
- **130×** Vermittler / Aggregator
- **128×** Junior / zu tiefes Level
- **123×** Beratung / Agentur
- **61×** Firmen-Ausschluss der Persona
- **40×** Distanz / Pendelzeit
- **28×** Anzeige nicht mehr verfügbar

### 2b Nach Volltextprüfung (die inhaltlich naheliegenden Fälle)

- **61×** Kein Homeoffice / Präsenzpflicht
  - Kantonale Verwaltung Altmark (Senior Product Owner (80–100 %)) · Telvaro Kommunikation AG (Product Owner Mobile App Digital Channels) · Cirrova Cloud AG (Product Owner Self-Service Plattform-Services) · Sanuvia Health AG (Senior Product Manager)
- **60×** Rückschritt / zu kleines Mandat
  - Telvaro Kommunikation AG (Senior Product Manager Digital Channels) · Trellin Immobilien AG (Product Manager Data Platform (80–100 %)) · Varella Energie AG (Product Owner Mobile App B2B) · Lernovi Bildung AG (Product Manager Data Platform)
- **60×** Führungsanforderung
  - Sanuvia Health AG (Product Owner Kundenportal) · Mirvel Medien AG (Product Owner Kundenportal) · Orvana Reisen AG (Product Owner Mobile App) · Sorvik Logistik AG (Product Owner Mobile App B2B)
- **57×** Formale Zugangsvoraussetzung
  - Brivana Privatbank AG (Senior Product Owner Kundenerlebnis) · Cirrova Cloud AG (Head of Product) · Fendrix Analytics AG (Product Manager Data Platform) · Telvaro Kommunikation AG (Product Owner Kundenportal)
- **57×** Kompetenzdistanz (Chance tief)
  - Brivana Privatbank AG (Senior Product Owner Kundenerlebnis) · Cirrova Cloud AG (Head of Product) · Fendrix Analytics AG (Product Manager Data Platform) · Telvaro Kommunikation AG (Product Owner Kundenportal)
- **51×** Kein Produktmandat / falscher Rollentyp
  - Telvaro Kommunikation AG (Senior Product Manager Digital Channels) · Trellin Immobilien AG (Product Manager Data Platform (80–100 %)) · Lernovi Bildung AG (Product Manager Data Platform) · Vendaro Retail AG (Product Manager Data Platform)
- **47×** Rollen-Präferenz der Persona
  - Telvaro Kommunikation AG (Product Owner Self-Service Kundenerlebnis) · Sanuvia Health AG (Product Owner Self-Service) · Sanuvia Health AG (Product Manager Data Platform) · Brivana Privatbank AG (Product Manager Data Platform Prozesse)
- **24×** Entscheid Alex
  - Varella Energie AG (Product Owner Mobile App B2B) · Orvana Reisen AG (Head of Product Kundenerlebnis) · Telvaro Kommunikation AG (Product Owner Kundenportal Kundenerlebnis) · Kalvit Software AG (Product Owner Mobile App Plattform-Services)
- **10×** Benannter Fähigkeits-Ausschluss (Payment)
  - Sorvik Logistik AG (Product Owner Payments) · Telvaro Kommunikation AG (Product Owner Payments) · Lernovi Bildung AG (Product Owner Payments B2B) · Mirvel Medien AG (Product Owner Payments (80–100 %))
- **10×** Distanz / Pendelzeit
  - Telvaro Kommunikation AG (Product Owner Kundenportal Kundenerlebnis) · Vendaro Retail AG (Lead Product Owner Plattform Plattform-Servic) · Quendor Versicherungen AG (Digital Product Lead Prozesse) · Kalvit Software AG (Lead Product Owner Plattform Kundenerlebnis)
- **9×** Fachwissen in fremder Domäne
  - Quelvia Pharma AG (Senior Product Manager Prozesse) · Ristra Finanztechnik AG (Digital Product Lead Prozesse) · Ristra Finanztechnik AG (Lead Product Owner Plattform) · Brivana Privatbank AG (Senior Product Manager (80–100 %))

**Befund:** Der häufigste Grund, warum eine inhaltlich passende Stelle ausfällt, ist **Kein Homeoffice / Präsenzpflicht** (61 Fälle).
An zweiter Stelle: Rückschritt / zu kleines Mandat (60).
## 3 — Welcher Kanal liefert?

| Kanal | gesichtet | volltextwürdig | Kandidaten |
|---|---:|---:|---:|
| portal | 1608 | 226 | 37 |
| netzwerk-suche | 545 | 87 | 13 |
| netzwerk-empfehlung | 62 | 14 | 4 |
| zielportal | 35 | 24 | 8 |
| behoerdenportal | 26 | 6 | 0 |

**Ertragreichster Kanal bisher:** portal mit 37 Kandidaten.

### Welcher Suchbegriff liefert?

| Begriff / Portal | gesichtet | volltextwürdig | Kandidaten |
|---|---:|---:|---:|
| Jobportal: «Product Lead», 24 h | 154 | 18 | 4 |
| Jobportal: «Produktverantwortung», 24 h | 151 | 22 | 2 |
| Jobportal: «Senior Product Owner», 24 h | 143 | 17 | 4 |
| Jobportal: «Lead Product Owner», 7 Tage | 142 | 15 | 3 |
| Jobportal: «KI» UND «Produkt», 24 h | 136 | 22 | 3 |
| Jobportal: «Plattform» UND «Owner», 24 h | 135 | 13 | 2 |
| Jobportal: «Digital Product», 24 h | 133 | 20 | 2 |
| Jobportal: «AI Product Manager», 24 h | 131 | 22 | 6 |
| Jobportal: «Product Owner», 24 h, Region Zürich | 126 | 25 | 2 |
| Jobportal: «Product Manager», 24 h | 120 | 19 | 3 |
| Netzwerk-Suche: Product Owner, Zürich, letzte 24 h | 120 | 17 | 1 |
| Jobportal: «Head of Product», 7 Tage | 116 | 16 | 4 |
| Netzwerk-Suche: Head of Product, Zürich, letzte Woche | 110 | 20 | 4 |
| Netzwerk-Suche: Product Owner, Bern, letzte 24 h | 103 | 16 | 1 |
| Jobportal: «Data Product», 24 h | 98 | 14 | 2 |
| Netzwerk-Suche: Product Manager, Bern, letzte 24 h | 96 | 19 | 4 |
| Netzwerk-Suche: Product Manager, Zürich, letzte 24 h | 93 | 13 | 3 |
| Netzwerk: Empfehlungen «Für dich» | 62 | 14 | 4 |
| Jobportal: «Projektleiter Digital», 24 h | 23 | 3 | 0 |
| Netzwerk-Suche: Product Owner, Ostschweiz | 23 | 2 | 0 |
| Stellenportal Kantonale Verwaltung Altmark | 16 | 5 | 0 |
| Stellenportal Stadtverwaltung Nordtal | 10 | 1 | 0 |
| Karriereseite Kalvit Software AG | 8 | 4 | 2 |
| Karriereseite Brivana Privatbank AG | 7 | 6 | 2 |
| Karriereseite Quendor Versicherungen AG | 5 | 2 | 0 |
| Karriereseite Varella Energie AG | 4 | 2 | 0 |
| Karriereseite Vendaro Retail AG | 4 | 4 | 2 |
| Karriereseite Sanuvia Health AG | 4 | 4 | 1 |
| Karriereseite Pelvio Mobility AG | 3 | 2 | 1 |

## 4 — Was der Markt in diesem Zeitraum überhaupt anbot

- **30 verschiedene Arbeitgeber** in den gesichteten Anzeigen.
- Mehrfach vertreten: Fendrix Analytics AG (102) · Kalvit Software AG (101) · Vendaro Retail AG (101) · Brivana Privatbank AG (95) · Sanuvia Health AG (93) · Lernovi Bildung AG (89) · Cirrova Cloud AG (83) · Quendor Versicherungen AG (83) · Trellin Immobilien AG (82) · Veltrima Gesundheitsdienste AG (82) · Sorvik Logistik AG (82) · Ristra Finanztechnik AG (81)
- Häufigste Arbeitsorte: Zürich (883) · Zug (240) · Baden (181) · Aarau (159) · Luzern (149) · Winterthur (108) · Schlieren (83) · St. Gallen (82)

## 5 — Lehren und konkrete Anpassungen

*Automatisch abgeleitet aus den Zahlen oben. Vorschläge gehen an Alex, nicht eigenmächtig ins Regelwerk.*

- **Vorfilter:** 130 Vermittler-Inserate. Bei jedem mit anonymisiertem Kunden prüfen, ob dieselbe Stelle auch direkt ausgeschrieben ist — die Direktbewerbung schlägt den Umweg.
- **Vorfilter schärfen:** 51× wurde erst im Volltext klar, dass die Rolle kein Produktmandat trägt. Die Aufgabenbegriffe (Roadmap, Backlog, Priorisierung, Produktvision) als VOLLTEXTSUCHE einsetzen statt nur als Bewertungskriterium — fehlen sie in der Anzeige, ist der Fall meist schon entschieden.
- **Dossier:** 60× an einer Führungsanforderung gescheitert. Entweder laterale Führung im CV deutlich sichtbarer machen — oder Rollen mit «Führung von Führungskräften» als Muss konsequent vorfiltern, statt Volltext zu lesen.
- **Vorfilter:** 61× stand die Präsenzpflicht erst im Volltext. Wo die Trefferliste die Arbeitsform zeigt, schon dort filtern.
- **Zielportale:** 8 Kandidaten kamen über Karriereseiten von Zielfirmen. Ob sie nur dort standen, zeigt `python3 scripts/kanal_auswertung.py` (Spalte «nur hier»); wenn ja, ist die Portalprüfung eine eigenständige Quelle und kein Zusatz.

## 6 — Die Grenze dieses Reports, ausdrücklich

Dieser Report misst, **was der Coach aussortiert** — nicht, **was der Markt über Alex denkt**. Die einzige echte Rückmeldung des Marktes sind Einladungen und Absagen; ihre Zahl ist klein. Alles unter Punkt 5 ist deshalb eine Hypothese über die Suche, keine Aussage über die Bewerbungschancen.

Was den Report belastbarer macht: Absagegründe erfassen, wo sie genannt werden, und den Zeitpunkt der Absage (Dossierprüfung vs. nach dem Gespräch, Feld `stadium`). Erst dann lässt sich trennen, ob Dossiers am Filter oder am Gespräch scheitern.

