#!/usr/bin/env python3
"""Vorscan Jobportal — mechanischer Teil des Screening-Sweeps ohne Sprachmodell.

Anlass: Ein Sweep las das ganze Regelwerk und fuhr das Jobportal im Browser; das kostete Zeit und Geld,
ohne dass das Modell bei den meisten Listeneintraegen etwas zu entscheiden hatte (data/retro_massnahmen.json,
Massnahme 2025-04-06-vorscan). Seither holt ein Skript die Trefferlisten, und das Modell sieht nur noch
die unklaren Neuzugaenge.

  scan          Im Betrieb holt ein Hintergrund-Job ausserhalb der Sweep-Session die Trefferlisten aller
                aktiven Vorscan-Abfragen (Katalog-Feld `netz: "vorscan"`) und schreibt data/vorscan/stand.json.
                IM SHOWCASE FINDET KEIN PORTAL-ZUGRIFF STATT: stand.json ist ein Fixture-Kanal
                (scripts/init_demo.py). `scan` prueft nur, ob der Stand vollstaendig und gueltig ist.
  uebernehmen   laeuft in der Sweep-Session (offener Sweep noetig): gleicht gegen das Sichtungs-Log ab,
                wendet die Rauschregeln an (scripts/vorscan_regeln.py), loggt `add` + `abfrage` je
                Vorscan-Abfrage und gibt NUR die unklaren Neuzugaenge aus — die entscheidet das Modell.
                Fehlt der Stand: Exit 4, die Abfragen von Hand fahren (`naechste --kanal portal`).
                Ist er aelter als MAX_ALTER_MIN: die Abfragen als nicht erreichbar loggen (TECHNIK:), kein
                Browser-Ersatz; der naechste Scan liest das Fenster seit dem letzten erfolgreichen Scan nach.
                --probe: nichts schreiben, nur zeigen.
  pruefen       Regeln gegen das ganze Sichtungs-Log: wie viele Kandidaten-, Volltext- und Offen-Faelle
                wuerden faelschlich vorgefiltert (Soll: 0 ausser Firmen-Ausschluessen), wie viel Rauschen
                faengt das Skript ab, decken die Regeln PRESCREEN.md ab (Drift-Waechter).
  status        Alter und Kennzahlen des letzten Stands.
"""
import contextlib
import io
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import heute as uhr  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
KATALOG = ROOT / "data" / "screening_kanaele.json"
LOG = ROOT / "data" / "screening_log.json"
VDIR = ROOT / "data" / "vorscan"
STAND = VDIR / "stand.json"
PRESCREEN = ROOT / "spec" / "PRESCREEN.md"
MAX_ALTER_MIN = 150
SCHUTZ_ENTSCHEIDE = ("kandidat", "volltext-nogo", "offen", "dublette")
EINTRAG_FELDER = ("id", "firma", "rolle", "ort", "publiziert", "url")


def vorscan_abfragen():
    """Aktive Katalog-Abfragen, die der Vorscan abdeckt (netz: vorscan; ohne Feld: Kanal portal)."""
    k = json.loads(KATALOG.read_text(encoding="utf-8"))
    return [a for a in k["abfragen"] if a.get("aktiv", True)
            and (a.get("netz") == "vorscan" or ("netz" not in a and a["kanal"] == "portal"))]


def _alter_min(zeit):
    """Alter eines Zeitstempels in Minuten gegen heute.jetzt() (naiv, Ortszeit)."""
    t = datetime.fromisoformat(zeit)
    if t.tzinfo is not None:
        t = t.astimezone().replace(tzinfo=None)
    return (uhr.jetzt() - t).total_seconds() / 60


def _stand_laden():
    return json.loads(STAND.read_text(encoding="utf-8"))


