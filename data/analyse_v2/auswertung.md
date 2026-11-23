# Auswertung Fit-Raster v2 — Anforderungs-Fit und Domänennähe gegen Einladungsergebnis

Generiert aus `data/pipeline.json` · `scripts/analyse_fit_v2.py`

## Population

- Kodierte Bewerbungen (v2): **36**, davon ex ante (vor dem Versand) kodiert: 36
- Davon mit arbeitgeberseitig entschiedenem Ergebnis: **21**
  - Einladung zum Erstgespräch: **12**
  - Dossier-Absage ohne Kontakt: **9**
- Ausgeschlossen: 1 zurückgezogen (eigener Abbruch, kein Arbeitgeber-Urteil), 14 offen (zensiert)
- Nicht kodierbar (Anzeige fehlt, A leer): 0

**Basisrate Einladung: 12/21 = 57.1%** (95%-Wilson: 36.5–75.5%)

## H1 — Domänen- und Aktivitätsnähe (B)

**Hypothese:** Bei Angebotsüberhang entscheidet, wer die Branche oder die Tätigkeit schon gemacht hat.

| B (Domänennähe) | Einlad. | Quote | 95%-KI |
|---|---|---|---|
| 2 einschlägig            |    4/5 |  80.0% | 37.6–96.4% |
| 1 benachbart             |    3/7 |  42.9% | 15.8–75.0% |
| 0 keine Nähe             |    5/9 |  55.6% | 26.7–81.1% |

**Fisher exakt (B=2 vs. B≤1): p = 0.3383**

## H2 — Anforderungs-Fit (A)

| A (Anforderungs-Fit) | Einlad. | Quote | 95%-KI |
|---|---|---|---|
| 2 alle Muss belegt       |  10/14 |  71.4% | 45.4–88.3% |
| 1 zwei bis drei Lücken   |    2/6 |  33.3% |  9.7–70.0% |
| 0 Kernlücke              |    0/1 |   0.0% |  0.0–79.3% |

**Fisher exakt (A=2 vs. A≤1): p = 0.1588**

Risikodifferenz **+42.9 Prozentpunkte** · Risk Ratio **2.50**

**Power:** Für die beobachteten Quoten wären bei 80% Power und alpha=0.05 rund **21 Fälle pro Gruppe** nötig (vorhanden: 14 vs. 7). Die Studie ist zu klein, um diesen Effekt statistisch abzusichern.

## H3 — Zweistufiges Modell: wirkt B erst bei erfülltem A?

| Zelle | Einlad. | Quote | 95%-KI |
|---|---|---|---|
| A=2, B=2                 |    4/4 | 100.0% | 51.0–100.0% |
| A=2, B=1                 |    3/5 |  60.0% | 23.1–88.2% |
| A=2, B=0                 |    3/5 |  60.0% | 23.1–88.2% |
| A=1, B=2                 |    0/1 |   0.0% |  0.0–79.3% |
| A=1, B=1                 |    0/1 |   0.0% |  0.0–79.3% |
| A=1, B=0                 |    2/4 |  50.0% | 15.0–85.0% |
| A=0, B=1                 |    0/1 |   0.0% |  0.0–79.3% |

**B-Effekt, geschichtet nach A:**

| A | B=2 | B≤1 | Differenz | Fisher p |
|---|---|---|---|---|
| A=2 | 4/4 (100%) | 6/10 (60%) | +40 pp | 0.2507 |
| A=1 | 0/1 (0%) | 2/5 (40%) | -40 pp | 1.0000 |

## H4 — Trennschärfe des v2-Verdikts

| Verdikt v2 | Einlad. | Quote | 95%-KI |
|---|---|---|---|
| hoch                     |   7/10 |  70.0% | 39.7–89.2% |
| mittel                   |    3/6 |  50.0% | 18.8–81.2% |
| tief                     |    2/5 |  40.0% | 11.8–76.9% |

**Fisher exakt (hoch vs. mittel+tief): p = 0.3870**

## H5 — Kanal als Confounder

| Kanal | Einlad. | Quote | 95%-KI |
|---|---|---|---|
| + Empfehlung/Kontakt     |    7/9 |  77.8% | 45.3–93.7% |
| 0 Portal                 |    3/7 |  42.9% | 15.8–75.0% |
| − Massenkanal            |    2/5 |  40.0% | 11.8–76.9% |

