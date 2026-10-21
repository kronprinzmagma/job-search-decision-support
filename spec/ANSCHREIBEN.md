# ANSCHREIBEN – Motivationsschreiben

Regelwerk für das Modell. Gilt für jedes Motivationsschreiben und für Portalantworten (Freitextfelder in
Bewerbungsportalen). Grundlage sind Anzeige, Firmen-Recherche ([`RECHERCHE.md`](RECHERCHE.md)), Personen-Recherche
([`PERSONEN.md`](PERSONEN.md)) und [`persona/PROFILE.md`](../persona/PROFILE.md). Der Coach entwirft und druckt;
**den Versand entscheidet Alex.** Im Schweizer Markt ist das Anschreiben eine Filterstufe und wird gelesen: Wo ein
Upload möglich ist, geht eines mit.

## Harte Formregeln

| Regel | Wert | Geprüft durch |
|---|---|---|
| Länge | **genau eine A4-Seite**; Richtwert 180–240 Wörter Brieftext in der Vorlage | `anschreiben_pdf.py` (FAIL bei mehr als einer Seite) |
| Sprache | Schweizer Hochdeutsch, durchgehend «ss» (kein Eszett) | Checkliste |
| Ort/Datum | Schweizer Langform: `Zürich, 24. März 2025` (Tag ohne Null, Monat ausgeschrieben) | `check_anschreiben_format.py` (Warnung) |
| Gruss | «Freundliche Grüsse» | `check_anschreiben_format.py` (Warnung) |
| Schrift, Farben, Kopf | fest in der Vorlage, nie im Text überschrieben | `check_anschreiben_format.py` |
| Betreff | konkrete Stellenbezeichnung wie in der Anzeige | Checkliste |
| Anrede | mit Namen, wenn Anzeige, Mail oder Personen-Recherche eine zuständige Person **belegt**; sonst «Sehr geehrte Damen und Herren» | Checkliste |
| Layout | keine Tabellen, Textboxen, Grafiken im Brieftext | Vorlage, Checkliste |
| Dateien | `Motivationsschreiben-Alex Müller-<Firma>-<Stelle>-<JJMMDD>` als `.md`, `.html`, `.pdf` im Fall-Ordner | Wächter in `jobcoach.py` |

## Quell-MD (Felder der Vorlage)

```markdown
# Bewerbung als Senior Product Owner

**Grundlage:** quendor-versicherungen-senior-product-owner--recherche--2025-03-20, quendor-versicherungen-senior-product-owner--personen--2025-03-20, quendor-versicherungen-senior-product-owner--anzeige, persona/PROFILE.md
**Empfänger:** Quendor Versicherungen AG · Personalabteilung · Zürich
**Ort/Datum:** Zürich, 24. März 2025

Sehr geehrte Damen und Herren

<Brieftext, Absätze durch Leerzeilen>

**Gruss:** Freundliche Grüsse
**Beilagen:** Lebenslauf
```

`# Titel` wird zum Betreff, « · » trennt die Empfängerzeilen, der Absender steht fest in der Vorlage, `**Grundlage:**` wird **nie gedruckt**.

## PDF – nur aus der Vorlage

1. Text steht, Quell-MD liegt im Fall-Ordner.
2. `python3 scripts/anschreiben_pdf.py "eingang/<id>/<Stamm>.md"` füllt `vorlagen/Motivationsschreiben-Template.html`
   ab und druckt sie mit Chromium headless (A4, ohne Kopf- und Fusszeile).
3. Das Skript ruft am Ende `scripts/check_anschreiben.py` (Producer = Browser-Druck, Grundlage-Zeile) und
   `scripts/check_anschreiben_format.py` (Vorlage unverändert laut SHA-256, eine Seite, A4, Schrift, Farben,
   Ort/Datum, Gruss) auf. **Nur bei PASS wird das PDF gemeldet.**
4. Nach dem Versand durch Alex: `python3 scripts/status.py <id> abgeschickt --quelle <Pfad zum PDF>`.

