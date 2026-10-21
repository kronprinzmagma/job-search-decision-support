# Prozess-Retro Screening — 2025-03-16 (Zeitraum 2025-03-09 bis 2025-03-15)

Misst die Qualität des Prozesses, nicht den Ertrag der Suche (der steht im Wochen-Review). Quelle: data/lauf_audit.json, data/screening_log.json, notes/, feedback/.

## Kennzahlen

| Kennzahl | diese Woche | Vorwoche | Ziel |
|---|---|---|---|
| Sweeps gestartet / Soll (nur Info) | 10 / 16 | 10 / 16 | — |
| Sweeps abgeschlossen | 9 | 10 | 16 |
| Sweeps abgebrochen | 1 | 0 | 0 |
| Sweeps ohne «ende» | 0 | 0 | 0 |
| Sweeps mit doppelt geloggten Abfragen | 0 | 0 | 0 |
| Abdeckung Mittel / Minimum | 97 % / 67 % | 100 % / 100 % | 100 % |
| Sessions je Sweep (Mittel) | 1 | 1 | ≤ 3 |
| Dauer je Sweep (Mittel / Median, min) | 60.7 / 58.5 | 56.3 / 55.5 | — |
| Abfragen nicht erreichbar | 0 | 5 | 0 |
| Abfragen teilweise / übersprungen | 7 / 0 | 9 / 0 | — / 0 |
| Berichtsform vollständig | 100 % (10 Notizen) | 100 % | 100 % |
| Sichtungen / Kandidaten | 201 / 9 | 228 / 2 | — |
| Kandidaten je Sweep | 0.9 | 0.2 | — |
| Abfragen nur mit Rauschen, 14 Tage (ohne Ziel-/Behördenportale) | 0 | 2 | — |
| Sammelposten | 0 | 0 | wenige |
| Feedback-Dateien mit Formbruch/Rezidiv | 0 | — | 0 |

## Fundgeschwindigkeit — wie alt war eine Anzeige, als wir sie fanden?

Zentrale Grösse für «schneller sein». Alter beim Fund = erste Sichtung minus Veröffentlichung. Über eine Woche alt = meist schwerer zu erreichen.

| Kennzahl | diese Woche | Vorwoche | Ziel |
|---|---|---|---|
| Relevante Fälle (Kandidat, Volltext, offen) mit Datum | 28 von 28 | 28 von 28 | alle |
| **Alter beim Fund, Median** | **0 Tage** | 0 Tage | ≤ 1 Tag |
| davon 0–1 Tag / 2–7 Tage / über 7 Tage | 26 / 2 / 0 | 24 / 2 / 2 | — |
| Über 7 Tage, obwohl die Abfrage schon lief (verpasst) | 0 | 0 | 0 |
| Sichtungen mit Publiziert-Datum im Log | 173 von 201 | 203 von 228 | möglichst alle |
| Alle Sichtungen: Alter beim Fund, Median | 0 Tage | 0 Tage | — |
| Go bis Versand, Median (Versand in der Woche, n) | 6 Tage (1) | - (0) | — |

Je Kanal (Sichtungen mit Datum, Median Alter): behoerdenportal 2× 6.5 Tage; netzwerk-empfehlung 5× 0 Tage; netzwerk-suche 46× 0 Tage; portal 119× 0 Tage; zielportal 1× 1 Tag

## Die drei grössten Abweichungen

1. **Sweeps nicht abgeschlossen** — 1 gestartete Sweeps blieben offen oder abgebrochen (1 abgebrochen).
2. **Abdeckung unter Soll** — Mittlere Abdeckung 97 % (Minimum 67 %). Am häufigsten fehlend: ne-empfehlungen (1x), ns-be-a (1x), ns-be-b (1x), ns-zh-a (1x), ns-zh-b (1x).

## Vorschläge (Entscheid bei Alex)

- **Sweeps nicht abgeschlossen** → Abbruchgründe in den Sweep-Notizen lesen; wenn Zeitbudget: Fortsetzungs-Sessions prüfen; wenn Werkzeug: Falle in den Katalog-Hinweis schreiben. *(Zieldatei: notes/, data/screening_kanaele.json)*
- **Abdeckung unter Soll** → Wenn dieselben IDs fehlen: Reihenfolge im Katalog ändern (früh im Sweep) oder den Eintrag prüfen (URL, Werkzeugfalle). Wenn breit verteilt: zusätzliche Fortsetzungs-Session im Zeitplan. *(Zieldatei: data/screening_kanaele.json / Zeitplan)*

## Wirkungskontrolle früherer Massnahmen

Je angenommene oder umgesetzte Massnahme: Metrik beim Vorschlag gegen diese Woche.

Keine angenommene Massnahme aus früheren Wochen.

## Kanal-Auswertung (2025-02-16 bis 2025-03-15, 28 Tage)

Gleiche Stelle = gleiche Firma + Rolle (normalisiert). «Nur hier» = in keinem anderen Kanal gesehen. «Zuerst hier» = bei Stellen in mehreren Kanälen hier zuerst gesichtet; Vorsprung = Median in Stunden zum nächsten Kanal.

| Kanal | Stellen | Kandidaten | nur hier | davon Kandidaten | zuerst hier | Vorsprung (h) |
|---|---|---|---|---|---|---|
| portal | 299 | 10 | 215 | 6 | 43 | 312 |
| netzwerk-suche | 134 | 5 | 57 | 2 | 34 | 24 |
| netzwerk-empfehlung | 15 | 1 | 6 | 0 | 5 | 31 |
| zielportal | 5 | 3 | 2 | 1 | 2 | 411 |
| behoerdenportal | 5 | 0 | 2 | 0 | 3 | 24 |

Zuerst publiziert (nur Stellen mit Publikationsdatum in mindestens zwei Kanälen, n = 42): portal 27, netzwerk-suche 13, netzwerk-empfehlung 3

### Karriere- und Behördenportale einzeln

| Portal | Stellen | Kandidaten | Kandidaten nur hier | zuerst hier |
|---|---|---|---|---|
| Karriereseite Kalvit Software AG | 2 | 1 | 1 | 1 |
| Karriereseite Brivana Privatbank AG | 1 | 1 | 0 | 1 |
| Karriereseite Sanuvia Health AG | 1 | 1 | 0 | 0 |
| Stellenportal Kantonale Verwaltung Altmark | 5 | 0 | 0 | 3 |
| Karriereseite Quendor Versicherungen AG | 1 | 0 | 0 | 0 |

Lesart: Ein Portal ohne Kandidaten «nur hier» und ohne «zuerst hier» liefert nichts, was Jobportal oder Netzwerk nicht auch zeigen — Kandidat zum Streichen im Wochen-Review (Entscheid bei Alex).

## Bei dir liegt

- Sweeps nicht abgeschlossen: **annehmen** (Umsetzung wie vorgeschlagen) / **ablehnen** (bleibt so, Grund vermerken) / **anders** (dein Vorschlag)
- Abdeckung unter Soll: **annehmen** (Umsetzung wie vorgeschlagen) / **ablehnen** (bleibt so, Grund vermerken) / **anders** (dein Vorschlag)

Markieren: `python3 scripts/prozess_retro.py --markiere <id> angenommen|abgelehnt|umgesetzt "Notiz"` — IDs: 2025-03-16-sweeps-nicht-abgeschlossen, 2025-03-16-abdeckung-unter-soll
