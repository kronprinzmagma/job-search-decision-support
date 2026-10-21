# Prozess-Retro Screening — 2025-03-23 (Zeitraum 2025-03-16 bis 2025-03-22)

Misst die Qualität des Prozesses, nicht den Ertrag der Suche (der steht im Wochen-Review). Quelle: data/lauf_audit.json, data/screening_log.json, notes/, feedback/.

## Kennzahlen

| Kennzahl | diese Woche | Vorwoche | Ziel |
|---|---|---|---|
| Sweeps gestartet / Soll (nur Info) | 16 / 16 | 10 / 16 | — |
| Sweeps abgeschlossen | 16 | 9 | 16 |
| Sweeps abgebrochen | 0 | 1 | 0 |
| Sweeps ohne «ende» | 0 | 0 | 0 |
| Sweeps mit doppelt geloggten Abfragen | 0 | 0 | 0 |
| Abdeckung Mittel / Minimum | 100 % / 100 % | 97 % / 67 % | 100 % |
| Sessions je Sweep (Mittel) | 1 | 1 | ≤ 3 |
| Dauer je Sweep (Mittel / Median, min) | 58.062 / 57.0 | 60.7 / 58.5 | — |
| Abfragen nicht erreichbar | 8 | 0 | 0 |
| Abfragen teilweise / übersprungen | 7 / 0 | 7 / 0 | — / 0 |
| Berichtsform vollständig | 100 % (16 Notizen) | 100 % | 100 % |
| Sichtungen / Kandidaten | 324 / 8 | 201 / 9 | — |
| Kandidaten je Sweep | 0.5 | 0.9 | — |
| Abfragen nur mit Rauschen, 14 Tage (ohne Ziel-/Behördenportale) | 0 | 0 | — |
| Sammelposten | 0 | 0 | wenige |
| Feedback-Dateien mit Formbruch/Rezidiv | 0 | — | 0 |

Nicht erreichbar: ns-be-b 2x; zp-mirvel 2x; ns-ost 1x; ns-zh-b 1x; zp-pelvio 1x; zp-quendor 1x

## Fundgeschwindigkeit — wie alt war eine Anzeige, als wir sie fanden?

Zentrale Grösse für «schneller sein». Alter beim Fund = erste Sichtung minus Veröffentlichung. Über eine Woche alt = meist schwerer zu erreichen.

| Kennzahl | diese Woche | Vorwoche | Ziel |
|---|---|---|---|
| Relevante Fälle (Kandidat, Volltext, offen) mit Datum | 46 von 46 | 28 von 28 | alle |
| **Alter beim Fund, Median** | **0 Tage** | 0 Tage | ≤ 1 Tag |
| davon 0–1 Tag / 2–7 Tage / über 7 Tage | 41 / 4 / 1 | 26 / 2 / 0 | — |
| Über 7 Tage, obwohl die Abfrage schon lief (verpasst) | 1 | 0 | 0 |
| Sichtungen mit Publiziert-Datum im Log | 274 von 324 | 173 von 201 | möglichst alle |
| Alle Sichtungen: Alter beim Fund, Median | 0 Tage | 0 Tage | — |
| Go bis Versand, Median (Versand in der Woche, n) | 2.5 Tage (6) | 6 Tage (1) | — |

Je Kanal (Sichtungen mit Datum, Median Alter): behoerdenportal 4× 5.5 Tage; netzwerk-empfehlung 6× 0 Tage; netzwerk-suche 62× 0 Tage; portal 194× 0 Tage; zielportal 8× 4 Tage

Späte Funde (über eine Woche alt):

| Firma — Rolle | Alter | Art | gefunden über | Entscheid |
|---|---|---|---|---|
| Pelvio Mobility AG — Digital Product Lead B2B | 8 Tage | verpasst | Karriereseite Pelvio Mobility AG | kandidat |

## Die drei grössten Abweichungen

1. **Stellen zu spät gefunden (verpasst)** — 1 relevante Anzeige(n) erst nach über einer Woche gefunden, obwohl die Abfrage schon lief: Pelvio Mobility AG — Digital Product Lead B2B (8 Tage, über Karriereseite Pelvio Mobility AG).
2. **Portale wiederholt nicht erreichbar** — ns-be-b 2x; zp-mirvel 2x

## Vorschläge (Entscheid bei Alex)

