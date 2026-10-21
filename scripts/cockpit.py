#!/usr/bin/env python3
"""cockpit — EIN Ort fuer «was lief heute» und «was liegt bei Alex».

Anlass: Der Ueberblick ging verloren. Was heute lief und angeschaut werden sollte, verschwand zwischen
Sweep-Notizen, Tracker und Chat; relevante Stellen wurden zu spaet erkannt.

Der Block wird von jobcoach.py ganz oben in STATUS.md geschrieben (Einstieg jeder Session) und kann
einmal am Abend als Push-Meldung verschickt werden. Ein Eintrag verschwindet erst, wenn der Entscheid
im Datensatz steht — nicht, wenn er im Chat gefallen ist.

Quellen: data/pipeline.json (vorgelegt, Zweitpruefung an Alex, Drafts mit Go, Gespraeche ohne Debrief),
data/screening_log.json (Kandidaten ohne Datensatz = Bereinigungsbedarf), notes/ (Routinen des Tages),
data/lauf_audit.json (Sweeps).

    python3 scripts/cockpit.py            # Block auf stdout
    python3 scripts/cockpit.py --push     # kurze Fassung fuer die Push-Meldung
"""
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from dublettencheck import norm  # noqa: E402
from heute import heute  # noqa: E402

try:
    import publiziert  # noqa: E402
except ImportError:  # Gruppe Screening; ohne das Modul bleibt das Anzeigen-Alter unbekannt
    publiziert = None

TODAY = heute()


def lade(p, default):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def offene_kandidaten(log, apps, tage=14):
    """Im Sweep als Kandidat vorgelegt, aber kein Datensatz (weder vorgelegt noch Go noch NoGo)."""
    grenze = (TODAY - datetime.timedelta(days=tage)).isoformat()
    out, gesehen = [], set()
    for e in reversed(log.get("gesichtet", [])):
        if e.get("entscheid") != "kandidat" or e.get("datum", "") < grenze:
            continue
        k = (norm(e.get("firma")), norm(e.get("rolle")))
        if k in gesehen:
            continue
        gesehen.add(k)
        if entschieden(e, apps):
            continue  # Datensatz vorhanden -> erfasst
        out.append(e)
    return out


STOPP = {"kanton", "stadt", "bank", "digital", "group", "ag", "sa", "the", "of", "und", "and"}


def entschieden(e, apps):
    """Beliebiger Datensatz zum Kandidaten vorhanden? Firma: Containment ODER ein gemeinsames tragendes Wort;
    Rolle: Containment oder zwei gemeinsame Woerter (wie dublettencheck) oder Wortmenge zu >= 60 % gleich.
    Auch Status 'vorgelegt' zaehlt: pipeline.json ist die kanonische Aktionsliste, das Screening-Log nur
    die Herkunftsspur."""
    nf, nr = norm(e.get("firma")), norm(e.get("rolle"))
    fw = {x for x in nf.split() if len(x) > 2 and x not in STOPP}
    rw = {x for x in nr.split() if len(x) > 2}
    for a in apps:
        ef, er = norm(a.get("firma")), norm(a.get("rolle"))
        ew = {x for x in ef.split() if len(x) > 2 and x not in STOPP}
        firma_ok = (nf and ef and (nf in ef or ef in nf)) or bool(fw & ew)
        if not firma_ok:
            continue
        erw = {x for x in er.split() if len(x) > 2}
        rolle_ok = bool(nr and er and (nr in er or er in nr or len(rw & erw) >= 2
                                       or (rw and len(rw & erw) / len(rw) >= 0.6)))
        if rolle_ok:
            return True
    return False


def sweep_notiz_empfehlung(e):
    """Empfehlung aus der Sweep-Notiz des Tages ziehen (Zeile «Empfehlung:» im Kandidatenblock)."""
    for art in ("nachmittag", "mittag", "morgen"):
        p = ROOT / "notes" / f"{e.get('datum')}_screening_{art}.md"
        if not p.exists():
            continue
        txt = p.read_text(encoding="utf-8", errors="ignore")
        i = txt.find(e.get("firma", "")[:20])
        if i < 0:
            continue
        m = re.search(r"Empfehlung:\*?\*?\s*\**([^\n*]{3,120})", txt[i:i + 4000])
        if m:
            return m.group(1).strip(), p.name
        return "", p.name
    return "", ""


