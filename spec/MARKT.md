# MARKT – monatliche Marktbeobachtung (Blöcke A bis D)

Regelwerk für das Modell. Das Screening ([`SWEEP.md`](SWEEP.md), werktäglich) fragt «Welche Stellen gibt es?»,
der Marktreport (`scripts/marktreport.py`, wöchentlich) «Welcher Kanal liefert, warum fallen Stellen raus?».
Diese Routine fragt monatlich: **Was verlangt der Markt an KI-Fähigkeiten, wer bekommt die Stellen, die Alex
wollte, und wo steht Alex dagegen?** Jede Aussage über Alex stützt sich auf
[`persona/PROFILE.md`](../persona/PROFILE.md); Massnahmen empfiehlt das Modell, entscheiden tut Alex.

**Warum monatlich:** Anzeigen wechseln täglich, Anforderungen und Besetzungen über Monate; wöchentlich wäre es
Rauschen. Eine Einmalerhebung scheitert an der Fallzahl, und die lässt sich nur durch Zeit beheben.

## Leitprinzipien

- **Blind kodieren.** Wer kodiert, sieht nur Anzeigentext und Schema, nicht `PROFILE.md` und nicht den Ausgang.
- **Schema eingefroren.** Änderungen nur als Nachtrag mit Datum und Grund, nie rückwirkend. Sonst sind die
  Übereinstimmungswerte wertlos, und Regeln lassen sich nachschärfen, bis das Ergebnis passt.
- **Jede Zahl mit Fallzahl und Zeitraum.** **«Nicht gefunden» ist ein Ergebnis**, kein Anlass zum Raten.

## Block A – Nachfrage

- **Grundgesamtheit:** alle im Zeitraum neu abgelegten Anzeigen (`stellen/*/`, `eingang/*/`, Datei
  `<id>--anzeige--<datum>.md`, Datum = Erfassung). Volltext verbatim (Hard-Gate in [`AGENTS.md`](../AGENTS.md))
  und mit SHA-256 ablegen: Anzeigen verschwinden oft kurz nach der Kodierung.
- **Einschluss:** KI muss in **Aufgaben oder Anforderungen** stehen. KI nur im Firmenteil ergibt K00.
- **Kodierung** nach [`ki_kodierschema.json`](ki_kodierschema.json), Mehrfachkodierung erlaubt. Gezählt wird je
  Anzeige, ob eine Kategorie vorkommt, nicht wie oft. «Von Vorteil», «idealerweise» u. ä. = Wunsch, sonst Muss.

| ID | Kategorie | löst aus (Kurzfassung, Volltext und Beispiele im Schema) |
|---|---|---|
| K01 | KI-Anwendungsfälle priorisieren | Use Cases finden, bewerten, priorisieren; Business Case; Anbieterwahl |
| K02 | LLM-Produkte betreiben | vom Pilot in den Betrieb, skalieren, überwachen, Kosten steuern |
| K03 | Evaluation und Qualitätsmessung | Testfälle, Metriken, Abnahmeschwellen für KI-Ergebnisse |
| K04 | Daten- und Governance-Kompetenz | Datengrundlage sichern; KI-Richtlinien und Prüfprozesse |
| K05 | Prompt- und Agenten-Praxis | Prompts, KI-Agenten, Automatisierung, Retrieval, Low-Code-Assistenten |
| K06 | Change und Enablement | KI einführen, Mitarbeitende befähigen, Adoption messen |
| K07 | Regulierung und Risiko | EU AI Act, Datenschutz bei KI, verantwortungsvolle KI |
| K08 | Technische Tiefe und Hands-on | eigene Technikarbeit: Modelle trainieren, Python, MLOps |
| K09 | Allgemeines KI-Verständnis | Affinität, Grundkenntnis, erste Erfahrung, ohne Tätigkeit |
| K00 | Keine KI-Anforderung | keine der obigen Kategorien in Aufgaben und Profil |

**Kodierregeln** (vollständig im Schema): nur Wortlaut · KI-Bezug im Satz selbst · Verantwortung für ein
Ergebnis löst aus (Tätigkeit, Begleitaufgabe, Zielzustand der Rolle), eine blosse Eigenschaft nicht · **Wissen
ist nicht Handarbeit:** «Verständnis für ML-Verfahren» ist K09, nicht K08; «unser Stack umfasst …» ist kein
Code · im Zweifel die schwächere Lesart, als unsicher markiert · passt nichts: Code «NEU» mit Vorschlag.

## Methodik – Kodierung, Zweitkodierung, Übereinstimmung

1. **Erstkodierung** durch das Modell, blind, je Code mit Zitat. **Zweitkodierung** von mindestens 20 % durch
   ein anderes Modell in getrenntem Arbeitsbereich, ohne Zugriff auf die Erstcodes. Zwei Instanzen desselben
   Modells irren gleich: ihre Übereinstimmung ist eine Obergrenze, keine Bestätigung.
