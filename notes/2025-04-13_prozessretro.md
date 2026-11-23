# Prozess-Retro Screening — 2025-04-13 (Zeitraum 2025-04-06 bis 2025-04-12)

Misst die Qualität des Prozesses, nicht den Ertrag der Suche (der steht im Wochen-Review). Quelle: data/lauf_audit.json, data/screening_log.json, notes/, feedback/.

## Kennzahlen

| Kennzahl | diese Woche | Vorwoche | Ziel |
|---|---|---|---|
| Sweeps gestartet / Soll (nur Info) | 16 / 16 | 16 / 16 | — |
| Sweeps abgeschlossen | 16 | 16 | 16 |
| Sweeps abgebrochen | 0 | 0 | 0 |
| Sweeps ohne «ende» | 0 | 0 | 0 |
| Sweeps mit doppelt geloggten Abfragen | 0 | 0 | 0 |
| Abdeckung Mittel / Minimum | 100 % / 100 % | 100 % / 100 % | 100 % |
| Sessions je Sweep (Mittel) | 1 | 1 | ≤ 3 |
| Dauer je Sweep (Mittel / Median, min) | 31 / 29.5 | 60.25 / 62.0 | — |
| Abfragen nicht erreichbar | 6 | 3 | 0 |
| Abfragen teilweise / übersprungen | 7 / 0 | 6 / 0 | — / 0 |
| Berichtsform vollständig | 100 % (16 Notizen) | 100 % | 100 % |
| Sichtungen / Kandidaten | 302 / 8 | 341 / 9 | — |
| Kandidaten je Sweep | 0.5 | 0.562 | — |
| Abfragen nur mit Rauschen, 14 Tage (ohne Ziel-/Behördenportale) | 0 | 0 | — |
| Sammelposten | 0 | 0 | wenige |
| Feedback-Dateien mit Formbruch/Rezidiv | 0 | — | 0 |

Nicht erreichbar: bp-altmark 1x; ne-empfehlungen 1x; ns-be-a 1x; ns-be-b 1x; ns-zh-a 1x; zp-vendaro 1x

## Fundgeschwindigkeit — wie alt war eine Anzeige, als wir sie fanden?

Zentrale Grösse für «schneller sein». Alter beim Fund = erste Sichtung minus Veröffentlichung. Über eine Woche alt = meist schwerer zu erreichen.

| Kennzahl | diese Woche | Vorwoche | Ziel |
|---|---|---|---|
| Relevante Fälle (Kandidat, Volltext, offen) mit Datum | 50 von 50 | 51 von 51 | alle |
| **Alter beim Fund, Median** | **0 Tage** | 0 Tage | ≤ 1 Tag |
| davon 0–1 Tag / 2–7 Tage / über 7 Tage | 46 / 4 / 0 | 44 / 7 / 0 | — |
| Über 7 Tage, obwohl die Abfrage schon lief (verpasst) | 0 | 0 | 0 |
| Sichtungen mit Publiziert-Datum im Log | 274 von 302 | 305 von 341 | möglichst alle |
| Alle Sichtungen: Alter beim Fund, Median | 0 Tage | 0 Tage | — |
| Go bis Versand, Median (Versand in der Woche, n) | 3 Tage (3) | 3 Tage (8) | — |

Je Kanal (Sichtungen mit Datum, Median Alter): behoerdenportal 5× 5 Tage; netzwerk-empfehlung 10× 0 Tage; netzwerk-suche 70× 0 Tage; portal 182× 0 Tage; zielportal 7× 2 Tage

## Die drei grössten Abweichungen

Keine — alle Kennzahlen im Ziel.

## Vorschläge (Entscheid bei Alex)

Keine.

## Wirkungskontrolle früherer Massnahmen

Je angenommene oder umgesetzte Massnahme: Metrik beim Vorschlag gegen diese Woche.

