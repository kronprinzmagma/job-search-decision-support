# Prozess-Retro Screening — 2025-04-20 (Zeitraum 2025-04-13 bis 2025-04-19)

Misst die Qualität des Prozesses, nicht den Ertrag der Suche (der steht im Wochen-Review). Quelle: data/lauf_audit.json, data/screening_log.json, notes/, feedback/.

## Kennzahlen

| Kennzahl | diese Woche | Vorwoche | Ziel |
|---|---|---|---|
| Sweeps gestartet / Soll (nur Info) | 16 / 16 | 16 / 16 | — |
| Sweeps abgeschlossen | 15 | 16 | 16 |
| Sweeps abgebrochen | 1 | 0 | 0 |
| Sweeps ohne «ende» | 0 | 0 | 0 |
| Sweeps mit doppelt geloggten Abfragen | 0 | 0 | 0 |
| Abdeckung Mittel / Minimum | 97 % / 56 % | 100 % / 100 % | 100 % |
| Sessions je Sweep (Mittel) | 1 | 1 | ≤ 3 |
| Dauer je Sweep (Mittel / Median, min) | 31.875 / 29.0 | 31 / 29.5 | — |
| Abfragen nicht erreichbar | 5 | 6 | 0 |
| Abfragen teilweise / übersprungen | 3 / 0 | 7 / 0 | — / 0 |
| Berichtsform vollständig | 100 % (16 Notizen) | 100 % | 100 % |
| Sichtungen / Kandidaten | 325 / 10 | 302 / 8 | — |
| Kandidaten je Sweep | 0.625 | 0.5 | — |
| Abfragen nur mit Rauschen, 14 Tage (ohne Ziel-/Behördenportale) | 0 | 0 | — |
| Sammelposten | 0 | 0 | wenige |
| Feedback-Dateien mit Formbruch/Rezidiv | 0 | — | 0 |

Nicht erreichbar: ns-zh-a 1x; ns-zh-b 1x; zp-sanuvia 1x; zp-varella 1x; zp-vendaro 1x

## Fundgeschwindigkeit — wie alt war eine Anzeige, als wir sie fanden?

Zentrale Grösse für «schneller sein». Alter beim Fund = erste Sichtung minus Veröffentlichung. Über eine Woche alt = meist schwerer zu erreichen.

| Kennzahl | diese Woche | Vorwoche | Ziel |
|---|---|---|---|
| Relevante Fälle (Kandidat, Volltext, offen) mit Datum | 67 von 67 | 50 von 50 | alle |
| **Alter beim Fund, Median** | **0 Tage** | 0 Tage | ≤ 1 Tag |
| davon 0–1 Tag / 2–7 Tage / über 7 Tage | 63 / 4 / 0 | 46 / 4 / 0 | — |
| Über 7 Tage, obwohl die Abfrage schon lief (verpasst) | 0 | 0 | 0 |
| Sichtungen mit Publiziert-Datum im Log | 287 von 325 | 274 von 302 | möglichst alle |
| Alle Sichtungen: Alter beim Fund, Median | 0 Tage | 0 Tage | — |
| Go bis Versand, Median (Versand in der Woche, n) | 4 Tage (6) | 3 Tage (3) | — |

Je Kanal (Sichtungen mit Datum, Median Alter): behoerdenportal 2× 3 Tage; netzwerk-empfehlung 7× 0 Tage; netzwerk-suche 61× 0 Tage; portal 213× 0 Tage; zielportal 4× 4 Tage

## Die drei grössten Abweichungen

1. **Sweeps nicht abgeschlossen** — 1 gestartete Sweeps blieben offen oder abgebrochen (1 abgebrochen).
2. **Abdeckung unter Soll** — Mittlere Abdeckung 97 % (Minimum 56 %). Am häufigsten fehlend: ne-empfehlungen (1x), ns-be-a (1x), ns-be-b (1x), ns-zh-a (1x), ns-zh-b (1x).

## Vorschläge (Entscheid bei Alex)

- **Sweeps nicht abgeschlossen** → Abbruchgründe in den Sweep-Notizen lesen; wenn Zeitbudget: Fortsetzungs-Sessions prüfen; wenn Werkzeug: Falle in den Katalog-Hinweis schreiben. *(Zieldatei: notes/, data/screening_kanaele.json)*
- **Abdeckung unter Soll** → Wenn dieselben IDs fehlen: Reihenfolge im Katalog ändern (früh im Sweep) oder den Eintrag prüfen (URL, Werkzeugfalle). Wenn breit verteilt: zusätzliche Fortsetzungs-Session im Zeitplan. *(Zieldatei: data/screening_kanaele.json / Zeitplan)*

## Wirkungskontrolle früherer Massnahmen

