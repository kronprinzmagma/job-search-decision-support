#!/usr/bin/env python3
"""Listet die Faelle mit Status «vorgelegt» (Kandidaten-Chat, AGENTS.md «Grundregel Entscheide»).
Ersetzt einen frei geschriebenen Einzeiler im Kandidaten-Prompt: pipeline.json ist ein Objekt
mit den Schluesseln _doc, status_schema, applications — ein Einzeiler, der den ersten Wert
nimmt, zaehlt 0 und beendet die Session still.
Exit 0 = nichts vorgelegt, Exit 1 = es gibt vorgelegte Faelle (IDs je Zeile)."""
import json
import sys
from pathlib import Path

d = json.loads((Path(__file__).resolve().parent.parent / "data" / "pipeline.json").read_text(encoding="utf-8"))
ids = [x["id"] for x in d["applications"] if x.get("status") == "vorgelegt"]
print(f"VORGELEGT: {len(ids)}")
for i in ids:
    print(i)
sys.exit(1 if ids else 0)