| Massnahme | Entscheid | Metrik | damals | jetzt | Wirkung |
|---|---|---|---|---|---|
| 2025-03-16 Zwei Sessions am selben Sweep, 9 Abfragen doppelt geloggt | umgesetzt | sweeps_doppelt | 1 | 0 | **gewirkt** — Sperrmuster wie pipeline_tx |
| 2025-03-23 Zwei Abfragen liefern seit zwei Wochen nur Rauschen | umgesetzt | abfragen_ohne_kandidat_14d | 2 | 0 | **gewirkt** — aktiv:false mit Datum und Grund |
| 2025-04-06 Ein Sweep liest rund 280 KB Regelwerk und faehrt das Jobportal im Browser | umgesetzt | dauer_min_median | 54 | 29.5 | **gewirkt** — Wirkungskontrolle: scripts/umbau_kontrolle.py |

Massnahmen seit Beginn der Vorwoche (2025-03-30): 2025-04-06-vorscan **gewirkt**.

Noch unentschieden aus früheren Retros: 2025-03-16-sweeps-nicht-abgeschlossen, 2025-03-16-abdeckung-unter-soll, 2025-03-23-stellen-zu-spaet-gefunden-verpasst, 2025-03-23-portale-wiederholt-nicht-erreichbar, 2025-03-30-stellen-zu-spaet-gefunden-verpasst, 2025-03-30-portale-wiederholt-nicht-erreichbar, 2025-03-30-sweeps-nicht-abgeschlossen

## Kanal-Auswertung (2025-03-16 bis 2025-04-12, 28 Tage)

Gleiche Stelle = gleiche Firma + Rolle (normalisiert). «Nur hier» = in keinem anderen Kanal gesehen. «Zuerst hier» = bei Stellen in mehreren Kanälen hier zuerst gesichtet; Vorsprung = Median in Stunden zum nächsten Kanal.

| Kanal | Stellen | Kandidaten | nur hier | davon Kandidaten | zuerst hier | Vorsprung (h) |
|---|---|---|---|---|---|---|
| portal | 790 | 25 | 631 | 17 | 69 | 24 |
| netzwerk-suche | 284 | 8 | 157 | 4 | 64 | 24 |
| netzwerk-empfehlung | 37 | 2 | 19 | 0 | 10 | 22 |
| zielportal | 25 | 5 | 11 | 1 | 12 | 24 |
| behoerdenportal | 15 | 0 | 10 | 0 | 5 | 6 |

Zuerst publiziert (nur Stellen mit Publikationsdatum in mindestens zwei Kanälen, n = 44): portal 28, netzwerk-suche 10, netzwerk-empfehlung 3, zielportal 3

### Karriere- und Behördenportale einzeln

| Portal | Stellen | Kandidaten | Kandidaten nur hier | zuerst hier |
|---|---|---|---|---|
| Karriereseite Kalvit Software AG | 5 | 1 | 1 | 2 |
| Karriereseite Brivana Privatbank AG | 4 | 1 | 0 | 2 |
| Karriereseite Pelvio Mobility AG | 3 | 1 | 0 | 1 |
| Karriereseite Vendaro Retail AG | 3 | 1 | 0 | 2 |
| Karriereseite Sanuvia Health AG | 2 | 1 | 0 | 2 |
| Stellenportal Kantonale Verwaltung Altmark | 8 | 0 | 0 | 2 |
| Stellenportal Stadtverwaltung Nordtal | 7 | 0 | 0 | 3 |
| Karriereseite Quendor Versicherungen AG | 4 | 0 | 0 | 2 |
| Karriereseite Varella Energie AG | 4 | 0 | 0 | 1 |

Lesart: Ein Portal ohne Kandidaten «nur hier» und ohne «zuerst hier» liefert nichts, was Jobportal oder Netzwerk nicht auch zeigen — Kandidat zum Streichen im Wochen-Review (Entscheid bei Alex).

## Bei dir liegt

Keine Entscheide.

Markieren: `python3 scripts/prozess_retro.py --markiere <id> angenommen|abgelehnt|umgesetzt "Notiz"` — IDs: keine neuen
