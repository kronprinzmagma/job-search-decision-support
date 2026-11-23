# Prozess-Retro Screening — 2025-03-30 (Zeitraum 2025-03-23 bis 2025-03-29)

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
| Dauer je Sweep (Mittel / Median, min) | 54.938 / 52.0 | 58.062 / 57.0 | — |
| Abfragen nicht erreichbar | 10 | 8 | 0 |
| Abfragen teilweise / übersprungen | 8 / 0 | 7 / 0 | — / 0 |
| Berichtsform vollständig | 100 % (16 Notizen) | 100 % | 100 % |
| Sichtungen / Kandidaten | 286 / 6 | 324 / 8 | — |
| Kandidaten je Sweep | 0.375 | 0.5 | — |
| Abfragen nur mit Rauschen, 14 Tage (ohne Ziel-/Behördenportale) | 0 | 0 | — |
| Sammelposten | 0 | 0 | wenige |
| Feedback-Dateien mit Formbruch/Rezidiv | 0 | — | 0 |

Nicht erreichbar: ns-zh-b 3x; ns-be-b 2x; ns-zh-a 1x; zp-mirvel 1x; zp-pelvio 1x; zp-sanuvia 1x; zp-vendaro 1x

## Fundgeschwindigkeit — wie alt war eine Anzeige, als wir sie fanden?

Zentrale Grösse für «schneller sein». Alter beim Fund = erste Sichtung minus Veröffentlichung. Über eine Woche alt = meist schwerer zu erreichen.

| Kennzahl | diese Woche | Vorwoche | Ziel |
|---|---|---|---|
| Relevante Fälle (Kandidat, Volltext, offen) mit Datum | 41 von 41 | 46 von 46 | alle |
| **Alter beim Fund, Median** | **0 Tage** | 0 Tage | ≤ 1 Tag |
| davon 0–1 Tag / 2–7 Tage / über 7 Tage | 32 / 7 / 2 | 41 / 4 / 1 | — |
| Über 7 Tage, obwohl die Abfrage schon lief (verpasst) | 2 | 1 | 0 |
| Sichtungen mit Publiziert-Datum im Log | 251 von 286 | 274 von 324 | möglichst alle |
| Alle Sichtungen: Alter beim Fund, Median | 0 Tage | 0 Tage | — |
| Go bis Versand, Median (Versand in der Woche, n) | 3 Tage (3) | 2.5 Tage (6) | — |

Je Kanal (Sichtungen mit Datum, Median Alter): behoerdenportal 1× 5 Tage; netzwerk-empfehlung 9× 0 Tage; netzwerk-suche 47× 0 Tage; portal 186× 0 Tage; zielportal 8× 3.5 Tage

Späte Funde (über eine Woche alt):

| Firma — Rolle | Alter | Art | gefunden über | Entscheid |
|---|---|---|---|---|
| Brivana Privatbank AG — Lead Product Owner Plattform Kundenerlebnis | 12 Tage | verpasst | Karriereseite Brivana Privatbank AG | kandidat |
| Quendor Versicherungen AG — Product Owner Self-Service Prozesse | 12 Tage | verpasst | Karriereseite Quendor Versicherungen AG | volltext-nogo |

## Die drei grössten Abweichungen

1. **Stellen zu spät gefunden (verpasst)** — 2 relevante Anzeige(n) erst nach über einer Woche gefunden, obwohl die Abfrage schon lief: Brivana Privatbank AG — Lead Product Owner Plattform Kundenerlebnis (12 Tage, über Karriereseite Brivana Privatbank AG); Quendor Versicherungen AG — Product Owner Self-Service Prozesse (12 Tage, über Karriereseite Quendor Versicherungen AG).
2. **Portale wiederholt nicht erreichbar** — ns-zh-b 3x; ns-be-b 2x
3. **Sweeps nicht abgeschlossen** — 1 gestartete Sweeps blieben offen oder abgebrochen (1 abgebrochen).

Weitere: Abdeckung unter Soll

## Vorschläge (Entscheid bei Alex)

- **Stellen zu spät gefunden (verpasst)** → Je Fall prüfen, warum die laufende Abfrage die Anzeige nicht zeigte (Zeitfenster der Abfrage zu kurz, Begriff fehlt, Liste nur teilweise gelesen) und den Katalog-Eintrag bzw. Begriff anpassen. *(Zieldatei: data/screening_kanaele.json)*
- **Portale wiederholt nicht erreichbar** → Je Portal: verifizierten Weg und Werkzeugfalle im Katalog-Hinweis prüfen und ergänzen. Erst wenn die Quelle selbst tot ist: Portal ausrangieren (Entscheid Alex). *(Zieldatei: data/screening_kanaele.json)*
- **Sweeps nicht abgeschlossen** → Abbruchgründe in den Sweep-Notizen lesen; wenn Zeitbudget: Fortsetzungs-Sessions prüfen; wenn Werkzeug: Falle in den Katalog-Hinweis schreiben. *(Zieldatei: notes/, data/screening_kanaele.json)*