def validieren(st):
    """Liste der Befunde am Stand (leer = gueltig): Pflichtfelder, Trefferzahl, Katalog-Abdeckung."""
    befunde = []
    if not isinstance(st.get("abfragen"), dict) or not st.get("zeit"):
        return ["Grundstruktur fehlt (Felder `zeit`, `abfragen`)"]
    try:
        datetime.fromisoformat(st["zeit"])
    except ValueError:
        befunde.append(f"Zeitstempel unlesbar: {st['zeit']}")
    soll = {a["id"] for a in vorscan_abfragen()}
    for aid in sorted(soll - set(st["abfragen"])):
        befunde.append(f"{aid}: fehlt im Stand (Abfrage von Hand fahren)")
    for aid, r in st["abfragen"].items():
        if aid not in soll:
            befunde.append(f"{aid}: nicht (mehr) aktiv im Katalog — wird ignoriert")
        if r.get("status") != "ok":
            befunde.append(f"{aid}: Status {r.get('status')} ({r.get('fehler', '-')})")
            continue
        ein = r.get("eintraege") or []
        if r.get("treffer") is not None and r["treffer"] != len(ein):
            befunde.append(f"{aid}: {len(ein)} Eintraege, aber {r['treffer']} Treffer gemeldet (Liste unvollstaendig)")
        for i, e in enumerate(ein):
            fehlt = [f for f in EINTRAG_FELDER if f not in e]
            if fehlt or not e.get("firma") or not e.get("rolle"):
                befunde.append(f"{aid} Eintrag {i}: Felder fehlen oder leer ({', '.join(fehlt) or 'firma/rolle'})")
                break
    return befunde


def cmd_scan():
    print("Showcase: Hier findet kein Portal-Zugriff statt. Im Betrieb holt ein Hintergrund-Job die "
          "Trefferlisten; hier ist data/vorscan/stand.json ein Fixture-Kanal (scripts/init_demo.py).")
    if not STAND.exists():
        print("Kein Stand vorhanden (data/vorscan/stand.json)."); return 1
    st = _stand_laden()
    befunde = validieren(st)
    n = sum(len(r.get("eintraege") or []) for r in st["abfragen"].values())
    print(f"Stand {st['zeit']} ({_alter_min(st['zeit']):.0f} Min.), Quelle: {st.get('quelle', '-')}: "
          f"{len(st['abfragen'])} Abfragen, {n} Eintraege")
    for b in befunde:
        print("  BEFUND:", b)
    print("gueltig" if not befunde else f"{len(befunde)} Befund(e)")
    return 0 if not befunde else 1


def gelernte_listen(g):
    """Aus dem Log gelernte Vermittler-Firmen und Distanz-Orte; Firmen und Orte, die je zu einem
    Kandidaten-, Volltext-, Offen- oder Dubletten-Fall gehoerten, sind ausgenommen."""
    from vorscan_regeln import n
    schutz = {n(x["firma"]).strip() for x in g if x.get("entscheid") in SCHUTZ_ENTSCHEIDE}
    verm = {n(x["firma"]).strip() for x in g if "vermittler" in (x.get("grund") or "").lower()} - schutz - {""}
    schutz_ort = {n(x.get("ort")).strip() for x in g if x.get("entscheid") in SCHUTZ_ENTSCHEIDE}
    dist = {n(x.get("ort")).strip() for x in g if "distanz" in (x.get("grund") or "").lower()} - schutz_ort - {""}
    return frozenset(verm), frozenset(dist)


