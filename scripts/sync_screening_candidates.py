#!/usr/bin/env python3
"""Offene Screening-Kandidaten als kanonische ``vorgelegt``-Datensaetze erfassen.

Das Screening-Log bleibt die Herkunftsspur. Die Aktionsliste lebt in ``data/pipeline.json``:
ein Kandidat, der nur im Log steht, erscheint nirgends als offener Entscheid und geht unter.
Standard ist eine Vorschau; ``--apply`` schreibt ueber ``pipeline_tx.py`` und ueberschreibt keine
bestehenden Datensaetze.

    python3 scripts/sync_screening_candidates.py
    python3 scripts/sync_screening_candidates.py --apply [--tage 14]
"""

import argparse
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from cockpit import entschieden  # noqa: E402
from heute import heute  # noqa: E402
from jobcoach import slugify  # noqa: E402
from pipeline_tx import Konflikt, transaktion  # noqa: E402

LOG = ROOT / "data" / "screening_log.json"


def kandidaten(log, apps, tage):
    grenze = (heute() - datetime.timedelta(days=tage)).isoformat()
    out, gesehen = [], set()
    for eintrag in reversed(log.get("gesichtet", [])):
        if eintrag.get("entscheid") != "kandidat" or eintrag.get("datum", "") < grenze:
            continue
        schluessel = (eintrag.get("firma", "").strip().lower(), eintrag.get("rolle", "").strip().lower())
        if schluessel in gesehen or entschieden(eintrag, apps):
            continue
        gesehen.add(schluessel)
        out.append(eintrag)
    return list(reversed(out))


def neue_id(eintrag, bestehend):
    basis = slugify(f"{eintrag.get('firma', '')}-{eintrag.get('rolle', '')}")[:60].rstrip("-")
    kandidat, nummer = basis, 2
    while kandidat in bestehend:
        kandidat, nummer = f"{basis}-{nummer}", nummer + 1
    bestehend.add(kandidat)
    return kandidat


def datensatz(eintrag, bestehend):
    lauf = eintrag.get("lauf_id") or ""
    tag, art = lauf.rsplit("-", 1) if "-" in lauf else (eintrag.get("datum") or "", "")
    notiz = ROOT / "notes" / f"{tag}_screening_{art}.md"
    quelle = str(notiz.relative_to(ROOT)) if notiz.exists() else f"data/screening_log.json ({lauf or 'ohne Lauf-ID'})"
    grund = (eintrag.get("grund") or "").strip()
    return {
        "id": neue_id(eintrag, bestehend),
        "firma": eintrag.get("firma"),
        "rolle": eintrag.get("rolle"),
        "status": "vorgelegt",
        "datum": eintrag.get("datum"),
        "standort": eintrag.get("ort") or "unbekannt",
        "quelle": quelle,
        "notiz": f"Aus Screening-Log kanonisiert; Go/NoGo offen. {grund}".strip(),
        "verlauf": [{
            "datum": eintrag.get("datum"),
            "ereignis": "vorgelegt",
            "quelle": quelle,
            "notiz": "Als Kandidat vorgelegt; Entscheid bei Alex offen.",
        }],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Datensaetze transaktional schreiben")
    parser.add_argument("--tage", type=int, default=14, help="Rueckblick im Screening-Log (Standard: 14)")
    args = parser.parse_args()

    log = json.loads(LOG.read_text(encoding="utf-8"))
    pipeline = json.loads((ROOT / "data" / "pipeline.json").read_text(encoding="utf-8"))
    offen = kandidaten(log, pipeline["applications"], args.tage)
    if not offen:
        print("Keine Log-Kandidaten ohne Pipeline-Datensatz.")
        return 0

    print(f"{len(offen)} Log-Kandidat(en) ohne Pipeline-Datensatz:")
    for eintrag in offen:
        print(f"- {eintrag.get('firma')} — {eintrag.get('rolle')} ({eintrag.get('datum')})")
    if not args.apply:
        print("Vorschau; mit --apply als Status 'vorgelegt' erfassen.")
        return 0

    try:
        with transaktion("sync_screening_candidates.py") as data:
            offen = kandidaten(log, data["applications"], args.tage)
            bestehend = {a.get("id") for a in data["applications"] if a.get("id")}
            data["applications"].extend(datensatz(e, bestehend) for e in offen)
    except Konflikt as exc:
        raise SystemExit(f"KONFLIKT: {exc}")
    print(f"{len(offen)} Datensatz/Datensätze mit Status 'vorgelegt' geschrieben.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
