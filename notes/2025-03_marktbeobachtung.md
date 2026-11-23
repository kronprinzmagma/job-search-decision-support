# Marktbeobachtung 2025-03

**Zeitraum:** 2025-03-01 bis 2025-03-31 · **Anzeigen kodiert:** 153 · Regelwerk `spec/MARKT.md` · erzeugt mit
`python3 scripts/marktcheck.py` (Stichwort-Variante der Demo; im Betrieb kodiert das Modell mit Zweitkodierung)

Lesereihenfolge für Alex: zuerst «Was folgt daraus», dann die Blöcke. Jede Zahl steht mit ihrer Fallzahl.

## Was folgt daraus (Vorschläge, Entscheid bei Alex)

- **Change und Enablement** (Beleg schärfen; verlangt in 21 von 153 Anzeigen, davon 0 nur als Wunsch): Einführung im Pilotprojekt (wer wurde befähigt, mit welchem Ergebnis) als Beleg ergänzen
- **Technische Tiefe und Hands-on** (Lücke mit Gewicht; verlangt in 20 von 153 Anzeigen, davon 0 nur als Wunsch): Nicht schliessen, sondern ehrlich positionieren: Produktrolle mit technischem Verständnis; Rollen mit Muss-Handarbeit meiden
- **Daten- und Governance-Kompetenz** (Beleg schärfen; verlangt in 17 von 153 Anzeigen, davon 0 nur als Wunsch): Datenschutz-Erfahrung als KI-Governance-Beleg formulieren (Richtlinie, Prüfprozess, Ergebnis)
- **Prompt- und Agenten-Praxis** (Lücke mit Gewicht; verlangt in 17 von 153 Anzeigen, davon 4 nur als Wunsch): Ein Agenten- oder Prompt-Projekt mit messbarem Ergebnis umsetzen und öffentlich dokumentieren
- **Evaluation und Qualitätsmessung** (Beleg schärfen; verlangt in 16 von 153 Anzeigen, davon 1 nur als Wunsch): Kleines Evaluationsset mit Testfällen und Metriken für ein eigenes KI-Projekt bauen und dokumentieren
- **Regulierung und Risiko** (Beleg schärfen; verlangt in 16 von 153 Anzeigen, davon 0 nur als Wunsch): Weiterbildung zur KI-Regulierung mit Anwendung auf einen eigenen Fall
- Vor jeder Massnahme die Nullmessung festhalten (spec/MARKT.md). Entscheid bei Alex.

## A – Nachfrage: welche KI-Fähigkeiten die Anzeigen verlangen

Gezählt wird je Anzeige, ob eine Kategorie vorkommt (Mehrfachnennung möglich). Kodiert sind nur Aufgaben
und Anforderungen, nicht der Firmenteil. «Nur Wunsch»: ausschliesslich als «von Vorteil» o. ä. verlangt.

| Kategorie | Anzeigen | Anteil | 95 %-Wilson | davon nur Wunsch | Vormonat | Beispiele |
|---|---:|---:|---|---:|---:|---|
| KI-Anwendungsfälle priorisieren (K01) | 20 | 13 % | 9–19 % | 0 | – | `trellin-immobilien-product-manager-data-platform`, `lernovi-bildung-product-manager-data-platform` |
| LLM-Produkte betreiben (K02) | 13 | 8 % | 5–14 % | 0 | – | `telvaro-kommunikation-product-owner-mobile-app`, `sanuvia-health-senior-product-manager` |
| Evaluation und Qualitätsmessung (K03) | 16 | 10 % | 7–16 % | 1 | – | `brivana-privatbank-senior-product-owner-kundenerlebnis`, `mirvel-medien-product-owner-kundenportal` |
| Daten- und Governance-Kompetenz (K04) | 17 | 11 % | 7–17 % | 0 | – | `brivana-privatbank-product-owner-self-service`, `sanuvia-health-product-manager-data-platform` |
| Prompt- und Agenten-Praxis (K05) | 17 | 11 % | 7–17 % | 4 | – | `fendrix-analytics-product-manager-data-platform`, `ristra-finanztechnik-product-manager-data-platform` |
| Change und Enablement (K06) | 21 | 14 % | 9–20 % | 0 | – | `trellin-immobilien-product-manager-data-platform`, `fendrix-analytics-product-manager-data-platform` |
| Regulierung und Risiko (K07) | 16 | 10 % | 7–16 % | 0 | – | `telvaro-kommunikation-senior-product-manager-digital`, `ristra-finanztechnik-product-manager-data-platform` |
| Technische Tiefe und Hands-on (K08) | 20 | 13 % | 9–19 % | 0 | – | `cirrova-cloud-head-of-product`, `trellin-immobilien-product-manager-data-platform` |
| Allgemeines KI-Verständnis (K09) | 21 | 14 % | 9–20 % | 0 | – | `sorvik-logistik-product-owner-payments`, `sanuvia-health-product-owner-kundenportal` |
| Keine KI-Anforderung (K00) | 52 | 34 % | 27–42 % | 0 | – | `kantonale-verwaltung-altmark-senior-product-owner-80100`, `cirrova-cloud-product-owner-self-service` |

