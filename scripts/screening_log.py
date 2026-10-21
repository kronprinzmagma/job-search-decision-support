#!/usr/bin/env python3
"""Sichtungs-Log fuer das Stellen-Screening — damit jeder Lauf nur das Delta prueft.

Das Problem, das dieses Log loest: `data/pipeline.json` enthaelt nur Faelle, die es bis zu einer
Bewertung geschafft haben. Alles, was auf LISTENEBENE aussortiert wurde (Vermittler, Engineering,
Distanz, physisches Produkt), stand nirgends — und waere am naechsten Morgen erneut durchgegangen
worden. Je Lauf sind das Hunderte von Listeneintraegen.

Zwei Dinge werden gefuehrt:
  1. gesichtet  — jede Anzeige, die ein Auge gesehen hat, mit Entscheid und Grund.
  2. laeufe     — welcher Kanal wann mit welchem Filter abgefragt wurde, damit der
                  naechste Lauf das Zeitfenster kennt und Kanaele nicht doppelt macht.

Jeder Durchgang laeuft als SWEEP gegen den Soll-Katalog data/screening_kanaele.json
(Mechanik in scripts/screening_sweep.py, Arbeitskarte spec/SWEEP.md). Ablauf eines Sweeps:

  python3 scripts/screening_log.py start morgen|mittag|nachmittag  # Sweep anlegen / fortsetzen (Exit 3 = schon fertig, Exit 4 = andere Session laeuft)
  python3 scripts/vorscan.py uebernehmen                           # Jobportal ohne Modell (Vorscan)
  python3 scripts/screening_log.py naechste [--alle] [--kanal K]  # offene Katalog-Abfragen in Reihenfolge
  python3 scripts/screening_log.py check -                        # Trefferliste gegen das Log (Firma|Rolle je Zeile)
  python3 scripts/screening_log.py add     "Firma|Rolle|Ort|Kanal|Entscheid|Grund|GefundenUeber|Publiziert[|Anzeige]"   # SOFORT je Sichtung
  python3 scripts/screening_log.py abfrage "ID|Status|Gesichtet|Notiz"   # SOFORT nach jeder Abfrage (Status: ok|leer|teilweise|nicht-erreichbar|uebersprungen)
  python3 scripts/screening_log.py ende [--abbrechen "Grund"]     # Session schliessen; Sweep fertig bei 100 %; Audit-Datensatz
  python3 scripts/screening_log.py bericht [sweep-id] [--schreiben]   # erzeugter Bericht; --schreiben legt notes/<datum>_screening_<art>.md an

Weitere Aufrufe:
  python3 scripts/screening_log.py check   "Firma|Rolle"          # oder --datei <datei> / -
  python3 scripts/screening_log.py sweeps  [--tage N]             # Uebersicht der Sweeps
  python3 scripts/screening_log.py audit   [--aktualisieren [--alle|--tage N]]   # Audit-Datensaetze je Sweep
  python3 scripts/screening_log.py status                         # Sweeps heute, Kanal-Stand, Entscheide
  python3 scripts/screening_log.py delta   --tage 1               # was seit N Tagen neu ist
  python3 scripts/screening_log.py abdeckung [JJJJ-MM-TT|sweep-id] # Abdeckungs-Tabelle eines Tages bzw. Sweep-Bericht
  python3 scripts/screening_log.py ertrag                         # Ertrag je Kanal und Abfrage
  python3 scripts/screening_log.py titel                          # Titel im Markt, die im Katalog fehlen

Entscheide: kandidat | volltext-nogo | vorfilter | dublette | geschlossen | offen
Ausgabe von `check`: BEKANNT (gleiche Rolle) | PRUEFEN (aehnliche Rolle derselben Firma, von Hand
vergleichen) | NEU. Exit-Code 1 nur bei BEKANNT.
`Publiziert` (8. Feld von `add`): Veroeffentlichungsdatum, wie die Trefferliste es zeigt — daraus rechnet
die Prozess-Retro, wie alt eine Anzeige beim Fund war (Fundgeschwindigkeit).
`Anzeige` (9. Feld, Pflicht bei kandidat und volltext-nogo): Pfad der verbatim abgelegten Anzeige.

Kanalnamen sind eine feste Liste (KANAELE), keine Freitexte — sonst zaehlt der Marktreport
Schreibvarianten als eigene Kanaele. Das konkrete Portal gehoert in `abfrage`, nicht in `kanal`.
`gefunden_ueber` haelt den Suchbegriff bzw. die Abfrage fest, mit der die Anzeige aufgetaucht ist;
ohne dieses Feld laesst sich nicht messen, welche Abfrage traegt (Grundlage jeder Ausrangierung).
"""
import json
import os
import re
import sys
import unicodedata
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import heute as uhr  # noqa: E402
import publiziert  # noqa: E402
import screening_log_tx as tx  # noqa: E402
import screening_sweep as sw  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "data" / "screening_log.json"


