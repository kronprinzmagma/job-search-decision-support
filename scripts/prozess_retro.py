#!/usr/bin/env python3
"""Prozess-Retro für die Screening-Routine (wöchentlich, Sonntag).

Zweck: den Prozess regelmässig verbessern, damit die Resultate besser werden. Der Wochen-Review misst den
ERTRAG der Suche (welcher Begriff, welcher Kanal bringt Kandidaten). Diese Retro misst die QUALITÄT DES
PROZESSES: Läuft alles, was laufen soll? Wird die Form eingehalten? Wird alles geloggt? Wo bricht es ab?
Und: Hat die Massnahme von letzter Woche gewirkt?

Datenbasis: data/lauf_audit.json (ein Datensatz je Sweep, geschrieben von `screening_log.py ende` bzw.
`screening_log.py audit --aktualisieren`), data/screening_log.json (Sweeps, Läufe, Sichtungen),
notes/*_screening_*.md, feedback/*.md der Woche, data/retro_massnahmen.json. Fehlt lauf_audit.json ganz,
rechnet die Retro die Datensätze mit scripts/screening_sweep.py nach (ohne sie zu schreiben).

Aufrufe:
  python3 scripts/prozess_retro.py                       # Retro für die letzten 7 Tage (bis gestern),
                                                         # schreibt notes/<heute>_prozessretro.md
  python3 scripts/prozess_retro.py --tage 14             # anderer Zeitraum
  python3 scripts/prozess_retro.py --markiere <id> angenommen|abgelehnt|umgesetzt ["Notiz"]
  python3 scripts/prozess_retro.py --massnahmen          # Massnahmen-Liste anzeigen

Vorschläge gehen an Alex; das Skript ändert weder Katalog noch Spec noch Prompt.
"""
import json, re, sys, statistics
from pathlib import Path
from datetime import date, datetime, timedelta

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from heute import heute  # noqa: E402

AUDIT = ROOT / "data" / "lauf_audit.json"
LOG = ROOT / "data" / "screening_log.json"
KATALOG = ROOT / "data" / "screening_kanaele.json"
MASSN = ROOT / "data" / "retro_massnahmen.json"
PIPE = ROOT / "data" / "pipeline.json"
NOTES = ROOT / "notes"
FEEDBACK = ROOT / "feedback"
# Soll-Sweeps je Wochentag (Mo..So): werktags morgen, mittag, nachmittag; Samstag nur morgen; Sonntag frei.
SOLL_SWEEPS_JE_WOCHENTAG = (3, 3, 3, 3, 3, 1, 0)
NUR_MORGENS = {"zielportal", "behoerdenportal"}   # werden nicht wegen Ertrag gestrichen (marktreport.py, 3)
ZIEL = {"alter_median_max": 1, "abdeckung": 1.0, "format_ok": 1.0, "sessions_max": 3, "uebersprungen": 0}
# Wirkungskontrolle: in welche Richtung sich eine Metrik bessert
RICHTUNG = {"abdeckung_mean": "hoeher", "format_quote": "hoeher", "sweeps_abgeschlossen": "hoeher",
            "kandidaten_je_sweep": "hoeher", "mit_pub": "hoeher",
            "sweeps_ohne_ende": "tiefer", "nicht_erreichbar": "tiefer", "sessions_mean": "tiefer",
            "uebersprungen": "tiefer", "sammelposten": "tiefer", "verpasst": "tiefer", "rel_median": "tiefer",
            "dauer_mean": "tiefer", "dauer_min_median": "tiefer", "sweeps_doppelt": "tiefer",
            "abfragen_ohne_kandidat_14d": "tiefer", "teilweise_je_sweep": "tiefer"}


def laden(p, default):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def audit_laden(log):
    """(Datensätze, nachgerechnet?) — lauf_audit.json, sonst aus dem Log über screening_sweep nachgerechnet."""
    if AUDIT.exists():
        return json.loads(AUDIT.read_text(encoding="utf-8")), False
    import screening_sweep as sw
    _, aktive = sw.katalog()
    return [sw.audit_datensatz(log, s, aktive) for s in log.get("sweeps", []) if s.get("status") != "migriert"], True


def soll_sweeps(von, bis):
    """Soll-Sweeps über den Zeitraum, tagesgenau nach Wochentag."""
    v, b = date.fromisoformat(von), date.fromisoformat(bis)
    total, d = 0, v
    while d <= b:
        total += SOLL_SWEEPS_JE_WOCHENTAG[d.weekday()]
        d += timedelta(days=1)
    return total


