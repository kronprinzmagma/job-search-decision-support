# Datenverlust durch parallele Sessions

**Datum:** 2025-03-11 · **Mechanik danach:** `scripts/pipeline_tx.py`, `scripts/screening_log_tx.py`

## Was passiert ist

Zwei Sessions (Sweep und Kandidaten-Chat) lasen `data/pipeline.json` ein, arbeiteten parallel und schrieben am Ende ihren ganzen Stand zurueck. Die zweite ueberschrieb die Entscheide der ersten. Aufgefallen ist es erst, als ein Go im Cockpit wieder als offen erschien.

## Ursache

Jede Session hielt eine eigene Kopie der Datei; niemand pruefte vor dem Schreiben, ob sich die Datei inzwischen geaendert hatte.

## Regel

Es gibt genau einen Schreibweg: `pipeline_tx.transaktion()`. Sperrdatei (exklusiv angelegt), Vergleich der Aenderungszeit vor dem Schreiben, atomares Ersetzen. Bei Konflikt wird nicht gewartet und nicht ueberschrieben, sondern abgebrochen und gemeldet.