def norm(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c)).replace("ss", "s")
    # ae/oe/ue gleich behandeln wie ä/ö/ü («Gruenwald» = «Grünwald»)
    s = s.replace("ae", "a").replace("oe", "o").replace("ue", "u")
    s = re.sub(r"\b(ag|sa|gmbh|holding|group|gruppe|co|und|and|the)\b", " ", s)
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


KANAELE = ["netzwerk-suche", "netzwerk-tracker", "netzwerk-empfehlung", "portal",
           "zielportal", "behoerdenportal", "karriereseite", "abo", "netzwerk", "manuell"]

# Freitext -> Kanal. Reihenfolge zaehlt: das Spezifische zuerst (zielportal vor portal).
ALIAS = [
    ("netzwerk-tracker", "netzwerk-tracker"), ("job-tracker", "netzwerk-tracker"), ("tracker", "netzwerk-tracker"),
    ("netzwerk-empfehlung", "netzwerk-empfehlung"), ("empfehlung", "netzwerk-empfehlung"),
    ("netzwerk-suche", "netzwerk-suche"), ("netzwerk suche", "netzwerk-suche"),
    ("behoerdenportal", "behoerdenportal"), ("verwaltung", "behoerdenportal"), ("kanton", "behoerdenportal"),
    ("stadt", "behoerdenportal"), ("gemeinde", "behoerdenportal"), ("bund", "behoerdenportal"),
    ("zielportal", "zielportal"), ("zielfirma", "zielportal"),
    ("karriereseite", "karriereseite"),
    ("jobportal", "portal"), ("stellenportal", "portal"), ("portal", "portal"),
    ("abo", "abo"), ("jobagent", "abo"), ("suchabo", "abo"),
    ("netzwerk", "netzwerk"), ("manuell", "manuell"), ("alex", "manuell"),
]


def kanal_norm(roh):
    """Freitext-Kanal auf die feste Liste abbilden. Gibt (kanal, rest) zurueck;
    `rest` ist der Originalwert, wenn er zusaetzliche Information traegt (Portalname)."""
    r = (roh or "").strip()
    if r in KANAELE:
        return r, ""
    low = norm(r)
    for muster, ziel in ALIAS:
        if norm(muster) and norm(muster) in low:
            return ziel, r
    return (r or "unbekannt"), ""


def laden():
    if LOG.exists():
        return json.loads(LOG.read_text(encoding="utf-8"))
    return {"gesichtet": [], "laeufe": [], "sweeps": []}


def speichern(d):
    # Atomar schreiben (Massnahme 2025-03-16-log-sperre): temporaere Datei, dann umbenennen,
    # damit ein paralleler Leser nie eine halb geschriebene Datei sieht.
    tmp = LOG.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, LOG)