def _veraltet_loggen(st, alter):
    """Stand zu alt: offene Vorscan-Abfragen als nicht erreichbar loggen (kein Browser-Ersatz)."""
    import screening_log as sl
    import screening_log_tx as tx
    import screening_sweep as sw
    try:
        tx._sperren("vorscan.py uebernehmen (veraltet)")
    except tx.Konflikt as e:
        print(f"ABGEBROCHEN: {e}"); return 5
    try:
        d = sl.laden(); s = sw.aktueller_sweep(d)
        if not s or s.get("status") != "offen":
            print("Kein offener Sweep."); return 2
        _, aktive = sw.katalog(); erledigt, _ = sw.soll_ist(d, s, aktive)
        zeilen = [f"{a['id']}|nicht-erreichbar||TECHNIK: Vorscan veraltet (Stand {st['zeit'][:16]}, {alter:.0f} Min.) — "
                  f"kein Browser-Ersatz; der naechste Scan liest das Fenster seit dem letzten erfolgreichen Scan nach"
                  for a in vorscan_abfragen() if a["id"] not in erledigt]
        with contextlib.redirect_stdout(io.StringIO()):
            if zeilen:
                sw.cmd_abfrage(zeilen, d, sl.speichern, sl.kanal_norm, sl.KANAELE)
    finally:
        tx._freigeben()
    print(f"VORSCAN VERALTET ({alter:.0f} Min.) — {len(zeilen)} Abfragen als nicht erreichbar geloggt, KEIN Browser-Ersatz. "
          f"Das Delta holt der naechste Scan nach. Weiter mit den uebrigen Abfragen.")
    return 0