- **Anzeigen mit KI-Anforderung:** 101 von 153 (mindestens eine Kategorie K01–K09).
- **KI erwähnt, keiner Kategorie zugeordnet:** 0 (im Betrieb: Code «NEU» prüfen).
- Wilson-Intervalle sind eine Untergrenze der Unsicherheit, nicht ihr Mass: Die Anzeigen stammen aus den eigenen Suchbegriffen und Kanälen, nicht aus einer Zufallsstichprobe.

## B – Besetzung: wer die Stellen bekommt, die Alex wollte (pseudonymisiert)

Nur öffentlich sichtbare, rollenrelevante Merkmale, nur aggregiert. Gruppen und Zellen unter 5 Fällen werden
nicht ausgewiesen; ein Median erst ab 10 Fällen.

Stellen mit Absage: 14 · Besetzung gefunden (erhoben bis 2025-03-31): unter 5 · ohne Fund (offen oder nicht auffindbar, nicht geraten): 14.

Zu wenig Fälle für eine Auswertung: berichtet wird erst ab 5 gefundenen Besetzungen.

## C – Position: Nachfrage gegen Alex' Beleglage

Beleglage aus `persona/PROFILE.md` (Zusammenfassung in `persona/belege.json`). «Lücke mit Gewicht» heisst:
nicht belegt und in mindestens 10 % der Anzeigen verlangt.

| Kategorie | Nachfrage | Beleglage Alex | Einordnung |
|---|---:|---|---|
| KI-Anwendungsfälle priorisieren (K01) | 20 von 153 | belegt: KI-Pilotprojekte von der Anbieter-Evaluation bis zum Betrieb | trägt |
| LLM-Produkte betreiben (K02) | 13 von 153 | teilweise: Pilotprojekte bis zum Betrieb; kein skaliertes KI-Produkt im Dauerbetrieb belegt | beobachten |
| Evaluation und Qualitätsmessung (K03) | 16 von 153 | teilweise: Anbieter-Evaluation belegt; systematische Qualitätsmessung von KI-Ergebnissen nicht | Beleg schärfen |
| Daten- und Governance-Kompetenz (K04) | 17 von 153 | teilweise: Datenschutz im Produktalltag belegt; Daten-Governance für KI nicht | Beleg schärfen |
| Prompt- und Agenten-Praxis (K05) | 17 von 153 | Lücke: in PROFILE.md nicht belegt | Lücke mit Gewicht |
| Change und Enablement (K06) | 21 von 153 | teilweise: Führung interdisziplinärer Teams; Befähigung zu KI nicht ausdrücklich belegt | Beleg schärfen |
| Regulierung und Risiko (K07) | 16 von 153 | teilweise: regulierte Umfelder (Gesundheit, Versicherung); KI-Regulierung nicht belegt | Beleg schärfen |
| Technische Tiefe und Hands-on (K08) | 20 von 153 | Lücke: kein Hochschulabschluss in Informatik; keine eigene Technikarbeit belegt | Lücke mit Gewicht |
| Allgemeines KI-Verständnis (K09) | 21 von 153 | belegt: Produktrollen mit KI-Anteil, KI-Pilotprojekte | trägt |

## D – Eigenanalyse: die eigenen Fälle im Zeitraum

Vollerhebung, keine Stichprobe. Vertiefung: `scripts/marktreport.py` (Trichter, Ausschlussgründe),
`scripts/marktbild.py` (Vorfilter und Volltext je Grund), `scripts/kanal_auswertung.py` (Kanäle),
`scripts/analyse_fit_v2.py` (sagt das Raster Einladungen voraus?).

| Stufe | Anzahl |
|---|---:|
| Fälle im Zeitraum (Volltext bewertet) | 153 |
| aussortiert | 137 |
| Entscheid offen (vorgelegt, draft) | 0 |
| beworben | 16 |
| Einladung zum Gespräch | 8 |
| Absage (davon ohne Gespräch) | 13 (8) |
| Angebot | 0 |

Häufigste Ausschlussgründe im Volltext: Kein Homeoffice / Präsenzpflicht 31 · Führungsanforderung 25 · Formale Zugangsvoraussetzung 24.
Kohorte = Fälle mit Datum im Zeitraum; Ergebnisse fliessen nach. Nur abgeschlossene Kohorten vergleichen.

## Was die Zahlen nicht hergeben

- **Erreichbarer Markt, nicht der Markt:** gemessen wird, was die eigenen Suchbegriffe und Kanäle finden.
- **Stichwort statt Urteil:** Die Demo-Kodierung erkennt weder Wissen gegen Tätigkeit noch Umschreibungen
  ohne Stichwort. Belastbar ist erst die Modellkodierung mit gemessener Zweitkodierung.
- **Besetzungen erklären keine Absage:** Sie zeigen, welches Profil genommen wurde, nicht welches Kriterium
  den Ausschlag gab. Interne Besetzungen und nicht gepflegte Profile fehlen.
- **Ein Monat ist eine Momentaufnahme:** Veränderungen erst gegen die Nullmessung und über mehrere Monate lesen.