2. **Übereinstimmung messen:** Cohen-Kappa je Kategorie über das Vorkommen je Anzeige, dazu die mittlere
   Jaccard-Ähnlichkeit der Codemengen (`python3 scripts/marktcheck.py --zweitkodierung <datei>`). Ziel ≥ 0.70.
3. **Audit am Wortlaut:** Stichprobe von 10 % der Codes gegen den Text, Urteil korrekt / vertretbar / falsch,
   Ziel falsch ≤ 10 %. Das ist die eigentliche Gültigkeitsprüfung.

### Welche Zahlen belastbar sind

| Lage | So wird berichtet |
|---|---|
| Kappa ≥ 0.70 und Audit bestanden | Anteil mit 95 %-Wilson-Intervall |
| Kappa < 0.70 oder Kodierer liegen > 12 Prozentpunkte auseinander | **nur als Spanne beider Kodierer**, nie als Punktwert; Schlüsse darauf als unsicher markiert |
| weniger als 10 Anzeigen | keine Anteile, nur Anzahl |

- **Wilson-Intervalle sind eine Untergrenze der Unsicherheit, nicht ihr Mass:** Die Anzeigen stammen aus den
  eigenen Suchbegriffen und Kanälen, nicht aus einer Zufallsstichprobe. Das steht bei jeder Intervallangabe.
- **Randverteilungen halten, Einzelzuordnungen nicht:** Einzelne Anzeigen sind Beispiele, keine Befunde.
  Kategorien mit Auslegungsspielraum (Betrieb als Zielzustand, Verständnis gegen Tätigkeit) zuerst prüfen.

## Block B – Besetzung (pseudonymisiert)

**Ziel:** Welches Profil bekommt Stellen, die Alex wollte, und wo liegt die Kompetenzlücke? Der einzige direkte
Kontrast: nicht irgendwer in einer KI-Rolle, sondern wer genau die Stelle bekam, auf die Alex eine Absage erhielt.

- **Auslöser:** Fälle mit Absage. Zuerst Absagen nach einem Gespräch (wer gewann, gewann direkt gegen Alex),
  dann Dossier-Absagen. Fehlen Rolle oder Bereich im Fall, zuerst bei Alex ergänzen, nicht blind suchen.
- **Suchfenster:** frühestens fünf Monate nach der Absage (Kündigungsfrist, Profilpflege), dann höchstens alle
  zwei Monate; nach vier erfolglosen Suchen oder zwölf Monaten gilt die Stelle als nicht auffindbar.
- **Aufnahme nur bei eindeutiger Übereinstimmung:** gleicher Arbeitgeber, gleiche oder klar entsprechende Rolle,
  Eintritt nach der Absage. Monatlich höchstens so viele Profile öffnen, wie die Quote braucht (5 bis 8).

| Feld (`data/besetzung.json`, dazu `pseudonym` P001 …, `fall_id`, `firma`, `rolle`, `erhoben_am`) | Werte |
|---|---|
| `jahre_rollentyp` | Jahre in einer vergleichbaren Produktrolle (ganze Zahl) |
| `vorbranche` | Branche der vorherigen Station, nie deren Arbeitgeber |
| `vorstufe` | Product Owner · Senior PO/PM · Lead/Head of Product · andere Funktion |
| `abschluss` | Informatik/Technik · Wirtschaft · andere · unbekannt |
| `ki_belege` | ja / nein (KI-Rolle oder KI-Projekt im Profil sichtbar) |
| `wechsel` | intern / extern |

**Schutzregeln, verbindlich:**

- Nur **öffentlich sichtbare, rollenrelevante** Merkmale aus der Tabelle. **Keine Namen, keine Profil-Links,
  keine Fotos, keine Freitexte über Personen.** Keine sensiblen Merkmale (Alter, Geschlecht, Herkunft,
  Gesundheit, Familie, Aufenthaltsstatus). Unbekanntes bleibt leer.
- **Pseudonym-Schlüssel** (Pseudonym → Person) liegt ausserhalb des Repos und wird **nie versioniert**.
  `data/besetzung.json` bleibt wie die Pipeline privat; öffentlich sind nur erfundene Demo-Einträge.
- **Nur aggregiert berichten:** Gruppen und Zellen ab 5 Fällen, sonst «unter 5» bzw. «zu wenig Fälle»; Median ab 10.
- **Keine Kontaktaufnahme** zu erhobenen Personen, in keiner Form.
- **Abbruchregeln:** Sicherheitsprüfung, Warnung oder CAPTCHA → sofort abbrechen, melden, nicht umgehen.
  Nicht eindeutig auffindbar → nicht erheben, nicht raten.

