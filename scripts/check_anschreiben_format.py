#!/usr/bin/env python3
"""
check_anschreiben_format — Schlusskontrolle: entspricht das Motivationsschreiben dem Format der Vorlage?

    python3 scripts/check_anschreiben_format.py "stellen/<id>/Motivationsschreiben-….pdf"
    python3 scripts/check_anschreiben_format.py --vorlage-pinnen      # nur auf ausdrückliche Anweisung von Alex

Wird von scripts/anschreiben_pdf.py als letzter Schritt automatisch aufgerufen. Referenz ist die Vorlage
vorlagen/Motivationsschreiben-Template.html selbst, nicht eine Sammlung früherer PDFs: was die Vorlage
festlegt (Seitenformat, Schrift, Farben), muss im PDF wieder auftauchen, und nichts anderes.

Geprüft wird:
  A  Vorlage unverändert: SHA-256 der Vorlage gegen den festgehaltenen Wert
     (vorlagen/Motivationsschreiben-Template.sha256), und die abgefüllte .html unterscheidet sich von der
     Vorlage nur im #defaultMd-Block und im localStorage-KEY.
  B  PDF: Druckengine Skia/Chromium, genau 1 Seite, A4, Schriften aus genau einer erlaubten Familie,
     Farben nur die der Vorlage (:root --text und --akzent) und Weiss.
  C  Quell-MD neben dem PDF vorhanden; Ort/Datum in Schweizer Langform und Gruss «Freundliche Grüsse»
     (nur Warnung). Ein Kopf-Vergleich der MD entfällt: Absenderblock steht fest in der Vorlage und ist über
     die Prüfsumme gesichert.

Zur Schrift: Die Vorlage nennt den Stapel Arial, «Liberation Sans», sans-serif. Arial liegt auf
macOS und Windows bei, Liberation Sans ist frei verfügbar (SIL OFL) und metrisch identisch mit Arial; unter
Linux löst Fontconfig Arial ohnehin auf Liberation Sans auf. So ergibt der Druck auf jeder Plattform denselben
Umbruch, ohne dass eine Webschrift eingebettet oder geladen werden muss. Erlaubt ist darum je PDF genau eine
dieser Familien (Regular, Bold, Italic). Mischen zwei Familien oder taucht eine fremde Schrift auf, hat der
Browser Glyphen ersetzt (fehlende Schrift, Sonderzeichen) — dann stimmt der Umbruch nicht mehr: FAIL.

Die Vorlage wird nie automatisch «repariert» oder neu festgehalten: Abweichung = FAIL, Alex entscheidet.
Nur Standardbibliothek. Exit-Code != 0 bei FAIL.
"""
import hashlib
import re
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VORLAGE = ROOT / "vorlagen" / "Motivationsschreiben-Template.html"
PIN = VORLAGE.with_suffix(".sha256")

# PostScript-Namen je erlaubter Familie (so, wie Chromium sie als /BaseFont einbettet).
SCHRIFT_FAMILIEN = {
    "Arial": {"ArialMT", "Arial-BoldMT", "Arial-ItalicMT", "Arial-BoldItalicMT"},
    "Liberation Sans": {"LiberationSans", "LiberationSans-Bold", "LiberationSans-Italic",
                        "LiberationSans-BoldItalic"},
}
WEISS = (1.0, 1.0, 1.0)
MONATE = "Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalisiert(html: str) -> str:
    html = re.sub(r'(<script type="text/markdown" id="defaultMd">).*?(</script>)', r"\1\2", html, count=1, flags=re.S)
    return re.sub(r'var KEY = "[^"]*";', 'var KEY = "";', html, count=1)


def vorlage_farben(html: str) -> dict:
    """Farben aus dem :root-Block der Vorlage (--name: #rrggbb) -> {name: (r, g, b)} wie im PDF gerundet."""
    root = re.search(r":root\s*\{(.*?)\}", html, re.S)
    out = {}
    for name, hexwert in re.findall(r"--([\w-]+)\s*:\s*#([0-9a-fA-F]{6})\s*;", root.group(1) if root else ""):
        out[name] = tuple(round(int(hexwert[i:i + 2], 16) / 255, 3) for i in (0, 2, 4))
    return out


def pdf_daten(pdf: Path):
    d = pdf.read_bytes()
    prod = re.search(rb"/Producer\s*\(([^)]*)\)", d)
    seiten = len(re.findall(rb"/Type\s*/Page[^s]", d))
    mb = re.search(rb"/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]", d)
    schriften = {re.sub(r"^[A-Z]{6}\+", "", f.decode()) for f in re.findall(rb"/BaseFont\s*/([A-Za-z0-9+\-]+)", d)}
    farben = set()
    for m in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", d, re.S):
        try:
            t = zlib.decompress(m.group(1))
        except Exception:
            continue
        for c in re.findall(rb"([\d.]+) ([\d.]+) ([\d.]+) (?:rg|RG)", t):
            farben.add(tuple(round(float(x), 3) for x in c))
    return {"producer": prod.group(1).decode("latin-1") if prod else "", "seiten": seiten,
            "mediabox": tuple(float(x) for x in mb.groups()) if mb else None,
            "schriften": schriften, "farben": farben}


