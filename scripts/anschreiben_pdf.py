#!/usr/bin/env python3
"""
anschreiben_pdf — Motivationsschreiben aus der Vorlage abfüllen und als PDF drucken.

    python3 scripts/anschreiben_pdf.py "stellen/<id>/Motivationsschreiben-Alex Müller-<Firma>-<Stelle>-<JJMMDD>.md"

Das ist der verbindliche, automatische Weg (kein Handdruck durch Alex nötig):
  1. Quell-MD lesen (liegt im Fall-Ordner stellen/<id>/ oder eingang/<id>/; Felder siehe Kopfkommentar
     der Vorlage).
  2. Vorlage vorlagen/Motivationsschreiben-Template.html kopieren, den #defaultMd-Block mit der MD füllen,
     localStorage-KEY brief-spezifisch setzen -> <Stamm>.html (abgefüllte Vorlage, neben der MD).
  3. Diese HTML mit echtem Chromium headless drucken (A4 laut @page der Vorlage, Hintergrundgrafiken an,
     ohne Kopf-/Fusszeile) -> <Stamm>.pdf. Das ist der Vorlagen-Druck (Producer Skia/PDF), kein Code-Nachbau.
  4. scripts/check_anschreiben.py und scripts/check_anschreiben_format.py auf das PDF laufen lassen;
     Exit-Code != 0, sobald eine der beiden Kontrollen durchfällt oder das PDF mehr als eine Seite hat.

Anlass: ein im Code nachgebautes Schreiben sah ungefähr gleich aus, wich aber bei Kopf, Abständen und Farbe
jedes Mal anders ab. Darum gibt es genau einen Weg zum PDF: die Vorlage im Browser drucken.

Nur Standardbibliothek. Browser-Suche: $CHROME_BIN, Playwright-Chromium (/opt/pw-browsers,
~/.cache/ms-playwright), macOS Chrome/Chromium/Edge/Brave, dann PATH.
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "vorlagen" / "Motivationsschreiben-Template.html"


def find_browser():
    env = os.environ.get("CHROME_BIN")
    if env and Path(env).exists():
        return env
    kandidaten = []
    for base in (os.environ.get("PLAYWRIGHT_BROWSERS_PATH"), "/opt/pw-browsers",
                 str(Path.home() / ".cache" / "ms-playwright"),
                 str(Path.home() / "Library" / "Caches" / "ms-playwright")):
        if not base:
            continue
        kandidaten += sorted(glob.glob(f"{base}/chromium-*/chrome-linux/chrome"), reverse=True)
        kandidaten += sorted(glob.glob(f"{base}/chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium"), reverse=True)
        kandidaten.append(f"{base}/chromium/chrome-linux/chrome")
    kandidaten += [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        str(Path.home() / "Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    ]
    for k in kandidaten:
        if k and Path(k).exists() and os.access(k, os.X_OK):
            return k
    for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        p = shutil.which(n)
        if p:
            return p
    return None


def fuellen(md_text: str, stamm: str) -> str:
    html = TEMPLATE.read_text(encoding="utf-8")
    md_safe = md_text.replace("</script", "<\\/script").strip("\n") + "\n"
    neu, n = re.subn(r'(<script type="text/markdown" id="defaultMd">)(.*?)(</script>)',
                     lambda m: m.group(1) + "\n" + md_safe + m.group(3), html, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("FEHLER: #defaultMd-Block in der Vorlage nicht gefunden.")
    key = "cover:" + re.sub(r"[^A-Za-z0-9]+", "-", stamm).strip("-").lower()
    neu, n = re.subn(r'var KEY = "[^"]*";', lambda m: f'var KEY = "{key}";', neu, count=1)
    if n != 1:
        raise SystemExit("FEHLER: localStorage-KEY in der Vorlage nicht gefunden.")
    return neu


def drucken(html_pfad: Path, pdf_pfad: Path, browser: str):
    # Frisches Profil je Druck: kein localStorage-Text aus einer früheren Handbearbeitung.
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as prof:
        if pdf_pfad.exists():
            pdf_pfad.unlink()
        cmd = [browser, "--headless=new", "--no-sandbox", "--disable-gpu",
               "--disable-dev-shm-usage", f"--user-data-dir={prof}",
               "--no-pdf-header-footer", "--virtual-time-budget=8000",
               f"--print-to-pdf={pdf_pfad}", html_pfad.resolve().as_uri()]
        # Manche Chromium-Builds (z. B. Playwright unter macOS) schreiben das PDF und beenden sich dann nicht.
        # Darum warten, bis das PDF vollständig ist (%%EOF, Grösse stabil), und den Browser dann beenden.
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        ende, groesse = time.monotonic() + 120, -1
        while proc.poll() is None and time.monotonic() < ende:
            time.sleep(0.5)
            if pdf_pfad.exists():
                n = pdf_pfad.stat().st_size
                if n == groesse and n > 0 and pdf_pfad.read_bytes()[-32:].rstrip().endswith(b"%%EOF"):
                    break
                groesse = n
        if proc.poll() is None:
            proc.kill()
        _, fehler = proc.communicate()
    if not pdf_pfad.exists() or pdf_pfad.stat().st_size < 2000:
        raise SystemExit("FEHLER: PDF-Druck fehlgeschlagen.\n" + (fehler or "")[-800:])


def seiten(pdf: Path) -> int:
    return len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes()))


def main():
    if len(sys.argv) != 2 or not sys.argv[1].lower().endswith(".md"):
        raise SystemExit(__doc__)
    md = Path(sys.argv[1]).expanduser().resolve()
    if not md.exists():
        raise SystemExit(f"FEHLER: {md} nicht gefunden.")
    if not TEMPLATE.exists():
        raise SystemExit(f"FEHLER: Vorlage fehlt ({TEMPLATE}).")
    if md.parent.parent not in (ROOT / "stellen", ROOT / "eingang"):
        print(f"WARNUNG: {md.name} liegt nicht in einem Fall-Ordner (stellen/<id>/ oder eingang/<id>/); "
              "die Grundlage lässt sich dann nur über die ID in der Grundlage-Zeile prüfen.")
    browser = find_browser()
    if not browser:
        raise SystemExit("FEHLER: kein Chromium/Chrome gefunden (CHROME_BIN setzen).")
    html, pdf = md.with_suffix(".html"), md.with_suffix(".pdf")
    html.write_text(fuellen(md.read_text(encoding="utf-8"), md.stem), encoding="utf-8")
    drucken(html, pdf, browser)
    n = seiten(pdf)
    print(f"HTML: {html}\nPDF:  {pdf}  ({n} Seite(n), Browser: {browser})", flush=True)
    if n != 1:
        print("WARNUNG: mehr als eine A4-Seite — Text kürzen (harte Formregel: höchstens eine Seite).", flush=True)
    rc = subprocess.call([sys.executable, str(ROOT / "scripts" / "check_anschreiben.py"), str(pdf)])
    rc2 = subprocess.call([sys.executable, str(ROOT / "scripts" / "check_anschreiben_format.py"), str(pdf)])
    sys.exit((rc or rc2) if n == 1 else (rc or rc2 or 2))


if __name__ == "__main__":
    main()