def kennzahlen(audit, von, bis, log):
    sweeps_log = log.get("sweeps", [])
    a = [r for r in audit if von <= r["datum"] <= bis]
    tage = max(0, (date.fromisoformat(bis) - date.fromisoformat(von)).days + 1)
    fertig = [r for r in a if r["status"] == "abgeschlossen"]
    def mean(xs):
        xs = [x for x in xs if x is not None]
        return round(statistics.mean(xs), 3) if xs else None
    ne, feh = {}, {}
    for r in a:
        for pid in r.get("nicht_erreichbar", []):
            ne[pid] = ne.get(pid, 0) + 1
        for pid in r.get("fehlend", []):
            feh[pid] = feh.get(pid, 0) + 1
    fmt = [r["format_ok"] for r in a if r.get("format_ok") is not None]
    # Sweeps, die im Log existieren, aber keinen Audit-Datensatz haben (ende nie aufgerufen)
    mit_audit = {r["sweep"] for r in a}
    ohne_ende = [s["id"] for s in sweeps_log if von <= s["datum"] <= bis and s["status"] != "migriert"
                 and s["id"] not in mit_audit]
    # Doppelt geloggte Abfragen im selben Sweep (zwei Sessions am selben Sweep)
    je_sweep = {}
    for l in log.get("laeufe", []):
        if von <= (l.get("datum") or "") <= bis and l.get("abfrage_id"):
            je_sweep.setdefault(l.get("lauf_id"), []).append(l["abfrage_id"])
    doppelt = sorted(sid for sid, ids in je_sweep.items() if len(ids) != len(set(ids)))
    # Abfragen, die in den 14 Tagen bis Fensterende nur Rauschen lieferten: kein volltextwürdiger Treffer
    # (Kandidat oder Volltext-NoGo). Ziel- und Behördenportale zählen nicht: sie werden nicht wegen Ertrag gestrichen.
    v14 = (date.fromisoformat(bis) - timedelta(days=13)).isoformat()
    kat = laden(KATALOG, {"abfragen": []})["abfragen"]
    gelaufen = {l.get("abfrage_id") for l in log.get("laeufe", []) if v14 <= (l.get("datum") or "") <= bis}
    kand_ueber = {e.get("gefunden_ueber") for e in log.get("gesichtet", [])
                  if v14 <= (e.get("datum") or "") <= bis and e.get("entscheid") in ("kandidat", "volltext-nogo")}
    ohne_kand = sorted(q["id"] for q in kat if q.get("aktiv", True) and q.get("kanal") not in NUR_MORGENS
                       and q["id"] in gelaufen and not ({q["id"], q.get("name")} & kand_ueber))
    kand_zp_mittag = sum(1 for e in log.get("gesichtet", []) if von <= (e.get("datum") or "") <= bis
                         and e.get("entscheid") == "kandidat" and e.get("kanal") == "zielportal"
                         and (e.get("lauf_id") or "").endswith("-mittag"))
    dauern = [r["dauer_min"] for r in a if r.get("dauer_min")]
    return {
        "von": von, "bis": bis, "tage": tage,
        "sweeps_soll": soll_sweeps(von, bis) if tage > 0 else 0, "sweeps_gestartet": len(a),
        "sweeps_abgeschlossen": len(fertig),
        "sweeps_abgebrochen": sum(1 for r in a if r["status"] == "abgebrochen"),
        "sweeps_ohne_ende": ohne_ende,
        "abdeckung_mean": mean([r["abdeckung"] for r in a]),
        "abdeckung_min": min([r["abdeckung"] for r in a if r["abdeckung"] is not None], default=None),
        "sessions_mean": mean([r["sessions"] for r in a]),
        "dauer_mean": mean(dauern),
        "dauer_min_median": statistics.median(dauern) if dauern else None,
        "nicht_erreichbar": sorted(ne.items(), key=lambda x: (-x[1], x[0])),
        "fehlend_haeufig": sorted(feh.items(), key=lambda x: (-x[1], x[0]))[:10],
        "uebersprungen": sum(r.get("uebersprungen", 0) for r in a),
        "teilweise": sum(r.get("teilweise", 0) for r in a),
        "format_quote": round(sum(1 for f in fmt if f) / len(fmt), 3) if fmt else None,
        "format_n": len(fmt),
        "sichtungen": sum(r["neu"] for r in a), "kandidaten": sum(r["kandidaten"] for r in a),
        "sammelposten": sum(r.get("sammelposten", 0) for r in a),
        "kandidaten_je_sweep": mean([r["kandidaten"] for r in a]),
        "teilweise_je_sweep": round(sum(r.get("teilweise", 0) for r in a) / len(a), 2) if a else None,
        "sweeps_doppelt": len(doppelt), "sweeps_doppelt_ids": doppelt,
        "abfragen_ohne_kandidat_14d": len(ohne_kand), "abfragen_ohne_kandidat_ids": ohne_kand,
        "kandidaten_zielportal_mittag": kand_zp_mittag,
    }