## Wirkungskontrolle früherer Massnahmen

Je angenommene oder umgesetzte Massnahme: Metrik beim Vorschlag gegen diese Woche.

| Massnahme | Entscheid | Metrik | damals | jetzt | Wirkung |
|---|---|---|---|---|---|
| 2025-03-16 Zwei Sessions am selben Sweep, 9 Abfragen doppelt geloggt | umgesetzt | sweeps_doppelt | 1 | 0 | **gewirkt** — Sperrmuster wie pipeline_tx |
| 2025-03-23 Zwei Abfragen liefern seit zwei Wochen nur Rauschen | umgesetzt | abfragen_ohne_kandidat_14d | 2 | 0 | **gewirkt** — aktiv:false mit Datum und Grund |

Massnahmen seit Beginn der Vorwoche (2025-03-16): 2025-03-16-log-sperre **gewirkt**; 2025-03-23-ausrangieren **gewirkt**.

Noch unentschieden aus früheren Retros: 2025-03-16-sweeps-nicht-abgeschlossen, 2025-03-16-abdeckung-unter-soll, 2025-03-23-stellen-zu-spaet-gefunden-verpasst, 2025-03-23-portale-wiederholt-nicht-erreichbar

## Kanal-Auswertung (2025-03-02 bis 2025-03-29, 28 Tage)

Gleiche Stelle = gleiche Firma + Rolle (normalisiert). «Nur hier» = in keinem anderen Kanal gesehen. «Zuerst hier» = bei Stellen in mehreren Kanälen hier zuerst gesichtet; Vorsprung = Median in Stunden zum nächsten Kanal.

| Kanal | Stellen | Kandidaten | nur hier | davon Kandidaten | zuerst hier | Vorsprung (h) |
|---|---|---|---|---|---|---|
| portal | 698 | 24 | 522 | 14 | 86 | 125 |
| netzwerk-suche | 270 | 9 | 119 | 3 | 68 | 24 |
| netzwerk-empfehlung | 31 | 2 | 12 | 0 | 11 | 27 |
| zielportal | 22 | 7 | 9 | 2 | 10 | 15 |
| behoerdenportal | 10 | 0 | 5 | 0 | 5 | 24 |

Zuerst publiziert (nur Stellen mit Publikationsdatum in mindestens zwei Kanälen, n = 70): portal 46, netzwerk-suche 19, netzwerk-empfehlung 5, zielportal 1

### Karriere- und Behördenportale einzeln

| Portal | Stellen | Kandidaten | Kandidaten nur hier | zuerst hier |
|---|---|---|---|---|
| Karriereseite Kalvit Software AG | 6 | 2 | 2 | 2 |
| Karriereseite Brivana Privatbank AG | 4 | 2 | 0 | 3 |
| Karriereseite Pelvio Mobility AG | 3 | 1 | 0 | 1 |
| Karriereseite Sanuvia Health AG | 2 | 1 | 0 | 1 |
| Karriereseite Vendaro Retail AG | 2 | 1 | 0 | 1 |
| Stellenportal Kantonale Verwaltung Altmark | 6 | 0 | 0 | 3 |
| Karriereseite Quendor Versicherungen AG | 4 | 0 | 0 | 1 |
| Stellenportal Stadtverwaltung Nordtal | 4 | 0 | 0 | 2 |
| Karriereseite Varella Energie AG | 1 | 0 | 0 | 1 |

Lesart: Ein Portal ohne Kandidaten «nur hier» und ohne «zuerst hier» liefert nichts, was Jobportal oder Netzwerk nicht auch zeigen — Kandidat zum Streichen im Wochen-Review (Entscheid bei Alex).

## Bei dir liegt

- Stellen zu spät gefunden (verpasst): **annehmen** (Umsetzung wie vorgeschlagen) / **ablehnen** (bleibt so, Grund vermerken) / **anders** (dein Vorschlag)
- Portale wiederholt nicht erreichbar: **annehmen** (Umsetzung wie vorgeschlagen) / **ablehnen** (bleibt so, Grund vermerken) / **anders** (dein Vorschlag)
- Sweeps nicht abgeschlossen: **annehmen** (Umsetzung wie vorgeschlagen) / **ablehnen** (bleibt so, Grund vermerken) / **anders** (dein Vorschlag)

Markieren: `python3 scripts/prozess_retro.py --markiere <id> angenommen|abgelehnt|umgesetzt "Notiz"` — IDs: 2025-03-30-stellen-zu-spaet-gefunden-verpasst, 2025-03-30-portale-wiederholt-nicht-erreichbar, 2025-03-30-sweeps-nicht-abgeschlossen
