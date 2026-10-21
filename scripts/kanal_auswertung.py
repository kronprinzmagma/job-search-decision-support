#!/usr/bin/env python3
"""Kanal-Auswertung für die Prozess-Retro: welcher Kanal hat mehr Anzeigen, wo sind sie schneller verfügbar?

Liest nur data/screening_log.json (gesichtet), schreibt nichts. Karriere- und Behördenportale werden
zusätzlich einzeln ausgewiesen.

Je Kanal (und je Zielportal): gesichtet, Kandidaten, «nur hier» (Stelle in keinem anderen Kanal gesehen),
«zuerst hier» (bei Stellen, die in mehreren Kanälen auftauchen: wo zuerst gesichtet) und der Vorsprung
in Stunden gegenüber dem nächsten Kanal. «Zuerst publiziert» nur, wo ein Publikationsdatum geloggt ist.
Gleiche Stelle = gleiche Firma + gleiche Rolle nach Normalisierung (Grenze: leicht anders benannte Titel
werden nicht als dieselbe Stelle erkannt).

Aufruf: python3 scripts/kanal_auswertung.py [--tage 28]
"""
import json, re, sys, unicodedata
from collections import defaultdict
from datetime import datetime, timedelta, date
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from heute import heute  # noqa: E402

LOG = ROOT / "data" / "screening_log.json"
KANAELE = ["portal", "netzwerk-suche", "netzwerk-empfehlung", "netzwerk-tracker",
           "zielportal", "karriereseite", "behoerdenportal", "abo", "netzwerk", "manuell"]
PORTALE = ("zielportal", "karriereseite", "behoerdenportal")