def geschwindigkeit(von, bis, log):
    """Fundgeschwindigkeit: die zentrale Grösse, wenn Alex schneller sein will. Stellen, die über eine Woche
    alt sind, sind meist schwerer zu erreichen.

    Alter beim Fund = Datum der ersten Sichtung im Log minus Veröffentlichungsdatum.
    Quellen für das Veröffentlichungsdatum: Log-Feld `publiziert` (8. Feld von `add`), sonst die Kopfzeile
    «Publiziert:» der Anzeigen-Datei (nur Fälle mit Volltext).
    Späte Funde (> 7 Tage) werden eingeordnet: «verpasst» = die Katalog-Abfrage, über die der Fund kam, lief
    schon vor der Veröffentlichung; sonst «Altbestand» (Kanal neu oder Empfehlungsblock mit älteren Anzeigen)
    — der Unterschied entscheidet, ob am Setup etwas zu ändern ist."""
    import screening_log as sl
    import publiziert as pub_mod
    g = log.get("gesichtet", [])
    erst_lauf = {}           # Abfrage (ID und Name, `gefunden_ueber` trägt je nach Kanal das eine oder andere)
    for l in log.get("laeufe", []):
        for schl in (l.get("abfrage_id"), l.get("abfrage")):
            if schl and l.get("datum") and (schl not in erst_lauf or l["datum"] < erst_lauf[schl]):
                erst_lauf[schl] = l["datum"]
    sw_in = [e for e in g if von <= (e.get("datum") or "") <= bis]
    mit_pub = [e for e in sw_in if e.get("publiziert")]
    def alter(e, p):
        return (date.fromisoformat(e["datum"]) - p).days
    alle = [alter(e, date.fromisoformat(e["publiziert"])) for e in mit_pub]
    # relevante Fälle: Kandidat, Volltext geprüft, offen — Datum aus Log, sonst aus der Anzeigen-Datei
    rel = []
    pipe = laden(PIPE, {"applications": []})["applications"]
    for e in sw_in:
        if e.get("entscheid") not in ("kandidat", "volltext-nogo", "offen"):
            continue
        p = date.fromisoformat(e["publiziert"]) if e.get("publiziert") else None
        quelle = "Log" if p else None
        if p is None:
            def passt(a):
                nf, af = sl.norm(e["firma"]), sl.norm(a.get("firma"))
                if not nf or not af or not (f" {nf} " in f" {af} " or f" {af} " in f" {nf} "):
                    return False
                return sl.vergleich(sl.norm(e["rolle"]), sl.norm(a.get("rolle"))) == "gleich"
            a = next((a for a in pipe if passt(a)), None)
            datei = pub_mod.anzeige_datei(ROOT, a["id"]) if a else None
            if datei:
                p, _ = pub_mod.aus_anzeige(datei); quelle = "Anzeige" if p else None
        # erste Sichtung derselben Rolle (Repost zählt ab erster Sichtung)
        frueh = min([x["datum"] for x, st in sl.treffer(e["firma"], e["rolle"], log) if st == "gleich"] + [e["datum"]])
        # Negativ heisst: dieselbe Rolle war schon vor dieser (Neu-)Veröffentlichung bekannt -> rechtzeitig (0)
        n = max(0, (date.fromisoformat(frueh) - p).days) if p else None
        art = None
        if n is not None and n > pub_mod.ALT_SCHWELLE_TAGE:
            q = erst_lauf.get(e.get("gefunden_ueber") or "")
            art = "verpasst" if q and q <= p.isoformat() else "Altbestand"
        rel.append({"firma": e["firma"], "rolle": e["rolle"], "entscheid": e["entscheid"], "kanal": e["kanal"],
                    "ueber": e.get("gefunden_ueber") or "-", "alter": n, "quelle": quelle, "art": art,
                    "publiziert": p.isoformat() if p else None})
    # Dubletten (gleiche Rolle mehrfach im Fenster) nur einmal
    eind = {}
    for r in rel:
        eind.setdefault((sl.norm(r["firma"]), sl.norm(r["rolle"])), r)
    rel = list(eind.values())
    rel_alter = [r["alter"] for r in rel if r["alter"] is not None]
    je_kanal = {}
    for e in mit_pub:
        je_kanal.setdefault(e["kanal"], []).append(alter(e, date.fromisoformat(e["publiziert"])))
    # Go -> Versand (zweiter Teil der Geschwindigkeit)
    go_versand = []
    for a in pipe:
        v = a.get("verlauf") or []
        go = next((x["datum"] for x in v if x.get("ereignis") == "go"), None)
        ve = next((x["datum"] for x in v if x.get("ereignis") == "versand"), None)
        if go and ve and von <= ve <= bis:
            try:
                go_versand.append((date.fromisoformat(ve[:10]) - date.fromisoformat(go[:10])).days)
            except ValueError:
                pass
    med = lambda xs: statistics.median(xs) if xs else None
    return {
        "sichtungen": len(sw_in), "mit_pub": len(mit_pub),
        "alle_median": med(alle), "alle_ueber7": sum(1 for x in alle if x > 7),
        "rel_n": len(rel), "rel_mit_alter": len(rel_alter), "rel_median": med(rel_alter),
        "rel_0_1": sum(1 for x in rel_alter if x <= 1), "rel_2_7": sum(1 for x in rel_alter if 1 < x <= 7),
        "rel_ueber7": sum(1 for x in rel_alter if x > 7),
        "spaet": sorted([r for r in rel if r["art"]], key=lambda r: (-r["alter"], r["firma"])),
        "verpasst": sum(1 for r in rel if r["art"] == "verpasst"),
        "je_kanal": {k: (len(v), med(v)) for k, v in sorted(je_kanal.items())},
        "go_versand_n": len(go_versand), "go_versand_median": med(go_versand),
    }


