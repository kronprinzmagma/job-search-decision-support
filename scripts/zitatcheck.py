#!/usr/bin/env python3
"""
zitatcheck — jede Absage-Begruendung ist woertlich in der abgelegten Anzeige belegt.

    python3 scripts/zitatcheck.py            # alle aussortierten Faelle pruefen
    python3 scripts/zitatcheck.py <id> ...   # nur diese Faelle

Anlass: Ein NoGo stand bisher als Freitext im Datensatz. Die Regeln verlangen, dass jede Aussage die Stelle
in der Anzeige nennt, auf die sie sich stuetzt; geprueft wurde das nirgends, und ein Vorfall zeigt, dass eine
Bewertung schon einmal auf einer Umschreibung statt der Anzeige beruhte
(feedback/2025-03-25_bewertung-auf-paraphrase.md). Jetzt gilt: Das Modell belegt, das Skript prueft.

Regel je Fall mit Status `aussortiert`:
  - `zitate` ist eine Liste kurzer, woertlicher Ausschnitte aus der Anzeige (mindestens einer, je mindestens
    MIN_ZEICHEN Zeichen), und jeder Ausschnitt kommt in der Datei `anzeige` vor.
  - Verglichen wird nach Vereinheitlichung der Leerzeichen und Zeilenumbrueche, sonst exakt (Gross/klein,
    Umlaute, Satzzeichen). Der eigene Anhang «## Für cv-tailor» zaehlt nicht zur Anzeige.
  - Ausnahme nur ausdruecklich: `zitat_ausnahme` mit Grund (z. B. ein eigener Entscheid von Alex, dessen
    Grund nicht in der Anzeige steht). Gesetzt wird sie mit `status.py … --ohne-zitat "<Grund>"`.

Dieselbe Pruefung laeuft beim Schreiben: `status.py <id> aussortiert --zitat …` und
`screening_log.py add` (Entscheid volltext-nogo) nehmen ein NoGo nur mit belegtem Zitat an.

Exit-Code: 0 alles belegt, 1 mindestens ein Verstoss, 2 unbekannte ID.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIPE = ROOT / "data" / "pipeline.json"
MIN_ZEICHEN = 12
ANHANG = "\n## Für cv-tailor"


def normalisieren(s: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s)).strip()


def anzeige_text(pfad: Path) -> str:
    """Text der Anzeige ohne den eigenen Anhang, normalisiert."""
    text = pfad.read_text(encoding="utf-8")
    return normalisieren(text.split(ANHANG, 1)[0])


def zitat_fehler(text_normalisiert: str, zitate) -> list[str]:
    """Liste der Verstoesse fuer die Zitate gegen einen (normalisierten) Anzeigentext; leer = belegt."""
    if not isinstance(zitate, list) or not zitate:
        return ["kein Zitat aus der Anzeige"]
    out = []
    for z in zitate:
        if not isinstance(z, str) or len(normalisieren(z)) < MIN_ZEICHEN:
            out.append(f"Zitat zu kurz (mindestens {MIN_ZEICHEN} Zeichen): «{z}»")
        elif normalisieren(z) not in text_normalisiert:
            out.append(f"Zitat steht nicht woertlich in der Anzeige: «{z}»")
    return out


def pruefe_zitate(anzeige: str | None, zitate, root: Path = ROOT) -> list[str]:
    """Prueft Zitate gegen die Anzeige unter `anzeige` (Pfad relativ zu root)."""
    if not anzeige:
        return ["keine abgelegte Anzeige im Datensatz (Feld 'anzeige')"]
    pfad = root / anzeige
    if not pfad.is_file():
        return [f"Anzeige {anzeige} existiert nicht"]
    return zitat_fehler(anzeige_text(pfad), zitate)


def pruefe_fall(a: dict, root: Path = ROOT) -> list[str]:
    if a.get("status") != "aussortiert":
        return []
    if str(a.get("zitat_ausnahme") or "").strip():
        return []
    return pruefe_zitate(a.get("anzeige"), a.get("zitate"), root)


def main(argv=None):
    ids = (argv if argv is not None else sys.argv[1:])
    if any(x in ("-h", "--help") for x in ids):
        print(__doc__)
        return 0
    apps = json.loads(PIPE.read_text(encoding="utf-8"))["applications"]
    if ids:
        bekannt = {a.get("id") for a in apps}
        fehlt = [i for i in ids if i not in bekannt]
        if fehlt:
            print(f"FEHLER: unbekannte ID(s): {', '.join(fehlt)}", file=sys.stderr)
            return 2
        apps = [a for a in apps if a.get("id") in ids]
    geprueft = ausnahmen = 0
    verstoesse = []
    for a in apps:
        if a.get("status") != "aussortiert":
            continue
        if str(a.get("zitat_ausnahme") or "").strip():
            ausnahmen += 1
            continue
        geprueft += 1
        for f in pruefe_fall(a, ROOT):
            verstoesse.append(f"{a.get('id')}: {f}")
    for v in verstoesse:
        print(f"VERSTOSS {v}")
    zusammenfassung = (f"{geprueft} NoGo-Begruendungen geprueft, {ausnahmen} ausdrueckliche Ausnahmen, "
                       f"{len(verstoesse)} Verstoesse.")
    if verstoesse:
        print(f"FEHLER: {zusammenfassung} Jede Absage-Begruendung braucht ein woertliches Zitat aus der Anzeige "
              "(Feld 'zitate'), siehe spec/PRESCREEN.md.", file=sys.stderr)
        return 1
    print(f"OK: {zusammenfassung}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