**Grenzen:** Interne Besetzungen bleiben oft unsichtbar, Funde häufen sich in kleinen Firmen. Wer genommen wurde, sagt nicht, warum.

## Block C – Position

- Je Kategorie die **Nachfrage** (Block A) gegen die **Beleglage** in [`persona/belege.json`](../persona/belege.json)
  (abgeleitet aus `PROFILE.md`): belegt → trägt · teilweise → Beleg schärfen (ab 10 % Nachfrage) ·
  Lücke → **Lücke mit Gewicht** (ab 10 %) oder «kaum verlangt».
- Block B gegen Alex' Werte: Jahre im Rollentyp, Stufe, Abschluss, KI-Belege, Branchennähe, interner Wechsel.
- **Alex' Werte nach denselben Regeln** wie die der Gruppe (z. B. Jahre mit Roadmap-Hoheit, nicht alle
  Berufsjahre). Ein Bezugswert ohne nachgerechnete Herleitung wird nicht verwendet.
- **Die Vergleichsgruppe wird erweitert, nicht neu gezogen.** Sonst misst man zwei Dinge gleichzeitig.
- Je Lücke mit Gewicht **eine Massnahme**: konkret, prüfbar, mit dem Beleg, der danach existiert.

## Block D – Eigenanalyse

Die eigenen Fälle sind eine Vollerhebung, ohne Stichprobenproblem. Monatlich fortgeschrieben:

- **Trichter** gesichtet → Volltext → vorgelegt → beworben → Einladung → Angebot und **Ausschlussgründe**
  (`scripts/marktreport.py`, `scripts/marktbild.py`); **Kanäle** (`scripts/kanal_auswertung.py`);
  **Raster gegen Ergebnis** (`scripts/analyse_fit_v2.py`).
- Nur **abgeschlossene Kohorten** vergleichen. Absagegründe passiv aus dem Absagetext, nie durch Nachfragen.
- Das Feld `**Publiziert:**` in jeder Anzeige ist Pflicht; es lässt sich rückwirkend nicht nachholen.

## Nullmessung vor Massnahmen

Bevor eine Massnahme greift (CV-Änderung, neues Projekt, andere Suchbegriffe), wird der Stand festgehalten:
Nachfrage je Kategorie, Beleglage, Trichter mit Einladungsquote je Kohorte, mit Datum und Messvorschrift
(`notes/<datum>_nullmessung_markt.md`). Wiederholt wird frühestens nach sechs Monaten. Ohne Nullmessung
lässt sich nicht sagen, ob eine Massnahme etwas bewirkt hat.

## Was die Routine nicht kann

- Sie misst den **erreichbaren** Markt (eigene Suchbegriffe, Kanäle), nicht den Markt.
- Sie **erklärt keine Absagen.** Block B kennt nur besetzte, auffindbare Stellen, und bei Überangebot wird oft
  nach Kriterien entschieden, die nicht in der Anzeige stehen.
- **Die Stichwort-Variante** (`scripts/marktcheck.py`) erkennt weder Wissen gegen Tätigkeit noch
  Umschreibungen ohne Stichwort. Sie ist die deterministische Demo; im Betrieb kodiert das Modell.
- **Was mit der Zeit dazukommt:** nach einem Monat breite Intervalle, nach etwa sechs Monaten halb so breite und
  erste Block-B-Verteilungen, nach etwa zwölf Monaten eine Zeitachse und Segmente (Branche, intern gegen extern).

## Bericht an Alex

Höchstens eine Seite, Vorlage [`demo/texte/marktbericht.md`](../demo/texte/marktbericht.md), in dieser Reihenfolge:
**Was folgt daraus** (Massnahmen) · **was sich gegenüber dem Vormonat bewegt hat** (stabile Werte nicht
wiederholen) · **neue Fallzahl** und was dadurch erstmals belastbar wird · **Dein Stand** (Block C, B) ·
**was die Zahlen nicht hergeben** (fest eingebaut). Kategorien ausgeschrieben, die ID höchstens in Klammern.

## Ablage und Aufruf

| Was | Wo |
|---|---|
| Kodierschema (eingefroren) | `spec/ki_kodierschema.json` |
| Beleglage und Vergleichswerte der Persona | `persona/belege.json` |
| Besetzungen, pseudonymisiert | `data/besetzung.json`; Schlüssel ausserhalb des Repos |
| Zweitkodierung | `data/zweitkodierung_<JJJJ-MM>.json` (`{fall_id: [IDs]}`) |
| Monatsbericht | `notes/<JJJJ-MM>_marktbeobachtung.md` |

Aufruf: `python3 scripts/marktcheck.py [--monat JJJJ-MM | --von … --bis …] [--schreiben]` (Standard: Vormonat
auf stdout) und `--zweitkodierung <datei>` für Kappa je Kategorie.
