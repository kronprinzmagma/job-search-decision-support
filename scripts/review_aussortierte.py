#!/usr/bin/env python3
"""Zweitprüfung der Aussortierten — wöchentlich, für alles ohne Hard-Gate.

Zweck: Einmal pro Woche die Aussortierten nochmals durchgehen, die kein Hard-Gate getroffen haben, ihre
Anzeigen im Detail lesen und Alex die Zweifelsfälle zeigen (Leitprinzip in spec/PRESCREEN.md: «Zweifel
gehen an Alex, nie in die Aussortierung»).

Die Idee: Ein Hard-Gate ist nachprüfbar und endgültig (Junior, Distanz, kein Homeoffice, Beratung, Payment,
Firmen-Ausschluss, Vermittler, Engineering, physisches Produkt, offensichtliche Nicht-Rolle, Stelle weg,
Dublette, Entscheid Alex). Alles andere ist ein URTEIL des Coaches — Ausschluss 5 (Rückschritt),
Ausschluss 6 (Kernfähigkeits-Lücke), Domänen- und Levellücke, Rollen-Präferenz, Kompetenzdistanz. Genau diese
Urteile werden einmal pro Woche gegen den Volltext gegengeprüft; im Zweifel geht der Fall an Alex.

Zwei Quellen:
  data/pipeline.json      — bewertete Fälle mit Status `aussortiert`
  data/screening_log.json — Anzeigen, die nur auf LISTENEBENE weggefallen sind (`vorfilter`),
                            also nie im Volltext gesehen wurden

Aufrufe:
  python3 scripts/review_aussortierte.py                 # fällige Fälle auflisten
  python3 scripts/review_aussortierte.py --alle          # auch schon geprüfte und harte zeigen
  python3 scripts/review_aussortierte.py --json          # maschinenlesbar
  python3 scripts/review_aussortierte.py --markiere <id> "<ergebnis>"
        # trägt {"datum": heute, "ergebnis": "..."} in pipeline.json ein (Feld `zweitpruefung`,
        # geschrieben über scripts/pipeline_tx.py)

Ergebnis-Werte für --markiere: bestaetigt | an-alex | reaktiviert | stelle-weg
"""
import json, re, sys, unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from heute import heute  # noqa: E402

PIPE = ROOT / "data" / "pipeline.json"
LOG = ROOT / "data" / "screening_log.json"

# Wie lange eine Zweitprüfung gilt, bevor ein Fall erneut fällig wird.
GUELTIG_TAGE = 56
# Älter als das ist die Stelle im Markt ohnehin nicht mehr offen.
MAX_ALTER_TAGE = 90
ERGEBNISSE = ("bestaetigt", "an-alex", "reaktiviert", "stelle-weg")

# Hard-Gates: nachprüfbar, endgültig, keine Zweitprüfung nötig. Muster laufen auf norm()-Text
# (klein, ohne Akzente), deshalb je Umlaut beide Schreibweisen («ue» und «u»).
HARD = [
    ("Ausschluss 1 (Junior/Praktikum)", r"ausschluss 1\b|junior|praktikum|trainee|lehrstelle|werkstudent"),
    ("Ausschluss 2 (Distanz)", r"ausschluss 2\b|pendelzeit|(?<!kompetenz)distanz|zu weit|ortstabelle"),
    ("Ausschluss 3 (kein Homeoffice)", r"ausschluss 3\b|kein homeoffice|100 ?% vor ort"),
    ("Ausschluss 4 (Beratung/Agentur)", r"ausschluss 4\b|beratung|consulting|agentur"),
    ("Benannter Fähigkeits-Ausschluss Payment", r"payment|zahlungsverkehr|acquiring"),
    ("Firmen-Ausschluss (Glücksspielbranche)", r"firmen-ausschluss|gl(ue|u)cksspiel"),
    ("Vermittler", r"vermittler|personalvermittlung|staffing|headhunter"),
    ("Stelle nicht mehr offen", r"nicht mehr verf(ue|u)gbar|stelle weg|stelle wurde intern besetzt|zur(ue|u)ckgezogen"),
    ("Kein Schweizer Anstellungsverhältnis", r"kein schweizer anstellungsverh|ohne schweizer standortbindung"),
    ("Dublette", r"dublette|doppelt|bereits abgelegt|bereits aussortiert"),
    ("Aggregator/Jobplattform", r"aggregator|jobplattform"),
    ("Engineering-/Entwicklerrolle", r"engineering|entwickler"),
    ("Physisches Produkt", r"physisch|hardware|maschinen|lebensmittel|industrieprodukt"),
    # spec/SWEEP.md, «Listenebene»: offensichtliche Nicht-Rollen (Scrum Master, Business Analyst, UX) dürfen
    # ungeöffnet wegfallen. Steht vor WEICH, auch wenn der Grund zusätzlich «Ausschluss 5» nennt.
    ("Offensichtliche Nicht-Rolle (Listenebene)", r"nicht-rolle"),
    ("Entscheid Alex", r"entscheid alex|alex-entscheid|manuell aussortiert"),
]
# Weiche Urteile: genau die Fälle, die geprüft werden sollen.
WEICH = [
    ("Ausschluss 5 (Rückschritt)", r"ausschluss 5\b|r(ue|u)ckschritt|kein produkt-?mandat|ticket-(ue|u)bersetzer"),
    ("Ausschluss 6 (Kernfähigkeits-Lücke)", r"ausschluss 6\b|kernf(ae|a)higkeit"),
    ("Domänen-/Branchenlücke", r"dom(ae|a)nen|branchenl(ue|u)cke|sektor"),
    ("Level-/Führungslücke", r"f(ue|u)hrungsl(ue|u)cke|level-l(ue|u)cke|level-/f|seniorit"),
    ("Rollen-Präferenz", r"rollen-pr(ae|a)ferenz|ui-design|figma"),
    ("Kompetenzdistanz (Schritt 2)", r"kompetenzdistanz|chance tief|verdikt tief"),
]


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))