def rueckweisungen(von, bis):
    """Feedback-Dateien der Woche, die auf einen Formbruch oder eine wiederholte Regel deuten."""
    hits = []
    for f in sorted(FEEDBACK.glob("*.md")):
        m = re.match(r"(\d{4}-\d{2}-\d{2})", f.name)
        if not m or not (von <= m.group(1) <= bis):
            continue
        txt = f.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"rezidiv|wiederholung|format|regel ab sofort|nicht eingehalten|zur[uü]ckgewiesen", txt, re.I):
            hits.append(f.name)
    return hits


def abweichungen(k, vor, gs=None):
    """Regelbasiert: was weicht vom Ziel ab, wie stark, und was wäre der nächste Schritt."""
    out = []
    def add(score, titel, beleg, vorschlag, zieldatei, metrik):
        out.append({"score": score, "titel": titel, "beleg": beleg, "vorschlag": vorschlag,
                    "zieldatei": zieldatei, "metrik": metrik})
    # Fehlende Sweeps sind KEINE Abweichung: läuft der Rechner nicht, holt der nächstmögliche Sweep nach.
    # Die Zahl steht nur in der Kennzahlentabelle.
    if k["abdeckung_mean"] is not None and k["abdeckung_mean"] < 0.98:
        top = ", ".join(f"{p} ({n}x)" for p, n in k["fehlend_haeufig"][:5])
        add(8 * (1 - k["abdeckung_mean"]) * 10, "Abdeckung unter Soll",
            f"Mittlere Abdeckung {round(100*k['abdeckung_mean'])} % (Minimum {round(100*(k['abdeckung_min'] or 0))} %). "
            f"Am häufigsten fehlend: {top or '-'}.",
            "Wenn dieselben IDs fehlen: Reihenfolge im Katalog ändern (früh im Sweep) oder den Eintrag "
            "prüfen (URL, Werkzeugfalle). Wenn breit verteilt: zusätzliche Fortsetzungs-Session im Zeitplan.",
            "data/screening_kanaele.json / Zeitplan", "abdeckung_mean")
    if k["sweeps_abgeschlossen"] < k["sweeps_gestartet"]:
        add(6 * (k["sweeps_gestartet"] - k["sweeps_abgeschlossen"]), "Sweeps nicht abgeschlossen",
            f"{k['sweeps_gestartet'] - k['sweeps_abgeschlossen']} gestartete Sweeps blieben offen oder abgebrochen"
            f"{' (' + str(k['sweeps_abgebrochen']) + ' abgebrochen)' if k['sweeps_abgebrochen'] else ''}.",
            "Abbruchgründe in den Sweep-Notizen lesen; wenn Zeitbudget: Fortsetzungs-Sessions prüfen; "
            "wenn Werkzeug: Falle in den Katalog-Hinweis schreiben.",
            "notes/, data/screening_kanaele.json", "sweeps_abgeschlossen")
    if k["sweeps_ohne_ende"]:
        add(7, "Sweeps ohne «ende»",
            f"{len(k['sweeps_ohne_ende'])} Sweep(s) ohne Audit-Datensatz: {', '.join(k['sweeps_ohne_ende'][:4])} — "
            f"`screening_log.py ende` wurde nie aufgerufen.",
            "Arbeitskarte: `ende` als letzten Pflichtbefehl jeder Session hervorheben; der Wächter meldet es bereits.",
            "spec/SWEEP.md", "sweeps_ohne_ende")
    if k["sweeps_doppelt"]:
        add(6, "Abfragen im selben Sweep doppelt geloggt",
            f"{k['sweeps_doppelt']} Sweep(s) mit doppelt geloggten Abfragen: {', '.join(k['sweeps_doppelt_ids'][:4])} — "
            f"Hinweis auf zwei parallele Sessions.",
            "Sperre des Logs prüfen (scripts/screening_log_tx.py); eine Session ohne Ende darf keinen Neustart zulassen.",
            "scripts/screening_log_tx.py", "sweeps_doppelt")
    if k["format_quote"] is not None and k["format_quote"] < 1.0:
        add(6 * (1 - k["format_quote"]) * 10, "Berichtsform nicht eingehalten",
            f"{round(100*k['format_quote'])} % der Sweep-Notizen vollständig ({k['format_n']} geprüft): Pflichtsektionen oder "
            f"ausgefüllte Kandidatenblöcke fehlen.",
            "Ursache je Notiz benennen (Platzhalter stehen geblieben vs. Sektion fehlt); Satz in der Arbeitskarte "
            "schärfen oder das Skelett anpassen, wenn das Skelett selbst hinderlich ist.",
            "spec/SWEEP.md / scripts/screening_sweep.py", "format_quote")
    if k["nicht_erreichbar"]:
        wieder = [(p, n) for p, n in k["nicht_erreichbar"] if n >= 2]
        if wieder:
            add(4 * len(wieder), "Portale wiederholt nicht erreichbar",
                "; ".join(f"{p} {n}x" for p, n in wieder),
                "Je Portal: verifizierten Weg und Werkzeugfalle im Katalog-Hinweis prüfen und ergänzen. "
                "Erst wenn die Quelle selbst tot ist: Portal ausrangieren (Entscheid Alex).",
                "data/screening_kanaele.json", "nicht_erreichbar")
    if k["sessions_mean"] and k["sessions_mean"] > ZIEL["sessions_max"]:
        add(3, "Viele Sessions je Sweep",
            f"Im Mittel {k['sessions_mean']} Sessions je Sweep (Ziel: höchstens {ZIEL['sessions_max']}).",
            "Katalog auf teure Abfragen prüfen (Begriffe mit viel Rauschen) — Vorschlag zur Zusammenlegung an Alex, "
            "nicht eigenmächtig.",
            "data/screening_kanaele.json", "sessions_mean")
    if k["uebersprungen"] > 0:
        add(3 + k["uebersprungen"], "Abfragen übersprungen",
            f"{k['uebersprungen']} Abfragen mit Status «uebersprungen» — zählen nicht als abgedeckt.",
            "Grund je Fall in den Notizen nachlesen; «uebersprungen» ist nur für bewusste Auslassungen mit Grund.",
            "notes/", "uebersprungen")
    if k["sichtungen"] and k["sammelposten"] / max(1, k["sichtungen"]) > 0.3:
        add(3, "Hoher Sammelposten-Anteil",
            f"{k['sammelposten']} von {k['sichtungen']} Sichtungen sind Sammelposten — für `check` unsichtbar.",
            "Sammelposten nur mit Begründung; sonst Einzeleinträge.",
            "spec/SWEEP.md", "sammelposten")
    if gs:
        if gs["verpasst"]:
            fv = [r for r in gs["spaet"] if r["art"] == "verpasst"]
            add(9 + gs["verpasst"], "Stellen zu spät gefunden (verpasst)",
                f"{gs['verpasst']} relevante Anzeige(n) erst nach über einer Woche gefunden, obwohl die Abfrage schon lief: "
                + "; ".join(f"{r['firma']} — {r['rolle']} ({r['alter']} Tage, über {r['ueber']})" for r in fv[:4]) + ".",
                "Je Fall prüfen, warum die laufende Abfrage die Anzeige nicht zeigte (Zeitfenster der Abfrage zu kurz, "
                "Begriff fehlt, Liste nur teilweise gelesen) und den Katalog-Eintrag bzw. Begriff anpassen.",
                "data/screening_kanaele.json", "verpasst")
        if gs["rel_median"] is not None and gs["rel_median"] > ZIEL["alter_median_max"]:
            add(8, "Fundgeschwindigkeit unter Ziel",
                f"Relevante Anzeigen (Kandidat, Volltext, offen) im Median {gs['rel_median']} Tage alt beim Fund "
                f"(Ziel höchstens {ZIEL['alter_median_max']} Tag).",
                "Kanäle mit hohem Alter beim Fund (Tabelle Fundgeschwindigkeit) früher im Sweep fahren oder ihr "
                "Zeitfenster prüfen.", "data/screening_kanaele.json", "rel_median")
        if gs["sichtungen"] >= 50 and gs["mit_pub"] / gs["sichtungen"] < 0.5:
            add(4, "Veröffentlichungsdatum zu selten erfasst",
                f"Nur {gs['mit_pub']} von {gs['sichtungen']} Sichtungen mit Publiziert-Datum — die Fundgeschwindigkeit "
                f"ist nur für einen Teil messbar.",
                "Beim `add` das 8. Feld (Publiziert, wie in der Trefferliste angezeigt) füllen, wo die Liste ein Datum zeigt.",
                "spec/SWEEP.md (Ablauf Schritt 4)", "mit_pub")
    # Trend gegen Vorwoche
    if vor and vor["sweeps_gestartet"]:
        for key, name in (("abdeckung_mean", "Abdeckung"), ("format_quote", "Formquote")):
            a, b = k.get(key), vor.get(key)
            if a is not None and b is not None and a < b - 0.05:
                add(5, f"{name} schlechter als Vorwoche",
                    f"{name}: {round(100*a)} % gegen {round(100*b)} % in der Vorwoche.",
                    "Was hat sich seit der Vorwoche geändert (Katalog, Arbeitskarte, Modell, Rechner)? Änderungsliste prüfen.",
                    "notes/", key)
    out.sort(key=lambda x: (-x["score"], x["titel"]))
    return out


