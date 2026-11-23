#!/usr/bin/env python3
"""
check_anschreiben — Vor-Versand-Gate für Motivationsschreiben-PDFs.

    python3 scripts/check_anschreiben.py [PFAD ...]

Ohne Argument: prüft alle stellen/<id>/Motivationsschreiben-*.pdf und eingang/<id>/Motivationsschreiben-*.pdf.
Mit Argument(en): prüft die angegebenen PDF-Dateien; ein .md-Argument prüft nur die Grundlage-Zeile.

Erste Frage: Kommt das PDF aus dem *Druck der Vorlage* (Browser-/OS-Druck) oder wurde es *im Code
nachgebaut*? Ein Code-Nachbau (ReportLab u. ä.) sieht «ungefähr gleich» aus, driftet aber jedes Mal anders
(Kopf, Abstände, Farbe) und darf nie versendet werden. Verbindlicher letzter Schritt vor jedem Versand bzw.
bevor eine Bewerbung in data/pipeline.json auf 'abgeschickt' gesetzt wird. Erzeugt wird das PDF mit
scripts/anschreiben_pdf.py, das diese Prüfung am Ende selbst aufruft.

Marker ist das PDF-Metadatenfeld /Producer: ein Browser-/OS-Druck trägt Skia/Chromium/Quartz, ein
Code-Nachbau trägt ReportLab o. ä. Nur Standardbibliothek. Exit-Code != 0, sobald ein PDF durchfällt.

Zweite Frage: Nennt die Quell-MD (gleicher Stamm neben dem PDF) ihre Grundlage, also die datierte
Recherche im Fall-Ordner (<id>--recherche--JJJJ-MM-TT.md), oder einen Grund, warum ohne? Die Zeile belegt
die Grundlage, nicht den inhaltlichen Einbezug; der bleibt Checkliste. Andere Skripte können
grundlage_befund() als Wächter nutzen. Portalantworten (Portalantworten-*.md) fallen unter dieselbe Regel.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STELLEN = ROOT / "stellen"
EINGANG = ROOT / "eingang"

# Producer, die einen echten Druck belegen (Browser/OS) — erlaubt.
PRINT_ENGINES = ("skia", "chromium", "chrome", "quartz", "macos", "preview",
                 "webkit", "acrobat", "distiller", "pdfium")


def producer(path: Path):
    """/Producer aus dem Info-Dict (oder XMP) per Byte-Scan — ohne Fremdbibliothek."""
    try:
        data = path.read_bytes()
    except Exception:
        return None
    for pat in (rb"/Producer\s*\(([^)]*)\)", rb"<pdf:Producer>([^<]*)</pdf:Producer>"):
        m = re.search(pat, data)
        if m:
            return m.group(1).decode("latin-1", "replace").replace("\\(", "(").replace("\\)", ")").rstrip("\\")
    return None


def is_from_template(prod: str) -> bool:
    low = (prod or "").lower()
    return any(e in low for e in PRINT_ENGINES)


def quell_md(pdf: Path) -> Path:
    """Quell-MD zum PDF: gleicher Stamm im selben Fall-Ordner."""
    return pdf.with_suffix(".md")


def _fall_ordner(md: Path, fid: str):
    """Fall-Ordner der Stelle: der Ordner der MD selbst, sonst stellen/<id>/ bzw. eingang/<id>/."""
    if md.parent.parent in (STELLEN, EINGANG):
        return md.parent
    for basis in (STELLEN, EINGANG):
        if (basis / fid).is_dir():
            return basis / fid
    return None


def grundlage_befund(md: Path):
    """Grundlage-Zeile einer Quell-MD prüfen.

    None, wenn die Regel nicht greift (weder Motivationsschreiben- noch Portalantworten-Datei),
    sonst (ok, text). Gültig ist genau eine Zeile
    '**Grundlage:** <id>--anzeige, <id>--recherche, <id>--personen, persona/PROFILE.md' (Datum optional,
    `<id>--recherche--JJJJ-MM-TT.md`; wenn genannt, muss es stimmen)
    oder '**Grundlage:** ohne Recherche-Dokumente — <Grund>'.
    Im Fall-Ordner muss genau eine datierte Recherche liegen, und die Zeile muss die ID dieses Ordners nennen.
    Liegt eine Personen-Recherche im Ordner, muss die Zeile auch sie nennen (sie gehoert zur Grundlage).
    Position: beim Motivationsschreiben frei, weil die Vorlage die Grundlage-Zeile nie druckt;
    bei Portalantworten (kein Druck) im Kopf vor dem ersten --- bzw. ##.
    """
    if not md.name.startswith(("Motivationsschreiben-", "Portalantworten-")):
        return None
    if not md.exists():
        return False, f"Quell-MD fehlt ({md.name})"
    zeilen = [z.strip() for z in md.read_text(encoding="utf-8").splitlines()]
    treffer = [i for i, z in enumerate(zeilen) if z.startswith("**Grundlage:**")]
    if not treffer:
        return False, "Grundlage-Zeile fehlt"
    if len(treffer) > 1:
        return False, "Grundlage-Zeile mehrfach"
    if md.name.startswith("Portalantworten-"):
        kopf_ende = next((i for i, z in enumerate(zeilen) if z == "---" or z.startswith("## ")), len(zeilen))
        if treffer[0] > kopf_ende:
            return False, "Grundlage-Zeile nicht im Kopf (vor dem ersten --- bzw. ##)"
    rest = zeilen[treffer[0]][len("**Grundlage:**"):].strip()
    ohne = re.match(r"ohne Recherche-Dokumente\s*[—–-]\s*(\S.*)$", rest)
    if ohne:
        return True, f"ohne Recherche-Dokumente — {ohne.group(1)}"
    nennungen = re.findall(r"(?<![\w-])([a-z0-9][a-z0-9-]*?)--recherche(?:--(\d{4}-\d{2}-\d{2}))?", rest)
    ids = {fid for fid, _ in nennungen}
    if len(ids) != 1:
        return False, f"Grundlage nennt nicht genau eine Recherche (<id>--recherche), gefunden {len(ids)}"
    fid = ids.pop()
    ordner = _fall_ordner(md, fid)
    if ordner is None:
        return False, f"kein Fall-Ordner zu {fid} unter stellen/ oder eingang/"
    if ordner.name != fid:
        return False, f"Grundlage nennt die Recherche einer anderen Stelle ({fid}, Ordner {ordner.name})"
    rech = sorted(ordner.glob(f"{fid}--recherche--????-??-??.md"))
    if len(rech) != 1:
        return False, f"im Fall-Ordner erwartet: genau eine datierte Recherche (gefunden {len(rech)})"
    daten = {d for _, d in nennungen if d}
    if daten and daten != {rech[0].name[len(fid) + len("--recherche--"):-3]}:
        return False, f"Grundlage-Zeile nennt ein anderes Datum als die vorhandene {rech[0].name}"
    pers = sorted(ordner.glob(f"{fid}--personen--????-??-??.md"))
    if pers and not re.search(rf"(?<![\w-]){re.escape(fid)}--personen", rest):
        return False, f"Grundlage nennt die vorhandene Personen-Recherche nicht ({pers[0].name})"
    try:
        ort = ordner.relative_to(ROOT)
    except ValueError:
        ort = ordner
    return True, f"{rech[0].name} ({ort}/)"


def main(argv):
    if argv:
        targets = [Path(a).resolve() for a in argv]  # relativer Pfad: sonst «Quell-MD fehlt»
    else:
        targets = sorted(f for r in (STELLEN, EINGANG) if r.exists() for f in r.glob("*/Motivationsschreiben-*.pdf"))
        if not targets:
            print("Keine zu prüfenden Motivationsschreiben-PDFs gefunden (stellen/ und eingang/).")
            return 0

    fails = 0
    grundlage_fails = 0
    grundlage_geprueft = 0
    for p in targets:
        if not p.exists():
            print(f"FEHLT  | {p}")
            fails += 1
            continue
        if p.suffix.lower() == ".md":
            # Kein PDF (z. B. Portalantworten): nur die Grundlage prüfen.
            befund = grundlage_befund(p)
            if befund is None:
                print(f"—      | Grundlage: Regel greift nicht (kein Motivationsschreiben/keine Portalantworten) | {p.name}")
                continue
            grundlage_geprueft += 1
            ok, text = befund
            print(f"{'PASS' if ok else 'FAIL'}   | Grundlage: {text} | {p.name}")
            grundlage_fails += not ok
            continue
        prod = producer(p)
        if is_from_template(prod):
            print(f"PASS   | aus der Vorlage gedruckt (Producer: {prod}) | {p.name}")
        else:
            fails += 1
            print(f"FAIL   | NICHT aus der Vorlage (Producer: {prod or 'unlesbar'}) | {p.name}")
        befund = grundlage_befund(quell_md(p))
        if befund is not None:
            grundlage_geprueft += 1
            ok, text = befund
            if ok:
                print(f"PASS   | Grundlage: {text} | {p.name}")
            else:
                grundlage_fails += 1
                print(f"FAIL   | Grundlage: {text} | {p.name}")

    print()
    if fails:
        print(f"✗ {fails} PDF(s) durchgefallen. Neu erzeugen: python3 scripts/anschreiben_pdf.py <Quell-MD> "
              f"(oder vorlagen/Motivationsschreiben-Template.html im Browser öffnen → «Drucken», Ränder Keine, "
              f"Hintergrundgrafiken An). NIE im Code (ReportLab) bauen.")
    if grundlage_fails:
        print(f"✗ {grundlage_fails} Datei(en) ohne gültige Grundlage. <id>--recherche--JJJJ-MM-TT.md im Fall-Ordner "
              f"lesen und einbeziehen, dann die Zeile '**Grundlage:** <id>--anzeige, <id>--recherche, "
              f"persona/PROFILE.md' setzen (oder 'ohne Recherche-Dokumente — <Grund>').")
    if not fails and not grundlage_fails:
        zusatz = f"; Grundlage bei {grundlage_geprueft} Datei(en) in Ordnung" if grundlage_geprueft else ""
        n_pdf = sum(1 for t in targets if t.suffix.lower() == ".pdf")
        if n_pdf:
            print(f"✓ Alle {n_pdf} PDF(s) stammen aus dem Druck der Vorlage{zusatz}.")
        else:
            print(f"✓ Keine Befunde{zusatz}.")
    return 1 if (fails or grundlage_fails) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
