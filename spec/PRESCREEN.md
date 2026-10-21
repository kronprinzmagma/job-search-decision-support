# PRESCREEN – Bewertung einer Stellenanzeige (Schritt 1 und Schritt 2)

Regelwerk für das Modell. Es bewertet Anzeigen **gegen die Persona** in [`persona/PROFILE.md`](../persona/PROFILE.md)
und gibt eine **Empfehlung**; entscheiden tut Alex. Gelesen wird diese Datei bei jeder Bewertung im Volltext
(Kandidaten-Chat, Wochen-Review). Der Sweep liest nur die Arbeitskarte [`SWEEP.md`](SWEEP.md).

## Leitprinzipien

- **Zwei Stufen, nicht sechs Gates.** Schritt 1 fragt «Will Alex das?», Schritt 2 «Lädt man Alex ein?».
  Die Ausschlüsse unten sind die einzigen harten Kriterien; alles andere ist ein Hinweis mit Gewicht.
- **Zweifel gehen an Alex, nie in die Aussortierung.** Ist ein Ausschluss nicht eindeutig belegt, wird der
  Fall vorgelegt, mit dem Zweifel als benannter Frage. Ein falsch aussortierter Fall ist unsichtbar;
  ein falsch vorgelegter kostet Alex eine Minute.
- **Nur auf Volltext.** Ohne vollständigen Anzeigentext aus der Primärquelle keine Bewertung (Hard-Gate in
  [`AGENTS.md`](../AGENTS.md)). Jede Aussage nennt die Stelle in der abgelegten Anzeige, auf die sie sich stützt.
- **Weiche Urteile werden nachgeprüft.** Was nicht unter einen Ausschluss fällt, sondern ein Urteil ist
  (Ausschluss 5, Ausschluss 6, Domänen- oder Level-Lücke), prüft der Wochen-Review gegen den Volltext erneut
  (`scripts/review_aussortierte.py`).

## Schritt 1 – Passung: «Will Alex das, und bringt es die Karriere weiter?»

### Ausschlüsse

| Nr. | Ausschluss | hart / weich | Belegt durch |
|---|---|---|---|
| 1 | Junior, Praktikum, Trainee | hart | Titel oder Profil |
| 2 | Distanz: Pendelzeit über 60 Minuten ab Zürich HB | hart | Ort der Anzeige, Ortstabelle unten |
| 3 | kein Homeoffice (100 % vor Ort) | hart | Volltext |
| 4 | Beratung oder Agentur (Arbeit für Kunden statt eigenes Produkt) | hart | Firma, Volltext |
| 5 | Rückschritt: kein Produktmandat, keine eigene Hoheit über Roadmap und Priorisierung | **weich** | Volltext, Urteil |
| 6 | Kernfähigkeits-Lücke: ein Muss-Kriterium, das bei Alex unbelegt ist | **weich** | Volltext gegen `PROFILE.md` |

Dazu, unabhängig von der Anzeige:

- **Benannter Fähigkeits-Ausschluss:** Produktrollen im Zahlungsverkehr (Payment, Acquiring).
- **Firmen-Ausschluss der Persona:** Glücksspielbranche.
- **Harte Vorfilter auf Listenebene:** Personalvermittler, Engineering- und Entwicklerrollen, physische Produkte
  (Hardware, Maschinen, Lebensmittel). Diese Fälle dürfen ungeöffnet wegfallen; sie stehen trotzdem mit Grund
  im Sichtungs-Log.

### Ortstabelle (Pendelzeit ab Zürich HB)

| bis 30 Min. | bis 60 Min. | über 60 Min. (Ausschluss 2) |
|---|---|---|
| Zürich, Schlieren, Dübendorf, Kloten, Baden, Winterthur, Zug | Aarau, Luzern, Basel, Bern | St. Gallen, Lausanne, Genf |

### Plus-Punkte (in dieser Reihenfolge)

1. Roadmap-Hoheit und Führung eines Produktteams
2. Plattform- oder Self-Service-Produkt im B2B-Umfeld
3. KI-Anteil im bestehenden Produkt (Anwendung, nicht Forschung)
4. regulierte Branche, in der Alex' Erfahrung trägt (Gesundheit, Versicherung)

### Passungs-Note

**hoch / mittel / tief**, mit einem Satz, der die tragenden Punkte nennt. Scope (wie gross ist die Rolle?) und
Karrierewert (bringt sie Alex weiter?) sind zwei getrennte Aussagen.

### Pflichtfragen fürs Gespräch

Was die Anzeige offenlässt und über die Passung entscheidet (z. B. «Wer entscheidet über die Roadmap?»),
wird als Frage notiert, nicht geraten.

## Schritt 2 – Chance: «Lädt man Alex zum Gespräch ein?»

| Grösse | Skala | Frage |
|---|---|---|
| **A** Anforderungs-Fit | 0–2 | Wie viele Muss-Kriterien der Anzeige sind bei Alex belegt? |
| **B** Domänen- und Aktivitätsnähe | 0–2 | Wie nah ist Alex' bisheriger Kontext an Branche und Tätigkeit der Rolle? |
| **Kanal** | + / 0 / − | Empfehlung oder Kontakt (+), Portal (0), Massenkanal mit erkennbar vielen Bewerbungen (−) |

Screening-Risiken (Formalkriterien wie ein bestimmter Abschluss, Branchenjahre) werden **qualitativ** genannt,
nicht verrechnet.

**Verdikt:** Chance auf ein Gespräch **hoch / mittel / tief**. Ein tiefes Verdikt aus reiner
Kompetenzdistanz ist ein NoGo-Vorschlag, den Alex bestätigt.

### Feldformat `fit_v2` in `data/pipeline.json`

```json
{"datum": "2025-03-18", "ex_ante": true, "A": 2, "A_begruendung": "…", "B": 1, "B_begruendung": "…",
 "kanal": "0", "verdikt": "hoch", "ergebnis": "offen", "methode": "ex ante vor dem Versand"}
```

`ex_ante: true` heisst: vor dem Versand kodiert, ohne Kenntnis des Ausgangs. Nur so lässt sich später prüfen,
ob das Raster etwas vorhersagt (`scripts/analyse_fit_v2.py`: Einladung vs. Dossier-Absage, Fisher-Exakt und
Wilson-Intervalle). `ergebnis` wird nachgeführt: `einladung`, `absage-dossier` oder `offen`.

## Ausgabe an Alex

Kurz und scanbar: Empfehlung zuerst, dann die Ausschlüsse einzeln mit Beleg, Schritt 1, Schritt 2, offene
Fragen. Keine internen Kürzel: nicht «Ausschluss 5 greift», sondern «Rückschritt beim Mandat: aus der
Anzeige geht keine eigene Hoheit über die Roadmap hervor».

## Nachfass

Eine Bewerbung ohne Rückmeldung nach 21 Tagen erscheint als «stale» in den Wächter-Befunden
(`scripts/jobcoach.py`); Nachfassen oder Abschreiben entscheidet Alex.
