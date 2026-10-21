#!/usr/bin/env python3
"""Marktreport — was die Screenings über den Markt und über die Suche sagen.

Zweck: im Nachhinein aus den Sweeps einen Markt- und Bewerbungsreport bauen, der zeigt, wo die Probleme
liegen, weshalb Stellen nicht in Frage kommen und was daraus für Suche und Dossier folgt.

Quellen (beide deterministisch, nichts wird von Hand gepflegt):
  data/screening_log.json  — jede gesichtete Anzeige mit Entscheid und Grund, jeder Abfrage-Lauf
  data/pipeline.json       — jeder bewertete Fall mit Begründung, Status, Verlauf und fit_v2

Erzeugt MARKTREPORT.md. Aufruf:
  python3 scripts/marktreport.py            # Report schreiben
  python3 scripts/marktreport.py --stdout   # nur ausgeben
"""
import json, re, sys, unicodedata
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from heute import heute  # noqa: E402

LOG = ROOT / "data" / "screening_log.json"
PIPE = ROOT / "data" / "pipeline.json"
OUT = ROOT / "views" / "MARKTREPORT.md"

# Blocker-Muster: wonach in den Begründungen gesucht wird (auf norm()-Text: klein, ohne Akzente,
# deshalb je Umlaut beide Schreibweisen: «ue» und «u»). Reihenfolge = Priorität.
BLOCKER = [
    ("Benannter Fähigkeits-Ausschluss (Payment)", r"payment|zahlungsverkehr|acquiring"),
    ("Fachwissen in fremder Domäne", r"ausschluss 6|kernf(ae|a)higkeits|vertieftes verst|tiefes .*wissen|tiefes verst|"
                                     r"fundierte kenntnis|dom(ae|a)nen-?(luecke|lucke|mismatch)|sektor-mismatch|"
                                     r"branchenanforderung|jahre? (branchen|sektor|dom(ae|a)nen)"),
    ("Kein Produktmandat / falscher Rollentyp", r"kein produkt-?mandat|ohne produkt-?mandat|roadmap-hoheit fehlt|"
                                                r"nicht-rolle|kein digitales produkt|rollen-typ"),
    ("Draft verfallen / nie eingereicht", r"draft-bereinigung|nie eingereicht|nicht versendet|zur(ue|u)ckgezogen"),
    ("Rückschritt / zu kleines Mandat", r"ausschluss 5|r(ue|u)ckschritt|scope-mismatch nach unten|ticket-(ue|u)bersetzer|"
                                        r"setzt tickets um|kein lernschritt"),
    ("Führungsanforderung", r"people manager|disziplinarisch|f(ue|u)hrungsanforderung|f(ue|u)hrungsl(ue|u)cke|"
                            r"f(ue|u)hrung von f(ue|u)hrungskr"),
    ("Kein Homeoffice / Präsenzpflicht", r"ausschluss 3|kein homeoffice|100 ?% vor ort"),
    ("Formale Zugangsvoraussetzung", r"hochschulabschluss|formalkriterium|informatik-studium|zertifizierung|"
                                     r"abschluss in informatik"),
    ("Kompetenzdistanz (Chance tief)", r"kompetenzdistanz|chance tief|verdikt tief"),
    ("Engineering-/Entwicklerrolle", r"engineering|entwickler"),
    ("Distanz / Pendelzeit", r"ausschluss 2|pendelzeit|(?<!kompetenz)distanz"),
    ("Vermittler / Aggregator", r"vermittler|staffing|aggregator|personaldienstleist"),
    ("Beratung / Agentur", r"ausschluss 4|beratung|consulting|agentur"),
    ("Junior / zu tiefes Level", r"ausschluss 1|junior|praktikum|trainee"),
    ("Physisches Produktmanagement", r"physisch|maschinen|hardware|lebensmittel"),
    ("Firmen-Ausschluss der Persona", r"firmen-ausschluss|gl(ue|u)cksspiel"),
    ("Rollen-Präferenz der Persona", r"rollen-pr(ae|a)ferenz|ui-design|figma"),
    ("Dublette (anderer Kanal)", r"dublette|bereits gesichtet"),
    ("Anzeige nicht mehr verfügbar", r"nicht mehr verf(ue|u)gbar|fehlerseite"),
    ("Entscheid Alex", r"entscheid alex|alex-entscheid|manuell aussortiert"),
]
BEWORBEN = {"abgeschickt", "in_pruefung", "gespraech", "abgesagt", "angebot"}


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def laden():
    log = json.loads(LOG.read_text(encoding="utf-8")) if LOG.exists() else {"gesichtet": [], "laeufe": []}
    pipe = json.loads(PIPE.read_text(encoding="utf-8"))
    def eintraege(o):
        if isinstance(o, list):
            for x in o:
                yield from eintraege(x)
        elif isinstance(o, dict):
            if "id" in o and "firma" in o:
                yield o
            for v in o.values():
                yield from eintraege(v)
    return log, list(eintraege(pipe))