def wert(k, metrik):
    """Metrik als Zahl (Listen zählen als Anzahl bzw. Summe der Vorkommen)."""
    v = k.get(metrik)
    if isinstance(v, list):
        return sum(x[1] if isinstance(x, (list, tuple)) else 1 for x in v)
    return v


def wirkung(m, jetzt):
    """gewirkt | unverändert | nicht gewirkt | nicht messbar — gegen den Wert bei Vorschlag."""
    damals, richtung = m.get("wert_bei_vorschlag"), RICHTUNG.get(m.get("metrik"))
    if not isinstance(damals, (int, float)) or not isinstance(jetzt, (int, float)) or not richtung:
        return "nicht messbar"
    if jetzt == damals:
        return "unverändert"
    besser = jetzt < damals if richtung == "tiefer" else jetzt > damals
    return "gewirkt" if besser else "nicht gewirkt"


def massnahmen_laden():
    return laden(MASSN, [])


def massnahmen_speichern(m):
    MASSN.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def fmt_pct(x):
    return "-" if x is None else f"{round(100*x)} %"


def retro(tage):
    log = laden(LOG, {"sweeps": [], "laeufe": [], "gesichtet": []})
    audit, nachgerechnet = audit_laden(log)
    tag = heute()
    # Fenster endet gestern, nicht heute — sonst misst die Retro einen angebrochenen Tag als Abweichung.
    bis_datum = tag - timedelta(days=1)
    bis = bis_datum.isoformat(); von = (bis_datum - timedelta(days=tage - 1)).isoformat()
    v_bis = (bis_datum - timedelta(days=tage)).isoformat(); v_von = (bis_datum - timedelta(days=2 * tage - 1)).isoformat()
    k = kennzahlen(audit, von, bis, log)
    vor = kennzahlen(audit, v_von, v_bis, log)
    rw = rueckweisungen(von, bis)
    gs = geschwindigkeit(von, bis, log)
    gs_vor = geschwindigkeit(v_von, v_bis, log)
    k.update({"rel_median": gs["rel_median"], "verpasst": gs["verpasst"], "mit_pub": gs["mit_pub"]})
    abw = abweichungen(k, vor, gs)
    massn = massnahmen_laden()

    z = []; w = z.append
    w(f"# Prozess-Retro Screening — {tag.isoformat()} (Zeitraum {von} bis {bis})")
    w("")
    w("Misst die Qualität des Prozesses, nicht den Ertrag der Suche (der steht im Wochen-Review). "
      "Quelle: data/lauf_audit.json, data/screening_log.json, notes/, feedback/.")
    if nachgerechnet:
        w("")
        w("*data/lauf_audit.json fehlt: Audit-Datensätze aus data/screening_log.json nachgerechnet "
          "(`python3 scripts/screening_log.py audit --aktualisieren --alle` schreibt sie).*")
    w("")
    w("## Kennzahlen")
    w("")
    w("| Kennzahl | diese Woche | Vorwoche | Ziel |")
    w("|---|---|---|---|")
    w(f"| Sweeps gestartet / Soll (nur Info) | {k['sweeps_gestartet']} / {k['sweeps_soll']} | {vor['sweeps_gestartet']} / {vor['sweeps_soll']} | — |")
    w(f"| Sweeps abgeschlossen | {k['sweeps_abgeschlossen']} | {vor['sweeps_abgeschlossen']} | {k['sweeps_soll']} |")
    w(f"| Sweeps abgebrochen | {k['sweeps_abgebrochen']} | {vor['sweeps_abgebrochen']} | 0 |")
    w(f"| Sweeps ohne «ende» | {len(k['sweeps_ohne_ende'])} | {len(vor['sweeps_ohne_ende'])} | 0 |")
    w(f"| Sweeps mit doppelt geloggten Abfragen | {k['sweeps_doppelt']} | {vor['sweeps_doppelt']} | 0 |")
    w(f"| Abdeckung Mittel / Minimum | {fmt_pct(k['abdeckung_mean'])} / {fmt_pct(k['abdeckung_min'])} | {fmt_pct(vor['abdeckung_mean'])} / {fmt_pct(vor['abdeckung_min'])} | 100 % |")
    w(f"| Sessions je Sweep (Mittel) | {k['sessions_mean'] or '-'} | {vor['sessions_mean'] or '-'} | ≤ {ZIEL['sessions_max']} |")
    w(f"| Dauer je Sweep (Mittel / Median, min) | {k['dauer_mean'] or '-'} / {k['dauer_min_median'] or '-'} | {vor['dauer_mean'] or '-'} / {vor['dauer_min_median'] or '-'} | — |")
    w(f"| Abfragen nicht erreichbar | {sum(n for _, n in k['nicht_erreichbar'])} | {sum(n for _, n in vor['nicht_erreichbar'])} | 0 |")
    w(f"| Abfragen teilweise / übersprungen | {k['teilweise']} / {k['uebersprungen']} | {vor['teilweise']} / {vor['uebersprungen']} | — / 0 |")
    w(f"| Berichtsform vollständig | {fmt_pct(k['format_quote'])} ({k['format_n']} Notizen) | {fmt_pct(vor['format_quote'])} | 100 % |")
    w(f"| Sichtungen / Kandidaten | {k['sichtungen']} / {k['kandidaten']} | {vor['sichtungen']} / {vor['kandidaten']} | — |")
    w(f"| Kandidaten je Sweep | {k['kandidaten_je_sweep'] or 0} | {vor['kandidaten_je_sweep'] or 0} | — |")
    w(f"| Abfragen nur mit Rauschen, 14 Tage (ohne Ziel-/Behördenportale) | {k['abfragen_ohne_kandidat_14d']} | {vor['abfragen_ohne_kandidat_14d']} | — |")
    w(f"| Sammelposten | {k['sammelposten']} | {vor['sammelposten']} | wenige |")
    w(f"| Feedback-Dateien mit Formbruch/Rezidiv | {len(rw)} | — | 0 |")
    w("")
    if rw:
        w("Feedback der Woche: " + ", ".join(rw))
        w("")
    if k["nicht_erreichbar"]:
        w("Nicht erreichbar: " + "; ".join(f"{p} {n}x" for p, n in k["nicht_erreichbar"]))
        w("")
    w("## Fundgeschwindigkeit — wie alt war eine Anzeige, als wir sie fanden?")
    w("")
    w("Zentrale Grösse für «schneller sein». Alter beim Fund = erste Sichtung minus Veröffentlichung. "
      "Über eine Woche alt = meist schwerer zu erreichen.")
    w("")
    fm = lambda x: "-" if x is None else (f"{x:g} Tag" if x == 1 else f"{x:g} Tage")
    w("| Kennzahl | diese Woche | Vorwoche | Ziel |")
    w("|---|---|---|---|")
    w(f"| Relevante Fälle (Kandidat, Volltext, offen) mit Datum | {gs['rel_mit_alter']} von {gs['rel_n']} | {gs_vor['rel_mit_alter']} von {gs_vor['rel_n']} | alle |")
    w(f"| **Alter beim Fund, Median** | **{fm(gs['rel_median'])}** | {fm(gs_vor['rel_median'])} | ≤ {ZIEL['alter_median_max']} Tag |")
    w(f"| davon 0–1 Tag / 2–7 Tage / über 7 Tage | {gs['rel_0_1']} / {gs['rel_2_7']} / {gs['rel_ueber7']} | {gs_vor['rel_0_1']} / {gs_vor['rel_2_7']} / {gs_vor['rel_ueber7']} | — |")
    w(f"| Über 7 Tage, obwohl die Abfrage schon lief (verpasst) | {gs['verpasst']} | {gs_vor['verpasst']} | 0 |")
    w(f"| Sichtungen mit Publiziert-Datum im Log | {gs['mit_pub']} von {gs['sichtungen']} | {gs_vor['mit_pub']} von {gs_vor['sichtungen']} | möglichst alle |")
    w(f"| Alle Sichtungen: Alter beim Fund, Median | {fm(gs['alle_median'])} | {fm(gs_vor['alle_median'])} | — |")
    w(f"| Go bis Versand, Median (Versand in der Woche, n) | {fm(gs['go_versand_median'])} ({gs['go_versand_n']}) | {fm(gs_vor['go_versand_median'])} ({gs_vor['go_versand_n']}) | — |")
    w("")
    if gs["je_kanal"]:
        w("Je Kanal (Sichtungen mit Datum, Median Alter): " + "; ".join(
            f"{kn} {n}× {fm(m)}" for kn, (n, m) in gs["je_kanal"].items()))
        w("")
    if gs["spaet"]:
        w("Späte Funde (über eine Woche alt):")
        w("")
        w("| Firma — Rolle | Alter | Art | gefunden über | Entscheid |")
        w("|---|---|---|---|---|")
        for r in gs["spaet"][:12]:
            w(f"| {r['firma']} — {r['rolle']} | {r['alter']} Tage | {r['art']} | {r['ueber']} | {r['entscheid']} |")
        w("")
    w("## Die drei grössten Abweichungen")
    w("")
    if not abw:
        w("Keine — alle Kennzahlen im Ziel.")
    for i, a in enumerate(abw[:3], 1):
        w(f"{i}. **{a['titel']}** — {a['beleg']}")
    if len(abw) > 3:
        w("")
        w("Weitere: " + "; ".join(a["titel"] for a in abw[3:]))
    w("")
    w("## Vorschläge (Entscheid bei Alex)")
    w("")
    neu = []
    for a in abw[:3]:
        t = a["titel"].lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
        mid = f"{tag.isoformat()}-{re.sub(r'[^a-z0-9]+', '-', t).strip('-')[:40]}"
        if any(m["id"] == mid for m in massn):
            continue
        rec = {"id": mid, "datum": tag.isoformat(), "befund": a["titel"], "beleg": a["beleg"], "vorschlag": a["vorschlag"],
               "zieldatei": a["zieldatei"], "metrik": a["metrik"], "wert_bei_vorschlag": wert(k, a["metrik"]),
               "entscheid": "offen", "notiz": ""}
        massn.append(rec); neu.append(rec)
    if not abw:
        w("Keine.")
    for a in abw[:3]:
        w(f"- **{a['titel']}** → {a['vorschlag']} *(Zieldatei: {a['zieldatei']})*")
    w("")
    w("## Wirkungskontrolle früherer Massnahmen")
    w("")
    w("Je angenommene oder umgesetzte Massnahme: Metrik beim Vorschlag gegen diese Woche.")
    w("")
    fr = [m for m in massn if m["datum"] < tag.isoformat() and m["entscheid"] in ("angenommen", "umgesetzt")]
    if not fr:
        w("Keine angenommene Massnahme aus früheren Wochen.")
    else:
        w("| Massnahme | Entscheid | Metrik | damals | jetzt | Wirkung |")
        w("|---|---|---|---|---|---|")
    vorwoche, urteile = [], {}
    for m in fr:
        jetzt = wert(k, m.get("metrik"))
        urteil = wirkung(m, jetzt)
        urteile[m["id"]] = urteil
        stichtag = m.get("entscheid_datum") or m["datum"]
        if v_von <= stichtag < tag.isoformat():
            vorwoche.append(m)
        w(f"| {m['datum']} {m['befund']} | {m['entscheid']} | {m.get('metrik')} | {m.get('wert_bei_vorschlag')} | "
          f"{'-' if jetzt is None else jetzt} | **{urteil}**{' — ' + m['notiz'] if m.get('notiz') else ''} |")
    w("")
    if fr:
        if vorwoche:
            w(f"Massnahmen seit Beginn der Vorwoche ({v_von}): "
              + "; ".join(f"{m['id']} **{urteile[m['id']]}**" for m in vorwoche) + ".")
        else:
            w(f"Seit Beginn der Vorwoche ({v_von}) wurde keine Massnahme umgesetzt; die Tabelle prüft alle früheren weiter.")
        schlecht = [m for m in fr if urteile[m["id"]] == "nicht gewirkt"]
        if schlecht:
            w("")
            w("Nicht gewirkt: " + ", ".join(m["id"] for m in schlecht) + " — Ursache klären, bevor eine neue "
              "Massnahme zur selben Metrik vorgeschlagen wird.")
        w("")
    offen = [m for m in massn if m["entscheid"] == "offen" and m["datum"] < tag.isoformat()]
    if offen:
        w("Noch unentschieden aus früheren Retros: " + ", ".join(m["id"] for m in offen))
        w("")
    try:
        import kanal_auswertung
        for zeile in kanal_auswertung.abschnitt(28, bis):
            w(zeile)
    except Exception as e:
        w(f"## Kanal-Auswertung\n\nNicht erstellt: {e}")
    w("")
    w("## Bei dir liegt")
    w("")
    if not abw:
        w("Keine Entscheide.")
    for a in abw[:3]:
        w(f"- {a['titel']}: **annehmen** (Umsetzung wie vorgeschlagen) / **ablehnen** (bleibt so, Grund vermerken) / **anders** (dein Vorschlag)")
    w("")
    w("Markieren: `python3 scripts/prozess_retro.py --markiere <id> angenommen|abgelehnt|umgesetzt \"Notiz\"` — IDs: "
      + (", ".join(m["id"] for m in neu) if neu else "keine neuen"))
    text = "\n".join(z)
    massnahmen_speichern(massn)
    NOTES.mkdir(exist_ok=True)
    pfad = NOTES / f"{tag.isoformat()}_prozessretro.md"
    # Handgeschriebener Teil (ab «## Ursachen») bleibt bei einem erneuten Lauf erhalten
    rest = ""
    if pfad.exists():
        alt = pfad.read_text(encoding="utf-8")
        if "\n## Ursachen" in alt:
            rest = "\n" + alt[alt.index("\n## Ursachen"):].strip("\n") + "\n"
    pfad.write_text(text + "\n" + rest, encoding="utf-8")
    print(text)
    print(f"\nGeschrieben: {pfad.relative_to(ROOT)}; {len(neu)} neue Massnahme(n) in data/retro_massnahmen.json")
    return 0


def main():
    a = sys.argv[1:]
    if "--massnahmen" in a:
        for m in massnahmen_laden():
            print(f"{m['id']:60s} {m['entscheid']:10s} {m['befund']} — {m.get('notiz', '')}")
        return 0
    if "--markiere" in a:
        i = a.index("--markiere")
        if len(a) < i + 3:
            print(__doc__); return 2
        mid, ent = a[i + 1], a[i + 2]
        notiz = a[i + 3] if len(a) > i + 3 else ""
        if ent not in ("angenommen", "abgelehnt", "umgesetzt", "offen"):
            print("Entscheid: angenommen | abgelehnt | umgesetzt | offen"); return 2
        m = massnahmen_laden()
        for r in m:
            if r["id"] == mid:
                r["entscheid"] = ent; r["notiz"] = notiz; r["entscheid_datum"] = heute().isoformat()
                massnahmen_speichern(m); print(f"{mid}: {ent}"); return 0
        print(f"{mid} nicht gefunden"); return 1
    tage = int(a[a.index("--tage") + 1]) if "--tage" in a else 7
    return retro(tage)


if __name__ == "__main__":
    sys.exit(main())