# Fuellwoerter und Pensum-/Genderzusaetze zaehlen beim Rollenvergleich nicht. Anlass: zwei Fuellwoerter
# («fur die») machten neue, fremde Inserate derselben Firma zu «schon gesichtet».
ROLLEN_STOPP = {"fur", "die", "der", "das", "den", "dem", "des", "und", "in", "im", "mit", "von", "vom",
                "zu", "zur", "zum", "auf", "an", "am", "bei", "als", "oder", "a", "of", "for", "to", "on",
                "at", "with", "w", "m", "d", "f", "h", "x", "alle", "all", "genders", "gender",
                "mba", "befristet", "per", "sofort"}


def _rollenwoerter(n):
    return {w for w in n.split() if w not in ROLLEN_STOPP and not w.isdigit() and len(w) > 1}


def vergleich(nr, er):
    """Rollenvergleich bei gleicher Firma. Zwei gemeinsame Rollenwoerter reichen nicht fuer «bekannt»:
    sonst werden Reposts und neue Stellen derselben Firma als «schon gesichtet» gefuehrt.
      gleich   - gleiche Rolle: Wortmengen gleich, oder die kuerzere (>= 2 Woerter) steckt ganz in
                 der laengeren und es fehlt hoechstens ein Wort
      aehnlich - mindestens zwei gemeinsame Rollenwoerter, sonst verschieden: von Hand vergleichen
      firma    - nur die Firma stimmt ueberein"""
    if not nr or not er:
        return "firma"
    if nr == er:
        return "gleich"
    a, b = _rollenwoerter(nr), _rollenwoerter(er)
    if a and a == b:
        return "gleich"
    k, l = (a, b) if len(a) <= len(b) else (b, a)
    if len(k) >= 2 and k <= l and len(l) - len(k) <= 1:
        return "gleich"
    if len(a & b) >= 2:
        return "aehnlich"
    return "firma"


def treffer(firma, rolle, daten):
    """Alle Log-Eintraege derselben Firma mit Vergleichsstufe gleich | aehnlich | firma."""
    nf, nr = norm(firma), norm(rolle)
    out = []
    for e in daten["gesichtet"]:
        ef = norm(e.get("firma"))
        if not ef or not nf:
            continue
        # ganze Woerter statt Teilstring: «Kalvit» passt sonst in «Kalvitra», «Sorvik» in «Sorvikon»
        if f" {nf} " in f" {ef} " or f" {ef} " in f" {nf} ":
            out.append((e, vergleich(nr, norm(e.get("rolle")))))
    return out


RANG = {"gleich": 0, "aehnlich": 1, "firma": 2}


def cmd_check(args, d):
    """Ausgabe je Zeile:
      BEKANNT  - dieselbe Rolle steht schon im Log -> nicht oeffnen
      PRUEFEN  - aehnliche Rolle derselben Firma im Log -> Rolle von Hand vergleichen (Repost?)
      NEU      - nicht im Log (ggf. mit Hinweis auf andere Rollen derselben Firma) -> oeffnen
    Exit-Code 1, wenn mindestens eine Zeile BEKANNT ist."""
    if args and args[0] == "-":
        paare = [l.strip().split("|") for l in sys.stdin if l.strip()]
    elif args and args[0] == "--datei":
        paare = [l.strip().split("|") for l in Path(args[1]).read_text(encoding="utf-8").splitlines() if l.strip()]
    else:
        paare = [args[0].split("|")] if args else []
    if not paare:
        print(__doc__); return 2
    bekannt = False
    marken = {"gleich": "gleiche Rolle", "aehnlich": "aehnliche Rolle - von Hand vergleichen",
              "firma": "gleiche Firma, andere Rolle"}
    for p in paare:
        firma = p[0].strip(); rolle = (p[1] if len(p) > 1 else "").strip()
        tr = sorted(treffer(firma, rolle, d), key=lambda x: (RANG[x[1]], x[0].get("datum") or ""))
        stufe = tr[0][1] if tr else None
        if stufe == "gleich":
            bekannt = True
            print(f"BEKANNT    | {firma} | {rolle}")
        elif stufe == "aehnlich":
            print(f"PRUEFEN    | {firma} | {rolle}")
        else:
            print(f"NEU        | {firma} | {rolle}")
        for e, st in tr[:4]:
            print(f"           -> {marken[st]}: {e['firma']} — {e['rolle']} "
                  f"[{e['entscheid']}, {e['datum']}, {e['kanal']}]")
            if st != "firma" and e.get("grund"):
                print(f"              Grund: {e['grund']}")
        if len(tr) > 4:
            print(f"           -> ... und {len(tr) - 4} weitere Eintraege derselben Firma")
    return 1 if bekannt else 0


