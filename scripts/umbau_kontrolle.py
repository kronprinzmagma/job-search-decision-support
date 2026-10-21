#!/usr/bin/env python3
"""Wirkungskontrolle Kostenumbau Screening-Sweep (Massnahme 2025-04-06-vorscan in data/retro_massnahmen.json).

Anlass: Der Sweep wurde billiger gemacht (Vorscan ohne Modell für das Jobportal, schlanke Arbeitskarte
spec/SWEEP.md, kleineres Modell). Gemessen wird, dass dabei die Zahl der Kandidaten nicht einbricht: solange
passende Stellen weiterhin so schnell wie möglich sichtbar werden, ist der Umbau ein Erfolg.

Vergleicht die Sweeps VOR dem Umbau (ab VORHER_AB, Drei-Sweep-Modell) mit den Sweeps NACH dem Umbau
(ab UMBAU_AB). Gemessen wird, was zählt:
  1. Kandidaten je Sweep (gesamt und Jobportal)        -> bricht die Ausbeute ein?
  2. Kandidatenquote = Kandidaten / neue Sichtungen     -> korrigiert schwache Markttage (Wochenende)
  3. Minuten vom Sweep-Start bis der Kandidat geloggt ist (Median) -> erscheinen Stellen weiter schnell?
  4. Abgeschlossene Sweeps je Tag                        -> fällt etwas aus?
  5. Kosten: Dauer je Sweep (Median), Modell, Anteil Jobportal-Abfragen über den Vorscan -> wirkt der Umbau?
ALARM (Poisson, einseitig 5 %): weniger Kandidaten als nach dem Vorher-Schnitt zu erwarten, erst ab
MIN_SWEEPS_NACHHER Sweeps nachher.
Aufruf: python3 scripts/umbau_kontrolle.py [--kurz]   Exit 1 bei ALARM. jobcoach.py zeigt ALARM als Wächter-Befund
(warnungen()).
"""
import json, math, sys, statistics
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Grenzen der Vergleichsphasen (Sweep-IDs <datum>-<art>). Demo: Drei-Sweep-Modell ab 2025-03-17,
# Umbau ab dem ersten Sweep am 2025-04-07 (vgl. scripts/init_demo.py, UMBAU).
VORHER_AB, UMBAU_AB = "2025-03-17-morgen", "2025-04-07-morgen"
ARTEN = {"morgen": 0, "mittag": 1, "nachmittag": 2, "zusatz": 3}
MIN_SWEEPS_NACHHER = 9
KANAL_VORSCAN = "portal"          # Kanal, den der Vorscan ohne Modell übernimmt
MIN_ANTEIL_VORSCAN = 0.8          # darunter: Vorscan wird nachher nicht wie vorgesehen genutzt


def schluessel(sid):
    d, _, art = sid.rpartition("-")
    return (d, ARTEN.get(art, 9))


def poisson_cdf(k, lam):
    return sum(math.exp(-lam) * lam ** i / math.factorial(i) for i in range(k + 1))


def _dauer(s):
    mins = 0.0
    for se in s.get("sessions") or []:
        try:
            mins += max(0, (datetime.fromisoformat(se["ende"]) - datetime.fromisoformat(se["start"])).total_seconds() / 60)
        except (KeyError, TypeError, ValueError):
            pass
    return mins or None


