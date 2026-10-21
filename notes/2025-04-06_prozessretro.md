# Prozess-Retro Screening — 2025-04-06 (Zeitraum 2025-03-30 bis 2025-04-05)

Misst die Qualität des Prozesses, nicht den Ertrag der Suche (der steht im Wochen-Review). Quelle: data/lauf_audit.json, data/screening_log.json, notes/, feedback/.

## Kennzahlen

| Kennzahl | diese Woche | Vorwoche | Ziel |
|---|---|---|---|
| Sweeps gestartet / Soll (nur Info) | 16 / 16 | 16 / 16 | — |
| Sweeps abgeschlossen | 16 | 15 | 16 |
| Sweeps abgebrochen | 0 | 1 | 0 |
| Sweeps ohne «ende» | 0 | 0 | 0 |
| Sweeps mit doppelt geloggten Abfragen | 0 | 0 | 0 |
| Abdeckung Mittel / Minimum | 100 % / 100 % | 97 % / 56 % | 100 % |
| Sessions je Sweep (Mittel) | 1 | 1 | ≤ 3 |
| Dauer je Sweep (Mittel / Median, min) | 60.25 / 62.0 | 54.938 / 52.0 | — |
| Abfragen nicht erreichbar | 3 | 10 | 0 |
| Abfragen teilweise / übersprungen | 6 / 0 | 8 / 0 | — / 0 |
| Berichtsform vollständig | 100 % (16 Notizen) | 100 % | 100 % |
| Sichtungen / Kandidaten | 341 / 9 | 286 / 6 | — |
| Kandidaten je Sweep | 0.562 | 0.375 | — |
| Abfragen nur mit Rauschen, 14 Tage (ohne Ziel-/Behördenportale) | 0 | 0 | — |
| Sammelposten | 0 | 0 | wenige |
| Feedback-Dateien mit Formbruch/Rezidiv | 0 | — | 0 |

Nicht erreichbar: bp-nordtal 1x; ns-zh-a 1x; zp-pelvio 1x

## Fundgeschwindigkeit — wie alt war eine Anzeige, als wir sie fanden?

Zentrale Grösse für «schneller sein». Alter beim Fund = erste Sichtung minus Veröffentlichung. Über eine Woche alt = meist schwerer zu erreichen.

| Kennzahl | diese Woche | Vorwoche | Ziel |
|---|---|---|---|
| Relevante Fälle (Kandidat, Volltext, offen) mit Datum | 51 von 51 | 41 von 41 | alle |
| **Alter beim Fund, Median** | **0 Tage** | 0 Tage | ≤ 1 Tag |
| davon 0–1 Tag / 2–7 Tage / über 7 Tage | 44 / 7 / 0 | 32 / 7 / 2 | — |
| Über 7 Tage, obwohl die Abfrage schon lief (verpasst) | 0 | 2 | 0 |
| Sichtungen mit Publiziert-Datum im Log | 305 von 341 | 251 von 286 | möglichst alle |
| Alle Sichtungen: Alter beim Fund, Median | 0 Tage | 0 Tage | — |
| Go bis Versand, Median (Versand in der Woche, n) | 3 Tage (8) | 3 Tage (3) | — |

Je Kanal (Sichtungen mit Datum, Median Alter): behoerdenportal 5× 3 Tage; netzwerk-empfehlung 11× 0 Tage; netzwerk-suche 74× 0 Tage; portal 212× 0 Tage; zielportal 3× 5 Tage

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

Massnahmen seit Beginn der Vorwoche (2025-03-23): 2025-03-23-ausrangieren **gewirkt**.

Noch unentschieden aus früheren Retros: 2025-03-16-sweeps-nicht-abgeschlossen, 2025-03-16-abdeckung-unter-soll, 2025-03-23-stellen-zu-spaet-gefunden-verpasst, 2025-03-23-portale-wiederholt-nicht-erreichbar, 2025-03-30-stellen-zu-spaet-gefunden-verpasst, 2025-03-30-portale-wiederholt-nicht-erreichbar, 2025-03-30-sweeps-nicht-abgeschlossen

## Kanal-Auswertung (2025-03-09 bis 2025-04-05, 28 Tage)

Gleiche Stelle = gleiche Firma + Rolle (normalisiert). «Nur hier» = in keinem anderen Kanal gesehen. «Zuerst hier» = bei Stellen in mehreren Kanälen hier zuerst gesichtet; Vorsprung = Median in Stunden zum nächsten Kanal.

| Kanal | Stellen | Kandidaten | nur hier | davon Kandidaten | zuerst hier | Vorsprung (h) |
|---|---|---|---|---|---|---|
| portal | 745 | 28 | 578 | 19 | 73 | 25 |
| netzwerk-suche | 279 | 10 | 138 | 3 | 71 | 24 |
| netzwerk-empfehlung | 34 | 2 | 14 | 0 | 12 | 25 |
| zielportal | 20 | 6 | 9 | 2 | 9 | 23 |
| behoerdenportal | 12 | 0 | 7 | 0 | 5 | 6 |

Zuerst publiziert (nur Stellen mit Publikationsdatum in mindestens zwei Kanälen, n = 55): portal 33, netzwerk-suche 17, netzwerk-empfehlung 4, zielportal 2

### Karriere- und Behördenportale einzeln

| Portal | Stellen | Kandidaten | Kandidaten nur hier | zuerst hier |
|---|---|---|---|---|
| Karriereseite Kalvit Software AG | 5 | 2 | 2 | 1 |
| Karriereseite Brivana Privatbank AG | 3 | 1 | 0 | 2 |
| Karriereseite Pelvio Mobility AG | 3 | 1 | 0 | 1 |
| Karriereseite Sanuvia Health AG | 2 | 1 | 0 | 2 |
| Karriereseite Vendaro Retail AG | 2 | 1 | 0 | 1 |
| Stellenportal Kantonale Verwaltung Altmark | 7 | 0 | 0 | 2 |
| Stellenportal Stadtverwaltung Nordtal | 5 | 0 | 0 | 3 |
| Karriereseite Quendor Versicherungen AG | 3 | 0 | 0 | 1 |
| Karriereseite Varella Energie AG | 2 | 0 | 0 | 1 |

Lesart: Ein Portal ohne Kandidaten «nur hier» und ohne «zuerst hier» liefert nichts, was Jobportal oder Netzwerk nicht auch zeigen — Kandidat zum Streichen im Wochen-Review (Entscheid bei Alex).

## Bei dir liegt

Keine Entscheide.

Markieren: `python3 scripts/prozess_retro.py --markiere <id> angenommen|abgelehnt|umgesetzt "Notiz"` — IDs: keine neuen