def cmd_uebernehmen(args):
    import screening_log as sl
    import screening_log_tx as tx
    import screening_sweep as sw
    from vorscan_regeln import entscheid, n
    probe = "--probe" in args
    if not STAND.exists():
        print("VORSCAN FEHLT (data/vorscan/stand.json) — die Vorscan-Abfragen diesmal von Hand fahren "
              "(screening_log.py naechste --kanal portal)."); return 4
    st = _stand_laden()
    befunde = [b for b in validieren(st) if "nicht (mehr) aktiv" not in b and "fehlt im Stand" not in b]
    if any("Grundstruktur" in b or "Zeitstempel" in b for b in befunde):
        print(f"VORSCAN-STAND UNGUELTIG: {befunde[0]} — Abfragen von Hand fahren."); return 4
    alter = _alter_min(st["zeit"])
    if alter < -5:
        print(f"VORSCAN-STAND UNPLAUSIBEL: Zeitstempel {st['zeit']} liegt nach jetzt ({uhr.jetzt():%Y-%m-%dT%H:%M}). "
              f"Uhr pruefen; nichts geloggt."); return 4
    if alter > MAX_ALTER_MIN and "--alter-egal" not in args:
        if probe:
            print(f"VORSCAN VERALTET ({alter:.0f} Min.) — Probe, nichts geloggt."); return 4
        return _veraltet_loggen(st, alter)
    if not probe:
        try:
            tx._sperren("vorscan.py uebernehmen")
        except tx.Konflikt as e:
            print(f"ABGEBROCHEN: {e}"); return 5
    try:
        d = sl.laden()
        s = sw.aktueller_sweep(d)
        if not s or s.get("status") != "offen":
            print("Kein offener Sweep. Zuerst: screening_log.py start <art>"); return 2
        _, aktive = sw.katalog()
        erledigt, _ = sw.soll_ist(d, s, aktive)
        verm, dist = gelernte_listen(d["gesichtet"])
        stempel = st["zeit"][11:16] + " Ortszeit"
        gesehen, adds, abfr, unklar, von_hand = set(), [], [], [], []
        zahl = {"neu": 0, "regel": 0, "unklar": 0, "bekannt": 0}
        for a in vorscan_abfragen():
            aid = a["id"]
            if aid in erledigt:
                continue
            r = st["abfragen"].get(aid)
            if not r or r.get("status") != "ok":
                von_hand.append(f"{aid} ({(r or {}).get('fehler', 'nicht im Stand')})"); continue
            neu_q = 0
            for e in r["eintraege"]:
                # dieselbe Anzeige taucht oft unter mehreren Abfragen auf: nur unter der ersten loggen
                schluessel = (n(e["firma"]).strip(), n(e["rolle"]).strip())
                if e["id"] in gesehen or schluessel in gesehen:
                    continue
                gesehen |= {e["id"], schluessel}
                # Nur dieselbe Rolle gilt als bekannt; eine aehnliche Rolle derselben Firma (moeglicher
                # Repost) geht an das Modell.
                stufen = {stufe for _, stufe in sl.treffer(e["firma"], e["rolle"], d)}
                if "gleich" in stufen:
                    zahl["bekannt"] += 1; continue
                neu_q += 1; zahl["neu"] += 1
                ent, grund = entscheid(e["firma"], e["rolle"], e["ort"], verm, dist)
                feld = lambda x: " ".join((x or "").replace("|", "/").split())
                pub = (e.get("publiziert") or "")[:10]   # Fundgeschwindigkeit
                if ent == "vorfilter":
                    zahl["regel"] += 1
                    adds.append(f"{feld(e['firma'])}|{feld(e['rolle'])}|{feld(e['ort'])}|{a['kanal']}|vorfilter|"
                                f"{grund} (Vorscan-Regel)|{aid}|{pub}")
                else:
                    zahl["unklar"] += 1
                    hinweis = " [PRUEFEN: aehnliche Rolle derselben Firma im Log - Repost?]" if "aehnlich" in stufen else ""
                    unklar.append(f"{feld(e['firma'])}|{feld(e['rolle'])}|{feld(e['ort'])}|{aid}|{e['url']}|{pub}{hinweis}")
            weg = (f"Vorscan {stempel}: Trefferliste vollstaendig per Skript gelesen "
                   f"({r.get('seiten', '?')} Seite(n), {r.get('treffer', len(r['eintraege']))} Treffer)")
            # Das Skript liest jede Liste bis zum Ende; weniger Treffer als ueblich heisst kleinerer Bestand im Fenster.
            notiz = f"BESTAND KLEINER: {weg}; {neu_q} neu, je Anzeige unter der ersten Abfrage geloggt"
            abfr.append(f"{aid}|ok|{len(r['eintraege'])}|{notiz}")
        if not probe:
            stumm = io.StringIO()
            with contextlib.redirect_stdout(stumm):
                if adds:
                    sl.cmd_add(adds, d)
                if abfr:
                    sw.cmd_abfrage(abfr, d, sl.speichern, sl.kanal_norm, sl.KANAELE)
            for w in [l for l in stumm.getvalue().splitlines() if l.strip().startswith("!")][:10]:
                print("WARNUNG", w)
            VDIR.mkdir(exist_ok=True)
            with open(VDIR / f"unklar_{s['id']}.txt", "a", encoding="utf-8") as f:
                f.write("\n".join(unklar) + ("\n" if unklar else ""))
        print(f"# Vorscan uebernommen ({'PROBE, nichts geschrieben' if probe else 'geloggt'}) — Stand {st['zeit']} ({alter:.0f} Min.)")
        print(f"{len(abfr)} Abfragen abgedeckt · {zahl['bekannt']} schon gesichtet · {zahl['neu']} neu: "
              f"{zahl['regel']} per Regel vorgefiltert, {zahl['unklar']} unklar")
        if von_hand:
            zeig = von_hand if len(von_hand) <= 8 else von_hand[:8] + [f"... und {len(von_hand) - 8} weitere"]
            print(f"\nVON HAND FAHREN ({len(von_hand)}): " + "; ".join(zeig))
        print("\nUNKLAR — du entscheidest (Firma|Rolle|Ort|Abfrage|URL|Publiziert); je Zeile `screening_log.py add` "
              "mit Entscheid, Publiziert als 8. Feld uebernehmen:")
        for u in unklar:
            print(u)
        if not unklar:
            print("(keine)")
        return 0
    finally:
        if not probe:
            tx._freigeben()


def _prescreen_branchen():
    """Branchen aus spec/PRESCREEN.md «Firmen-Ausschluss der Persona: …»."""
    try:
        txt = PRESCREEN.read_text(encoding="utf-8")
    except OSError:
        return None
    m = re.search(r"Firmen-Ausschluss der Persona:?\*{0,2}:?\s*(.+)", txt)
    if not m:
        return None
    roh = re.sub(r"[*.]", "", m.group(1))
    return [re.sub(r"branche$", "", b.strip(), flags=re.I).strip() for b in re.split(r",| und ", roh) if b.strip()]


