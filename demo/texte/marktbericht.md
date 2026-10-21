# Marktbeobachtung {monat}

**Zeitraum:** {zeitraum} · **Anzeigen kodiert:** {n_anzeigen} · Regelwerk `spec/MARKT.md` · erzeugt mit
`python3 scripts/marktcheck.py` (Stichwort-Variante der Demo; im Betrieb kodiert das Modell mit Zweitkodierung)

Lesereihenfolge für Alex: zuerst «Was folgt daraus», dann die Blöcke. Jede Zahl steht mit ihrer Fallzahl.

## Was folgt daraus (Vorschläge, Entscheid bei Alex)

{massnahmen}

## A – Nachfrage: welche KI-Fähigkeiten die Anzeigen verlangen

Gezählt wird je Anzeige, ob eine Kategorie vorkommt (Mehrfachnennung möglich). Kodiert sind nur Aufgaben
und Anforderungen, nicht der Firmenteil. «Nur Wunsch»: ausschliesslich als «von Vorteil» o. ä. verlangt.

{tabelle_nachfrage}

## B – Besetzung: wer die Stellen bekommt, die Alex wollte (pseudonymisiert)

Nur öffentlich sichtbare, rollenrelevante Merkmale, nur aggregiert. Gruppen und Zellen unter 5 Fällen werden
nicht ausgewiesen; ein Median erst ab 10 Fällen.

{tabelle_besetzung}

## C – Position: Nachfrage gegen Alex' Beleglage

Beleglage aus `persona/PROFILE.md` (Zusammenfassung in `persona/belege.json`). «Lücke mit Gewicht» heisst:
nicht belegt und in mindestens 10 % der Anzeigen verlangt.

{tabelle_position}

## D – Eigenanalyse: die eigenen Fälle im Zeitraum

Vollerhebung, keine Stichprobe. Vertiefung: `scripts/marktreport.py` (Trichter, Ausschlussgründe),
`scripts/marktbild.py` (Vorfilter und Volltext je Grund), `scripts/kanal_auswertung.py` (Kanäle),
`scripts/analyse_fit_v2.py` (sagt das Raster Einladungen voraus?).

{tabelle_eigen}

## Was die Zahlen nicht hergeben

- **Erreichbarer Markt, nicht der Markt:** gemessen wird, was die eigenen Suchbegriffe und Kanäle finden.
- **Stichwort statt Urteil:** Die Demo-Kodierung erkennt weder Wissen gegen Tätigkeit noch Umschreibungen
  ohne Stichwort. Belastbar ist erst die Modellkodierung mit gemessener Zweitkodierung.
- **Besetzungen erklären keine Absage:** Sie zeigen, welches Profil genommen wurde, nicht welches Kriterium
  den Ausschlag gab. Interne Besetzungen und nicht gepflegte Profile fehlen.
- **Ein Monat ist eine Momentaufnahme:** Veränderungen erst gegen die Nullmessung und über mehrere Monate lesen.