# Ein ausdrücklicher Entscheid von Alex ist ein Hard-Gate — auch wenn die Begründung mit «Ausschluss 6»
# beginnt und Alex erst im Fliesstext zitiert wird. Erkannt wird der Entscheid, NICHT die blosse Erwähnung
# («bei Alex unbelegt» ist ein Urteil des Coaches über Alex, kein Entscheid von Alex).
ALEX_ENTSCHEID = re.compile(r"entscheid alex|alex-entscheid|manuell aussortiert")
# Gegenprobe: «Einordnung Alex ausstehend» heisst das GEGENTEIL — der Fall wartet noch auf Alex
# und bleibt in der Zweitprüfung.
ALEX_OFFEN = re.compile(r"alex ausstehend|einordnung alex")


def kategorie(text):
    t = norm(text)
    if ALEX_ENTSCHEID.search(t) and not ALEX_OFFEN.search(t):
        return "hard", "Entscheid Alex"
    for name, muster in HARD:
        if re.search(muster, t):
            return "hard", name
    for name, muster in WEICH:
        if re.search(muster, t):
            return "weich", name
    return "weich", "ohne erkennbaren Grund"


def datum_von(a):
    for feld in ("datum", "datum_eingereicht"):
        if a.get(feld):
            try:
                return date.fromisoformat(a[feld][:10])
            except ValueError:
                pass
    return None


def faellig(eintrag, tag):
    zp = eintrag.get("zweitpruefung") or {}
    if not zp.get("datum"):
        return True
    try:
        return (tag - date.fromisoformat(zp["datum"][:10])).days > GUELTIG_TAGE
    except ValueError:
        return True


def sammeln(alle=False):
    tag = heute()
    pipe = json.loads(PIPE.read_text(encoding="utf-8"))
    out = []
    for a in pipe["applications"]:
        if a.get("status") != "aussortiert":
            continue
        art, grund = kategorie(f"{a.get('begruendung', '')} {a.get('notiz', '')}")
        d = datum_von(a)
        alter = (tag - d).days if d else None
        if art == "hard" and not alle:
            continue
        if alter is not None and alter > MAX_ALTER_TAGE and not alle:
            continue
        if not faellig(a, tag) and not alle:
            continue
        out.append({"quelle": "pipeline", "id": a["id"], "firma": a.get("firma", ""),
                    "rolle": a.get("rolle", ""), "datum": d.isoformat() if d else "",
                    "alter_tage": alter, "art": art, "grund": grund,
                    "anzeige": a.get("anzeige", ""),
                    "zweitpruefung": a.get("zweitpruefung", {}),
                    "begruendung": (a.get("begruendung") or "")[:400]})
    if LOG.exists():
        log = json.loads(LOG.read_text(encoding="utf-8"))
        for e in log.get("gesichtet", []):
            if e.get("entscheid") != "vorfilter":
                continue
            art, grund = kategorie(e.get("grund", ""))
            try:
                alter = (tag - date.fromisoformat(e["datum"])).days
            except (KeyError, ValueError):
                alter = None
            if art == "hard" and not alle:
                continue
            if alter is not None and alter > MAX_ALTER_TAGE and not alle:
                continue
            out.append({"quelle": "screening_log", "id": "", "firma": e.get("firma", ""),
                        "rolle": e.get("rolle", ""), "datum": e.get("datum", ""),
                        "alter_tage": alter, "art": art, "grund": grund or e.get("grund", ""),
                        "anzeige": "", "zweitpruefung": {},
                        "begruendung": e.get("grund", "")})
    out.sort(key=lambda x: (x["quelle"], x["datum"], x["id"]))
    return out