_SAMMEL = re.compile(r"\b(\d+|rund\s+\d+|ca\.?\s*\d+|zwei|drei|vier|f(?:ue|ü)nf|sechs|sieben|acht|neun|zehn|mehrere|diverse|div\.|alle)"
                     r"\s+(?:\w+\s+){0,2}(weitere|Treffer|Stellen|Inserate|Anzeigen|Zeilen|Eintr)", re.I)


def _ablage_pruefen(t, kanal):
    """Ein im Volltext geprufter Fall (volltext-nogo, kandidat) wird nur mit dem Pfad der abgelegten
    Anzeige als 9. Feld angenommen (Hard-Gate Quelle, feedback/2025-03-25_bewertung-auf-paraphrase.md).
    Fehlt der Datensatz in pipeline.json, legt dieser Befehl ihn selbst an — ein Befehl, ein Schritt."""
    pfad = (t[8] if len(t) > 8 else "").strip()
    if not pfad or "--anzeige--" not in pfad or not (ROOT / pfad).is_file():
        return None, ("Volltext-Fall ohne abgelegte Anzeige. Zuerst stellen/<id>/<id>--anzeige--<datum>.md "
                      "(bei Kandidaten eingang/<id>/…) mit Kopfblock und Text 1:1 schreiben, dann den Pfad als 9. Feld angeben.")
    fid = Path(pfad).parent.name
    try:
        from pipeline_tx import transaktion
        with transaktion(f"screening_log.py add ({fid})") as data:
            apps = data["applications"]
            if not any(a.get("id") == fid or a.get("anzeige") == pfad for a in apps):
                heute = uhr.heute().isoformat()
                kand = t[4] == "kandidat"
                r = {"id": fid, "firma": t[0], "rolle": t[1], "standort": t[2],
                     "quelle": f"{kanal} — Volltext {heute}; Fund via {t[6]}".strip(),
                     "status": "vorgelegt" if kand else "aussortiert", "datum": heute,
                     "anzeige": pfad, "dossier": str(Path(pfad).parent),
                     "verlauf": [{"datum": heute, "ereignis": "vorgelegt" if kand else "nogo",
                                  "quelle": "screening_log.py add", "notiz": t[5][:200]}]}
                if not kand:
                    r["begruendung"] = t[5]
                apps.append(r)
                return pfad, f"Datensatz {fid} angelegt ({r['status']})"
    except Exception as ex:
        return None, f"Datensatz nicht anlegbar ({ex}) — spaeter erneut eintragen"
    return pfad, None


