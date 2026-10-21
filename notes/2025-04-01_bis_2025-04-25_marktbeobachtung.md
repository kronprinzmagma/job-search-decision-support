# Marktbeobachtung 2025-04-01_bis_2025-04-25

**Zeitraum:** 2025-04-01 bis 2025-04-25 · **Anzeigen kodiert:** 204 · Regelwerk `spec/MARKT.md` · erzeugt mit
`python3 scripts/marktcheck.py` (Stichwort-Variante der Demo; im Betrieb kodiert das Modell mit Zweitkodierung)

Lesereihenfolge für Alex: zuerst «Was folgt daraus», dann die Blöcke. Jede Zahl steht mit ihrer Fallzahl.

## Was folgt daraus (Vorschläge, Entscheid bei Alex)

- **LLM-Produkte betreiben** (Beleg schärfen; verlangt in 35 von 204 Anzeigen, davon 0 nur als Wunsch): Betriebsphase eines Piloten mit Kennzahlen (Nutzung, Kosten, Verbesserungen) als Beleg aufbereiten
- **Evaluation und Qualitätsmessung** (Beleg schärfen; verlangt in 31 von 204 Anzeigen, davon 12 nur als Wunsch): Kleines Evaluationsset mit Testfällen und Metriken für ein eigenes KI-Projekt bauen und dokumentieren
- **Change und Enablement** (Beleg schärfen; verlangt in 27 von 204 Anzeigen, davon 0 nur als Wunsch): Einführung im Pilotprojekt (wer wurde befähigt, mit welchem Ergebnis) als Beleg ergänzen
- **Prompt- und Agenten-Praxis** (Lücke mit Gewicht; verlangt in 23 von 204 Anzeigen, davon 6 nur als Wunsch): Ein Agenten- oder Prompt-Projekt mit messbarem Ergebnis umsetzen und öffentlich dokumentieren
- **Daten- und Governance-Kompetenz** (Beleg schärfen; verlangt in 22 von 204 Anzeigen, davon 0 nur als Wunsch): Datenschutz-Erfahrung als KI-Governance-Beleg formulieren (Richtlinie, Prüfprozess, Ergebnis)
- **Technische Tiefe und Hands-on** (Lücke mit Gewicht; verlangt in 21 von 204 Anzeigen, davon 0 nur als Wunsch): Nicht schliessen, sondern ehrlich positionieren: Produktrolle mit technischem Verständnis; Rollen mit Muss-Handarbeit meiden
- Vor jeder Massnahme die Nullmessung festhalten (spec/MARKT.md). Entscheid bei Alex.

## A – Nachfrage: welche KI-Fähigkeiten die Anzeigen verlangen

Gezählt wird je Anzeige, ob eine Kategorie vorkommt (Mehrfachnennung möglich). Kodiert sind nur Aufgaben
und Anforderungen, nicht der Firmenteil. «Nur Wunsch»: ausschliesslich als «von Vorteil» o. ä. verlangt.

| Kategorie | Anzeigen | Anteil | 95 %-Wilson | davon nur Wunsch | Vormonat | Beispiele |
|---|---:|---:|---|---:|---:|---|
| KI-Anwendungsfälle priorisieren (K01) | 22 | 11 % | 7–16 % | 0 | – | `trellin-immobilien-product-owner-mobile-app`, `pelvio-mobility-product-manager-data-platform-2` |
| LLM-Produkte betreiben (K02) | 35 | 17 % | 13–23 % | 0 | – | `ristra-finanztechnik-senior-product-owner-digital`, `cirrova-cloud-product-owner-mobile-app-2` |
| Evaluation und Qualitätsmessung (K03) | 31 | 15 % | 11–21 % | 12 | – | `kalvit-software-digital-product-lead`, `pelvio-mobility-product-owner-self-service` |
| Daten- und Governance-Kompetenz (K04) | 22 | 11 % | 7–16 % | 0 | – | `trellin-immobilien-product-manager-data-platform-2`, `kantonale-verwaltung-altmark-lead-product-owner-plattform` |
| Prompt- und Agenten-Praxis (K05) | 23 | 11 % | 8–16 % | 6 | – | `trellin-immobilien-product-owner-mobile-app`, `sanuvia-health-senior-product-owner-b2b` |
| Change und Enablement (K06) | 27 | 13 % | 9–19 % | 0 | – | `mirvel-medien-senior-product-owner`, `varella-energie-product-owner-self-service-2` |
| Regulierung und Risiko (K07) | 19 | 9 % | 6–14 % | 0 | – | `pelvio-mobility-product-manager-data-platform-2`, `varella-energie-product-owner-self-service-3` |
| Technische Tiefe und Hands-on (K08) | 21 | 10 % | 7–15 % | 0 | – | `trellin-immobilien-product-manager-data-platform-2`, `mirvel-medien-senior-product-owner` |
| Allgemeines KI-Verständnis (K09) | 27 | 13 % | 9–19 % | 0 | – | `kalvit-software-digital-product-lead`, `quendor-versicherungen-product-owner-kundenportal` |
| Keine KI-Anforderung (K00) | 63 | 31 % | 25–38 % | 0 | – | `varella-energie-head-of-product-b2b`, `cirrova-cloud-lead-product-owner-plattform` |

- **Anzeigen mit KI-Anforderung:** 141 von 204 (mindestens eine Kategorie K01–K09).
- **KI erwähnt, keiner Kategorie zugeordnet:** 0 (im Betrieb: Code «NEU» prüfen).
- Wilson-Intervalle sind eine Untergrenze der Unsicherheit, nicht ihr Mass: Die Anzeigen stammen aus den eigenen Suchbegriffen und Kanälen, nicht aus einer Zufallsstichprobe.

