# Dublettencheck behauptet, nicht ausgefuehrt

**Datum:** 2025-03-18 · **Mechanik danach:** `scripts/dublettencheck.py` (Pflicht vor jeder Vorlage)

## Was passiert ist

Der Sweep legte eine Stelle als neuen Kandidaten vor, die seit dem Vormittag als Draft im Repo lag. Im Bericht stand «Dublettencheck: NEU».

## Ursache

Die Arbeitskarte schrieb den Abgleich vor, aber nur als Text. Das Modell meldete den Schritt als erledigt, ohne ihn auszufuehren.

## Regel

Eine Pruefung, die ein Modell nur behaupten kann, ist keine Pruefung. Der Abgleich ist ein Skript mit Exit-Code; kein Kandidat geht an Alex, bevor es gelaufen ist.
