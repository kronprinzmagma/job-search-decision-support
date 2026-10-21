#!/usr/bin/env python3
"""Sweep-Mechanik fuer das Stellen-Screening.

Zweck: mehrmals am Tag ein vollumfaenglicher Durchgang ueber alle Kanaele, damit neue Anzeigen
moeglichst frueh gefunden werden. Ein Durchgang darf auf mehrere Sessions verteilt sein; alles wird
geloggt, damit sich Abdeckung, Ertrag und Dauer im Nachhinein auswerten lassen.

Begriffe:
  Sweep     = ein vollumfaenglicher Durchgang (morgen | mittag | nachmittag | zusatz). Darf aus
              mehreren Sessions bestehen. Abgeschlossen erst, wenn jede aktive Abfrage aus
              data/screening_kanaele.json einen Status hat.
  Abfrage   = ein Eintrag des Katalogs (ID), z. B. pt-a-product-owner, ns-zh-a, zp-quendor.
  Status    = ok | leer | teilweise | nicht-erreichbar | uebersprungen
              («uebersprungen» zaehlt NICHT als abgedeckt, «teilweise» nur mit «TECHNIK:» in der Notiz)

Alles landet in data/screening_log.json (Listen `sweeps`, `laeufe`, `gesichtet`) und je Sweep in
data/lauf_audit.json (ein Audit-Datensatz je Sweep, Grundlage der Prozess-Retro).

Wird ueber screening_log.py aufgerufen (Befehle start, naechste, abfrage, ende, bericht, sweeps, audit).
"""
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import heute as uhr  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "data" / "screening_log.json"
KATALOG = ROOT / "data" / "screening_kanaele.json"
AUDIT = ROOT / "data" / "lauf_audit.json"
AKTUELL = ROOT / "data" / ".screening_sweep"          # ID des laufenden Sweeps (git-ignoriert)
NOTES = ROOT / "notes"

STATI = ["ok", "leer", "teilweise", "nicht-erreichbar", "uebersprungen"]
# Massnahme 2025-03-16-log-sperre: Session ohne «ende», die juenger ist als diese Schwelle, gilt als
# moeglicherweise noch aktiv und blockiert einen Neustart desselben Sweeps.
SPERRE_SESSION_MIN = 60
ABGEDECKT = {"ok", "leer", "teilweise", "nicht-erreichbar"}
ARTEN = ["morgen", "mittag", "nachmittag", "zusatz"]
AUSSORTIERT = {"vorfilter", "volltext-nogo", "dublette", "geschlossen"}
KANAL_REIHENFOLGE = ["netzwerk-tracker", "netzwerk-empfehlung", "netzwerk-suche", "portal",
                     "behoerdenportal", "zielportal", "karriereseite", "abo", "netzwerk", "manuell"]
PFLICHTSEKTIONEN = ["## Abdeckung", "## Kandidaten", "## Weggefallen", "## Befunde", "## Bei dir liegt"]
# Skelett-Platzhalter, die im fertigen Bericht nicht mehr vorkommen duerfen
PLATZHALTER = ["<NEU/TREFFER eintragen>", "<Publiziert-Datum aus der Anzeige", "<Portal, verbatim abgerufen",
               "<bewerben / nicht bewerben", "<Was am Setup, an Begriffen", "<Offene Entscheide als benannte Optionen",
               "Schritt 1 (Passt zu mir): <>"]
# Ziel- und Behoerdenportale aendern sich selten: nur im Morgen-Sweep (Katalog-Regel).
NUR_MORGENS = {"zielportal", "behoerdenportal"}
# «ok» mit auffaellig wenig Sichtungen: unter diesem Anteil des Ueblichen wird der Eintrag abgewiesen
OK_MIN_ANTEIL = 0.4


def jetzt():
    return uhr.jetzt().strftime("%Y-%m-%dT%H:%M:%S")


def katalog():
    if not KATALOG.exists():
        sys.exit("Katalog fehlt: data/screening_kanaele.json")
    k = json.loads(KATALOG.read_text(encoding="utf-8"))
    return k, [a for a in k["abfragen"] if a.get("aktiv", True)]


def aktueller_sweep(d, arg=None):
    """Sweep-ID aus Argument, Marker-Datei oder dem juengsten offenen Sweep von heute."""
    if arg:
        for s in d.get("sweeps", []):
            if s["id"] == arg:
                return s
        sys.exit(f"Sweep {arg} nicht gefunden.")
    if AKTUELL.exists():
        sid = AKTUELL.read_text().strip()
        for s in d.get("sweeps", []):
            if s["id"] == sid:
                return s
    heute = uhr.heute().isoformat()
    offen = [s for s in d.get("sweeps", []) if s["datum"] == heute and s["status"] == "offen"]
    if offen:
        return offen[-1]
    return None


