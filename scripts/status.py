#!/usr/bin/env python3
"""
status — Statuswechsel in EINEM Schritt: Datensatz + Fall-Ordner + Ereignis + Nachtrag + Views.

Anlass: Fast jede Abweichung im Tracker entstand, weil eine Datei verschoben oder eine Rueckmeldung
abgelegt, der Datensatz aber nicht nachgefuehrt wurde (Absage im Ordner, Status noch «abgeschickt»).
Dieser Befehl macht beides zugleich.

    python3 scripts/status.py <id> <status> [Optionen] [--probe]

Status: vorgelegt | draft | abgeschickt | in_pruefung | gespraech | abgesagt | zurueckgezogen | angebot | aussortiert
Optionen:
  --datum JJJJ-MM-TT     Datum des Ereignisses (Default heute): Einreichung / Absage / Termin
  --quelle PFAD          Primaerdatei, die den Wechsel belegt (Pflicht ausser bei draft)
  --stadium TEXT         Pflicht bei abgesagt
  --begruendung TEXT     Pflicht bei abgesagt, aussortiert, zurueckgezogen
  --notiz TEXT           zusaetzlicher Nachtrag
  --ohne-recherche GRUND Versand ohne Recherche ausnahmsweise zulassen (Grund wird vermerkt)
  --probe                nichts schreiben, nur zeigen, was passieren wuerde

Der Status lebt nur im Datensatz. Einzige Dateibewegung: Bei offenem Entscheid oder offenem Versand
(vorgelegt, draft) liegt der ganze Fall-Ordner in eingang/<id>/, in allen anderen Status in stellen/<id>/.
Der Statuswechsel verschiebt den Ordner dorthin und fuehrt `anzeige`, `dossier` und die Belege im Verlauf
nach. Zusaetzlich schreibt er ein Ereignis in `verlauf` (go / versand / eingang / gespraech / absage /
rueckzug / nogo / angebot) mit Datum und Quelle.
Kein Versand ohne Recherche: `abgeschickt` bricht ab, solange <id>--recherche--<datum>.md oder
<id>--personen--<datum>.md fehlt.
Geschrieben wird ueber scripts/pipeline_tx.py (Sperre + Konfliktpruefung). Danach laeuft jobcoach.py.
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from heute import heute  # noqa: E402
from jobcoach import EMOJI, OFFENE_ABLAGE  # noqa: E402
from pipeline_tx import ROOT, Konflikt, transaktion  # noqa: E402

PFLICHT = {"abgesagt": ("stadium", "begruendung"), "aussortiert": ("begruendung",), "zurueckgezogen": ("begruendung",)}
EREIGNIS = {"abgeschickt": "versand", "in_pruefung": "eingang", "gespraech": "gespraech", "abgesagt": "absage",
            "zurueckgezogen": "rueckzug", "aussortiert": "nogo", "angebot": "angebot", "draft": "go",
            "vorgelegt": None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("status", choices=list(EMOJI))
    for o in ("datum", "quelle", "stadium", "begruendung", "notiz"):
        ap.add_argument("--" + o)
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--ohne-recherche", dest="ohne_recherche", metavar="GRUND",
                    help="Versand ohne Recherche ausnahmsweise zulassen (Grund Pflicht, wird vermerkt)")
    a = ap.parse_args()
    datum = a.datum or heute().isoformat()
    for f in PFLICHT.get(a.status, ()):
        if not getattr(a, f):
            sys.exit(f"Abbruch: --{f} ist bei Status '{a.status}' Pflicht.")
    if a.status != "draft" and not a.quelle:
        sys.exit("Abbruch: --quelle (Primaerdatei, die den Wechsel belegt) ist Pflicht.")
    if a.quelle and not (ROOT / a.quelle).exists():
        sys.exit(f"Abbruch: Quelle {a.quelle} existiert nicht.")
    # Kein Versand ohne Firmen- und Personen-Recherche (Pflicht nach dem Go, spec/RECHERCHE.md)
    if a.status == "abgeschickt" and not a.ohne_recherche:
        fehlt = [typ for typ in ("recherche", "personen")
                 if not any(list((ROOT / b / a.id).glob(f"{a.id}--{typ}--*.md")) for b in ("eingang", "stellen"))]
        if fehlt:
            sys.exit(f"Abbruch: Fuer {a.id} fehlt die Recherche: {' und '.join(fehlt)} ({a.id}--<typ>--<datum>.md im Fall-Ordner). "
                     "Erst erstellen — oder ausnahmsweise --ohne-recherche \"<Grund>\".")
    if a.ohne_recherche:
        a.notiz = ((a.notiz or "") + f" Versand ohne Recherche: {a.ohne_recherche}").strip()
    fertig = []

    def bewegungen_zurueckrollen():
        while fertig:
            q, z = fertig.pop()
            if z.exists() and not q.exists():
                os.rename(z, q)

    try:
        with transaktion(f"status.py {a.id} -> {a.status}") as data:
            treffer = [r for r in data["applications"] if r.get("id") == a.id]
            if len(treffer) != 1:
                raise SystemExit(f"Abbruch: id '{a.id}' kommt {len(treffer)}x vor.")
            r = treffer[0]
            alt = r.get("status")
            bewegungen = []
            if r.get("anzeige") and not (ROOT / r["anzeige"]).exists():
                raise SystemExit(f"Abbruch: Anzeige {r['anzeige']} existiert nicht — zuerst Feld 'anzeige' korrigieren.")
            if a.quelle and not a.quelle.startswith((f"stellen/{a.id}/", f"eingang/{a.id}/")):
                print(f"Hinweis: Quelle liegt nicht im Fall-Ordner ({a.id}) — Belege gehoeren dorthin.")
            r["status"] = a.status
            # Ablage des Fall-Ordners: vorgelegt/draft -> eingang/<id>/, alle anderen -> stellen/<id>/.
            # Der ganze Ordner wandert, Pfade im Datensatz werden nachgefuehrt.
            ziel_root = "eingang" if a.status in OFFENE_ABLAGE else "stellen"
            alt_root = next((w for w in ("eingang", "stellen") if (ROOT / w / a.id).is_dir()), None)
            if alt_root and alt_root != ziel_root:
                bewegungen.append((ROOT / alt_root / a.id, ROOT / ziel_root / a.id))
                alt_p, neu_p = f"{alt_root}/{a.id}/", f"{ziel_root}/{a.id}/"
                um = lambda v: (neu_p + v[len(alt_p):]) if isinstance(v, str) and v.startswith(alt_p) else v  # noqa: E731
                for k in ("anzeige", "dossier", "debrief"):
                    if isinstance(r.get(k), str):
                        r[k] = neu_p.rstrip("/") if r[k] == alt_p.rstrip("/") else um(r[k])
                for e in r.get("verlauf") or []:
                    e["quelle"] = um(e.get("quelle"))
                a.quelle = um(a.quelle)
            if a.status in ("abgeschickt", "in_pruefung") and not r.get("datum_eingereicht"):
                r["datum_eingereicht"] = datum
                r["datum_ist_einreichung"] = True
            if a.status == "abgesagt":
                r["absage_datum"] = datum
                r["stadium"] = a.stadium
                r["begruendung"] = a.begruendung
            if a.status in ("aussortiert", "zurueckgezogen"):
                r["begruendung"] = a.begruendung
                r.setdefault("datum", datum)
            if a.status == "gespraech":
                r["gespraech_termin"] = datum
            ereignis = EREIGNIS.get(a.status)
            if ereignis:
                r.setdefault("verlauf", []).append({"datum": datum, "ereignis": ereignis, "quelle": a.quelle or "status.py",
                                                    "notiz": (a.stadium or a.begruendung or a.notiz or "")[:200]})
            vermerk = f"Nachtrag {heute().isoformat()} (status.py): {alt} → {a.status} ({datum})"
            if a.quelle:
                vermerk += f"; Quelle: {a.quelle}"
            if a.notiz:
                vermerk += f"; {a.notiz}"
            r["notiz"] = (r["notiz"] + " || " if r.get("notiz") else "") + vermerk
            print(vermerk)
            for q, z in bewegungen:
                print(f"verschiebe {q.relative_to(ROOT)} → {z.relative_to(ROOT)}")
            if bewegungen and not a.probe:
                for q, z in bewegungen:
                    if z.exists():
                        raise SystemExit(f"Abbruch: Ziel {z.relative_to(ROOT)} existiert schon.")
                    z.parent.mkdir(parents=True, exist_ok=True)
                    os.rename(q, z)
                    fertig.append((q, z))
            if a.probe:
                raise KeyboardInterrupt  # nichts schreiben
    except KeyboardInterrupt:
        bewegungen_zurueckrollen()
        print("Probe — nichts geschrieben.")
        return
    except Konflikt as k:
        bewegungen_zurueckrollen()
        sys.exit(f"KONFLIKT: {k}")
    except BaseException:
        bewegungen_zurueckrollen()
        raise
    if a.status == "draft":
        print(f"\n>>> PFLICHT JETZT, IM SELBEN ZUG: Firmen- und Personen-Recherche fuer {a.id} "
              f"(eingang/{a.id}/{a.id}--recherche--<datum>.md und --personen--<datum>.md). Ohne sie kein Anschreiben "
              "und kein Versand "
              "(status.py bricht bei 'abgeschickt' ab).\n")
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "jobcoach.py")], cwd=ROOT)
    if result.returncode:
        sys.exit(f"Status wurde gespeichert, aber jobcoach.py ist mit Exit-Code {result.returncode} "
                 "fehlgeschlagen; generierte Views sind veraltet.")


if __name__ == "__main__":
    main()
