# Prozess-Retro Screening — 2025-03-09 (Zeitraum 2025-03-02 bis 2025-03-08)

Misst die Qualität des Prozesses, nicht den Ertrag der Suche (der steht im Wochen-Review). Quelle: data/lauf_audit.json, data/screening_log.json, notes/, feedback/.

## Kennzahlen

| Kennzahl | diese Woche | Vorwoche | Ziel |
|---|---|---|---|
| Sweeps gestartet / Soll (nur Info) | 10 / 16 | 0 / 16 | — |
| Sweeps abgeschlossen | 10 | 0 | 16 |
| Sweeps abgebrochen | 0 | 0 | 0 |
| Sweeps ohne «ende» | 0 | 0 | 0 |
| Sweeps mit doppelt geloggten Abfragen | 0 | 0 | 0 |
| Abdeckung Mittel / Minimum | 100 % / 100 % | - / - | 100 % |
| Sessions je Sweep (Mittel) | 1 | - | ≤ 3 |
| Dauer je Sweep (Mittel / Median, min) | 56.3 / 55.5 | - / - | — |
| Abfragen nicht erreichbar | 5 | 0 | 0 |
| Abfragen teilweise / übersprungen | 9 / 0 | 0 / 0 | — / 0 |
| Berichtsform vollständig | 100 % (10 Notizen) | - | 100 % |
| Sichtungen / Kandidaten | 228 / 2 | 0 / 0 | — |
| Kandidaten je Sweep | 0.2 | 0 | — |
| Abfragen nur mit Rauschen, 14 Tage (ohne Ziel-/Behördenportale) | 2 | 0 | — |
| Sammelposten | 0 | 0 | wenige |
| Feedback-Dateien mit Formbruch/Rezidiv | 0 | — | 0 |

Nicht erreichbar: bp-nordtal 1x; ns-ost 1x; ns-zh-a 1x; zp-mirvel 1x; zp-pelvio 1x

## Fundgeschwindigkeit — wie alt war eine Anzeige, als wir sie fanden?

Zentrale Grösse für «schneller sein». Alter beim Fund = erste Sichtung minus Veröffentlichung. Über eine Woche alt = meist schwerer zu erreichen.

| Kennzahl | diese Woche | Vorwoche | Ziel |
|---|---|---|---|
| Relevante Fälle (Kandidat, Volltext, offen) mit Datum | 28 von 28 | 0 von 0 | alle |
| **Alter beim Fund, Median** | **0 Tage** | - | ≤ 1 Tag |
| davon 0–1 Tag / 2–7 Tage / über 7 Tage | 24 / 2 / 2 | 0 / 0 / 0 | — |
| Über 7 Tage, obwohl die Abfrage schon lief (verpasst) | 0 | 0 | 0 |
| Sichtungen mit Publiziert-Datum im Log | 203 von 228 | 0 von 0 | möglichst alle |
| Alle Sichtungen: Alter beim Fund, Median | 0 Tage | - | — |
| Go bis Versand, Median (Versand in der Woche, n) | - (0) | - (0) | — |

Je Kanal (Sichtungen mit Datum, Median Alter): behoerdenportal 3× 8 Tage; netzwerk-empfehlung 6× 0 Tage; netzwerk-suche 47× 0 Tage; portal 144× 0 Tage; zielportal 3× 2 Tage

Späte Funde (über eine Woche alt):

| Firma — Rolle | Alter | Art | gefunden über | Entscheid |
|---|---|---|---|---|
| Brivana Privatbank AG — Product Manager Data Platform | 12 Tage | Altbestand | Karriereseite Brivana Privatbank AG | volltext-nogo |
| Kantonale Verwaltung Altmark — Senior Product Owner (80–100 %) | 8 Tage | Altbestand | Stellenportal Kantonale Verwaltung Altmark | volltext-nogo |

## Die drei grössten Abweichungen

Keine — alle Kennzahlen im Ziel.

## Vorschläge (Entscheid bei Alex)

Keine.

## Wirkungskontrolle früherer Massnahmen

Je angenommene oder umgesetzte Massnahme: Metrik beim Vorschlag gegen diese Woche.

Keine angenommene Massnahme aus früheren Wochen.

## Kanal-Auswertung (2025-02-09 bis 2025-03-08, 28 Tage)

Gleiche Stelle = gleiche Firma + Rolle (normalisiert). «Nur hier» = in keinem anderen Kanal gesehen. «Zuerst hier» = bei Stellen in mehreren Kanälen hier zuerst gesichtet; Vorsprung = Median in Stunden zum nächsten Kanal.

| Kanal | Stellen | Kandidaten | nur hier | davon Kandidaten | zuerst hier | Vorsprung (h) |
|---|---|---|---|---|---|---|
| portal | 165 | 3 | 121 | 1 | 23 | 473 |
| netzwerk-suche | 68 | 1 | 31 | 1 | 15 | 23 |
| netzwerk-empfehlung | 8 | 0 | 4 | 0 | 2 | 485 |
| zielportal | 4 | 2 | 1 | 0 | 2 | 411 |
| behoerdenportal | 3 | 0 | 0 | 0 | 3 | 24 |

Zuerst publiziert (nur Stellen mit Publikationsdatum in mindestens zwei Kanälen, n = 23): portal 15, netzwerk-suche 6, netzwerk-empfehlung 2

### Karriere- und Behördenportale einzeln

| Portal | Stellen | Kandidaten | Kandidaten nur hier | zuerst hier |
|---|---|---|---|---|
| Karriereseite Brivana Privatbank AG | 1 | 1 | 0 | 1 |
| Karriereseite Sanuvia Health AG | 1 | 1 | 0 | 0 |
| Stellenportal Kantonale Verwaltung Altmark | 3 | 0 | 0 | 3 |
| Karriereseite Kalvit Software AG | 1 | 0 | 0 | 1 |
| Karriereseite Quendor Versicherungen AG | 1 | 0 | 0 | 0 |

Lesart: Ein Portal ohne Kandidaten «nur hier» und ohne «zuerst hier» liefert nichts, was Jobportal oder Netzwerk nicht auch zeigen — Kandidat zum Streichen im Wochen-Review (Entscheid bei Alex).

## Bei dir liegt

Keine Entscheide.

Markieren: `python3 scripts/prozess_retro.py --markiere <id> angenommen|abgelehnt|umgesetzt "Notiz"` — IDs: keine neuen
