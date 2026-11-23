#!/usr/bin/env python3
"""ereignis — ein Ereignis in den Verlauf eines Falls schreiben.

Anlass: Je Fall gab es nur einen Status und ein Freitextfeld `notiz`; Versand, Eingangsbestaetigung,
Nachfass, Einladung, Gespraech und Absage lagen verstreut, und spaeter liess sich nicht mehr belegen,
was wann passiert war. Jetzt fuehrt jeder Datensatz `verlauf`: eine Liste {datum, ereignis, quelle, notiz}.

    python3 scripts/ereignis.py <id> <ereignis> [--datum JJJJ-MM-TT] [--quelle PFAD] [--notiz TEXT] [--probe]
    python3 scripts/ereignis.py <id>                       # Verlauf anzeigen
    python3 scripts/ereignis.py --offen                    # Faelle, deren Status ohne passendes Ereignis dasteht

Ereignisse: vorgelegt | go | nogo | versand | eingang | nachfass | einladung | gespraech | debrief |
            absage | rueckzug | zweitpruefung | nachtrag | angebot
Regeln:
  - Statuswechsel laufen ueber scripts/status.py (schreibt das Ereignis selbst mit).
    ereignis.py ist fuer alles, was den Status NICHT aendert: eingang, nachfass, einladung,
    debrief, nachtrag — und zum Nachtragen fehlender Ereignisse.
  - --quelle ist die Datei, die das Ereignis belegt (Rueckmeldung, Mail, Notiz). Bei versand, eingang,
    einladung, absage Pflicht; sie sollte im Fall-Ordner liegen.
  - Dasselbe Ereignis am selben Datum wird nicht doppelt geschrieben.
  - Geschrieben wird ueber scripts/pipeline_tx.py (Sperre, Konfliktpruefung).
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from heute import heute  # noqa: E402
from pipeline_tx import Konflikt, transaktion  # noqa: E402

EREIGNISSE = ["vorgelegt", "go", "nogo", "versand", "eingang", "nachfass", "einladung", "gespraech", "debrief",
              "absage", "rueckzug", "zweitpruefung", "nachtrag", "angebot"]
QUELLE_PFLICHT = {"eingang", "einladung", "absage", "versand"}
ERWARTET = {"abgeschickt": "versand", "in_pruefung": "versand", "gespraech": "gespraech", "abgesagt": "absage",
            "aussortiert": "nogo", "zurueckgezogen": "rueckzug", "angebot": "angebot"}


def zeigen(r):
    print(f"{r['id']} — {r['firma']} — {r['rolle']} [{r.get('status')}]")
    for e in r.get("verlauf") or []:
        print(f"  {e.get('datum')}  {e.get('ereignis'):13s} {e.get('quelle') or '-'}  {e.get('notiz') or ''}")
    if not r.get("verlauf"):
        print("  (kein Verlauf)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id", nargs="?")
    ap.add_argument("ereignis", nargs="?", choices=EREIGNISSE)
    ap.add_argument("--datum")
    ap.add_argument("--quelle")
    ap.add_argument("--notiz", default="")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--offen", action="store_true")
    a = ap.parse_args()
    data = json.loads((ROOT / "data" / "pipeline.json").read_text(encoding="utf-8"))
    if a.offen:
        for r in data["applications"]:
            erw = ERWARTET.get(r.get("status"))
            arten = {e.get("ereignis") for e in r.get("verlauf") or []}
            if erw and erw not in arten:
                print(f"{r['id']:60s} {r.get('status'):14s} fehlt: {erw}")
        return 0
    if not a.id:
        ap.print_help()
        return 2
    if not a.ereignis:
        r = next((x for x in data["applications"] if x["id"] == a.id), None)
        if not r:
            sys.exit(f"id {a.id} nicht gefunden")
        zeigen(r)
        return 0
    if a.ereignis in QUELLE_PFLICHT and not a.quelle:
        sys.exit(f"Abbruch: --quelle ist bei '{a.ereignis}' Pflicht (Datei, die das Ereignis belegt).")
    if a.quelle and not (ROOT / a.quelle).exists():
        sys.exit(f"Abbruch: Quelle {a.quelle} existiert nicht.")
    datum = a.datum or heute().isoformat()
    try:
        datetime.date.fromisoformat(datum)
    except ValueError:
        sys.exit(f"Abbruch: Datum {datum} ist kein JJJJ-MM-TT.")
    e = {"datum": datum, "ereignis": a.ereignis, "quelle": a.quelle or "", "notiz": a.notiz[:300]}
    if a.probe:
        print("Probe:", e)
        return 0
    try:
        with transaktion(f"ereignis.py {a.id} {a.ereignis} {datum}") as d:
            r = next((x for x in d["applications"] if x["id"] == a.id), None)
            if not r:
                raise SystemExit(f"id {a.id} nicht gefunden")
            vl = r.setdefault("verlauf", [])
            if any(x.get("datum") == datum and x.get("ereignis") == a.ereignis for x in vl):
                print("Ereignis existiert schon an diesem Datum — nichts geschrieben.")
                return 0
            vl.append(e)
            vl.sort(key=lambda x: x.get("datum", ""))
            zeigen(r)
    except Konflikt as k:
        sys.exit(f"KONFLIKT: {k}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
