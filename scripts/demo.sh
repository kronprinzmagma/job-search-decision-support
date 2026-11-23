#!/usr/bin/env bash
# demo.sh — erzeugt die Demo-Welt neu und rechnet alles Abgeleitete mit den echten Skripten.
#
#   bash scripts/demo.sh
#
# Reihenfolge wie im Betrieb: Rohdaten (init_demo.py) -> Audit je Sweep -> Prozess-Retro an jedem Sonntag
# -> Views und Cockpit (jobcoach.py) -> Reports. Die Uhr ist eingefroren (JC_HEUTE), das Ergebnis ist
# byte-identisch reproduzierbar; die CI prueft das mit `git diff --exit-code`.
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1

python3 scripts/init_demo.py

export JC_HEUTE=2025-04-25
python3 scripts/screening_log.py audit --aktualisieren --alle > /dev/null

# Prozess-Retro jeden Sonntag des Demo-Zeitraums (misst die Woche davor, prueft die Massnahmen der Vorwoche)
for sonntag in 2025-03-09 2025-03-16 2025-03-23 2025-03-30 2025-04-06 2025-04-13 2025-04-20; do
  JC_HEUTE=$sonntag python3 scripts/prozess_retro.py > /dev/null
done

python3 scripts/jobcoach.py > /dev/null
python3 scripts/marktreport.py > /dev/null
python3 scripts/marktbild.py > /dev/null
{ echo "# Kanal-Auswertung (generiert: scripts/kanal_auswertung.py --tage 56)"; echo; python3 scripts/kanal_auswertung.py --tage 56 | sed '1s/^## /### /'; } > views/KANAELE.md
python3 scripts/analyse_fit_v2.py --schreiben > /dev/null
# Monatliche Marktbeobachtung (spec/MARKT.md): Maerz komplett, April bis zum Demo-Stichtag
python3 scripts/marktcheck.py --monat 2025-03 --schreiben > /dev/null
python3 scripts/marktcheck.py --von 2025-04-01 --bis 2025-04-25 --schreiben > /dev/null

echo "Demo neu gerechnet (Stand $JC_HEUTE). Einstieg: views/STATUS.md"