def messen():
    log = json.loads((ROOT / "data" / "screening_log.json").read_text(encoding="utf-8"))
    sweeps = {s["id"]: s for s in log.get("sweeps", []) if s.get("status") == "abgeschlossen"
              and s["id"].rsplit("-", 1)[-1] in ("morgen", "mittag", "nachmittag")}
    kand, neu, minuten = {}, {}, {}
    luecken, portal_n, portal_vorscan = {}, {}, {}
    for l in log["laeufe"]:
        sid = l.get("lauf_id")
        if sid not in sweeps:
            continue
        if l.get("status") in ("teilweise", "nicht-erreichbar", "uebersprungen"):
            luecken[sid] = luecken.get(sid, 0) + 1
        if l.get("kanal") == KANAL_VORSCAN:
            portal_n[sid] = portal_n.get(sid, 0) + 1
            portal_vorscan[sid] = portal_vorscan.get(sid, 0) + ("vorscan" in (l.get("notiz") or "").lower())
    for e in log["gesichtet"]:
        sid = e.get("lauf_id")
        if sid not in sweeps:
            continue
        neu[sid] = neu.get(sid, 0) + 1
        if e.get("entscheid") == "kandidat":
            k = kand.setdefault(sid, {"alle": 0, "portal": 0})
            k["alle"] += 1
            k["portal"] += e.get("kanal") == KANAL_VORSCAN
            try:
                t0 = datetime.fromisoformat(sweeps[sid]["start"])
                t1 = datetime.fromisoformat(f"{e['datum']}T{e['zeit']}")
                minuten.setdefault(sid, []).append(max(0, (t1 - t0).total_seconds() / 60))
            except Exception:
                pass
    phasen = {"vorher": [], "nachher": []}
    for sid in sorted(sweeps, key=schluessel):
        if schluessel(sid) < schluessel(VORHER_AB):
            continue
        phasen["vorher" if schluessel(sid) < schluessel(UMBAU_AB) else "nachher"].append(sid)
    erg = {}
    for ph, ids in phasen.items():
        tage = {i.rsplit("-", 1)[0] for i in ids}
        mins = [m for i in ids for m in minuten.get(i, [])]
        dauern = [x for x in (_dauer(sweeps[i]) for i in ids) if x]
        modelle = Counter(se.get("modell") or "?" for i in ids for se in sweeps[i].get("sessions") or [])
        p_n = sum(portal_n.get(i, 0) for i in ids)
        erg[ph] = {"sweeps": len(ids), "tage": len(tage),
                   "kand": sum(kand.get(i, {}).get("alle", 0) for i in ids),
                   "kand_portal": sum(kand.get(i, {}).get("portal", 0) for i in ids),
                   "neu": sum(neu.get(i, 0) for i in ids),
                   "min_median": statistics.median(mins) if mins else None,
                   "sweeps_je_tag": len(ids) / max(len(tage), 1),
                   "luecken": sum(luecken.get(i, 0) for i in ids) / max(len(ids), 1) if ids else None,
                   "dauer_median": statistics.median(dauern) if dauern else None,
                   "modell": modelle.most_common(1)[0][0] if modelle else None,
                   "vorscan_anteil": sum(portal_vorscan.get(i, 0) for i in ids) / p_n if p_n else None}
    return erg