def cmd_add(args, d):
    for roh in args:
        t = [x.strip() for x in roh.split("|")]
        while len(t) < 8:
            t.append("")
        # Sperre: eine Zeile = eine Anzeige. Sammelzeilen sind fuer den Abgleich unsichtbar und
        # kommen im naechsten Lauf als NEU zurueck.
        if (_SAMMEL.search(t[0] + " " + t[1]) or "sammelposten" in (t[0] + t[1] + t[5]).lower()) \
                and "BEWUSST ALS SAMMELPOSTEN" not in t[5].upper():
            print(f"  ! ABGELEHNT (Sammelzeile): «{t[0]} | {t[1][:60]}» — jede Anzeige einzeln eintragen (Firma|Rolle je Zeile).")
            continue
        kanal, rest = kanal_norm(t[3])
        if kanal not in KANAELE:
            print(f"  ! unbekannter Kanal «{t[3]}» — erlaubt: {', '.join(KANAELE)}")
        anzeige = None
        if t[4] in ("volltext-nogo", "kandidat"):
            anzeige, meldung = _ablage_pruefen(t, kanal)
            if not anzeige:
                print(f"  ! ABGELEHNT (Ablage): «{t[0]} | {t[1][:60]}» — {meldung}")
                continue
            if meldung:
                print(f"  + {meldung}")
        s_akt = sw.aktueller_sweep(d)
        heute = uhr.heute()
        e = {"firma": t[0], "rolle": t[1], "ort": t[2], "kanal": kanal,
             "entscheid": t[4] or "vorfilter", "grund": t[5],
             "datum": heute.isoformat(), "gefunden_ueber": t[6] or rest,
             "lauf_id": s_akt["id"] if s_akt else "", "zeit": sw.jetzt()[11:]}
        # 8. Feld Publiziert, wie in der Trefferliste angezeigt: «2025-04-02», «02.04.2025», «Gestern»,
        # «vor 4 Stunden», «3 days ago». Relative Angaben werden auf heute gerechnet. Leer = Liste zeigt keins.
        if t[7]:
            pub = publiziert.parse(t[7], heute)
            e["publiziert_roh"] = t[7]
            if pub:
                e["publiziert"] = pub.isoformat()
                alter = (heute - pub).days
                if e["entscheid"] in ("kandidat", "offen") and alter > publiziert.ALT_SCHWELLE_TAGE:
                    print(f"  ! Anzeige ueber eine Woche alt ({alter} Tage) — im Kandidatenblock vermerken")
            else:
                print(f"  ! Publiziert «{t[7]}» nicht lesbar — als Rohtext gespeichert")
        if not s_akt:
            print("  ! kein offener Sweep — Sichtung ohne lauf_id geloggt. Vorher: screening_log.py start <art>")
        if not e["gefunden_ueber"]:
            print("  ! GefundenUeber fehlt — Ertrag dieser Abfrage ist nicht messbar")
        if anzeige:
            e["anzeige"] = anzeige
        d["gesichtet"].append(e)
        print(f"+ {e['firma']} — {e['rolle']} [{e['entscheid']}]")
    speichern(d)
    return 0


def cmd_status(d):
    heute = uhr.heute()
    print(f"Sichtungs-Log: {len(d['gesichtet'])} Anzeigen, {len(d['laeufe'])} Kanal-Laeufe, "
          f"{len(d.get('sweeps', []))} Sweeps\n")
    kat, aktive = sw.katalog()
    print(f"SWEEPS HEUTE ({heute}) — Katalog {kat.get('version', '')}, {len(aktive)} aktive Abfragen:")
    heutige = [x for x in d.get("sweeps", []) if x["datum"] == heute.isoformat()]
    for art in ("morgen", "mittag", "nachmittag", "zusatz"):
        for x in [y for y in heutige if y["art"] == art] or ([None] if art != "zusatz" else []):
            if not x:
                print(f"  {art:11s} NOCH NICHT GESTARTET")
                continue
            ist, soll, feh = sw._stand(d, x, aktive)
            print(f"  {art:11s} {x['status']:15s} {ist}/{soll} abgedeckt, "
                  f"{len(x.get('sessions', []))} Session(s), {len(sw._sicht(d, x))} Sichtungen")
    akt = sw.aktueller_sweep(d)
    akt = akt if akt and akt.get("status") == "offen" else None
    print(f"\nLAUFENDER SWEEP: {akt['id'] if akt else 'keiner'} — "
          f"{'weiter mit: screening_log.py naechste' if akt else 'starten mit: screening_log.py start <morgen|mittag|nachmittag>'}")

    print("\nLETZTER LAUF JE KANAL:")
    letzte = {}
    for l in d["laeufe"]:
        k = l["kanal"]
        if k not in letzte or (l["datum"], l.get("zeit", "")) > (letzte[k]["datum"], letzte[k].get("zeit", "")):
            letzte[k] = l
    for k in sorted(letzte, key=lambda x: (letzte[x]["datum"], letzte[x].get("zeit", ""))):
        l = letzte[k]
        alter = (heute - datetime.strptime(l["datum"], "%Y-%m-%d").date()).days
        print(f"  {l['datum']} {l.get('zeit', '')[:5]:5s} ({alter}d)  {k}: {l['abfrage'][:70]}")

    print("\nENTSCHEIDE:")
    z = {}
    for e in d["gesichtet"]:
        z[e["entscheid"]] = z.get(e["entscheid"], 0) + 1
    for k, v in sorted(z.items(), key=lambda x: -x[1]):
        print(f"  {v:4d}  {k}")
    offen = [e for e in d["gesichtet"] if e.get("entscheid") == "offen"]
    if offen:
        print(f"\nOFFEN (Volltext ausstehend): {len(offen)} — " + "; ".join(f"{e['firma']} — {e['rolle']}" for e in offen[:6]))
    return 0


