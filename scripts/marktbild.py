#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Marktbild: Tabellen über alles, was das Screening gesehen hat.

Zweck: Aus den Sweeps ein Marktbild ziehen. Die im Volltext geprüften Anzeigen liegen verbatim im
Fall-Ordner; die von vornherein ausgeschlossenen stehen hier in einer Tabelle, gruppiert nach Grund.

Erzeugt:
  MARKTBILD_VORFILTER.md         Tabelle aller auf Listenebene aussortierten Anzeigen,
                                 gruppiert nach Ausschlussgrund, mit Auswertung
  data/marktbild_vorfilter.csv   dieselben Daten als CSV zum Weiterrechnen
  MARKTBILD_VOLLTEXT.md          Tabelle aller im Volltext geprüften Fälle mit Verdikt,
                                 tragendem Ausschluss und Link auf die Anzeige

Aufruf:  python3 scripts/marktbild.py
"""
import csv, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "data" / "screening_log.json"
PIPE = ROOT / "data" / "pipeline.json"

# Grund-Kategorien für das Marktbild. Reihenfolge = Priorität beim Zuordnen.
KATEGORIEN = [
    ("Firmen-Ausschluss der Persona", r"firmen-ausschluss|glücksspiel|gluecksspiel"),
    ("Vermittler / Personalberatung", r"vermittler|personalberat|personalverleih|staffing|recruit"),
    ("Engineering / Entwicklung / Architektur", r"engineer|entwickl|architek|devops|developer|technisch"),
    ("Physisches Produktmanagement", r"physisch|hardware|maschin|lebensmittel|sortiment|textil|anlagen"),
    ("Distanz", r"(?<!kompetenz)distanz|pendel|ausserhalb|zu weit|ausschluss 2"),
    ("Junior / Praktikum / Lehrstelle", r"junior|praktik|lehrstell|trainee|schueler|studier"),
    ("Beratung / Agentur", r"beratung|agentur|consult|ausschluss 4"),
    ("Kein Produktmandat (Nicht-Rolle, Betrieb, Support)", r"nicht-rolle|kein produktmandat|betrieb|support|sachbearb|"
                                                           r"assistenz|administra|applikationsbetreu"),
    ("Business Analyse / Projektleitung", r"business analy|projektleit|business-analy"),
    ("Vertrieb / Marketing / HR / Finanzen", r"vertrieb|verkauf|sales|marketing|hr[- ]|personal|controlling|treasury|finanz"),
    ("Remote ohne Schweizer Standortbindung", r"remote emea|ohne schweizer standort|keine schweizer"),
    ("Klinik / Pflege / Fachberufe", r"pflege|klinik|aerzt|ärzt|therapeut|medizin|anaesthesie"),
]


def kategorie(grund):
    g = (grund or "").lower()
    for name, muster in KATEGORIEN:
        if re.search(muster, g):
            return name
    return "Sonstiges / nicht kategorisiert"


def zelle(x):
    return (x or "").replace("|", "/")


def main():
    d = json.loads(LOG.read_text(encoding="utf-8"))
    p = json.loads(PIPE.read_text(encoding="utf-8"))
    sicht = d.get("gesichtet", [])

    vor = [r for r in sicht if r.get("entscheid") == "vorfilter"]
    voll = [r for r in sicht if r.get("entscheid") in ("volltext-nogo", "kandidat", "dublette")]

    # ---------- CSV ----------
    csv_pfad = ROOT / "data" / "marktbild_vorfilter.csv"
    with csv_pfad.open("w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, delimiter=";")
        wr.writerow(["Datum", "Firma", "Rolle", "Ort", "Kanal", "Kategorie", "Grund", "GefundenUeber"])
        for r in sorted(vor, key=lambda x: (x.get("datum") or "", x.get("firma") or "")):
            wr.writerow([r.get("datum"), r.get("firma"), r.get("rolle"), r.get("ort"),
                         r.get("kanal"), kategorie(r.get("grund")), r.get("grund"), r.get("gefunden_ueber")])

    # ---------- MARKTBILD_VORFILTER.md ----------
    nach_kat = defaultdict(list)
    for r in vor:
        nach_kat[kategorie(r.get("grund"))].append(r)

    out = []
    out.append("# MARKTBILD — auf Listenebene aussortiert")
    out.append("")
    out.append("*Erzeugt von `scripts/marktbild.py` aus `data/screening_log.json`. Nicht von Hand bearbeiten.*")
    out.append("")
    out.append("Diese Datei enthält jede Anzeige, die das Screening gesehen und **ohne Volltext** aussortiert hat. "
               "Auf Listenebene dürfen nur Firmen-Ausschluss, Vermittler, Beratung/Agentur, Distanz laut Ortstabelle, "
               "Junior/Praktikum, Engineering- und Entwicklerrollen, offensichtliche Nicht-Rollen und physische Produkte "
               "entscheiden (`spec/SWEEP.md`, «Listenebene»). Die im Volltext geprüften Fälle stehen in "
               "`MARKTBILD_VOLLTEXT.md`, ihre Anzeigen als `<id>--anzeige--<erfasst>.md` im jeweiligen Fall-Ordner.")
    out.append("")
    out.append("Dieselben Daten als CSV zum Weiterrechnen: `data/marktbild_vorfilter.csv` (Semikolon-getrennt).")
    out.append("")
    out.append("## Überblick")
    out.append("")
    out.append("| Kategorie | Anzahl | Anteil |")
    out.append("|---|---:|---:|")
    total = len(vor) or 1
    for kat, rs in sorted(nach_kat.items(), key=lambda kv: -len(kv[1])):
        out.append(f"| {kat} | {len(rs)} | {100*len(rs)//total} % |")
    out.append(f"| **Total** | **{len(vor)}** | |")
    out.append("")

    kanal = Counter(r.get("kanal") for r in vor)
    out.append("## Woher das Rauschen kommt")
    out.append("")
    out.append("| Kanal | auf Listenebene weg |")
    out.append("|---|---:|")
    for k, n in kanal.most_common():
        out.append(f"| {k} | {n} |")
    out.append("")

    firmen = Counter(r.get("firma") for r in vor if r.get("firma"))
    mehrfach = [(f, n) for f, n in firmen.most_common() if n >= 3]
    if mehrfach:
        out.append("## Firmen mit drei oder mehr aussortierten Anzeigen")
        out.append("")
        out.append("*Wer oft auftaucht, sucht viel — auch wenn diesmal nichts passte. Kandidaten für die Zielportal-Liste.*")
        out.append("")
        out.append("| Firma | Anzeigen |")
        out.append("|---|---:|")
        for f, n in mehrfach:
            out.append(f"| {f} | {n} |")
        out.append("")

    out.append("## Alle Einträge nach Kategorie")
    out.append("")
    for kat, rs in sorted(nach_kat.items(), key=lambda kv: -len(kv[1])):
        out.append(f"### {kat} ({len(rs)})")
        out.append("")
        out.append("| Datum | Firma | Rolle | Ort | Kanal | Grund |")
        out.append("|---|---|---|---|---|---|")
        for r in sorted(rs, key=lambda x: (x.get("datum") or "", x.get("firma") or "")):
            g = zelle(r.get("grund"))
            if len(g) > 160:
                g = g[:157] + "…"
            out.append(f"| {r.get('datum') or ''} | {zelle(r.get('firma'))} | {zelle(r.get('rolle'))} | "
                       f"{zelle(r.get('ort'))} | {r.get('kanal') or ''} | {g} |")
        out.append("")

    (ROOT / "views").mkdir(exist_ok=True)
    (ROOT / "views" / "MARKTBILD_VORFILTER.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    # ---------- MARKTBILD_VOLLTEXT.md ----------
    def norm(x):
        t = (x or "").lower()
        for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue")):
            t = t.replace(a, b)
        return re.sub(r"[^a-z0-9]", "", t)

    nach_id = {a["id"]: a for a in p["applications"]}
    nach_firma_rolle = {}
    for a in p["applications"]:
        nach_firma_rolle.setdefault((norm(a.get("firma")), norm(a.get("rolle"))), a)

    def anzeige(r):
        """Anzeige der Sichtung: eigenes Feld, sonst über pipeline_id, sonst gleiche Firma und Rolle."""
        if r.get("anzeige"):
            a = nach_id.get(r.get("pipeline_id"))
            return (a or {}).get("anzeige") or r["anzeige"]   # Pipeline kennt den aktuellen Ort (eingang/ -> stellen/)
        a = nach_id.get(r.get("pipeline_id")) or nach_firma_rolle.get((norm(r.get("firma")), norm(r.get("rolle"))))
        return (a or {}).get("anzeige") or "—"

    o2 = []
    o2.append("# MARKTBILD — im Volltext geprüft")
    o2.append("")
    o2.append("*Erzeugt von `scripts/marktbild.py`. Nicht von Hand bearbeiten.*")
    o2.append("")
    o2.append("Jeder Fall, den das Screening im Volltext gelesen hat — mit Verdikt und dem Ausschluss, der getragen hat. "
              "Die Anzeigen liegen mit dem Wortlaut 1:1 als `<id>--anzeige--<erfasst>.md` im Fall-Ordner "
              "(`stellen/<id>/` oder, solange offen, `eingang/<id>/`).")
    o2.append("")
    zahl = Counter(r.get("entscheid") for r in voll)
    o2.append("| Verdikt | Anzahl |")
    o2.append("|---|---:|")
    for k, n in zahl.most_common():
        o2.append(f"| {k} | {n} |")
    o2.append(f"| **Total** | **{len(voll)}** |")
    o2.append("")
    o2.append("| Datum | Firma | Rolle | Ort | Verdikt | Tragender Grund | Anzeige |")
    o2.append("|---|---|---|---|---|---|---|")
    for r in sorted(voll, key=lambda x: (x.get("datum") or "", x.get("firma") or "")):
        datei = anzeige(r)
        g = zelle(r.get("grund"))
        if len(g) > 220:
            g = g[:217] + "…"
        o2.append(f"| {r.get('datum') or ''} | {zelle(r.get('firma'))} | {zelle(r.get('rolle'))} | {zelle(r.get('ort'))} | "
                  f"{r.get('entscheid')} | {g} | {f'`{datei}`' if datei != '—' else '—'} |")
    o2.append("")
    (ROOT / "views" / "MARKTBILD_VOLLTEXT.md").write_text("\n".join(o2) + "\n", encoding="utf-8")

    print(f"MARKTBILD_VORFILTER.md: {len(vor)} Einträge in {len(nach_kat)} Kategorien.")
    print(f"MARKTBILD_VOLLTEXT.md: {len(voll)} Einträge.")
    print("data/marktbild_vorfilter.csv geschrieben.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