## B – Besetzung: wer die Stellen bekommt, die Alex wollte (pseudonymisiert)

Nur öffentlich sichtbare, rollenrelevante Merkmale, nur aggregiert. Gruppen und Zellen unter 5 Fällen werden
nicht ausgewiesen; ein Median erst ab 10 Fällen.

Stellen mit Absage: 14 · Besetzung gefunden (erhoben bis 2025-04-25): 11 · ohne Fund (offen oder nicht auffindbar, nicht geraten): 3.

| Merkmal | Gruppe (n = 11) | Alex | Abstand |
|---|---|---|---|
| Jahre im Rollentyp | Median 8 · mehr als Alex: 6 | 6 | Alex -2 Jahre gegenüber dem Median |
| Vorherige Stufe | übrige Ausprägungen: 11 | Senior PO/PM | – |
| Abschluss Informatik/Technik | unter 5 | nicht Informatik/Technik | nicht auswertbar (Zelle unter 5) |
| KI-Belege im Profil | 7 | ja | gleichauf |
| Aus der Branche der Stelle | 6 von 11 | 4 von 11 | Lücke: Branchennähe |
| Interner Wechsel | unter 5 | extern | nicht auswertbar (Zelle unter 5) |

- Nach Stadium: Absage nach Gespräch 5, nach Dossier 6.
- Ein gefundenes Profil zeigt, wer genommen wurde, nicht warum. Interne Besetzungen bleiben oft unsichtbar.

## C – Position: Nachfrage gegen Alex' Beleglage

Beleglage aus `persona/PROFILE.md` (Zusammenfassung in `persona/belege.json`). «Lücke mit Gewicht» heisst:
nicht belegt und in mindestens 10 % der Anzeigen verlangt.

| Kategorie | Nachfrage | Beleglage Alex | Einordnung |
|---|---:|---|---|
| KI-Anwendungsfälle priorisieren (K01) | 22 von 204 | belegt: KI-Pilotprojekte von der Anbieter-Evaluation bis zum Betrieb | trägt |
| LLM-Produkte betreiben (K02) | 35 von 204 | teilweise: Pilotprojekte bis zum Betrieb; kein skaliertes KI-Produkt im Dauerbetrieb belegt | Beleg schärfen |
| Evaluation und Qualitätsmessung (K03) | 31 von 204 | teilweise: Anbieter-Evaluation belegt; systematische Qualitätsmessung von KI-Ergebnissen nicht | Beleg schärfen |
| Daten- und Governance-Kompetenz (K04) | 22 von 204 | teilweise: Datenschutz im Produktalltag belegt; Daten-Governance für KI nicht | Beleg schärfen |
| Prompt- und Agenten-Praxis (K05) | 23 von 204 | Lücke: in PROFILE.md nicht belegt | Lücke mit Gewicht |
| Change und Enablement (K06) | 27 von 204 | teilweise: Führung interdisziplinärer Teams; Befähigung zu KI nicht ausdrücklich belegt | Beleg schärfen |
| Regulierung und Risiko (K07) | 19 von 204 | teilweise: regulierte Umfelder (Gesundheit, Versicherung); KI-Regulierung nicht belegt | beobachten |
| Technische Tiefe und Hands-on (K08) | 21 von 204 | Lücke: kein Hochschulabschluss in Informatik; keine eigene Technikarbeit belegt | Lücke mit Gewicht |
| Allgemeines KI-Verständnis (K09) | 27 von 204 | belegt: Produktrollen mit KI-Anteil, KI-Pilotprojekte | trägt |

## D – Eigenanalyse: die eigenen Fälle im Zeitraum

Vollerhebung, keine Stichprobe. Vertiefung: `scripts/marktreport.py` (Trichter, Ausschlussgründe),
`scripts/marktbild.py` (Vorfilter und Volltext je Grund), `scripts/kanal_auswertung.py` (Kanäle),
`scripts/analyse_fit_v2.py` (sagt das Raster Einladungen voraus?).

| Stufe | Anzahl |
|---|---:|
| Fälle im Zeitraum (Volltext bewertet) | 204 |
| aussortiert | 182 |
| Entscheid offen (vorgelegt, draft) | 5 |
| beworben | 16 |
| Einladung zum Gespräch | 4 |
| Absage (davon ohne Gespräch) | 1 (1) |
| Angebot | 0 |

Häufigste Ausschlussgründe im Volltext: Führungsanforderung 35 · Rollen-Präferenz der Persona 34 · Formale Zugangsvoraussetzung 33.
Kohorte = Fälle mit Datum im Zeitraum; Ergebnisse fliessen nach. Nur abgeschlossene Kohorten vergleichen.

## Was die Zahlen nicht hergeben

- **Erreichbarer Markt, nicht der Markt:** gemessen wird, was die eigenen Suchbegriffe und Kanäle finden.
- **Stichwort statt Urteil:** Die Demo-Kodierung erkennt weder Wissen gegen Tätigkeit noch Umschreibungen
  ohne Stichwort. Belastbar ist erst die Modellkodierung mit gemessener Zweitkodierung.
- **Besetzungen erklären keine Absage:** Sie zeigen, welches Profil genommen wurde, nicht welches Kriterium
  den Ausschlag gab. Interne Besetzungen und nicht gepflegte Profile fehlen.
- **Ein Monat ist eine Momentaufnahme:** Veränderungen erst gegen die Nullmessung und über mehrere Monate lesen.