# Wie oft lief eine Abfrage ueberhaupt? Ohne diese Zahl liest sich «0 Kandidaten» nach EINEM Lauf
# gleich wie nach zwanzig — und genau daraus wuerden Ausrangierungen abgeleitet, die die Daten nicht tragen.
MIN_LAEUFE = 4


def cmd_ertrag(d):
    """Was hat je Kanal und je Abfrage tatsaechlich einen Kandidaten geliefert?"""
    def zaehle(schluessel):
        z = {}
        for e in d["gesichtet"]:
            k = (e.get(schluessel) or "—").strip() or "—"
            a = z.setdefault(k, {"gesichtet": 0, "kandidat": 0})
            a["gesichtet"] += 1
            if e.get("entscheid") == "kandidat":
                a["kandidat"] += 1
        return z

    def laeufe_je(schluessel):
        z = {}
        for e in d["gesichtet"]:
            k = (e.get(schluessel) or "—").strip() or "—"
            z.setdefault(k, set()).add(e.get("datum"))
        return {k: len(v) for k, v in z.items()}

    for titel, schluessel in (("ERTRAG JE KANAL", "kanal"),
                              ("ERTRAG JE ABFRAGE", "gefunden_ueber")):
        print(f"\n{titel}:")
        z = zaehle(schluessel)
        lf = laeufe_je(schluessel)
        duenn = 0
        for k, a in sorted(z.items(), key=lambda x: (-x[1]["kandidat"], -x[1]["gesichtet"])):
            n = lf.get(k, 0)
            if a["kandidat"] == 0 and n < MIN_LAEUFE:
                marke = "  <-- noch keine Aussage"
                duenn += 1
            else:
                marke = ""
            print(f"  {a['kandidat']:3d} Kandidaten / {a['gesichtet']:4d} gesichtet / {n:2d} Tage   {k}{marke}")
        if duenn:
            print(f"\n  {duenn} Zeile(n) mit 0 Kandidaten stehen auf weniger als {MIN_LAEUFE} "
                  f"Lauftagen — sie tragen KEINE Ausrangierung, auch nicht als Tendenz.")
    if "—" in zaehle("gefunden_ueber"):
        print("\n  Hinweis: Eintraege ohne `gefunden_ueber` zaehlen nicht in die Auswertung je Abfrage.")
    return 0


