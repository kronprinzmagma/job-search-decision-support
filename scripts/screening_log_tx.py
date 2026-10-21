#!/usr/bin/env python3
"""
screening_log_tx — Sperrmechanismus fuer data/screening_log.json
(data/retro_massnahmen.json, Massnahme 2025-03-16-log-sperre).

Anlass: Zwei Sessions liefen gleichzeitig am selben Sweep (die erste ohne `ende`, die zweite
parallel gestartet) -> Lesefehler und doppelt geloggte Abfragen. Ursache: screening_log.py liest die
Datei beim Start komplett ein und schreibt am Ende komplett zurueck, ohne Koordination zwischen
parallelen Aufrufen (feedback/2025-03-11_datenverlust-parallele-sessions.md, gleiches Muster).

Gleiches Muster wie scripts/pipeline_tx.py fuer data/pipeline.json:
  1. Sperrdatei data/.screening_log.lock (exklusiv angelegt). Liegt sie schon da und ist
     juenger als SPERRE_MIN Minuten, bricht der Aufruf ab - nicht warten, nicht ueberschreiben.
     Eine aeltere Sperre gilt als verwaist, wird gemeldet und uebernommen.
  2. Geschrieben wird atomar (temporaere Datei, dann umbenennen).

Verwendung in Python (screening_log.py):
    from screening_log_tx import transaktion
    with transaktion("wer schreibt, wozu") as d:
        ...  # d aendern
        # Ruecksprung schreibt d automatisch zurueck
Kommandozeile:
    python3 scripts/screening_log_tx.py status      # zeigt, ob gerade jemand schreibt
"""
import contextlib
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from heute import jetzt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "screening_log.json"
LOCK = ROOT / "data" / ".screening_log.lock"
SPERRE_MIN = 15


class Konflikt(RuntimeError):
    pass


def _stempel(wer, zusatz=""):
    return f"{jetzt().isoformat(timespec='seconds')} | pid {os.getpid()} | {wer}{zusatz}\n"


def _sperre_info():
    try:
        return LOCK.read_text(encoding="utf-8").strip(), (time.time() - LOCK.stat().st_mtime) / 60
    except FileNotFoundError:
        return None, None


def _sperren(wer):
    for _ in range(2):
        try:
            fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.write(fd, _stempel(wer).encode())
            os.close(fd)
            return
        except FileExistsError:
            info, alter = _sperre_info()
            if alter is None:
                continue
            if alter < SPERRE_MIN:
                raise Konflikt(f"screening_log.json ist gesperrt ({alter:.0f} Min.): {info}. "
                               f"Eine andere Session schreibt gerade - abbrechen, nicht ueberschreiben.")
            print(f"WARNUNG: verwaiste Sperre uebernommen ({alter:.0f} Min. alt): {info}", file=sys.stderr)
            LOCK.write_text(_stempel(wer, " (uebernommen)"), encoding="utf-8")
            return
    raise Konflikt("Sperre konnte nicht gesetzt werden.")


def _freigeben():
    try:
        LOCK.unlink()
    except FileNotFoundError:
        pass
    except OSError:
        try:
            alt = time.time() - (SPERRE_MIN + 1) * 60
            os.utime(LOCK, (alt, alt))
        except OSError:
            pass


@contextlib.contextmanager
def transaktion(wer="unbekannt"):
    _sperren(wer)
    try:
        data = (json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists()
                else {"gesichtet": [], "laeufe": [], "sweeps": []})
        yield data
        tmp = DATA.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        os.replace(tmp, DATA)
    finally:
        _freigeben()


if __name__ == "__main__":
    info, alter = _sperre_info()
    if info and alter < SPERRE_MIN:
        print(f"GESPERRT seit {alter:.0f} Min.: {info}")
    else:
        print("frei" + (f" (abgelaufene Sperre: {info})" if info else ""))
