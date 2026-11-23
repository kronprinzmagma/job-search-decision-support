"""heute — ein einziger Ort fuer «heute» und «jetzt».

Im Betrieb ist das schlicht das Systemdatum. Fuer die Demo-Daten (fester, synthetischer Zeitraum)
und fuer Tests laesst sich die Uhr einfrieren:

    JC_HEUTE=2025-04-25 python3 scripts/jobcoach.py
    JC_JETZT=2025-04-25T18:30:00 python3 scripts/cockpit.py

JC_JETZT hat Vorrang; ohne JC_JETZT gilt JC_HEUTE um 18:30 Uhr (alle Sweeps des Tages sind dann durch).
"""
import datetime
import os


def jetzt() -> datetime.datetime:
    roh = os.environ.get("JC_JETZT")
    if roh:
        return datetime.datetime.fromisoformat(roh)
    tag = os.environ.get("JC_HEUTE")
    if tag:
        return datetime.datetime.combine(datetime.date.fromisoformat(tag), datetime.time(18, 30))
    return datetime.datetime.now()


def heute() -> datetime.date:
    return jetzt().date()