def cmd_titel(d):
    """Welche Rollentitel sind im Markt aufgetaucht, die in keiner Katalog-Abfrage stehen?

    Anlass: Passende Stellen tragen manchmal Titel, nach denen niemand sucht. Die Begriffsliste kann nie
    vollstaendig sein — also wird sie aus dem gemessen, was das Screening ohnehin sieht. Jeder gesichtete
    Titel wird in Wortgruppen zerlegt und gegen die Suchbegriffe des Katalogs («…» in name/abfrage)
    gehalten. Was mehrfach vorkommt und nirgends steht, ist ein Vorschlag fuer den Katalog — Entscheid Alex.
    """
    kat, _ = sw.katalog()
    bekannt = set()
    for a in kat["abfragen"]:
        for m in re.finditer(r"«([^»]+)»", f"{a.get('name', '')} {a.get('abfrage', '')}"):
            bekannt.add(norm(m.group(1)))
    rausch = {"m", "w", "d", "a", "in", "der", "die", "das", "und", "fur", "im", "bei", "mit",
              "von", "zur", "zum", "of", "for", "and", "the", "senior", "junior", "lead",
              "100", "80", "60", "stv", "ch", "de", "en"}

    def gruppen(titel):
        worte = [w for w in norm(titel).split() if w and w not in rausch and not w.isdigit()]
        raus = set()
        for i in range(len(worte)):
            raus.add(worte[i])
            if i + 1 < len(worte):
                raus.add(f"{worte[i]} {worte[i + 1]}")
        return raus

    zaehler, beispiele = {}, {}
    for e in d["gesichtet"]:
        titel = e.get("rolle") or ""
        if not titel:
            continue
        for g in gruppen(titel):
            if any(g in b or b in g for b in bekannt):
                continue
            zaehler[g] = zaehler.get(g, 0) + 1
            beispiele.setdefault(g, []).append(f"{e.get('firma', '')} — {titel}")

    tr = sorted(((g, n) for g, n in zaehler.items() if n >= 2 and " " in g), key=lambda x: -x[1])
    print("TITEL-INVENTAR — Wortgruppen aus gesichteten Anzeigen, die in keiner Katalog-Abfrage stehen")
    print("(nur Zweiwortgruppen ab 2 Vorkommen; Einzelwoerter waeren zu unscharf)\n")
    if not tr:
        print("  keine — der Katalog deckt die gesichteten Titel ab.")
        return 0
    for g, n in tr[:25]:
        print(f"  {n:3d}x  {g}")
        for b in beispiele[g][:2]:
            print(f"         z. B. {b}")
    print("\nVorgehen: Was inhaltlich zu Alex' Suchraum gehoert, als Abfrage vorschlagen (Entscheid Alex). "
          "Was Rauschen ist, ignorieren — die Liste ist ein Vorschlagsgenerator, kein Automatismus.")
    return 0


def cmd_delta(args, d):
    tage = int(args[args.index("--tage") + 1]) if "--tage" in args else 1
    grenze = (uhr.heute() - timedelta(days=tage)).isoformat()
    neu = [e for e in d["gesichtet"] if e["datum"] > grenze]
    print(f"{len(neu)} Anzeigen seit {grenze}:")
    for e in neu:
        print(f"  {e['datum']} {e['entscheid']:14s} {e['firma']} — {e['rolle']}")
    return 0