def blocker(text):
    t = norm(text)
    return [name for name, muster in BLOCKER if re.search(muster, t)]


def ereignisse(f):
    return {v.get("ereignis") for v in f.get("verlauf") or []}


def beworben(f):
    return f.get("status") in BEWORBEN or "versand" in ereignisse(f) or bool(f.get("datum_eingereicht"))


def bau():
    log, faelle = laden()
    ges = log["gesichtet"]
    laeufe = log["laeufe"]
    z = []
    w = z.append

    w("# MARKTREPORT — was das Screening über den Markt sagt")
    w("")
    w(f"**Generiert:** {heute().isoformat()} · `python3 scripts/marktreport.py` · **nicht von Hand editieren**")
    w(f"**Datenbasis:** {len(ges)} gesichtete Anzeigen aus {len(laeufe)} Abfrage-Läufen, {len(faelle)} bewertete Fälle in der Pipeline.")
    w("")
    w("Dieser Report beantwortet drei Fragen: **Warum kommen Stellen nicht in Frage? Welcher Kanal liefert? "
      "Was folgt daraus für Suche und Dossier?**")
    w("")

    # --- 1. Trichter
    w("## 1 — Der Trichter")
    w("")
    ent = Counter(e["entscheid"] for e in ges)
    total = len(ges)
    bew = [f for f in faelle if beworben(f)]
    einl = [f for f in bew if "einladung" in ereignisse(f) or f.get("status") in ("gespraech", "angebot")]
    absage = [f for f in bew if f.get("status") == "abgesagt"]
    absage_dossier = [f for f in absage if "einladung" not in ereignisse(f)]
    angebot = [f for f in bew if f.get("status") == "angebot"]
    w("| Stufe | Anzahl | Anteil |")
    w("|---|---:|---:|")
    if total:
        w(f"| Gesichtet (Listenebene) | {total} | 100% |")
        volltext = ent.get("kandidat", 0) + ent.get("volltext-nogo", 0)
        w(f"| Volltext geprüft | {volltext} | {volltext*100//total}% |")
        w(f"| Als Kandidat vorgelegt | {ent.get('kandidat', 0)} | {ent.get('kandidat', 0)*100//total}% |")
    w(f"| Beworben (Versand erfolgt) | {len(bew)} | — |")
    w(f"| Einladung zum Gespräch | {len(einl)} | {f'{len(einl)*100//len(bew)}% der Bewerbungen' if bew else '—'} |")
    w(f"| Absagen (davon ohne Gespräch) | {len(absage)} ({len(absage_dossier)}) | — |")
    w(f"| Angebote | {len(angebot)} | — |")
    w("")
    if bew:
        w(f"**Harte Zahl:** {len(bew)} Bewerbungen, {len(einl)} Einladungen, {len(absage_dossier)} Absagen schon "
          f"nach der Dossierprüfung. Die Einladungsquote ist der eigentliche Engpass, nicht die Zahl der gefundenen "
          f"Stellen. Ob das Raster sie vorhersagt: `python3 scripts/analyse_fit_v2.py`.")
        w("")

    # --- 2. Warum Stellen nicht in Frage kommen
    w("## 2 — Warum Stellen nicht in Frage kommen")
    w("")
    w("### 2a Auf Listenebene (Vorfilter, ohne Volltext)")
    w("")
    vf = Counter()
    for e in ges:
        if e["entscheid"] in ("vorfilter", "dublette", "geschlossen"):
            for b in blocker(e.get("grund", "")) or ["nicht klassifiziert"]:
                vf[b] += 1
    for k, v in vf.most_common():
        w(f"- **{v}×** {k}")
    w("")
    w("### 2b Nach Volltextprüfung (die inhaltlich naheliegenden Fälle)")
    w("")
    vt = Counter()
    beispiele = defaultdict(list)
    for f in faelle:
        if f.get("status") != "aussortiert":
            continue
        bs = blocker(f.get("begruendung", "")) or ["nicht klassifiziert"]
        for b in bs[:2]:
            vt[b] += 1
            if len(beispiele[b]) < 4:
                beispiele[b].append(f"{f['firma']} ({f.get('rolle', '')[:45]})")
    for k, v in vt.most_common():
        w(f"- **{v}×** {k}")
        if beispiele[k]:
            w(f"  - {' · '.join(beispiele[k])}")
    w("")
    echt = [(k, v) for k, v in vt.most_common() if k not in ("nicht klassifiziert", "Entscheid Alex")]
    if echt:
        w(f"**Befund:** Der häufigste Grund, warum eine inhaltlich passende Stelle ausfällt, ist **{echt[0][0]}** ({echt[0][1]} Fälle).")
        if len(echt) > 1:
            w(f"An zweiter Stelle: {echt[1][0]} ({echt[1][1]}).")
    if vt.get("nicht klassifiziert"):
        w("")
        w(f"*{vt['nicht klassifiziert']} Begründungen liessen sich nicht automatisch einordnen — meist frei formuliert. "
          f"Bei jeder neuen Begründungsart die Musterliste in `scripts/marktreport.py` prüfen.*")
        w("")

    # --- 3. Kanal-Ertrag
    w("## 3 — Welcher Kanal liefert?")
    w("")
    kanal_ges = Counter(e["kanal"] for e in ges)
    kanal_kand = Counter(e["kanal"] for e in ges if e["entscheid"] == "kandidat")
    kanal_vt = Counter(e["kanal"] for e in ges if e["entscheid"] in ("kandidat", "volltext-nogo"))
    w("| Kanal | gesichtet | volltextwürdig | Kandidaten |")
    w("|---|---:|---:|---:|")
    for k, v in kanal_ges.most_common():
        w(f"| {k} | {v} | {kanal_vt.get(k, 0)} | {kanal_kand.get(k, 0)} |")
    w("")
    if kanal_kand:
        best = kanal_kand.most_common(1)[0]
        w(f"**Ertragreichster Kanal bisher:** {best[0]} mit {best[1]} Kandidaten.")
    leer = [k for k in kanal_ges if kanal_vt.get(k, 0) == 0 and kanal_ges[k] >= 3]
    if leer:
        w("")
        # Kein Streichungsvorschlag: drei Monate ohne Treffer heissen nicht, dass in Monat vier keine Anzeige
        # kommt. Ziel- und Behördenportale werden nicht wegen Ertrag gestrichen, nur wenn sie inhaltlich nicht
        # mehr passen. Die Zahl bleibt als Beobachtung stehen.
        w(f"**Kanäle ohne einen einzigen volltextwürdigen Treffer:** {', '.join(sorted(leer))}. "
          f"Das ist eine Beobachtung, kein Streichungsgrund — Ziel- und Behördenportale bleiben im Delta-Betrieb "
          f"ohnehin billig.")
    w("")

    # --- 3b. Begriffs-Ertrag (Feld `gefunden_ueber`)
    begriffe = [e for e in ges if e.get("gefunden_ueber") and "nicht protokolliert" not in e["gefunden_ueber"]]
    w("### Welcher Suchbegriff liefert?")
    w("")
    if not begriffe:
        w("Noch keine Sichtung mit dem Feld `gefunden_ueber` — der Begriffs-Ertrag ist erst ab dem nächsten Lauf messbar.")
        w("")
    else:
        b_ges = Counter(e["gefunden_ueber"] for e in begriffe)
        b_kand = Counter(e["gefunden_ueber"] for e in begriffe if e["entscheid"] == "kandidat")
        b_vt = Counter(e["gefunden_ueber"] for e in begriffe if e["entscheid"] in ("kandidat", "volltext-nogo"))
        w("| Begriff / Portal | gesichtet | volltextwürdig | Kandidaten |")
        w("|---|---:|---:|---:|")
        for k, v in b_ges.most_common():
            w(f"| {k} | {v} | {b_vt.get(k, 0)} | {b_kand.get(k, 0)} |")
        w("")
        tot = [k for k, v in b_ges.items() if v >= 10 and b_vt.get(k, 0) == 0]
        if tot:
            w(f"**Begriffe ohne einen einzigen volltextwürdigen Treffer (>=10 Sichtungen):** {', '.join(sorted(tot))}. "
              f"Kandidaten für «ausrangiert» in `data/screening_kanaele.json` — Entscheid Alex.")
            w("")

    # --- 4. Was der Markt anbietet
    w("## 4 — Was der Markt in diesem Zeitraum überhaupt anbot")
    w("")
    firmen = Counter(e["firma"] for e in ges)
    w(f"- **{len(firmen)} verschiedene Arbeitgeber** in den gesichteten Anzeigen.")
    mehrfach = [f"{k} ({v})" for k, v in firmen.most_common() if v > 1]
    if mehrfach:
        w(f"- Mehrfach vertreten: {' · '.join(mehrfach[:12])}")
    orte = Counter(e.get("ort", "").split("/")[0].strip() for e in ges if e.get("ort"))
    w(f"- Häufigste Arbeitsorte: {' · '.join(f'{k} ({v})' for k, v in orte.most_common(8))}")
    w("")

    # --- 5. Lehren
    w("## 5 — Lehren und konkrete Anpassungen")
    w("")
    w("*Automatisch abgeleitet aus den Zahlen oben. Vorschläge gehen an Alex, nicht eigenmächtig ins Regelwerk.*")
    w("")
    vorschlaege = []
    if echt:
        b1, n1 = echt[0]
        if b1 == "Fachwissen in fremder Domäne":
            vorschlaege.append(
                f"**Suchbegriffe:** «{b1}» blockiert {n1} inhaltlich nahe Fälle. Konsequenz für die Suche: Rollen "
                f"bevorzugen, deren Gegenstand die ARBEITSWEISE ist (Plattform, Self-Service, Enablement, KI-Einführung), "
                f"nicht ein Fachgebiet. Diese Begriffe gehören nach vorne in `data/screening_kanaele.json`.")
            vorschlaege.append(
                "**Zielfirmen:** Der Domänen-Anker schlägt den Titel. Firmen aus den in `persona/PROFILE.md` belegten "
                "Umfeldern (Gesundheit, Versicherung, B2B-Software) direkt und regelmässig auf ihren Karriereseiten "
                "prüfen — dort greift Ausschluss 6 seltener.")
        if b1 == "Benannter Fähigkeits-Ausschluss (Payment)":
            vorschlaege.append(
                f"**Vorfilter schärfen:** {n1}× fiel eine Stelle erst im Volltext am Payment-Ausschluss. Begriffe wie "
                f"«Payments», «Zahlungsverkehr», «Acquiring» im Titel gehören auf Listenebene in die Rauschregeln "
                f"(`scripts/vorscan_regeln.py`), damit kein Volltext mehr dafür gelesen wird.")
    if vf.get("Vermittler / Aggregator", 0) >= 5:
        vorschlaege.append(
            f"**Vorfilter:** {vf['Vermittler / Aggregator']} Vermittler-Inserate. Bei jedem mit anonymisiertem Kunden "
            f"prüfen, ob dieselbe Stelle auch direkt ausgeschrieben ist — die Direktbewerbung schlägt den Umweg.")
    if vt.get("Kein Produktmandat / falscher Rollentyp", 0) >= 3:
        vorschlaege.append(
            f"**Vorfilter schärfen:** {vt['Kein Produktmandat / falscher Rollentyp']}× wurde erst im Volltext klar, "
            f"dass die Rolle kein Produktmandat trägt. Die Aufgabenbegriffe (Roadmap, Backlog, Priorisierung, "
            f"Produktvision) als VOLLTEXTSUCHE einsetzen statt nur als Bewertungskriterium — fehlen sie in der "
            f"Anzeige, ist der Fall meist schon entschieden.")
    if vt.get("Führungsanforderung", 0):
        vorschlaege.append(
            f"**Dossier:** {vt['Führungsanforderung']}× an einer Führungsanforderung gescheitert. Entweder laterale "
            f"Führung im CV deutlich sichtbarer machen — oder Rollen mit «Führung von Führungskräften» als Muss "
            f"konsequent vorfiltern, statt Volltext zu lesen.")
    if vt.get("Kein Homeoffice / Präsenzpflicht", 0) >= 3:
        vorschlaege.append(
            f"**Vorfilter:** {vt['Kein Homeoffice / Präsenzpflicht']}× stand die Präsenzpflicht erst im Volltext. "
            f"Wo die Trefferliste die Arbeitsform zeigt, schon dort filtern.")
    if kanal_kand.get("zielportal"):
        vorschlaege.append(
            f"**Zielportale:** {kanal_kand['zielportal']} Kandidaten kamen über Karriereseiten von Zielfirmen. Ob sie "
            f"nur dort standen, zeigt `python3 scripts/kanal_auswertung.py` (Spalte «nur hier»); wenn ja, ist die "
            f"Portalprüfung eine eigenständige Quelle und kein Zusatz.")
    for v in vorschlaege:
        w(f"- {v}")
    if not vorschlaege:
        w("- *(noch zu wenig Daten für belastbare Ableitungen — mindestens drei Läufe abwarten)*")
    w("")

    # --- 6. Grenze
    w("## 6 — Die Grenze dieses Reports, ausdrücklich")
    w("")
    w("Dieser Report misst, **was der Coach aussortiert** — nicht, **was der Markt über Alex denkt**. Die einzige "
      "echte Rückmeldung des Marktes sind Einladungen und Absagen; ihre Zahl ist klein. Alles unter Punkt 5 ist "
      "deshalb eine Hypothese über die Suche, keine Aussage über die Bewerbungschancen.")
    w("")
    w("Was den Report belastbarer macht: Absagegründe erfassen, wo sie genannt werden, und den Zeitpunkt der Absage "
      "(Dossierprüfung vs. nach dem Gespräch, Feld `stadium`). Erst dann lässt sich trennen, ob Dossiers am Filter "
      "oder am Gespräch scheitern.")
    w("")
    return "\n".join(z)


if __name__ == "__main__":
    text = bau()
    if "--stdout" in sys.argv:
        print(text)
    else:
        OUT.parent.mkdir(exist_ok=True)
        OUT.write_text(text + "\n", encoding="utf-8")
        print(f"MARKTREPORT.md geschrieben ({len(text.splitlines())} Zeilen).")
