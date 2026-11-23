"""Vor-Versand-Gate: anschreiben_pdf.py, check_anschreiben.py, check_anschreiben_format.py."""
import hashlib
import importlib.util
import re
from pathlib import Path

import pytest

from conftest import REPO, run


def mini_pdf(producer: bytes) -> bytes:
    """Kleinstes gültiges PDF: eine A4-Seite ohne Inhalt, /Producer im Info-Dict."""
    objekte = [b"<< /Type /Catalog /Pages 2 0 R >>",
               b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
               b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] >>",
               b"<< /Producer (" + producer + b") >>"]
    out, offs = b"%PDF-1.4\n", []
    for i, o in enumerate(objekte, 1):
        offs.append(len(out))
        out += b"%d 0 obj\n" % i + o + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objekte) + 1)
    out += b"".join(b"%010d 00000 n \n" % o for o in offs)
    out += b"trailer\n<< /Size %d /Root 1 0 R /Info 4 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objekte) + 1, xref)
    return out


def entwurf(demo: Path) -> Path:
    return sorted((demo / "stellen").glob("*/Motivationsschreiben-*.md"))[0]


def pdf_neben(md: Path, producer: bytes) -> Path:
    pdf = md.with_suffix(".pdf")
    pdf.write_bytes(mini_pdf(producer))
    return pdf


def test_code_nachbau_wird_abgewiesen(demo):
    pdf = pdf_neben(entwurf(demo), b"ReportLab PDF Library - www.reportlab.com")
    r = run(demo, "check_anschreiben.py", pdf)
    assert r.returncode == 1, r.stdout
    assert "NICHT aus der Vorlage (Producer: ReportLab" in r.stdout


def test_vorlagen_druck_wird_akzeptiert(demo):
    pdf = pdf_neben(entwurf(demo), b"Skia/PDF m141")
    r = run(demo, "check_anschreiben.py", pdf)
    assert r.returncode == 0, r.stdout
    assert "aus der Vorlage gedruckt (Producer: Skia/PDF m141)" in r.stdout
    assert "PASS   | Grundlage:" in r.stdout


def test_ohne_argument_findet_pdfs_in_fall_ordnern(demo):
    pdf_neben(entwurf(demo), b"ReportLab")
    r = run(demo, "check_anschreiben.py")
    assert r.returncode == 1 and "NICHT aus der Vorlage" in r.stdout


def test_quell_md_ohne_grundlage_faellt_durch(demo):
    md = entwurf(demo)
    md.write_text("\n".join(z for z in md.read_text(encoding="utf-8").splitlines()
                            if not z.startswith("**Grundlage:**")) + "\n", encoding="utf-8")
    pdf = pdf_neben(md, b"Skia/PDF m141")
    r = run(demo, "check_anschreiben.py", pdf)
    assert r.returncode == 1, r.stdout
    assert "Grundlage-Zeile fehlt" in r.stdout
    assert run(demo, "check_anschreiben.py", md).returncode == 1


def test_grundlage_mit_falschem_datum_oder_ohne_grund(demo):
    md = entwurf(demo)
    fid = md.parent.name
    md.write_text(f"# Test\n\n**Grundlage:** {fid}--recherche--1999-01-01.md\n", encoding="utf-8")
    assert "anderes Datum" in run(demo, "check_anschreiben.py", md).stdout
    md.write_text("# Test\n\n**Grundlage:** ohne Recherche-Dokumente — Initiativschreiben ohne Anzeige\n",
                  encoding="utf-8")
    assert run(demo, "check_anschreiben.py", md).returncode == 0


def test_pin_passt_zur_vorlage_im_repo():
    vorlage = REPO / "vorlagen" / "Motivationsschreiben-Template.html"
    soll = (REPO / "vorlagen" / "Motivationsschreiben-Template.sha256").read_text().split()[0]
    assert hashlib.sha256(vorlage.read_bytes()).hexdigest() == soll


def test_veraenderte_vorlage_faellt_durch_hash_check(demo):
    md = entwurf(demo)
    pdf = pdf_neben(md, b"Skia/PDF m141")
    r = run(demo, "check_anschreiben_format.py", pdf)
    assert "PASS | Vorlage unverändert" in r.stdout
    vorlage = demo / "vorlagen" / "Motivationsschreiben-Template.html"
    daten = bytearray(vorlage.read_bytes())
    i = daten.index(b"#1a1a1a")
    daten[i + 1] = ord("2")  # ein einziges Byte: #2a1a1a
    vorlage.write_bytes(bytes(daten))
    r = run(demo, "check_anschreiben_format.py", pdf)
    assert r.returncode == 1
    assert "FAIL | VORLAGE VERÄNDERT" in r.stdout


def test_abgefuellte_html_nur_text_und_key_anders(demo):
    md = entwurf(demo)
    pdf = pdf_neben(md, b"Skia/PDF m141")
    vorlage = (demo / "vorlagen" / "Motivationsschreiben-Template.html").read_text(encoding="utf-8")
    spec = importlib.util.spec_from_file_location("anschreiben_pdf", demo / "scripts" / "anschreiben_pdf.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    html = modul.fuellen(md.read_text(encoding="utf-8"), md.stem)
    assert html != vorlage and 'var KEY = "cover:motivationsschreiben-alex-m' in html
    md.with_suffix(".html").write_text(html, encoding="utf-8")
    assert "PASS | abgefüllte .html = Vorlage" in run(demo, "check_anschreiben_format.py", pdf).stdout
    md.with_suffix(".html").write_text(html.replace("font-size: 10.5pt", "font-size: 9pt"), encoding="utf-8")
    assert "FAIL | abgefüllte .html weicht" in run(demo, "check_anschreiben_format.py", pdf).stdout


# --- echter Druck (nur wenn ein Chromium/Chrome da ist) ------------------------------------------------

def _browser():
    spec = importlib.util.spec_from_file_location("anschreiben_pdf_b", REPO / "scripts" / "anschreiben_pdf.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul.find_browser()


@pytest.fixture
def browser():
    b = _browser()
    if not b:
        pytest.skip("kein Chromium/Chrome gefunden (CHROME_BIN setzen)")
    return b


def test_echter_druck_besteht_alle_checks(demo, browser):
    md = entwurf(demo)
    r = run(demo, "anschreiben_pdf.py", md)
    assert r.returncode == 0, r.stdout + r.stderr
    assert md.with_suffix(".pdf").exists() and md.with_suffix(".html").exists()
    assert "aus der Vorlage gedruckt (Producer: Skia/PDF" in r.stdout
    assert "FORMAT-CHECK PASS" in r.stdout
    assert "FAIL" not in r.stdout


def test_echter_druck_ueberlauf_auf_zweite_seite_faellt_durch(demo, browser):
    md = entwurf(demo)
    md.write_text(md.read_text(encoding="utf-8") + ("\nLanger Absatz mit Fülltext für den Test. " * 12 + "\n") * 20,
                  encoding="utf-8")
    r = run(demo, "anschreiben_pdf.py", md)
    assert r.returncode != 0
    assert re.search(r"FAIL \| Seiten: [2-9] \(Soll 1\)", r.stdout), r.stdout
