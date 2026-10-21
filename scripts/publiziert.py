#!/usr/bin/env python3
"""Veroeffentlichungsdatum einer Anzeige lesen und das Alter beim Fund rechnen.

Zweck: Die Fundgeschwindigkeit ist die zentrale Groesse, wenn die Suche schneller werden soll; sie gehoert
in die Retro und in jeden Priorisierungsentscheid. Stellen, die ueber eine Woche alt sind, sind meist
schwerer zu erreichen.

Zwei Quellen:
  - Sichtungs-Log: Feld `publiziert` (ISO-Datum), gesetzt von `screening_log.py add` (8. Feld).
  - Anzeigen-Datei: Kopfzeile «**Publiziert:** …» (Pflicht in jeder abgelegten Anzeige, Freitext mit Quelle).

`parse(text, bezug)` versteht ISO-Daten, «02 April 2025», «2. April 2025», «02.04.2025», Zeitstempel wie
«Fri Apr 04 02:01:00 UTC 2025», «datePosted: 2025-04-02», «eine Woche vor dem 2025-04-19» und relative
Angaben («vor 4 Stunden», «Gestern», «Heute», «3 days ago», «1 week ago», «2 months ago»). Relative Angaben
werden gegen das Abrufdatum im Text («Abruf 2025-04-01») oder gegen `bezug` gerechnet. Fristen
(«Bewerbungsfrist 2025-05-01») zaehlen nicht. «unbekannt» und Unlesbares -> None; ein Datum nach dem
Abruf ist unplausibel -> None. Es wird nie geschaetzt: «ca.» und «rund» werden wie die genannte Angabe
gelesen, nichts dazuerfunden.

    python3 scripts/publiziert.py "Netzwerk «1 week ago», Abruf 2025-04-01"   # Test
"""
import re
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import heute as uhr  # noqa: E402

ALT_SCHWELLE_TAGE = 7  # ueber eine Woche alt = meist schwerer zu erreichen

MONATE = {"januar": 1, "january": 1, "jan": 1, "februar": 2, "february": 2, "feb": 2,
          "märz": 3, "maerz": 3, "march": 3, "mar": 3, "april": 4, "apr": 4, "mai": 5, "may": 5,
          "juni": 6, "june": 6, "jun": 6, "juli": 7, "july": 7, "jul": 7, "august": 8, "aug": 8,
          "september": 9, "sep": 9, "sept": 9, "oktober": 10, "october": 10, "okt": 10, "oct": 10,
          "november": 11, "nov": 11, "dezember": 12, "december": 12, "dez": 12, "dec": 12}
EINHEIT_TAGE = {"minute": 0, "minuten": 0, "minutes": 0, "stunde": 0, "stunden": 0, "hour": 0, "hours": 0,
                "tag": 1, "tagen": 1, "tage": 1, "day": 1, "days": 1, "woche": 7, "wochen": 7,
                "week": 7, "weeks": 7, "monat": 30, "monaten": 30, "monate": 30, "month": 30, "months": 30}


def _abruf(text):
    m = re.search(r"(?:abruf|abgerufen|abrufdatum)\D{0,12}(\d{4}-\d{2}-\d{2})", text, re.I)
    return date.fromisoformat(m.group(1)) if m else None


def parse(text, bezug=None):
    """Veroeffentlichungsdatum aus Freitext oder None. Ein Datum nach dem Abruf ist unplausibel -> None."""
    d = _parse(text, bezug)
    grenze = _abruf(str(text or "")) or bezug
    if d and grenze and d > grenze:
        return None
    return d


