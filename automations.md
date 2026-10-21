# Automationen – Soll-Vertrag

Was im Betrieb als geplante Aufgabe läuft. Im Showcase läuft keine davon; die Demo-Daten zeigen, was sie
hinterlassen. Die Tabelle ist der prüfbare Vertrag: Jede Routine nennt, was sie liest, was sie schreiben darf
und wann sie den Menschen stört.

| Routine | Takt | Modell | Liest | Schreibt | Meldet an Alex |
|---|---|---|---|---|---|
| Vorscan (ohne Modell) | 3× täglich, vor den Sweeps | – | Abfrage-Katalog, Jobportal | nur `data/vorscan/` | nie |
| Screening-Sweep | 3× täglich (morgen, mittag, nachmittag) | günstig | `spec/SWEEP.md`, Katalog, Vorscan | Sichtungs-Log, Audit, Sweep-Notiz, Kandidaten als `vorgelegt` | nie direkt |
| Kandidaten-Chat | mehrmals täglich | stark | `spec/PRESCREEN.md`, vorgelegte Fälle | Entscheide von Alex über `status.py` | **jeder offene Fall mit Empfehlung** |
| Tägliche Pflege | abends | günstig | Repo-Zustand, Wächter | mechanische Korrekturen, Pflegenotiz, Views | nur Befunde, die Alex entscheiden muss |
| Wochen-Review | Samstag | stark | Aussortierte ohne hartes Kriterium | Feld `zweitpruefung` | Zweifelsfälle |
| Prozess-Retro | Sonntag | günstig | Audit, Log, Notizen, Lehren, Massnahmen | Retro-Notiz, neue Massnahmen | nur belastbare Prozessänderungen |
| Marktreport | monatlich | – | Log und Pipeline | `views/MARKTREPORT.md` | Monatsbefund |

## Regeln

1. **Modell nach Aufgabe:** Sichtung und Pflege auf dem günstigen Modell, die eigentliche Bewertung auf dem
   starken. Der Sweep liest nur die Arbeitskarte, nicht das ganze Regelwerk.
2. **Schreibziele sind Vertrag.** Eine Routine schreibt nur, was in der Spalte «Schreibt» steht. Neue
   Schreibziele zuerst gegen die Trust-Boundary in `AGENTS.md` prüfen.
3. **Wirkung messen, nicht vermuten.** Nach einer Änderung (Frequenz, Modell, Vorscan) wird zwei Wochen lang
   gemessen (`scripts/umbau_kontrolle.py`, `scripts/prozess_retro.py`), bevor weiter umgebaut wird.