- **Nie im Code nachbauen** (ReportLab u. ä.): Ein Nachbau sieht ungefähr gleich aus und driftet jedes Mal.
  **Die Vorlage wird nie geändert**; neu festhalten (`--vorlage-pinnen`) nur auf ausdrückliche Anweisung von Alex.
- **Der Coach druckt selbst.** Fehlt Chromium: `CHROME_BIN` setzen; scheitert das nachweislich, melden und die
  abgefüllte `.html` liefern.

## Pflicht-Grundlage

- **Vor dem ersten Satz ganz lesen:** Anzeige, Recherche, Personen-Datei, `persona/PROFILE.md`. Fehlt eine
  Begleitdatei, wird sie zuerst erstellt.
- **Firmenbezug nur aus ✓-Fakten** (Recherche, Zone A); Annahmen (~) und Offenes (?) nie als Tatsache.
- **Aufhänger** (Zone B) sind Kandidaten; der Beleg dahinter wird in `persona/PROFILE.md` nachgelesen.
- **Sperrliste** (Zone C) wird Punkt für Punkt gegen den Entwurf gehalten.
- **Personen-Datei steuert, erscheint aber nicht:** Anrede, Register, Gewichtung; keine Namen Dritter im Text
  ausser in der Anrede, keine Zitate oder Spiegelungen aus Profilen.
- **Genau eine Zeile `**Grundlage:**`**, entweder
  `<id>--recherche--<stand>, <id>--personen--<stand>, <id>--anzeige, persona/PROFILE.md`
  oder `ohne Recherche-Dokumente – <Grund>` (nur wenn Alex es entscheidet oder es keine Anzeige gibt).
  `check_anschreiben.py` prüft: die genannte Recherche gehört zu diesem Fall, im Ordner liegt genau eine datierte,
  ein genanntes Datum stimmt.
- **Sichtbar machen:** Mit dem Entwurf nennt der Coach, welche Aufhänger verwendet sind und welche nicht, und das
  Ergebnis der Sperrlisten-Prüfung. Ob die Dokumente inhaltlich einbezogen sind, prüft kein Skript.
- **Portalantworten** (`Portalantworten-…md`): gleiche Regeln, Grundlage-Zeile im Kopf vor dem ersten `---` bzw. `##`.

## Ton (Schweizer Senior-Markt)

- **Sachlich-bescheiden, direkt und höflich:** keine Superlative, kein Bittsteller-Ton, keine Konjunktiv-Demut.
- **Fakten statt Adjektive:** jede Behauptung mit Beleg (Zahl, Umfang, konkretes Projekt).
- **Aktiv-Verben statt Nominalstil:** «Ich habe das Team aufgebaut» statt «Verantwortlich für den Aufbau des Teams».
- **Register wie der Lebenslauf** (ruhig, erfahren, belegt); ein Aufhänger, die übrige Erfahrung als gleichwertige Säule.

## Aufbau in vier Blöcken

| Block | Inhalt | Beispiel (Persona, fiktive Firma) |
|---|---|---|
| 1 Einstieg | klares Statement mit Bezug auf Rolle oder Firma, **eine** Verkaufs-Achse | «Quendor will das Kundenportal zur Self-Service-Plattform ausbauen. Genau diese Arbeit habe ich in den letzten sechs Jahren mit eigener Roadmap verantwortet.» |
| 2 Eignung (1–2 Absätze) | Anforderungen der Anzeige auf Belege gemappt, keine Skill-Liste | Teamführung bis 12 Personen, KI-Piloten von der Anbieter-Evaluation bis zum Betrieb |
| 3 Firmenbezug | was die Firma laut Recherche gerade bewegt, kein Lob um des Lobes willen | ✓-Fakt aus Zone A, verbunden mit der Erfahrung im regulierten Umfeld |
| 4 Abschluss | knapp, Ausblick auf das Gespräch | «Gerne zeige ich Ihnen im Gespräch, wie ich dabei vorgehe.» |

## Du oder Sie