def bewerten(erg):
    v, n = erg["vorher"], erg["nachher"]
    befunde = []
    # Vollständigkeit: schon ab dem ersten Sweep prüfen — eine Seite oder ein Teil ist nicht gut genug.
    if n["sweeps"] and n["luecken"] is not None and n["luecken"] > 2 * (v["luecken"] or 0) + 1:
        befunde.append(f"ALARM Vollständigkeit: {n['luecken']:.1f} unvollständige Abfragen je Sweep (vorher {v['luecken'] or 0:.1f}) — "
                       f"Liste in notes/<Datum>_screening_<Art>.md, Abschnitt «Abdeckung»")
    if n["sweeps"] < MIN_SWEEPS_NACHHER:
        return befunde, ("auffällig — " if befunde else "") + f"zu früh für ein Urteil ({n['sweeps']} von mindestens {MIN_SWEEPS_NACHHER} Sweeps nach dem Umbau)"
    for feld, name in (("kand", "Kandidaten gesamt"), ("kand_portal", "Kandidaten über das Jobportal")):
        lam = v[feld] / max(v["sweeps"], 1) * n["sweeps"]
        p = poisson_cdf(n[feld], lam)
        if lam >= 3 and p < 0.05:
            befunde.append(f"ALARM Kostenumbau: {name} eingebrochen — {n[feld]} in {n['sweeps']} Sweeps, "
                           f"erwartet ~{lam:.0f} nach dem Schnitt vorher (Zufall unwahrscheinlich, p={p:.3f}). "
                           f"Rückweg: Vorscan aussetzen (Jobportal wieder im Browser) und Massnahme 2025-04-06-vorscan "
                           f"in der Prozess-Retro neu entscheiden")
    qv, qn = v["kand"] / max(v["neu"], 1), n["kand"] / max(n["neu"], 1)
    if qv and qn < 0.5 * qv:
        befunde.append(f"ALARM Kostenumbau: Kandidatenquote halbiert ({100*qn:.1f} % statt {100*qv:.1f} % der neuen Sichtungen)")
    if v["min_median"] is not None and n["min_median"] is not None and n["min_median"] > v["min_median"] + 15:
        befunde.append(f"Hinweis Kostenumbau: Kandidaten erscheinen später im Sweep (Median {n['min_median']:.0f} statt {v['min_median']:.0f} Min. nach Start)")
    if n["sweeps_je_tag"] < v["sweeps_je_tag"] - 0.4:
        befunde.append(f"ALARM Kostenumbau: nur {n['sweeps_je_tag']:.1f} abgeschlossene Sweeps je Tag (vorher {v['sweeps_je_tag']:.1f})")
    # Kostenseite: hat der Umbau überhaupt gespart?
    if v["dauer_median"] is not None and n["dauer_median"] is not None and n["dauer_median"] >= v["dauer_median"]:
        befunde.append(f"Hinweis Kostenumbau: keine Zeitersparnis (Dauer je Sweep im Median {n['dauer_median']:.0f} statt {v['dauer_median']:.0f} Min.)")
    if n["vorscan_anteil"] is not None and n["vorscan_anteil"] < MIN_ANTEIL_VORSCAN:
        befunde.append(f"Hinweis Kostenumbau: nur {100*n['vorscan_anteil']:.0f} % der Jobportal-Abfragen über den Vorscan "
                       f"(Soll mindestens {100*MIN_ANTEIL_VORSCAN:.0f} %)")
    return befunde, "im Rahmen" if not befunde else "auffällig"


def main():
    erg = messen()
    befunde, urteil = bewerten(erg)
    if "--kurz" not in sys.argv:
        print(f"Vorher: {VORHER_AB} bis vor {UMBAU_AB} · Nachher: ab {UMBAU_AB}\n")
        print("| | vorher | nachher |\n|---|---|---|")
        f = lambda x, d=1: "–" if x is None else (x if isinstance(x, str) else f"{x:.{d}f}")
        for ph in ("vorher", "nachher"):
            e = erg[ph]
            e["kps"] = e["kand"] / e["sweeps"] if e["sweeps"] else None
            e["pps"] = e["kand_portal"] / e["sweeps"] if e["sweeps"] else None
            e["q"] = 100 * e["kand"] / e["neu"] if e["neu"] else None
            e["vs"] = 100 * e["vorscan_anteil"] if e["vorscan_anteil"] is not None else None
        v, n = erg["vorher"], erg["nachher"]
        for name, key, d in (("Sweeps (abgeschlossen)", "sweeps", 0), ("Sweeps je Tag", "sweeps_je_tag", 1),
                             ("Kandidaten je Sweep", "kps", 2), ("davon Jobportal je Sweep", "pps", 2),
                             ("Kandidatenquote % der Neuen", "q", 2), ("Unvollständige Abfragen je Sweep", "luecken", 1),
                             ("Min. Sweep-Start → Kandidat (Median)", "min_median", 0),
                             ("Dauer je Sweep, Min. (Median)", "dauer_median", 0), ("Modell (häufigstes)", "modell", 0),
                             ("Jobportal-Abfragen über Vorscan %", "vs", 0)):
            print(f"| {name} | {f(v[key], d)} | {f(n[key], d)} |")
    print(f"Urteil: {urteil}")
    for b in befunde:
        print("  " + b)
    return 1 if any(b.startswith("ALARM") for b in befunde) else 0


def warnungen():
    """Für jobcoach.py: nur Befunde, kein Rauschen."""
    try:
        return bewerten(messen())[0]
    except Exception as e:
        return [f"umbau_kontrolle.py lief nicht: {e}"]


if __name__ == "__main__":
    sys.exit(main())