def schrift_familie(schriften: set):
    """Name der einen erlaubten Familie, aus der alle Schriften stammen, sonst None."""
    passend = [f for f, namen in SCHRIFT_FAMILIEN.items() if schriften and schriften <= namen]
    return passend[0] if len(passend) == 1 else None


def pruefen(pdf: Path):
    """-> Liste (status, text); status in PASS/FAIL/WARN."""
    out = []

    def add(ok, text, warn=False):
        out.append(("PASS" if ok else ("WARN" if warn else "FAIL"), text))

    # A — Vorlage
    soll_farben = {}
    if not VORLAGE.exists():
        add(False, "Vorlage fehlt")
    else:
        vorlage_html = VORLAGE.read_text(encoding="utf-8")
        soll_farben = vorlage_farben(vorlage_html)
        if not PIN.exists():
            add(False, f"Vorlage nicht festgehalten ({PIN.name} fehlt); nur auf Anweisung von Alex: --vorlage-pinnen")
        else:
            soll = (PIN.read_text().split() or [""])[0]
            ist = sha(VORLAGE)
            add(soll == ist, "Vorlage unverändert (Prüfsumme wie festgehalten)" if soll == ist else
                "VORLAGE VERÄNDERT (Prüfsumme weicht vom festgehaltenen Stand ab) — nicht drucken, Alex informieren")
        html = pdf.with_suffix(".html")
        if html.exists():
            gleich = normalisiert(html.read_text(encoding="utf-8")) == normalisiert(vorlage_html)
            add(gleich, "abgefüllte .html = Vorlage, nur Text und KEY unterscheiden sich" if gleich else
                "abgefüllte .html weicht ausserhalb von Text/KEY von der Vorlage ab (Schrift, Stil oder Standardinhalt verändert)")
        else:
            add(False, "abgefüllte .html fehlt neben dem PDF")

    # B — PDF
    p = pdf_daten(pdf)
    add(any(e in p["producer"].lower() for e in ("skia", "chromium", "chrome")), f"Druckengine: {p['producer'] or '—'}")
    add(p["seiten"] == 1, f"Seiten: {p['seiten']} (Soll 1)")
    mb = p["mediabox"]
    add(bool(mb) and 594 <= mb[2] <= 596.5 and 841 <= mb[3] <= 843.5,
        f"Seitenformat A4 ({mb[2]:.0f}×{mb[3]:.0f} pt)" if mb else "Seitenformat nicht lesbar")
    familie = schrift_familie(p["schriften"])
    add(familie is not None, "Schriften: " + (", ".join(sorted(p["schriften"])) or "keine") +
        (f" (Familie {familie})" if familie else f" (Soll: genau eine Familie aus {', '.join(SCHRIFT_FAMILIEN)})"))
    erlaubt = set(soll_farben.values()) | {WEISS}
    text_farbe = soll_farben.get("text")
    fremd = p["farben"] - erlaubt
    namen = ", ".join(f"--{n} {f}" for n, f in sorted(soll_farben.items()))
    add(text_farbe in p["farben"] and not fremd,
        f"Farben: nur die der Vorlage ({namen}) und Weiss" if text_farbe in p["farben"] and not fremd else
        f"Farben weichen ab (Textfarbe vorhanden: {text_farbe in p['farben']}, fremd: {sorted(fremd)})")

    # C — Quell-MD
    md = pdf.with_suffix(".md")
    if md.exists():
        text = md.read_text(encoding="utf-8")
        m = re.search(r"^\*\*Ort/Datum:\*\*\s*(.+)$", text, re.M)
        add(bool(m) and re.fullmatch(rf"Zürich, \d{{1,2}}\. ({MONATE}) 20\d\d", m.group(1).strip()) is not None,
            f"Ort/Datum: {m.group(1).strip()}" if m else "Ort/Datum fehlt", warn=True)
        g = re.search(r"^\*\*Gruss:\*\*\s*(.+)$", text, re.M)
        add(bool(g) and g.group(1).strip() == "Freundliche Grüsse",
            f"Gruss: {g.group(1).strip()}" if g else "Gruss fehlt", warn=True)
    else:
        add(False, "Quell-.md fehlt neben dem PDF")
    return out


def main():
    if sys.argv[1:] == ["--vorlage-pinnen"]:
        PIN.write_text(f"{sha(VORLAGE)}  {VORLAGE.name}\n")
        print(f"Vorlage festgehalten: {PIN}")
        return 0
    if len(sys.argv) != 2 or not sys.argv[1].lower().endswith(".pdf"):
        print(__doc__)
        return 2
    pdf = Path(sys.argv[1]).expanduser().resolve()
    if not pdf.exists():
        print(f"FEHLER: {pdf} nicht gefunden.")
        return 2
    res = pruefen(pdf)
    for s, t in res:
        print(f"  {s:4} | {t}")
    fails = [t for s, t in res if s == "FAIL"]
    if fails:
        print(f"\n✗ FORMAT-CHECK FAIL ({len(fails)}): entspricht nicht dem Format der Vorlage — nicht versenden.")
        return 1
    print("\n✓ FORMAT-CHECK PASS: entspricht dem Format der Vorlage.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