def cmd_pruefen():
    import vorscan_regeln as vr
    g = json.loads(LOG.read_text(encoding="utf-8"))["gesichtet"]
    verm, dist = gelernte_listen(g)
    falsch, gefangen, rausch = [], 0, 0
    for x in g:
        ent, grund = vr.entscheid(x["firma"], x["rolle"], x.get("ort", ""), verm, dist)
        if x.get("entscheid") in ("kandidat", "volltext-nogo", "offen"):
            gleich = (x.get("entscheid") == "volltext-nogo" and grund.startswith("Vermittler")
                      and "vermittler" in (x.get("grund") or "").lower())  # gleiches Ergebnis, kein Fehler
            if ent == "vorfilter" and not grund.startswith("Firmen-Ausschluss") and not gleich:
                falsch.append(f"{x['entscheid']} | {grund} | {x['firma']} | {x['rolle']}")
        elif x.get("entscheid") == "vorfilter":
            rausch += 1; gefangen += ent == "vorfilter"
    # Drift-Waechter: jede in PRESCREEN.md genannte Branche braucht eine Erkennungsregel, jeder im Log per
    # Firmen-Ausschluss aussortierte Arbeitgeber muss erkannt werden, die Ortstabelle muss lesbar sein.
    fehlt = []
    branchen = _prescreen_branchen()
    if branchen is None:
        fehlt.append("spec/PRESCREEN.md: Zeile «Firmen-Ausschluss der Persona» nicht gefunden")
    else:
        bekannt = {vr.n(b).strip() for _, b, _ in vr.FIRMEN_AUS}
        fehlt += [f"Branche «{b}» ohne Regel in FIRMEN_AUS" for b in branchen if vr.n(b).strip() not in bekannt]
    for f in sorted({x["firma"] for x in g if "firmen-ausschluss" in (x.get("grund") or "").lower()}):
        if not vr.entscheid(f, "Product Manager", "Zürich")[1].startswith("Firmen-Ausschluss"):
            fehlt.append(f"Arbeitgeber «{f}» (im Log per Firmen-Ausschluss aussortiert) wird nicht erkannt")
    if not vr.DISTANZ_ORTE:
        fehlt.append("Ortstabelle in spec/PRESCREEN.md (Spalte «über 60 Min.») nicht lesbar")
    for f in fehlt:
        print("  FEHLT:", f)
    print(f"Rauschen per Regel abgefangen: {gefangen} von {rausch} ({100 * gefangen / max(rausch, 1):.0f} %)")
    print(f"Faelschlich vorgefiltert (Kandidat/Volltext/offen, ohne Firmen-Ausschluss): {len(falsch)}")
    for f in falsch:
        print("  FALSCH:", f)
    return 1 if (falsch or fehlt) else 0


def cmd_status():
    if not STAND.exists():
        print("kein Stand vorhanden"); return 1
    st = _stand_laden()
    print(f"Stand {st['zeit']} ({_alter_min(st['zeit']):.0f} Min.), {len(st['abfragen'])} Abfragen, "
          f"{st.get('fehler')} Fehler, {st.get('dauer_s')} s — Quelle: {st.get('quelle', '-')}")
    for aid, r in st["abfragen"].items():
        print(f"  {aid:28} {r.get('status', '-'):6} Treffer {r.get('treffer', 0):4}  Seiten {r.get('seiten', 0):3}  "
              f"{(r.get('fehler') or '')[:80]}")
    return 0


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    if c == "uebernehmen":
        sys.exit(cmd_uebernehmen(sys.argv[2:]))
    befehle = {"scan": cmd_scan, "pruefen": cmd_pruefen, "status": cmd_status}
    if c not in befehle:
        print(__doc__); sys.exit(2)
    sys.exit(befehle[c]())