# Vorwarnfrist, bevor MAX_ALTER_TAGE einen Fall still aus der Liste wirft.
VORWARNUNG_TAGE = 21


def verfallswarnung(faelle):
    """Welche Fälle fallen demnächst ungeprüft aus der Liste — oder haben gar kein Datum?

    Anlass: Prüft die Routine je Lauf nur die zehn jüngsten Fälle, während MAX_ALTER_TAGE die ältesten nach
    90 Tagen still entfernt, erreicht die Prüfung bei stetem Zufluss die alten Fälle nie. Fälle ohne `datum`
    haben gar kein Alter und sortieren sich immer nach ganz oben, wo die Zehnerregel nie hinreicht.
    """
    out = []
    for f in faelle:
        if f["quelle"] != "pipeline":
            continue
        if f["alter_tage"] is None:
            out.append(f"OHNE DATUM (wird nie fällig, sortiert nie nach vorne): "
                       f"{f['firma']} — {f['rolle']} · id {f['id']}")
        elif f["alter_tage"] > MAX_ALTER_TAGE - VORWARNUNG_TAGE:
            rest = MAX_ALTER_TAGE - f["alter_tage"]
            out.append(f"verfällt in {rest} Tagen ({f['alter_tage']}d alt): "
                       f"{f['firma']} — {f['rolle']} · id {f['id']}")
    return out


def markieren(fall_id, ergebnis):
    """Schreibt das Feld `zweitpruefung` über den einzigen Schreibweg (Sperre, Konfliktprüfung)."""
    from pipeline_tx import transaktion, Konflikt
    if ergebnis not in ERGEBNISSE:
        print(f"Ergebnis «{ergebnis}» unbekannt. Erlaubt: {' | '.join(ERGEBNISSE)}")
        return 2
    tag = heute().isoformat()
    try:
        with transaktion(f"review_aussortierte.py --markiere {fall_id}") as pipe:
            treffer = [a for a in pipe["applications"] if a["id"] == fall_id]
            if not treffer:
                print(f"Kein Datensatz mit id {fall_id}")
                return 1
            treffer[0]["zweitpruefung"] = {"datum": tag, "ergebnis": ergebnis}
    except Konflikt as e:
        print(f"NICHT geschrieben: {e}")
        return 3
    print(f"{fall_id}: Zweitprüfung {tag} — {ergebnis}")
    return 0


def main():
    args = sys.argv[1:]
    if args and args[0] == "--markiere":
        if len(args) < 3:
            print(__doc__)
            return 2
        return markieren(args[1], args[2])
    alle = "--alle" in args
    faelle = sammeln(alle)
    if "--json" in args:
        print(json.dumps(faelle, ensure_ascii=False, indent=2))
        return 0
    aus_pipe = [f for f in faelle if f["quelle"] == "pipeline"]
    aus_log = [f for f in faelle if f["quelle"] == "screening_log"]
    print(f"ZWEITPRÜFUNG FÄLLIG — {len(aus_pipe)} bewertete Fälle, {len(aus_log)} nur "
          f"listengefilterte Anzeigen (Stand {heute().isoformat()})\n")
    warnungen = verfallswarnung(aus_pipe)
    if warnungen:
        print("!! VERFALLSWARNUNG — diese Fälle verschwinden ungeprüft aus der Liste:")
        for z in warnungen:
            print(f"   {z}")
        print()
    print("A) Bewertete Fälle ohne Hard-Gate (Volltext lesen, Urteil gegenprüfen):")
    for f in aus_pipe:
        alter = f"{f['alter_tage']}d" if f["alter_tage"] is not None else "OHNE DATUM"
        print(f"  [{f['datum'] or '—'}, {alter}] {f['firma']} — {f['rolle']}")
        print(f"      Grund damals: {f['grund']} · id {f['id']}")
        if f["anzeige"]:
            print(f"      Anzeige: {f['anzeige']}")
    if not aus_pipe:
        print("  keine")
    print("\nB) Nur auf Listenebene weggefallen — nie im Volltext gesehen:")
    for f in aus_log:
        print(f"  [{f['datum']}] {f['firma']} — {f['rolle']} ({f['grund']})")
    if not aus_log:
        print("  keine")
    print("\nVorgehen: Volltext aus der Primärquelle lesen, Ausschlüsse neu prüfen. "
          "Bestätigt -> `--markiere <id> bestaetigt`. Zweifel -> Alex vorlegen und "
          "`--markiere <id> an-alex`. Stelle weg -> `--markiere <id> stelle-weg`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