def _zaehlt(l, s=None):
    """Zaehlt ein Lauf als abgedeckt? «teilweise» nur bei technischem Hindernis (Notiz beginnt mit
    «TECHNIK:» und nennt Weg und Fehlerbild). Eine selbst gewaehlte Abkuerzung haelt die Abfrage
    offen; die naechste Session muss sie vollstaendig fahren."""
    st = l.get("status")
    if st in ("ok", "leer", "nicht-erreichbar"):
        return True
    return st == "teilweise" and (l.get("notiz") or "").strip().upper().startswith("TECHNIK:")


def bewaehrter_weg(d, aid, vor_sweep=None):
    """Notiz des Laufs mit den meisten Sichtungen unter den letzten 8 ok-Laeufen dieser Abfrage —
    das Methodengedaechtnis (wie wurde die Liste zuletzt vollstaendig gelesen?) — und der Median."""
    kand = [l for l in d["laeufe"] if l.get("abfrage_id") == aid and l.get("status") == "ok"
            and isinstance(l.get("gesichtet_n"), int)
            and (vor_sweep is None or l.get("lauf_id") != vor_sweep)][-8:]
    if not kand:
        return None
    best = max(kand, key=lambda l: l["gesichtet_n"])
    werte = sorted(l["gesichtet_n"] for l in kand)
    return best, werte[len(werte) // 2]


def _fuer_art(s, aktive):
    """Soll je Tageszeit: Mittag und Nachmittag ohne Ziel-/Behoerdenportale. Bricht ein frueherer
    Sweep des Tages ab, holt der naechste die Portale nach (Flag beim Anlegen gesetzt, cmd_start)."""
    if s.get("mit_portalen"):
        return aktive
    if s.get("art") in ("mittag", "nachmittag"):
        return [a for a in aktive if a.get("kanal") not in NUR_MORGENS]
    return aktive


def soll_ist(d, s, aktive):
    """Welche Katalog-IDs hat dieser Sweep abgedeckt, welche fehlen?"""
    aktive = _fuer_art(s, aktive)
    erledigt = {}
    for l in d["laeufe"]:
        if l.get("lauf_id") == s["id"] and l.get("abfrage_id") and _zaehlt(l, s):
            erledigt[l["abfrage_id"]] = l
        elif l.get("lauf_id") == s["id"] and l.get("abfrage_id") in erledigt and not _zaehlt(l, s):
            erledigt.pop(l["abfrage_id"])  # spaeterer Eintrag ersetzt frueheren
    fehlend = [a for a in aktive if a["id"] not in erledigt]
    return erledigt, fehlend


def _stand(d, s, aktive):
    """(ist, soll, fehlend) gegen das Soll dieses Sweeps; Ad-hoc- und ausrangierte IDs zaehlen nicht mit."""
    soll = _fuer_art(s, aktive)
    erledigt, fehlend = soll_ist(d, s, soll)
    return len(soll) - len(fehlend), len(soll), fehlend


def cmd_start(args, d, speichern):
    """start <morgen|mittag|nachmittag|zusatz> [--modell <name>] [--neu]
    Legt den Sweep des Tages an oder setzt einen offenen fort (neue Session)."""
    art = args[0] if args and args[0] in ARTEN else None
    if not art:
        print("Verwendung: start <morgen|mittag|nachmittag|zusatz> [--modell X]"); return 2
    modell = args[args.index("--modell") + 1] if "--modell" in args else ""
    heute = uhr.heute().isoformat()
    sid = f"{heute}-{art}"
    d.setdefault("sweeps", [])
    s = next((x for x in d["sweeps"] if x["id"] == sid), None)
    kat, aktive = katalog()
    nachholen = []
    if s is None:
        frueher = [x for x in d["sweeps"] if x["datum"] == heute and x["id"] != sid
                   and x["status"] != "abgeschlossen"]
        for x in frueher:
            nachholen += [a["id"] for a in soll_ist(d, x, aktive)[1]]
        mit_portalen = any(a.get("kanal") in NUR_MORGENS for a in aktive if a["id"] in nachholen)
        soll = _fuer_art({"art": art, "datum": heute, "mit_portalen": mit_portalen}, aktive)
        s = {"id": sid, "datum": heute, "art": art, "status": "offen", "mit_portalen": mit_portalen,
             "katalog_version": kat.get("version", ""), "soll": len(soll),
             "start": jetzt(), "ende": None, "sessions": [], "notiz": ""}
        d["sweeps"].append(s)
        print(f"SWEEP NEU       {sid} — Soll: {len(soll)} Abfragen (Katalog {kat.get('version', '')})")
        if nachholen:
            print(f"NACHHOLEN: {len(nachholen)} Abfragen aus abgebrochenem Sweep von heute sind im Soll"
                  f"{' (inkl. Ziel-/Behoerdenportale)' if mit_portalen else ''}: {', '.join(nachholen)}")
    elif s["status"] == "abgeschlossen" and "--neu" not in args:
        AKTUELL.write_text(sid)
        print(f"SWEEP ABGESCHLOSSEN {sid} — nichts zu tun. Session sofort beenden, keine Meldung an Alex.")
        return 3
    else:
        # Massnahme 2025-03-16-log-sperre (Anlass: zwei Sessions am selben Sweep, Abfragen doppelt
        # geloggt): Eine Session ohne «ende», die juenger als SPERRE_SESSION_MIN ist, laeuft
        # moeglicherweise noch. Dann wird nicht parallel weitergearbeitet.
        offen_juengst = [se for se in s["sessions"] if se.get("ende") is None]
        if offen_juengst:
            letzte = offen_juengst[-1]
            alter_min = (uhr.jetzt() - datetime.fromisoformat(letzte["start"])).total_seconds() / 60
            if alter_min < SPERRE_SESSION_MIN:
                print(f"ABGEBROCHEN: Sweep {sid} hat bereits eine Session ohne 'ende', gestartet vor "
                      f"{alter_min:.0f} Min. ({letzte['start']}). Moeglicherweise laeuft sie noch — "
                      f"nicht parallel weiterarbeiten. Falls sie sicher abgebrochen ist: "
                      f"screening_log.py ende --abbrechen \"verwaiste Session\" und danach neu starten.")
                return 4
        if s["status"] != "offen":
            s["status"] = "offen"
        print(f"SWEEP FORTSETZEN {sid} — Session {len(s['sessions']) + 1}")
    s["sessions"].append({"start": jetzt(), "ende": None, "modell": modell,
                          "pid_hinweis": os.environ.get("CLAUDE_SESSION_ID", "")})
    AKTUELL.write_text(sid)
    speichern(d)
    ist, soll, fehlend = _stand(d, s, aktive)
    print(f"Stand: {ist}/{soll} abgedeckt, {len(fehlend)} offen.")
    erledigt_keys = {(e["firma"], e["rolle"]) for e in d.get("gesichtet", [])
                     if e.get("datum") == heute and e.get("entscheid") != "offen"}
    offen = [e for e in d.get("gesichtet", []) if e.get("datum") == heute and e.get("entscheid") == "offen"
             and (e["firma"], e["rolle"]) not in erledigt_keys]
    for e in offen:
        print(f"OFFEN VOLLTEXT: {e['firma']}|{e['rolle']}|{e.get('ort', '')}|{e.get('kanal', '')} — "
              f"zuerst im Volltext pruefen (spec/SWEEP.md, Schritt 5)")
    print("Naechste Abfragen: python3 scripts/screening_log.py naechste")
    return 0


def cmd_naechste(args, d):
    """naechste [--alle] [--kanal <kanal>]  — offene Abfragen des laufenden Sweeps in Reihenfolge."""
    s = aktueller_sweep(d)
    if not s:
        print("Kein offener Sweep. Zuerst: screening_log.py start <morgen|mittag|nachmittag>"); return 2
    kat, aktive = katalog()
    ist, soll, fehlend = _stand(d, s, aktive)
    if "--kanal" in args:
        k = args[args.index("--kanal") + 1]
        fehlend = [a for a in fehlend if a["kanal"] == k]
    print(f"# {s['id']} — {ist}/{soll} abgedeckt, {len(fehlend)} offen")
    print("# add mit 8. Feld Publiziert, wie die Trefferliste es zeigt («2025-04-03», «Gestern», «vor 4 Stunden», "
          "«3 days ago»; leer, wenn keins) — daraus rechnet die Retro die Fundgeschwindigkeit\n")
    n = len(fehlend) if "--alle" in args else min(25, len(fehlend))
    for a in fehlend[:n]:
        print(f"{a['id']}")
        print(f"   {a['name']}")
        if a.get("abfrage"): print(f"   Abfrage: {a['abfrage']}")
        if a.get("url"):     print(f"   URL: {a['url']}")
        if a.get("filter"):  print(f"   Filter: {a['filter']}")
        if a.get("hinweis"): print(f"   Hinweis: {a['hinweis']}")
        if a.get("netz") == "vorscan":
            print("   Netz: Vorscan — mit `python3 scripts/vorscan.py uebernehmen` abdecken, nicht im Browser")
        bw = bewaehrter_weg(d, a["id"])
        if bw:
            print(f"   Bewaehrter Weg ({bw[0]['lauf_id']}, {bw[0]['gesichtet_n']} gesichtet, ueblich ~{bw[1]}): "
                  f"{(bw[0].get('notiz') or '(keine Notiz)')[:260]}")
    if len(fehlend) > n:
        print(f"\n... und {len(fehlend) - n} weitere (--alle zeigt alle).")
    print("\nLoggen: python3 scripts/screening_log.py abfrage \"<id>|<status>|<gesichtet>|<notiz>\"")
    return 0


def cmd_abfrage(args, d, speichern, kanal_norm, kanaele):
    """abfrage "ID|Status|Gesichtet|Notiz"  (mehrere Argumente moeglich)
    ID = Katalog-ID oder adhoc:<name>. Status aus STATI. Gesichtet = ganze Zahl
    (bei nicht-erreichbar/uebersprungen leer erlaubt)."""
    s = aktueller_sweep(d)
    if not s:
        print("Kein offener Sweep. Zuerst: screening_log.py start <morgen|mittag|nachmittag>"); return 2
    kat, aktive = katalog()
    ids = {a["id"]: a for a in kat["abfragen"]}
    fehler = 0
    for roh in args:
        t = [x.strip() for x in roh.split("|")]
        while len(t) < 4:
            t.append("")
        aid, status, ges, notiz = t[0], t[1], t[2], "|".join(t[3:]).strip()
        if status not in STATI:
            print(f"  ! Status «{status}» unbekannt — erlaubt: {', '.join(STATI)}"); fehler += 1; continue
        if aid.startswith("adhoc:"):
            kanal = "karriereseite"; name = aid[6:]; filt = ""
        elif aid in ids:
            a = ids[aid]; kanal = a["kanal"]; name = a["name"]; filt = a.get("filter", "")
        else:
            print(f"  ! Abfrage-ID «{aid}» steht nicht im Katalog (data/screening_kanaele.json). "
                  f"Ad-hoc-Abfragen mit adhoc:<name> loggen."); fehler += 1; continue
        if re.fullmatch(r"\d+", ges):
            ges_n = int(ges)
        elif status in ("nicht-erreichbar", "uebersprungen") and not ges:
            ges_n = None
        else:
            print(f"  ! «{ges}» ist keine ganze Zahl — Gesichtet muss eine Zahl sein "
                  f"(Erklaerungen gehoeren in die Notiz)."); fehler += 1; continue
        if status == "ok" and ges_n is not None and aid in ids:
            bw = bewaehrter_weg(d, aid, vor_sweep=s["id"])
            if bw and bw[1] >= 10 and ges_n < OK_MIN_ANTEIL * bw[1] and not notiz.upper().startswith("BESTAND KLEINER:"):
                print(f"  ! {aid}: «ok» mit {ges_n} gesichtet, ueblich ~{bw[1]}. Ganze Liste gelesen (alle Seiten)? "
                      f"Dann Notiz mit «BESTAND KLEINER: <Beleg, z. B. Trefferzahl der Seite>» beginnen. "
                      f"Sonst vollstaendig fahren oder «teilweise» loggen (zaehlt nicht als abgedeckt)."); fehler += 1; continue
        if status == "teilweise" and not notiz.upper().startswith("TECHNIK:"):
            print(f"  i {aid}: «teilweise» ohne «TECHNIK:» zaehlt nicht als abgedeckt — die Abfrage bleibt offen.")
        if status == "nicht-erreichbar" and not notiz:
            print("  ! nicht-erreichbar braucht eine Notiz: versuchter Weg + Fehlerbild"); fehler += 1; continue
        e = {"kanal": kanal, "abfrage": name, "filter": filt,
             "gesichtet": str(ges_n) if ges_n is not None else status.upper(),
             "notiz": notiz, "datum": s["datum"],
             "lauf_id": s["id"], "abfrage_id": aid, "status": status,
             "gesichtet_n": ges_n, "zeit": jetzt()[11:]}
        # Wiederholung derselben Abfrage im selben Sweep: alter Eintrag bleibt, neuer ersetzt
        # ihn in der Soll-Ist-Rechnung (soll_ist nimmt den letzten).
        d["laeufe"].append(e)
        print(f"+ {aid} [{status}] {ges_n if ges_n is not None else '-'}  {name}")
    speichern(d)
    ist, soll, fehlend = _stand(d, s, aktive)
    print(f"Stand {s['id']}: {ist}/{soll} abgedeckt, {len(fehlend)} offen.")
    return 1 if fehler else 0


def _sicht(d, s):
    return [e for e in d["gesichtet"] if e.get("lauf_id") == s["id"]]


def _laeufe(d, s):
    return [l for l in d["laeufe"] if l.get("lauf_id") == s["id"]]


def _kategorie(grund):
    g = (grund or "").lower()
    for k, muster in (("Vermittler", "vermittl|personalberat|headhunt|recruit"),
                      ("Engineering", "engineer|entwickl|architekt|developer|devops|software"),
                      ("physisches Produkt", "physisch|hardware|maschin|lebensmittel|textil"),
                      ("Distanz", "distanz|ausschluss 2|pendel|ort ausserhalb"),
                      ("Junior/Praktikum", "junior|praktik|lehrstell|trainee|werkstud"),
                      ("Beratung/Agentur", "beratung|agentur|consult|ausschluss 4"),
                      ("Kernfaehigkeits-Luecke", "ausschluss 6|fachwissen|kernf"),
                      ("kein Produktmandat", "kein produktmandat|keine produktrolle|kein mandat|ausschluss 5|nicht-rolle|nicht rolle"),
                      ("Sammelposten", "sammelposten"),
                      ("Firmen-Ausschluss", "firmen-ausschluss|firmenausschluss")):
        if re.search(muster, g):
            return k
    return "Sonstiges"


def aktive_am(d, s, aktive):
    """Katalog-Eintraege, die zum Soll dieses Sweeps gehoeren: Ein spaeter ergaenzter Eintrag zaehlt
    nicht rueckwirkend als «fehlend» in frueheren Sweeps. Ausgeschlossen wird ein Eintrag, wenn er ein
    Feld «seit» nach dem Sweep-Tag hat oder wenn er im Log erstmals NACH dem Sweep-Tag abgefragt wurde.
    Ein Eintrag, der noch nie abgefragt wurde, gehoert zum Soll (neu im Katalog, ab jetzt faellig)."""
    erst = {}
    for l in d.get("laeufe", []):
        aid = l.get("abfrage_id")
        if aid and l.get("datum") and (aid not in erst or l["datum"] < erst[aid]):
            erst[aid] = l["datum"]
    tag = s["datum"]
    aktive = _fuer_art(s, aktive)
    return [a for a in aktive
            if not (a.get("seit") and a["seit"] > tag)
            and not (a["id"] in erst and erst[a["id"]] > tag)]


def audit_datensatz(d, s, aktive):
    aktive = aktive_am(d, s, aktive)
    erledigt, fehlend = soll_ist(d, s, aktive)
    laeufe = _laeufe(d, s); sicht = _sicht(d, s)

    def dauer():
        mins = 0
        for se in s["sessions"]:
            if se.get("start") and se.get("ende"):
                a = datetime.fromisoformat(se["start"]); b = datetime.fromisoformat(se["ende"])
                mins += max(0, (b - a).total_seconds() / 60)
        return round(mins)
    stat = {k: sum(1 for l in laeufe if l.get("status") == k) for k in STATI}
    notiz = NOTES / f"{s['datum']}_screening_{s['art']}.md"
    fmt = None
    if notiz.exists():
        txt = notiz.read_text(encoding="utf-8")
        fmt = all(p in txt for p in PFLICHTSEKTIONEN) and not any(p in txt for p in PLATZHALTER)
    ist = len(aktive) - len(fehlend)   # nur Soll-Eintraege; Ad-hoc und Ausrangiertes zaehlen nicht
    return {"sweep": s["id"], "datum": s["datum"], "art": s["art"], "status": s["status"],
            "sessions": len(s["sessions"]), "dauer_min": dauer(),
            "soll": len(aktive), "ist": ist,
            "abdeckung": round(ist / len(aktive), 3) if aktive else None,
            "fehlend": [a["id"] for a in fehlend],
            "nicht_erreichbar": [l["abfrage_id"] for l in laeufe if l.get("status") == "nicht-erreichbar"],
            "teilweise": stat["teilweise"], "uebersprungen": stat["uebersprungen"],
            "gesichtet_total": sum((l.get("gesichtet_n") or 0) for l in laeufe),
            "neu": len(sicht),
            "kandidaten": sum(1 for e in sicht if e.get("entscheid") == "kandidat"),
            "volltext_nogo": sum(1 for e in sicht if e.get("entscheid") == "volltext-nogo"),
            "offen": sum(1 for e in sicht if e.get("entscheid") == "offen"),
            "sammelposten": sum(1 for e in sicht if "sammelposten" in (e.get("grund") or "").lower()),
            "notiz_datei": notiz.name if notiz.exists() else None,
            "format_ok": fmt,
            "start": s.get("start"), "ende": s.get("ende"), "notiz": s.get("notiz", "")}


def _reihenfolge(x):
    """Sortierschluessel fuer Sweeps und Audit-Datensaetze: Datum, dann Tageszeit (nicht alphabetisch)."""
    art = x.get("art") or ""
    return (x.get("datum") or "", ARTEN.index(art) if art in ARTEN else 99, x.get("sweep") or x.get("id") or "")


def audit_schreiben(rec):
    """Einen Datensatz (oder eine Liste davon) in data/lauf_audit.json einsetzen; je Sweep genau einer."""
    neu = rec if isinstance(rec, list) else [rec]
    ids = {r["sweep"] for r in neu}
    liste = json.loads(AUDIT.read_text(encoding="utf-8")) if AUDIT.exists() else []
    liste = [r for r in liste if r.get("sweep") not in ids] + neu
    liste.sort(key=_reihenfolge)
    tmp = AUDIT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(liste, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    os.replace(tmp, AUDIT)


def cmd_ende(args, d, speichern):
    """ende [--abbrechen "Grund"]  — Session schliessen; Sweep abgeschlossen bei 100 % Soll.
    Schreibt immer den Audit-Datensatz (auch fuer unvollstaendige Sweeps)."""
    s = aktueller_sweep(d)
    if not s:
        print("Kein offener Sweep."); return 2
    kat, aktive = katalog()
    if s["sessions"] and s["sessions"][-1].get("ende") is None:
        s["sessions"][-1]["ende"] = jetzt()
    ist, soll, fehlend = _stand(d, s, aktive)
    if "--abbrechen" in args:
        s["status"] = "abgebrochen"; s["ende"] = jetzt()
        s["notiz"] = args[args.index("--abbrechen") + 1] if len(args) > args.index("--abbrechen") + 1 else "abgebrochen"
        print(f"SWEEP ABGEBROCHEN {s['id']} — {ist}/{soll} abgedeckt. Grund: {s['notiz']}")
    elif not fehlend:
        s["status"] = "abgeschlossen"; s["ende"] = jetzt()
        print(f"SWEEP ABGESCHLOSSEN {s['id']} — {soll}/{soll} Abfragen abgedeckt.")
    else:
        print(f"SWEEP NICHT ABGESCHLOSSEN {s['id']} — {ist}/{soll} abgedeckt, "
              f"{len(fehlend)} offen: {', '.join(a['id'] for a in fehlend[:12])}"
              f"{' ...' if len(fehlend) > 12 else ''}")
        print("Die naechste Session setzt fort (start <art>). Kein Abschlussbericht an Alex, "
              "nur ein Zwischenstand, falls Kandidaten vorliegen.")
    speichern(d)
    audit_schreiben(audit_datensatz(d, s, aktive))
    print(f"Audit-Datensatz geschrieben: data/lauf_audit.json ({s['id']})")
    return 0 if s["status"] == "abgeschlossen" else 1


def bericht_text(d, s, aktive):
    """Der erzeugte Teil des Laufberichts — geht 1:1 in Notiz und Meldung."""
    aktive = aktive_am(d, s, aktive)
    erledigt, fehlend = soll_ist(d, s, aktive)
    laeufe = _laeufe(d, s); sicht = _sicht(d, s)
    ist = len(aktive) - len(fehlend)
    z = []
    w = z.append
    p = round(100 * ist / len(aktive)) if aktive else 0
    if s["status"] == "abgeschlossen":
        w(f"**Abdeckung: alle {len(aktive)} Abfragen des Katalogs durchlaufen ({p} %). Sweep {s['id']} abgeschlossen, {len(s['sessions'])} Session(s).**")
    else:
        w(f"**Abdeckung: NICHT abgeschlossen — {ist} von {len(aktive)} Abfragen ({p} %), Sweep {s['id']} Status {s['status']}, {len(s['sessions'])} Session(s).**")
        w(f"Fehlend: {', '.join(a['id'] for a in fehlend[:20])}{' ...' if len(fehlend) > 20 else ''}")
    w("")
    w("## Abdeckung")
    w("")
    w("| Kanal | Soll | Ist | Gefunden | Neu | davon Kandidat | davon Aussortiert | davon Offen | nicht erreichbar |")
    w("|---|---|---|---|---|---|---|---|---|")
    tot = [0] * 7
    kan = sorted({a["kanal"] for a in aktive} | {l["kanal"] for l in laeufe},
                 key=lambda k: KANAL_REIHENFOLGE.index(k) if k in KANAL_REIHENFOLGE else 99)
    for k in kan:
        soll = sum(1 for a in aktive if a["kanal"] == k)
        ist_k = sum(1 for a in aktive if a["kanal"] == k and a["id"] in erledigt)
        gef = sum((l.get("gesichtet_n") or 0) for l in laeufe if l["kanal"] == k)
        sk = [e for e in sicht if e.get("kanal") == k]
        neu = len(sk); kd = sum(1 for e in sk if e["entscheid"] == "kandidat")
        au = sum(1 for e in sk if e["entscheid"] in AUSSORTIERT); of = sum(1 for e in sk if e["entscheid"] == "offen")
        ne = sum(1 for l in laeufe if l["kanal"] == k and l.get("status") == "nicht-erreichbar")
        for i, v in enumerate((soll, ist_k, gef, neu, kd, au, of)):
            tot[i] += v
        w(f"| {k} | {soll} | {ist_k} | {gef} | {neu} | {kd} | {au} | {of} | {ne} |")
    w(f"| **Total** | **{tot[0]}** | **{tot[1]}** | **{tot[2]}** | **{tot[3]}** | **{tot[4]}** | **{tot[5]}** | **{tot[6]}** | |")
    w("")
    w("Neu = Kandidat + Aussortiert + Offen. Gefunden minus Neu = bereits aus frueheren Sweeps bekannt (Delta-Filter).")
    w("")
    ne = [l for l in laeufe if l.get("status") in ("nicht-erreichbar", "teilweise")]
    if ne:
        w("### Nicht erreichbar oder nur teilweise")
        w("")
        for l in ne:
            w(f"- **{l.get('abfrage_id')}** ({l['kanal']}) [{l['status']}]: {l.get('notiz') or '-'}")
        w("")
    w("### Was abgefragt wurde")
    w("")
    w("| Zeit | ID | Kanal | Status | Gesichtet | Notiz |")
    w("|---|---|---|---|---|---|")
    for l in laeufe:
        w(f"| {l.get('zeit', '')[:5]} | {l.get('abfrage_id', '')} | {l['kanal']} | {l.get('status', '')} | "
          f"{l.get('gesichtet_n') if l.get('gesichtet_n') is not None else '-'} | {(l.get('notiz') or '').replace('|', '/')} |")
    w("")
    w("## Kandidaten")
    w("")
    kand = [e for e in sicht if e["entscheid"] == "kandidat"]
    if not kand:
        w("Keine neuen Kandidaten in diesem Sweep.")

    # Das Alter der Anzeige ist ein Priorisierungsfaktor (ueber eine Woche alt = meist schwerer zu
    # erreichen): frischeste zuerst, ueber eine Woche alt markiert.
    def _pub(e):
        try:
            return datetime.strptime(e["publiziert"], "%Y-%m-%d").date() if e.get("publiziert") else None
        except ValueError:
            return None
    kand.sort(key=lambda e: (_pub(e) is None, -(_pub(e).toordinal()) if _pub(e) else 0))
    for e in kand:
        pub = _pub(e)
        if pub:
            n = (datetime.strptime(e["datum"], "%Y-%m-%d").date() - pub).days
            alter = (f"**ueber eine Woche alt ({n} Tage) — schwerer zu erreichen**" if n > 7
                     else ("heute publiziert" if n <= 0 else f"{n} Tag{'e' if n != 1 else ''}"))
            alter_zeile = f"Alter der Anzeige beim Fund: {alter} (publiziert {pub.isoformat()})"
        else:
            alter_zeile = "Alter der Anzeige beim Fund: <Publiziert-Datum aus der Anzeige oder «unbekannt»>"
        w(f"### {e['firma']} — {e['rolle']} ({e.get('ort', '')})")
        w(f"Gefunden ueber: {e.get('gefunden_ueber') or '-'} · Kanal: {e['kanal']} · Dublettencheck: <NEU/TREFFER eintragen>")
        w(alter_zeile)
        w("")
        w("Quelle: <Portal, verbatim abgerufen JJJJ-MM-TT>")
        w("Empfehlung: <bewerben / nicht bewerben / Unentschieden — Entscheid bei Alex>")
        w("Ausschluss-Check: 1 Junior — <> · 2 Distanz — <> · 3 Homeoffice — <> · 4 Beratung/Agentur — <> · 5 Rueckschritt — <> · 6 Kernfaehigkeits-Luecke — <>")
        w("Schritt 1 (Passt zu mir): <>")
        w("Schritt 2 (Chance): <>")
        w("Danach: <>")
        w("")
    w("## Weggefallen")
    w("")
    weg = [e for e in sicht if e["entscheid"] in AUSSORTIERT]
    if not weg:
        w("Nichts weggefallen.")
    else:
        grp = {}
        eigene = {"volltext-nogo": "Volltext-NoGo", "dublette": "Dublette", "geschlossen": "nicht mehr abrufbar"}
        for e in weg:
            grp.setdefault(eigene.get(e["entscheid"]) or _kategorie(e.get("grund")), []).append(e)
        w(f"{len(weg)} weg: " + ", ".join(f"{len(v)} {k}" for k, v in sorted(grp.items(), key=lambda x: -len(x[1]))))
        vt = grp.get("Volltext-NoGo", [])
        if vt:
            w("")
            w("Volltext geprueft und abgelehnt:")
            for e in vt:
                w(f"- {e['firma']} — {e['rolle']}: {e.get('grund') or '-'}")
    w("")
    offen_alle = [e for e in d["gesichtet"] if e.get("entscheid") == "offen"]
    w("### Offen im ganzen Log (Volltext ausstehend)")
    w("")
    if not offen_alle:
        w("Keine.")
    for e in offen_alle:
        w(f"- {e['firma']} — {e['rolle']} ({e['kanal']}, seit {e['datum']})")
    w("")
    w("## Befunde")
    w("")
    w("<Was am Setup, an Begriffen, Portalen oder Regeln aufgefallen ist — sonst «keine».>")
    w("")
    w("## Bei dir liegt")
    w("")
    w("<Offene Entscheide als benannte Optionen — sonst «keine».>")
    return "\n".join(z)


GEN_START = "<!-- generiert:start — nicht von Hand aendern, screening_log.py bericht --schreiben -->"
GEN_ENDE = "<!-- generiert:ende -->"


def cmd_bericht(args, d):
    """bericht [sweep-id] [--schreiben]
    Ohne --schreiben: Text auf stdout. Mit --schreiben: notes/<datum>_screening_<art>.md
    anlegen bzw. den generierten Block darin ersetzen (handgeschriebene Teile bleiben)."""
    sid = next((a for a in args if not a.startswith("--")), None)
    s = aktueller_sweep(d, sid)
    if not s:
        print("Kein Sweep gefunden."); return 2
    kat, aktive = katalog()
    txt = bericht_text(d, s, aktive)
    if "--schreiben" not in args:
        print(txt); return 0
    NOTES.mkdir(exist_ok=True)
    pfad = NOTES / f"{s['datum']}_screening_{s['art']}.md"
    block = f"{GEN_START}\n{txt}\n{GEN_ENDE}"
    if pfad.exists():
        alt = pfad.read_text(encoding="utf-8")
        if GEN_START in alt and GEN_ENDE in alt:
            neu = alt[:alt.index(GEN_START)] + block + alt[alt.index(GEN_ENDE) + len(GEN_ENDE):]
        else:
            neu = alt.rstrip() + "\n\n" + block + "\n"
    else:
        neu = (f"# Screening-Lauf {s['art'].capitalize()}, {s['datum']} (Sweep {s['id']})\n\n"
               f"{block}\n\n## Nachtraege\n\n<Entscheide Alex, Korrekturen nach dem Lauf — sonst leer.>\n")
    pfad.write_text(neu, encoding="utf-8")
    print(f"Notiz geschrieben: {pfad.relative_to(ROOT)}")
    print("Kandidatenbloecke im generierten Teil sind Skelette — im selben Zug ausfuellen "
          "(Vollformat, alle sechs Ausschluesse einzeln). Danach: bericht --schreiben NICHT erneut "
          "aufrufen, sonst werden die ausgefuellten Bloecke ueberschrieben; stattdessen unterhalb "
          "von <!-- generiert:ende --> ergaenzen oder die Bloecke direkt editieren.")
    return 0


def cmd_sweeps(args, d):
    """sweeps [--tage N] — Uebersicht der Sweeps mit Abdeckung (Soll wie im Audit: aktive_am)."""
    tage = int(args[args.index("--tage") + 1]) if "--tage" in args else 7
    kat, aktive = katalog()
    grenze = (uhr.heute() - timedelta(days=tage)).isoformat()
    sw = sorted((s for s in d.get("sweeps", []) if s["datum"] > grenze), key=_reihenfolge)
    print("| Sweep | Status | Sessions | Ist/Soll | Abdeckung | Neu | Kandidaten | Start | Ende |")
    print("|---|---|---|---|---|---|---|---|---|")
    for s in sw:
        soll_l = aktive_am(d, s, aktive)
        erl, feh = soll_ist(d, s, soll_l)
        soll = len(soll_l); ist = soll - len(feh)
        sicht = _sicht(d, s)
        p = f"{round(100 * ist / soll)} %" if soll else "-"
        print(f"| {s['id']} | {s['status']} | {len(s.get('sessions', []))} | {ist}/{soll} | {p} | "
              f"{len(sicht)} | {sum(1 for e in sicht if e['entscheid'] == 'kandidat')} | "
              f"{(s.get('start') or '')[11:16]} | {(s.get('ende') or '')[11:16]} |")
    if not sw:
        print(f"(keine Sweeps seit {grenze})")
    return 0


def audit_aktualisieren(d, tage=3):
    """Audit-Datensaetze der letzten `tage` Tage neu rechnen (tage=None: alle Sweeps). Der Format-Check
    greift erst, wenn die Notiz ausgefuellt ist — deshalb laeuft das im Pflegelauf nochmals."""
    kat, aktive = katalog()
    heute = uhr.heute()
    recs = [audit_datensatz(d, s, aktive) for s in d.get("sweeps", [])
            if tage is None or 0 <= (heute - datetime.strptime(s["datum"], "%Y-%m-%d").date()).days <= tage]
    if recs:
        audit_schreiben(recs)
    return len(recs)


def cmd_audit(args, d):
    """audit [--aktualisieren [--alle | --tage N]] — Audit-Datensaetze (data/lauf_audit.json) als Tabelle."""
    if "--aktualisieren" in args:
        tage = None if "--alle" in args else (int(args[args.index("--tage") + 1]) if "--tage" in args else 3)
        print(f"{audit_aktualisieren(d, tage)} Audit-Datensaetze neu gerechnet.")
    if not AUDIT.exists():
        print("Noch kein Audit-Datensatz."); return 0
    liste = json.loads(AUDIT.read_text(encoding="utf-8"))
    print("| Sweep | Status | Sess. | Dauer min | Abdeckung | n. erreichbar | Neu | Kand. | Format ok |")
    print("|---|---|---|---|---|---|---|---|---|")
    for r in liste[-30:]:
        ab = f"{round(100 * r['abdeckung'])} %" if r.get("abdeckung") is not None else "-"
        print(f"| {r['sweep']} | {r['status']} | {r['sessions']} | {r['dauer_min']} | {ab} | "
              f"{len(r.get('nicht_erreichbar', []))} | {r['neu']} | {r['kandidaten']} | "
              f"{'ja' if r.get('format_ok') else ('nein' if r.get('format_ok') is False else '-')} |")
    if len(liste) > 30:
        print(f"(die letzten 30 von {len(liste)} Datensaetzen)")
    return 0