- **Stellen zu spät gefunden (verpasst)** → Je Fall prüfen, warum die laufende Abfrage die Anzeige nicht zeigte (Zeitfenster der Abfrage zu kurz, Begriff fehlt, Liste nur teilweise gelesen) und den Katalog-Eintrag bzw. Begriff anpassen. *(Zieldatei: data/screening_kanaele.json)*
- **Portale wiederholt nicht erreichbar** → Je Portal: verifizierten Weg und Werkzeugfalle im Katalog-Hinweis prüfen und ergänzen. Erst wenn die Quelle selbst tot ist: Portal ausrangieren (Entscheid Alex). *(Zieldatei: data/screening_kanaele.json)*

## Wirkungskontrolle früherer Massnahmen

Je angenommene oder umgesetzte Massnahme: Metrik beim Vorschlag gegen diese Woche.

| Massnahme | Entscheid | Metrik | damals | jetzt | Wirkung |
|---|---|---|---|---|---|
| 2025-03-16 Zwei Sessions am selben Sweep, 9 Abfragen doppelt geloggt | umgesetzt | sweeps_doppelt | 1 | 0 | **gewirkt** — Sperrmuster wie pipeline_tx |

Massnahmen seit Beginn der Vorwoche (2025-03-09): 2025-03-16-log-sperre **gewirkt**.

Noch unentschieden aus früheren Retros: 2025-03-16-sweeps-nicht-abgeschlossen, 2025-03-16-abdeckung-unter-soll

## Kanal-Auswertung (2025-02-23 bis 2025-03-22, 28 Tage)

Gleiche Stelle = gleiche Firma + Rolle (normalisiert). «Nur hier» = in keinem anderen Kanal gesehen. «Zuerst hier» = bei Stellen in mehreren Kanälen hier zuerst gesichtet; Vorsprung = Median in Stunden zum nächsten Kanal.

| Kanal | Stellen | Kandidaten | nur hier | davon Kandidaten | zuerst hier | Vorsprung (h) |
|---|---|---|---|---|---|---|
| portal | 506 | 17 | 368 | 10 | 68 | 125 |
| netzwerk-suche | 213 | 7 | 95 | 3 | 52 | 24 |
| netzwerk-empfehlung | 24 | 2 | 7 | 0 | 9 | 31 |
| zielportal | 13 | 5 | 3 | 1 | 8 | 15 |
| behoerdenportal | 9 | 0 | 4 | 0 | 5 | 24 |

Zuerst publiziert (nur Stellen mit Publikationsdatum in mindestens zwei Kanälen, n = 58): portal 38, netzwerk-suche 15, netzwerk-empfehlung 5, zielportal 1

### Karriere- und Behördenportale einzeln

| Portal | Stellen | Kandidaten | Kandidaten nur hier | zuerst hier |
|---|---|---|---|---|
| Karriereseite Kalvit Software AG | 3 | 1 | 1 | 2 |
| Karriereseite Brivana Privatbank AG | 2 | 1 | 0 | 2 |
| Karriereseite Pelvio Mobility AG | 2 | 1 | 0 | 1 |
| Karriereseite Sanuvia Health AG | 1 | 1 | 0 | 0 |
| Karriereseite Vendaro Retail AG | 1 | 1 | 0 | 1 |
| Stellenportal Kantonale Verwaltung Altmark | 6 | 0 | 0 | 3 |
| Karriereseite Quendor Versicherungen AG | 3 | 0 | 0 | 1 |
| Stellenportal Stadtverwaltung Nordtal | 3 | 0 | 0 | 2 |
| Karriereseite Varella Energie AG | 1 | 0 | 0 | 1 |

Lesart: Ein Portal ohne Kandidaten «nur hier» und ohne «zuerst hier» liefert nichts, was Jobportal oder Netzwerk nicht auch zeigen — Kandidat zum Streichen im Wochen-Review (Entscheid bei Alex).

## Bei dir liegt

- Stellen zu spät gefunden (verpasst): **annehmen** (Umsetzung wie vorgeschlagen) / **ablehnen** (bleibt so, Grund vermerken) / **anders** (dein Vorschlag)
- Portale wiederholt nicht erreichbar: **annehmen** (Umsetzung wie vorgeschlagen) / **ablehnen** (bleibt so, Grund vermerken) / **anders** (dein Vorschlag)

Markieren: `python3 scripts/prozess_retro.py --markiere <id> angenommen|abgelehnt|umgesetzt "Notiz"` — IDs: 2025-03-23-stellen-zu-spaet-gefunden-verpasst, 2025-03-23-portale-wiederholt-nicht-erreichbar