**Test:** Du nur, wenn die Firma das Du **ausdrücklich auf den Bewerbungsprozess** bezieht. Reiner Du-Ton der Anzeige
(«Deine Aufgaben») ist Kultur, keine Einladung.

| Signal | Entscheid | Anrede |
|---|---|---|
| Du bezogen auf die Bewerbung, Kontaktperson belegt | Du | «Guten Tag <Vorname>» |
| Du bezogen auf die Bewerbung, keine Kontaktperson | Du | «Liebes <Team>-Team» |
| Du nur als Ton der Anzeige | Sie (Risiko asymmetrisch) | «Sehr geehrte Frau <Nachname>» oder «Sehr geehrte Damen und Herren» |
| kein Signal | Sie | wie oben |

Der Gruss bleibt in beiden Fällen «Freundliche Grüsse».

## Anti-Muster

- Floskel-Einstieg («Hiermit bewerbe ich mich …»); Text, der zu jeder Firma passt; Lebenslauf in Prosa
- Skill-Aufzählung ohne Bezug zur Stelle; Füllsätze; Schachtelsätze
- Anzeigen-Echo als Slogan; Abgrenzungs-Rhetorik, die andere abwertet; Beweisdruck statt Souveränität

## KI-Zeitalter: Authentizität

Die Trennlinie ist nicht «KI ja oder nein», sondern **generisch oder belegt**. Konkrete, nachprüfbare Eigenheiten
lassen sich nicht aus einem Prompt erzeugen; sie sind die beste Signatur.

| Statt (generisch) | Besser (belegt) |
|---|---|
| «Ich bringe umfassende Erfahrung in der digitalen Transformation mit.» | «Ich verantworte seit sechs Jahren die Roadmap eines B2B-Self-Service-Portals.» |
| «Ich bin nicht nur Produktmensch, sondern auch Teamplayer.» | «Ich führe ein Team aus Entwicklung, Design und Daten mit bis zu zwölf Personen.» |
| «KI ist für mich nicht Hype, sondern Haltung.» | «Ich habe einen KI-Piloten von der Anbieter-Evaluation bis in den Betrieb geführt.» |

**Typische Tells streichen:** Dreierfiguren, «nicht nur … sondern auch», Antithesen «nicht X, sondern Y»,
Superlativ-Häufung, glatte Übergangsfloskeln, Gedankenstrich-Inflation, aphoristische Schlusssätze.
**Schluss-Pass ist Pflicht:** Stimmt jeder Beleg? Klingt ein Satz nach Verkauf statt nach Alex? Ist der Firmenbezug
belegt oder geraten?

## ATS (maschineller Vorfilter)

- Das ATS prüft Lesbarkeit und Begriffe, nicht die KI-Herkunft. **Begriffe der Anzeige nur, wo belegt**, in echten
  Sätzen; kein Keyword-Stuffing. Die Vorlage liefert ein sauberes Text-PDF.
- **Portal-Feld «Kenntnisse»:** Schnittmenge Anzeige ∩ Beleg im Wortlaut der Anzeige; Recherche-Vokabular nie.

## Checkliste vor dem Absenden

- [ ] Anzeige, Recherche, Personen-Datei und `persona/PROFILE.md` ganz gelesen; Grundlage-Zeile gesetzt
- [ ] Firmenbezug nur aus ✓-Fakten; Sperrliste gegen den Text gehalten; Aufhänger genannt
- [ ] Einstieg ohne Floskel, eine Verkaufs-Achse, jede Stärke mit Beleg
- [ ] auf die Aufgaben der Anzeige gemappt; belegte Begriffe der Anzeige in echten Sätzen
- [ ] Du/Sie nach dem Test; Anrede nur mit belegter Person
- [ ] Aktiv-Verben, kein Hype, kein Eszett, KI-Tells gestrichen
- [ ] `anschreiben_pdf.py` ohne FAIL: eine Seite, Vorlage unverändert, Ort/Datum und Gruss korrekt
- [ ] Versand und Statuswechsel erst nach dem Entscheid von Alex
