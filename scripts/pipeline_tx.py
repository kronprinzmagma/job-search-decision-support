#!/usr/bin/env python3
"""
pipeline_tx — einziger Schreibweg in data/pipeline.json.

Anlass: parallele Sessions ueberschrieben sich gegenseitig
(feedback/2025-03-11_datenverlust-parallele-sessions.md). Mehrere Sessions (Sweep, Kandidaten-Chat,
Pflegelauf) schrieben ohne Koordination in dieselbe Datei; wer einen aelteren Stand eingelesen hatte,
ueberschrieb beim Speichern die Arbeit der anderen.

Zwei Schutzschichten:
  1. Sperrdatei data/.pipeline.lock (exklusiv angelegt). Liegt sie schon da und ist juenger
     als SPERRE_MIN Minuten, bricht der Schreibversuch ab — nicht warten, nicht ueberschreiben.
     Eine aeltere Sperre gilt als verwaist, wird gemeldet und uebernommen.
  2. Vergleich der Aenderungszeit: Hat sich pipeline.json zwischen Einlesen und Schreiben
     veraendert, wird NICHT geschrieben (Abbruch mit Meldung).
Geschrieben wird atomar (temporaere Datei, dann umbenennen).

Verwendung in Python:
    from pipeline_tx import transaktion
    with transaktion("wer schreibt, wozu") as data:
        ...  # data["applications"] aendern
Kommandozeile:
    python3 scripts/pipeline_tx.py status      # zeigt, ob gerade jemand schreibt
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
DATA = ROOT / "data" / "pipeline.json"
LOCK = ROOT / "data" / ".pipeline.lock"
SPERRE_MIN = 15


class Konflikt(RuntimeError):
    pass


def _stempel(wer, zusatz=""):
    return f"{jetzt().isoformat(timespec='seconds')} | pid {os.getpid()} | {wer}{zusatz}\n"


def _sperre_info():
    # Alter der Sperre nach Dateisystem-Zeit (nicht nach heute.py: die Sperre lebt in Echtzeit)
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
                continue  # Sperre ist zwischenzeitlich verschwunden: nochmals versuchen
            if alter < SPERRE_MIN:
                raise Konflikt(f"pipeline.json ist gesperrt ({alter:.0f} Min.): {info}. "
                               f"Eine andere Session schreibt gerade — abbrechen, nicht ueberschreiben.")
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
        # Kein Loeschrecht: Sperre als abgelaufen markieren (mtime in die Vergangenheit)
        try:
            alt = time.time() - (SPERRE_MIN + 1) * 60
            os.utime(LOCK, (alt, alt))
        except OSError:
            pass


@contextlib.contextmanager
def transaktion(wer="unbekannt"):
    _sperren(wer)
    try:
        m0 = DATA.stat().st_mtime_ns
        data = json.loads(DATA.read_text(encoding="utf-8"))
        yield data
        if DATA.stat().st_mtime_ns != m0:
            raise Konflikt("pipeline.json wurde waehrend der Bearbeitung von einer anderen Session "
                           "veraendert — NICHT geschrieben. Neu einlesen und Aenderung wiederholen.")
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