**Fisher exakt (Kanal+ vs. Kanal−): p = 0.2657**

**Kreuzung A × Kanal** (prüft, ob der A-Effekt nur den Kanal spiegelt):

| | Kanal + | Kanal 0 | Kanal − |
|---|---|---|---|
| A=2 | 5/6 | 3/5 | 2/3 |
| A=1 | 2/3 | 0/2 | 0/1 |
| A=0 | — | — | 0/1 |

## Einzelfall-Liste (entschiedene Fälle, sortiert nach Verdikt v2)

| Firma | A | B | Kanal | Verdikt v2 | Ergebnis |
|---|---|---|---|---|---|
| Brivana Privatbank AG | 2 | 2 | - | hoch | Einladung |
| Fendrix Analytics AG | 2 | 2 | + | hoch | Einladung |
| Kalvit Software AG | 2 | 1 | - | hoch | Einladung |
| Orvana Reisen AG | 2 | 1 | + | hoch | Einladung |
| Varella Energie AG | 2 | 2 | 0 | hoch | Einladung |
| Vendaro Retail AG | 2 | 2 | 0 | hoch | Einladung |
| Vendaro Retail AG | 2 | 1 | + | hoch | Einladung |
| Mirvel Medien AG | 2 | 1 | 0 | hoch | Dossier |
| Sanuvia Health AG | 1 | 2 | 0 | hoch | Dossier |
| Vendaro Retail AG | 2 | 1 | - | hoch | Dossier |
| Lernovi Bildung AG | 2 | 0 | + | mittel | Einladung |
| Mirvel Medien AG | 2 | 0 | + | mittel | Einladung |
| Pelvio Mobility AG | 2 | 0 | 0 | mittel | Einladung |
| Mirvel Medien AG | 2 | 0 | + | mittel | Dossier |
| Sanuvia Health AG | 2 | 0 | 0 | mittel | Dossier |
| Vendaro Retail AG | 1 | 1 | - | mittel | Dossier |
| Quendor Versicherungen AG | 1 | 0 | + | tief | Einladung |
| Vendaro Retail AG | 1 | 0 | + | tief | Einladung |
| Kalvit Software AG | 1 | 0 | 0 | tief | Dossier |
| Lernovi Bildung AG | 0 | 1 | - | tief | Dossier |
| Varella Energie AG | 1 | 0 | + | tief | Dossier |

## Sensitivität — wie stabil sind die Befunde gegenüber der Fallauswahl?

Jeder entschiedene Fall wird einmal weggelassen (Leave-one-out). Kippt die Richtung oder springt der p-Wert über die Schwelle, hängt der Befund an einzelnen Fällen.

| Kontrast | p (alle) | p min–max ohne je einen Fall | Richtung kippt |
|---|---|---|---|
| A=2 vs. A≤1 | 0.1588 | 0.0498–0.1611 | nein |
| B=2 vs. B≤1 | 0.3383 | 0.1166–0.6027 | nein |
| Verdikt hoch vs. Rest | 0.3870 | 0.1968–0.6499 | nein |

## Limitationen — was diese Auswertung nicht kann

1. **Zensierte Fälle.** 14 Bewerbungen sind noch offen. Fallen ihre Ergebnisse anders aus als die der entschiedenen (z. B. weil Einladungen schneller kommen als Absagen), verzerrt das die Quoten oben.

2. **Kodierzeitpunkt.** 21 von 21 entschiedenen Fällen sind ex ante kodiert (vor dem Versand, ohne Kenntnis des Ausgangs). Nur diese sind ein sauberer Test; nachträglich vergebene Werte kennen den Ausgang.

3. **Fallzahl.** 12 Ereignisse auf 21 Fälle. Die besetzten Zellen der A×B-Matrix enthalten 1 bis 5 Fälle; ein einzelner Fall verschiebt eine kleine Zelle um viele Prozentpunkte.

4. **Auswahl.** Beworben wird nur, was Schritt 1 bestanden hat und von Alex ein Go bekam. Die Skalen sind deshalb nach unten ausgedünnt; eine Aussage über Fälle, die nie versandt wurden, ist nicht möglich.

5. **Zeit als Confounder.** Einladungsquote nach Monat der Einreichung: 2025-03 5/11 · 2025-04 7/10. Frühe und späte Bewerbungen liegen in unterschiedlichen Marktphasen; A, B und Zeit sind nicht entflochten.