def _n(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\((m|w|d|f|h|x|all|w/m/d|m/w/d|m/f/d|f/m/d|w/d/m)[^)]*\)", " ", s)
    s = re.sub(r"\b\d{2,3}\s*(-|–|bis)?\s*\d{0,3}\s*%", " ", s)
    s = re.sub(r"\b(ag|gmbh|sa|ltd|inc|schweiz|switzerland|suisse)\b", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def _zeit(x):
    try:
        return datetime.fromisoformat(f"{x['datum']}T{x.get('zeit') or '12:00:00'}")
    except Exception:
        return None


def _publiziert(x):
    p = (x.get("publiziert") or "").strip().lower()
    if not p:
        return None
    try:
        if re.match(r"^\d{4}-\d{2}-\d{2}", p):
            return date.fromisoformat(p[:10])
        d = date.fromisoformat(x["datum"])
        if p in ("heute", "today") or re.search(r"stunde|minute|hour", p):
            return d
        if p in ("gestern", "yesterday"):
            return d - timedelta(days=1)
        m = re.search(r"(\d+)\s*(tag|day)", p)
        if m:
            return d - timedelta(days=int(m.group(1)))
        m = re.search(r"(\d+)\s*(woche|week)", p)
        if m:
            return d - timedelta(weeks=int(m.group(1)))
    except Exception:
        return None
    return None


def _kanal(k):
    return k if k in KANAELE else "sonstige"


def auswerten(tage=28, bis=None):
    g = json.loads(LOG.read_text(encoding="utf-8"))["gesichtet"]
    bis = bis or (heute() - timedelta(days=1)).isoformat()
    von = (date.fromisoformat(bis) - timedelta(days=tage - 1)).isoformat()
    stellen = defaultdict(list)          # Schlüssel -> Sichtungen
    for x in g:
        if not x.get("firma") or not x.get("rolle") or not x.get("datum"):
            continue
        stellen[(_n(x["firma"]), _n(x["rolle"]))].append(x)
    k = defaultdict(lambda: defaultdict(float)); portal = defaultdict(lambda: defaultdict(float))
    vorsprung = defaultdict(list); pub_frueher = defaultdict(int); pub_vergleiche = 0
    for key, xs in stellen.items():
        erst = min(xs, key=lambda x: (_zeit(x) or datetime.max))
        if not (von <= erst["datum"] <= bis):
            continue                      # Stelle zuerst im Fenster gesehen
        kan = {}
        for x in xs:
            kk = _kanal(x.get("kanal")); t = _zeit(x)
            if t and (kk not in kan or t < kan[kk][0]):
                kan[kk] = (t, x)
        kandidat = any(x.get("entscheid") == "kandidat" for x in xs)
        for kk, (t, x) in kan.items():
            k[kk]["gesichtet"] += 1
            if kandidat: k[kk]["kandidaten"] += 1
            if kk in PORTALE:
                pid = x.get("gefunden_ueber") or "?"
                portal[pid]["gesichtet"] += 1
                if kandidat: portal[pid]["kandidaten"] += 1
                if len(kan) == 1 and kandidat: portal[pid]["nur_hier_kand"] += 1
        if len(kan) == 1:
            kk = next(iter(kan)); k[kk]["nur_hier"] += 1
            if kandidat: k[kk]["nur_hier_kand"] += 1
        else:
            reihe = sorted(kan.items(), key=lambda e: e[1][0])
            (k1, (t1, x1)), (k2, (t2, _)) = reihe[0], reihe[1]
            k[k1]["zuerst"] += 1
            vorsprung[k1].append((t2 - t1).total_seconds() / 3600)
            if k1 in PORTALE:
                portal[x1.get("gefunden_ueber") or "?"]["zuerst"] += 1
            pubs = {kk: _publiziert(x) for kk, (t, x) in kan.items()}
            pubs = {kk: p for kk, p in pubs.items() if p}
            if len(pubs) >= 2:
                pub_vergleiche += 1
                frueh = min(pubs.values())
                for kk, p in pubs.items():
                    if p == frueh: pub_frueher[kk] += 1
    return von, bis, k, portal, vorsprung, pub_frueher, pub_vergleiche


def abschnitt(tage=28, bis=None):
    von, bis, k, portal, vors, pubf, pubv = auswerten(tage, bis)
    z = [f"## Kanal-Auswertung ({von} bis {bis}, {tage} Tage)", "",
         "Gleiche Stelle = gleiche Firma + Rolle (normalisiert). «Nur hier» = in keinem anderen Kanal gesehen. "
         "«Zuerst hier» = bei Stellen in mehreren Kanälen hier zuerst gesichtet; Vorsprung = Median in Stunden zum nächsten Kanal.", "",
         "| Kanal | Stellen | Kandidaten | nur hier | davon Kandidaten | zuerst hier | Vorsprung (h) |",
         "|---|---|---|---|---|---|---|"]
    for kk in KANAELE + ["sonstige"]:
        if kk not in k: continue
        v = k[kk]; vs = vors.get(kk)
        z.append(f"| {kk} | {int(v['gesichtet'])} | {int(v['kandidaten'])} | {int(v['nur_hier'])} | {int(v['nur_hier_kand'])} | "
                 f"{int(v['zuerst'])} | {round(median(vs)) if vs else '-'} |")
    z += ["", f"Zuerst publiziert (nur Stellen mit Publikationsdatum in mindestens zwei Kanälen, n = {pubv}): "
          + (", ".join(f"{kk} {n}" for kk, n in sorted(pubf.items(), key=lambda e: -e[1])) if pubv else "noch keine Vergleichsfälle"), ""]
    if portal:
        z += ["### Karriere- und Behördenportale einzeln", "",
              "| Portal | Stellen | Kandidaten | Kandidaten nur hier | zuerst hier |", "|---|---|---|---|---|"]
        for pid, v in sorted(portal.items(), key=lambda e: (-e[1]["kandidaten"], -e[1]["gesichtet"], e[0])):
            z.append(f"| {pid} | {int(v['gesichtet'])} | {int(v['kandidaten'])} | {int(v['nur_hier_kand'])} | {int(v['zuerst'])} |")
        z += ["", "Lesart: Ein Portal ohne Kandidaten «nur hier» und ohne «zuerst hier» liefert nichts, was Jobportal oder "
              "Netzwerk nicht auch zeigen — Kandidat zum Streichen im Wochen-Review (Entscheid bei Alex)."]
    return z


if __name__ == "__main__":
    a = sys.argv[1:]
    tage = int(a[a.index("--tage") + 1]) if "--tage" in a else 28
    print("\n".join(abschnitt(tage)))