def _parse(text, bezug=None):
    if not text:
        return None
    t = str(text).strip()
    if re.match(r"^\s*unbekannt", t, re.I):
        return None
    abruf = _abruf(t)
    # Abrufdatum aus dem Text entfernen, damit es nicht als Publikationsdatum gelesen wird
    ohne = re.sub(r"(?:abruf|abgerufen|abrufdatum)\D{0,12}\d{4}-\d{2}-\d{2}", " ", t, flags=re.I)
    # Fristen und Gueltigkeitsdaten sind kein Publikationsdatum: ab dort abschneiden
    ohne = re.split(r"(?i)bewerbungsfrist|\bfrist\b|validthrough|g[uü]ltig bis|einsendeschluss|deadline|stellenantritt|eintritt", ohne)[0]
    # «eine Woche vor dem 2025-04-19»: relative Angabe zu einem genannten Datum
    m = re.search(r"(\d+|eine|einer|einem|ein)\s+(tag(?:en|e)?|wochen?|monat(?:en|e)?)\s+vor\s+dem\s+(\d{4}-\d{2}-\d{2})", ohne, re.I)
    if m:
        n = 1 if not m.group(1).isdigit() else int(m.group(1))
        return date.fromisoformat(m.group(3)) - timedelta(days=n * EINHEIT_TAGE[m.group(2).lower()])
    # strukturierte Daten zuerst (datePosted)
    m = re.search(r"datePosted\D{0,6}(\d{4}-\d{2}-\d{2})", ohne)
    if m:
        return date.fromisoformat(m.group(1))
    m = re.search(r"(\d{1,2})\.?\s+([A-Za-zäÄ]+)\.?\s+(\d{4})", ohne)
    if m and m.group(2).lower() in MONATE:
        return date(int(m.group(3)), MONATE[m.group(2).lower()], int(m.group(1)))
    m = re.search(r"\b(?:[A-Za-z]{3}\s+)?([A-Za-z]{3})\s+(\d{1,2})\s+[\d:]+\s+\w+\s+(\d{4})", ohne)  # «Fri Apr 04 02:01:00 UTC 2025»
    if m and m.group(1).lower() in MONATE:
        return date(int(m.group(3)), MONATE[m.group(1).lower()], int(m.group(2)))
    m = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", ohne)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.search(r"\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b", ohne)
    if m:
        return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    basis = abruf or bezug
    if basis is None:
        return None
    low = ohne.lower()
    if re.search(r"\bgestern\b|\byesterday\b", low):
        return basis - timedelta(days=1)
    if re.search(r"\bheute\b|\btoday\b|just now|gerade eben", low):
        return basis
    m = re.search(r"(?:vor\s+)?(\d+|einer|einem|eine|ein|an|a)\s+(minuten?|minutes?|stunden?|hours?|tag(?:en|e)?|days?|wochen?|weeks?|monat(?:en|e)?|months?)\b", low)
    if m:
        n = m.group(1)
        n = 1 if not n.isdigit() else int(n)
        return basis - timedelta(days=n * EINHEIT_TAGE[m.group(2)])
    return None


def aus_anzeige(pfad):
    """(datum|None, rohtext|None) aus der Kopfzeile «**Publiziert:**» einer Anzeigen-Datei."""
    try:
        txt = Path(pfad).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None, None
    m = re.search(r"^\*\*Publiziert:?\*\*:?\s*(.*)$", txt, re.M)
    if not m:
        return None, None
    roh = m.group(1).strip()
    erf = re.search(r"--anzeige--(\d{4}-\d{2}-\d{2})", str(pfad))
    bezug = date.fromisoformat(erf.group(1)) if erf else None
    return parse(roh, bezug), roh


def anzeige_datei(root, fid):
    """Pfad der Anzeigen-Datei eines Falls (stellen/ oder eingang/) oder None."""
    for basis in ("stellen", "eingang"):
        d = Path(root) / basis / fid
        if d.is_dir():
            treffer = sorted(d.glob("*--anzeige--*.md"))
            if treffer:
                return treffer[0]
    return None


def alter_text(pub, bezug):
    """«5 Tage» / «über eine Woche alt (12 Tage)» / «unbekannt»."""
    if pub is None:
        return "unbekannt"
    n = (bezug - pub).days
    if n > ALT_SCHWELLE_TAGE:
        return f"über eine Woche alt ({n} Tage)"
    return "heute publiziert" if n <= 0 else f"{n} Tag{'e' if n != 1 else ''}"


if __name__ == "__main__":
    for a in sys.argv[1:]:
        print(a, "->", parse(a, uhr.heute()))