Je angenommene oder umgesetzte Massnahme: Metrik beim Vorschlag gegen diese Woche.

| Massnahme | Entscheid | Metrik | damals | jetzt | Wirkung |
|---|---|---|---|---|---|
| 2025-03-16 Zwei Sessions am selben Sweep, 9 Abfragen doppelt geloggt | umgesetzt | sweeps_doppelt | 1 | 0 | **gewirkt** — Sperrmuster wie pipeline_tx |
| 2025-03-23 Zwei Abfragen liefern seit zwei Wochen nur Rauschen | umgesetzt | abfragen_ohne_kandidat_14d | 2 | 0 | **gewirkt** — aktiv:false mit Datum und Grund |
| 2025-04-06 Ein Sweep liest rund 280 KB Regelwerk und faehrt das Jobportal im Browser | umgesetzt | dauer_min_median | 54 | 29.0 | **gewirkt** — Wirkungskontrolle: scripts/umbau_kontrolle.py |

Massnahmen seit Beginn der Vorwoche (2025-04-06): 2025-04-06-vorscan **gewirkt**.

Noch unentschieden aus früheren Retros: 2025-03-16-sweeps-nicht-abgeschlossen, 2025-03-16-abdeckung-unter-soll, 2025-03-23-stellen-zu-spaet-gefunden-verpasst, 2025-03-23-portale-wiederholt-nicht-erreichbar, 2025-03-30-stellen-zu-spaet-gefunden-verpasst, 2025-03-30-portale-wiederholt-nicht-erreichbar, 2025-03-30-sweeps-nicht-abgeschlossen

## Kanal-Auswertung (2025-03-23 bis 2025-04-19, 28 Tage)

Gleiche Stelle = gleiche Firma + Rolle (normalisiert). «Nur hier» = in keinem anderen Kanal gesehen. «Zuerst hier» = bei Stellen in mehreren Kanälen hier zuerst gesichtet; Vorsprung = Median in Stunden zum nächsten Kanal.

| Kanal | Stellen | Kandidaten | nur hier | davon Kandidaten | zuerst hier | Vorsprung (h) |
|---|---|---|---|---|---|---|
| portal | 786 | 26 | 656 | 21 | 51 | 24 |
| netzwerk-suche | 257 | 6 | 149 | 3 | 60 | 24 |
| netzwerk-empfehlung | 35 | 1 | 23 | 0 | 8 | 18 |
| zielportal | 21 | 4 | 14 | 2 | 6 | 25 |
| behoerdenportal | 13 | 0 | 8 | 0 | 5 | 3 |

Zuerst publiziert (nur Stellen mit Publikationsdatum in mindestens zwei Kanälen, n = 28): portal 17, netzwerk-suche 8, zielportal 2, netzwerk-empfehlung 1

### Karriere- und Behördenportale einzeln

| Portal | Stellen | Kandidaten | Kandidaten nur hier | zuerst hier |
|---|---|---|---|---|
| Karriereseite Kalvit Software AG | 5 | 1 | 1 | 1 |
| Karriereseite Brivana Privatbank AG | 4 | 1 | 0 | 1 |
| Karriereseite Sanuvia Health AG | 3 | 1 | 0 | 2 |
| Karriereseite Vendaro Retail AG | 3 | 1 | 1 | 1 |
| Stellenportal Kantonale Verwaltung Altmark | 8 | 0 | 0 | 3 |
| Stellenportal Stadtverwaltung Nordtal | 5 | 0 | 0 | 2 |
| Karriereseite Varella Energie AG | 3 | 0 | 0 | 0 |
| Karriereseite Quendor Versicherungen AG | 2 | 0 | 0 | 1 |
| Karriereseite Pelvio Mobility AG | 1 | 0 | 0 | 0 |

Lesart: Ein Portal ohne Kandidaten «nur hier» und ohne «zuerst hier» liefert nichts, was Jobportal oder Netzwerk nicht auch zeigen — Kandidat zum Streichen im Wochen-Review (Entscheid bei Alex).

## Bei dir liegt

- Sweeps nicht abgeschlossen: **annehmen** (Umsetzung wie vorgeschlagen) / **ablehnen** (bleibt so, Grund vermerken) / **anders** (dein Vorschlag)
- Abdeckung unter Soll: **annehmen** (Umsetzung wie vorgeschlagen) / **ablehnen** (bleibt so, Grund vermerken) / **anders** (dein Vorschlag)

Markieren: `python3 scripts/prozess_retro.py --markiere <id> angenommen|abgelehnt|umgesetzt "Notiz"` — IDs: 2025-04-20-sweeps-nicht-abgeschlossen, 2025-04-20-abdeckung-unter-soll
