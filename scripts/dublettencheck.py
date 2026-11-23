#!/usr/bin/env python3
"""Dublettencheck gegen data/pipeline.json.

Anlass: Der Sweep legte eine Stelle als neuen Kandidaten vor, die seit dem Vormittag als Draft im Repo
lag; der Abgleich stand als Text in der Arbeitskarte, wurde behauptet, aber nicht ausgefuehrt
(feedback/2025-03-18_dublette-behauptet-nicht-geprueft.md).

Dieses Skript macht den Abgleich ausfuehrbar. Es wird VOR jeder Vorlage aufgerufen, nicht danach.

Aufruf:
    python3 scripts/dublettencheck.py "Beispiel Versicherung AG" "Product Owner"
    python3 scripts/dublettencheck.py --datei kandidaten.txt   # eine Zeile: Firma|Rolle
    echo "Beispiel Versicherung AG|Product Owner" | python3 scripts/dublettencheck.py -

Ausgabe je Kandidat: NEU / TREFFER (mit Status, Datum, id).
Exit-Code 1, sobald mindestens ein Treffer vorliegt.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIPE = ROOT / "data" / "pipeline.json"


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("ss", "s")
    # ae/oe/ue gleich behandeln wie ä/ö/ü («Zuerich» = «Zürich»)
    s = s.replace("ae", "a").replace("oe", "o").replace("ue", "u")
    # Rechtsformen und Fuellwoerter raus
    s = re.sub(r"\b(ag|sa|gmbh|holding|group|gruppe|schweiz|switzerland|co|and|und|the)\b", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def eintraege(obj):
    if isinstance(obj, list):
        for x in obj:
            yield from eintraege(x)
    elif isinstance(obj, dict):
        if "id" in obj and "firma" in obj:
            yield obj
        for v in obj.values():
            yield from eintraege(v)


def laden():
    with PIPE.open(encoding="utf-8") as fh:
        return list(eintraege(json.load(fh)))


def pruefe(firma, rolle, daten):
    nf, nr = norm(firma), norm(rolle)
    treffer = []
    for e in daten:
        ef = norm(e.get("firma") or "")
        if not ef or not nf:
            continue
        # Firmentreffer: eines enthaelt das andere
        if nf in ef or ef in nf:
            er = norm(e.get("rolle") or "")
            rollen_naehe = bool(nr and er and (nr in er or er in nr or
                                               len(set(nr.split()) & set(er.split())) >= 2))
            treffer.append((e, rollen_naehe))
    return treffer


def main():
    args = sys.argv[1:]
    paare = []
    if args and args[0] == "-":
        paare = [l.strip().split("|", 1) for l in sys.stdin if l.strip()]
    elif args and args[0] == "--datei":
        for l in Path(args[1]).read_text(encoding="utf-8").splitlines():
            if l.strip():
                paare.append(l.strip().split("|", 1))
    elif len(args) >= 2:
        paare = [[args[0], args[1]]]
    else:
        print(__doc__)
        return 2

    daten = laden()
    gefunden = False
    for p in paare:
        firma = p[0].strip()
        rolle = (p[1] if len(p) > 1 else "").strip()
        tr = pruefe(firma, rolle, daten)
        if not tr:
            # Zweite Stufe: taucht die Firma irgendwo im Freitext auf (Begruendungen, Notizen),
            # ohne eigenen Datensatz? Dann wurde sie schon einmal gesehen und nie abgelegt.
            roh = PIPE.read_text(encoding="utf-8")
            kern = [w for w in firma.split() if len(w) > 3 and
                    w.lower() not in ("group", "partner", "gruppe", "holding", "genossenschaft",
                                      "versicherung", "versicherungen", "schweiz", "suisse",
                                      "informatik", "solutions", "services", "consulting")]
            erwaehnt = [w for w in kern if w in roh]
            if erwaehnt:
                print(f"NEU*     | {firma} | {rolle}")
                print(f"         -> ACHTUNG: «{erwaehnt[0]}» kommt im Freitext von pipeline.json vor, "
                      f"aber ohne eigenen Datensatz. Schon einmal gesehen und nie abgelegt? Pruefen.")
            else:
                print(f"NEU      | {firma} | {rolle}")
            continue
        gefunden = True
        for e, nah in tr:
            marke = "ROLLE GLEICH" if nah else "gleiche Firma, andere Rolle"
            print(f"TREFFER  | {firma} | {rolle}")
            print(f"         -> {marke}: {e.get('firma')} — {e.get('rolle')} "
                  f"[{e.get('status')}, {e.get('datum') or e.get('datum_eingereicht') or '?'}, id={e.get('id')}]")
    return 1 if gefunden else 0


if __name__ == "__main__":
    sys.exit(main())
