#!/usr/bin/env python3
"""Offene Pflicht-Auftraege nach dem Go — deterministisch, ohne Modell.

Anlass: Nach einem klaren Go blieben Firmen- und Personen-Recherche liegen, bis der Mensch sie von Hand anstiess.
Eine Pflicht, die nur in einem Prompt steht, wird vergessen; dieses Skript macht sie pruefbar.

Jeder offene Fall nach dem Go (draft, abgeschickt, in_pruefung, gespraech, angebot) braucht im Fall-Ordner
`<id>--recherche--<datum>.md` und `<id>--personen--<datum>.md` (spec/RECHERCHE.md). Ausgabe: je Fall eine Zeile mit dem, was fehlt, und seit wann das Go steht.
Exit 1, wenn etwas offen ist.
Wird gelesen von: jobcoach.py (Waechter), Kandidaten-Chat (holt Offenes selbst ab), Pflegelauf.

    python3 scripts/offene_auftraege.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OFFEN = ("draft", "abgeschickt", "in_pruefung", "gespraech", "angebot")
PFLICHT = ("recherche", "personen")


def offene():
    d = json.loads((ROOT / "data" / "pipeline.json").read_text(encoding="utf-8"))
    out = []
    for a in d.get("applications", []):
        if a.get("status") not in OFFEN or not a.get("id"):
            continue
        go = [e.get("datum", "") for e in a.get("verlauf") or [] if e.get("ereignis") == "go"]
        go_datum = max(go) if go else "?"
        ordner = next((r / a["id"] for r in (ROOT / "eingang", ROOT / "stellen") if (r / a["id"]).is_dir()), None)
        if not ordner:
            out.append((a["id"], go_datum, ["Fall-Ordner fehlt"]))
            continue
        fehlt = [t for t in PFLICHT if not list(ordner.glob(f"{a['id']}--{t}--*.md"))]
        if fehlt:
            out.append((a["id"], go_datum, fehlt))
    return out


def warnungen():
    o = offene()
    if not o:
        return []
    return [f"GO OHNE RECHERCHE: {len(o)} Fall/Fälle — Pflicht nach dem Go nicht erfüllt "
            f"(Kandidaten-Chat holt das automatisch ab; Liste: python3 scripts/offene_auftraege.py)"] + \
           [f"    – {i} (Go {g}): fehlt {', '.join(f)}" for i, g, f in o]


if __name__ == "__main__":
    o = offene()
    if not o:
        print("Keine offenen Pflicht-Aufträge nach dem Go.")
        sys.exit(0)
    print(f"{len(o)} Fall/Fälle mit Go ohne Recherche:")
    for i, g, f in o:
        print(f"  {i} | Go {g} | fehlt: {', '.join(f)}")
    sys.exit(1)