def cmd_abdeckung(args, d):
    """abdeckung [JJJJ-MM-TT | sweep-id] — Abdeckung eines Tages ueber alle Sweeps.

    Mit Sweep-ID: der erzeugte Sweep-Bericht (der massgebende Weg). Mit Datum: eine Zeile je Kanal mit
    Gefunden/Neu/Kandidat/Aussortiert/Offen, damit «was ist mit dem Rest» keine offene Frage bleibt,
    danach je Sweep des Tages die Abdeckung gegen das Soll.
    """
    arg = args[0] if args and not args[0].startswith("--") else uhr.heute().isoformat()
    kat, aktive = sw.katalog()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}-(%s)" % "|".join(sw.ARTEN), arg):
        print(sw.bericht_text(d, sw.aktueller_sweep(d, arg), aktive)); return 0
    laeufe = [l for l in d["laeufe"] if l.get("datum") == arg]
    sicht = [e for e in d["gesichtet"] if e.get("datum") == arg]
    print(f"# ABDECKUNG {arg}\n")
    if not laeufe:
        print("Keine Kanal-Laeufe an diesem Datum protokolliert.")
        return 0
    print("## Uebersicht nach Kanal\n")
    print("| Kanal | Gefunden | Neu | davon Kandidat | davon Aussortiert | davon Offen |")
    print("|---|---|---|---|---|---|")
    kanaele = sorted({l.get("kanal", "") for l in laeufe},
                     key=lambda k: sw.KANAL_REIHENFOLGE.index(k) if k in sw.KANAL_REIHENFOLGE else 99)
    tot = [0] * 5
    for k in kanaele:
        sk = [e for e in sicht if e.get("kanal") == k]
        werte = (sum((l.get("gesichtet_n") or 0) for l in laeufe if l.get("kanal") == k), len(sk),
                 sum(1 for e in sk if e.get("entscheid") == "kandidat"),
                 sum(1 for e in sk if e.get("entscheid") in sw.AUSSORTIERT),
                 sum(1 for e in sk if e.get("entscheid") == "offen"))
        tot = [a + b for a, b in zip(tot, werte)]
        print(f"| {k} | " + " | ".join(str(v) for v in werte) + " |")
    print("| **Total** | " + " | ".join(f"**{v}**" for v in tot) + " |\n")
    print("Lesehilfe: *Gefunden* ist die Listengroesse aus den Abfrage-Laeufen (dieselbe Anzeige kann ueber "
          "mehrere Abfragen auftauchen). *Neu* ist, was nicht schon im Sichtungs-Log stand; *Neu* zerfaellt "
          "restlos in Kandidat + Aussortiert + Offen.\n")
    print("## Sweeps des Tages\n")
    for s in sorted((x for x in d.get("sweeps", []) if x["datum"] == arg), key=sw._reihenfolge):
        ist, soll, feh = sw._stand(d, s, aktive)
        print(f"- {s['id']} [{s['status']}]: {ist}/{soll} abgedeckt"
              + (f", fehlend: {', '.join(a['id'] for a in feh[:10])}" if feh else ""))
    offen = [e for e in d["gesichtet"] if e.get("entscheid") == "offen"]
    print("\n## Noch offen im ganzen Log (Volltext ausstehend)\n")
    if not offen:
        print("Keine. Kein Eintrag im Log steht auf `offen`.")
    for e in offen:
        print(f"- {e.get('firma')} — {e.get('rolle')} ({e.get('kanal')}, seit {e.get('datum')})")
    return 0


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    cmd, args = sys.argv[1], sys.argv[2:]
    befehle = {"check": lambda: cmd_check(args, d),
               "add": lambda: cmd_add(args, d),
               "status": lambda: cmd_status(d),
               "delta": lambda: cmd_delta(args, d),
               "abdeckung": lambda: cmd_abdeckung(args, d),
               "ertrag": lambda: cmd_ertrag(d),
               "titel": lambda: cmd_titel(d),
               "start": lambda: sw.cmd_start(args, d, speichern),
               "naechste": lambda: sw.cmd_naechste(args, d),
               "abfrage": lambda: sw.cmd_abfrage(args, d, speichern, kanal_norm, KANAELE),
               "ende": lambda: sw.cmd_ende(args, d, speichern),
               "bericht": lambda: sw.cmd_bericht(args, d),
               "sweeps": lambda: sw.cmd_sweeps(args, d),
               "audit": lambda: sw.cmd_audit(args, d)}
    if cmd not in befehle:
        print(__doc__); return 2
    # Sperre fuer den gesamten Aufruf (Massnahme 2025-03-16-log-sperre): verhindert, dass zwei
    # gleichzeitig laufende Sessions denselben Stand einlesen und sich beim Schreiben ueberschreiben.
    try:
        tx._sperren(f"screening_log.py {cmd}")
    except tx.Konflikt as e:
        print(f"ABGEBROCHEN: {e}")
        return 5
    try:
        d = laden()
        return befehle[cmd]()
    finally:
        tx._freigeben()


if __name__ == "__main__":
    sys.exit(main())