def anzeige_alter(a):
    """(Tage seit Veroeffentlichung oder None, Text) aus der Anzeigen-Datei des Falls.
    Prioritaet nach Alter: eine Anzeige, die ueber eine Woche alt ist, ist meist schwerer zu erreichen."""
    if publiziert is None:
        return None, "Anzeige: Alter unbekannt (publiziert.py fehlt)"
    datei = publiziert.anzeige_datei(ROOT, a["id"])
    pub, _ = publiziert.aus_anzeige(datei) if datei else (None, None)
    if pub is None:
        return None, "Anzeige: Alter unbekannt"
    n = (TODAY - pub).days
    if n > publiziert.ALT_SCHWELLE_TAGE:
        return n, f"⚠ Anzeige {n} Tage alt"
    return n, f"Anzeige {n} Tag{'e' if n != 1 else ''} alt"


def block(kurz=False):
    log = lade(ROOT / "data" / "screening_log.json", {"gesichtet": [], "laeufe": [], "sweeps": []})
    pipe = lade(ROOT / "data" / "pipeline.json", {"applications": []})
    apps = pipe["applications"]
    audit = lade(ROOT / "data" / "lauf_audit.json", [])
    L = []
    w = L.append
    tag = TODAY.isoformat()
    limit = 5 if kurz else 8

    def begrenzen(eintraege):
        return eintraege[:limit], max(0, len(eintraege) - limit)

    def nach_alter(faelle):
        mit_alter = [(a, *anzeige_alter(a)) for a in faelle]
        mit_alter.sort(key=lambda x: (x[1] is None, x[1] if x[1] is not None else 0))
        return mit_alter

    # --- Bei dir liegt ---
    w("## Bei dir liegt")
    w("")
    n = 0
    vorgelegt = [a for a in apps if a.get("status") == "vorgelegt"]
    if vorgelegt:
        w(f"**Vom Sweep vorgelegt, Entscheid bei dir** ({len(vorgelegt)} offen; Go/NoGo im Kandidaten-Chat, "
          "verschwindet mit dem Entscheid; frischeste Anzeige zuerst):")
        sichtbar, weitere = begrenzen(nach_alter(vorgelegt))
        for a, _, alt_txt in sichtbar:
            n += 1
            emp = ""
            for e in a.get("verlauf") or []:
                if e.get("ereignis") == "nachtrag" and "Empfehlung" in (e.get("notiz") or ""):
                    emp = e["notiz"]
            w(f"- **{a['firma']} — {a['rolle']}** · `{a['id']}` · {a.get('datum') or ''} · {alt_txt}"
              + (f" · {emp}" if emp else ""))
        if weitere:
            w(f"- … **{weitere} weitere** vorgelegte Fälle in `APPLICATIONS.md` ({len(sichtbar)} von {len(vorgelegt)} gezeigt)")
        w("")
    kand = offene_kandidaten(log, apps)
    if kand:
        w("**Bereinigungsbedarf: Kandidaten nur im Screening-Log** (noch kein `vorgelegt`-Datensatz; "
          "`python3 scripts/sync_screening_candidates.py --apply`):")
        sichtbar, weitere = begrenzen(kand)
        for e in sichtbar:
            emp, quelle = sweep_notiz_empfehlung(e)
            n += 1
            w(f"- **{e.get('firma')} — {e.get('rolle')}** ({e.get('ort') or '-'}, {e.get('datum')})"
              + (f" · Empfehlung: {emp}" if emp else "") + (f" · `notes/{quelle}`" if quelle and not kurz else ""))
        if weitere:
            w(f"- … **{weitere} weitere** Log-Kandidaten; vollständige Herkunft in `data/screening_log.json`")
        w("")
    zp = [a for a in apps if isinstance(a.get("zweitpruefung"), dict) and a["zweitpruefung"].get("ergebnis") == "an-alex"]
    if zp:
        w("**Wochen-Review hat zurückgegeben (Zweitprüfung, Entscheid bei dir):**")
        for a in zp:
            n += 1
            w(f"- **{a['firma']} — {a['rolle']}** · `{a['id']}` · aussortiert am {a.get('datum') or '?'}: "
              f"{(a.get('begruendung') or '')[:110]}")
        w("")
    drafts = [a for a in apps if a.get("status") == "draft"]
    if drafts:
        w("**Go gegeben, noch nicht verschickt — frischeste Anzeige zuerst:**")
        sichtbar, weitere = begrenzen(nach_alter(drafts))
        for a, _, alt_txt in sichtbar:
            n += 1
            alter = ""
            go = next((e["datum"] for e in a.get("verlauf") or [] if e.get("ereignis") == "go"), a.get("datum"))
            if go:
                try:
                    alter = f", Go seit {(TODAY - datetime.date.fromisoformat(go[:10])).days} Tagen"
                except ValueError:
                    pass
            w(f"- **{a['firma']} — {a['rolle']}** · `{a['id']}`{alter} · {alt_txt}")
        if weitere:
            w(f"- … **{weitere} weitere** Drafts in `data/pipeline.json`")
        w("")
    ohne_debrief = []
    for a in apps:
        d = next((r / a["id"] for r in (ROOT / "eingang", ROOT / "stellen") if (r / a["id"]).is_dir()), None)
        if d is None:
            continue
        for g in d.glob("gespraech_*_vorbereitung.md"):
            m = re.search(r"gespraech_(\d{4}-\d{2}-\d{2})_(.+?)_vorbereitung", g.name)
            if m and datetime.date.fromisoformat(m.group(1)) < TODAY and not list(d.glob(f"gespraech_{m.group(1)}_*debrief.md")):
                ohne_debrief.append((a, m.group(1), m.group(2)))
    if ohne_debrief:
        w("**Gespräche ohne Debrief (nur du kannst das liefern — oder sagen, dass es keins gibt):**")
        for a, dat, typ in ohne_debrief:
            n += 1
            w(f"- {a['firma']} — {typ} am {dat} · `{a['id']}`")
        w("")
    if n == 0:
        w("Nichts. Alle vorgelegten Kandidaten sind entschieden, keine Rückgaben, keine offenen Debriefs.")
        w("")

    # --- Heute gelaufen ---
    w("## Heute gelaufen")
    w("")
    sw = [s for s in log.get("sweeps", []) if s.get("datum") == tag]
    if not sw:
        w("- Screening: **noch kein Sweep heute**")
    fehlend = [a for a in ("morgen", "mittag", "nachmittag") if not any(s.get("art") == a for s in sw)]
    if sw and fehlend:
        w(f"- Screening: noch nicht gelaufen: {', '.join(fehlend)}")
    for s in sw:
        rec = next((r for r in audit if r.get("sweep") == s["id"]), None)
        ist = rec["ist"] if rec else "?"
        soll = rec["soll"] if rec else s.get("soll", "?")
        sicht = [e for e in log.get("gesichtet", []) if e.get("lauf_id") == s["id"]]
        kd = sum(1 for e in sicht if e.get("entscheid") == "kandidat")
        ne = len(rec.get("nicht_erreichbar", [])) if rec else 0
        w(f"- Screening **{s['art']}**: {s['status']}, {ist}/{soll} Abfragen, {len(s.get('sessions', []))} Session(s), "
          f"{len(sicht)} neue Sichtungen, **{kd} Kandidat(en)**" + (f", {ne} nicht erreichbar" if ne else "")
          + ("" if kurz else f" · `notes/{tag}_screening_{s['art']}.md`"))
    for name, muster in (("Pflegelauf", f"{tag}_pflegelauf"), ("Wochen-Review", f"{tag}_wochenreview"),
                         ("Prozess-Retro", f"{tag}_prozessretro")):
        t = sorted((ROOT / "notes").glob(muster + "*.md"))
        if t:
            w(f"- {name}: gelaufen" + ("" if kurz else f" · `notes/{t[-1].name}`"))
    w("")
    return "\n".join(L)


if __name__ == "__main__":
    print(block(kurz="--push" in sys.argv))
