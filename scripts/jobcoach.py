#!/usr/bin/env python3
"""
jobcoach — generiert die lesbaren Views aus der EINZIGEN Quelle data/pipeline.json.

    python3 scripts/jobcoach.py

Erzeugt deterministisch APPLICATIONS.md (Voll-Tracker), STATUS.md (Session-Einstieg: Cockpit «Bei dir
liegt», Zahlen, Befunde in Kurzform) und WARNINGS.md (alle Waechter-Befunde). Vergibt fehlende IDs
(Slug aus Firma + Rolle) und schreibt sie ueber scripts/pipeline_tx.py zurueck.

Pflege-Waechter: Schema (unbekannte Felder, Pflichtfelder je Status) · fit_v2 fehlt nach dem Go
(spec/PRESCREEN.md, Schritt 2) · stale oder datenlose Bewerbungen · Anzeige fehlt, liegt falsch, traegt
keinen portablen Namen oder kein «Publiziert» · Fall-Ordner ohne Datensatz, lose Dateien im Eingang ·
Go ohne Recherche · Volltext-NoGo ohne Ablage · Sichtungs-Log und Sweeps gegen den Soll-Katalog ·
Verlauf ohne passendes Ereignis, Gespraech ohne Debrief, Widerspruch Datei <-> Status · Wirkungskontrolle.

Felder (Kontrakt KNOWN_FIELDS), u.a.: `anzeige` = stellen/<id>/<id>--anzeige--<erfasst>.md (bei vorgelegt
und draft unter eingang/<id>/), `dossier` = Fall-Ordner, `verlauf` = Liste {datum, ereignis, quelle, notiz}
(scripts/ereignis.py, scripts/status.py), `fit_v2` = Raster Schritt 2 ex ante, `gespraech_termin`, `debrief`.

Status lebt NUR in pipeline.json; die erzeugten .md-Dateien nie von Hand editieren.
Nur Standardbibliothek. Zeit nur ueber scripts/heute.py (JC_HEUTE friert die Uhr ein).
"""
import collections
import datetime
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from heute import heute, jetzt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "pipeline.json"
NARRATIVE = ROOT / "data" / "applications_narrative.md"
VIEWS = ROOT / "views"
APPS_MD = VIEWS / "APPLICATIONS.md"
STATUS_MD = VIEWS / "STATUS.md"
WARNINGS_MD = VIEWS / "WARNINGS.md"
STALE_DAYS = 21
TODAY = heute()

EMOJI = {
    "vorgelegt": "🔎 Vorgelegt", "draft": "📝 Draft", "abgeschickt": "📤 Abgeschickt",
    "in_pruefung": "👀 In Prüfung", "gespraech": "📞 Gespräch", "abgesagt": "❌ Abgesagt",
    "zurueckgezogen": "🗑 Zurückgezogen", "angebot": "✅ Angebot", "aussortiert": "🚫 Aussortiert",
}
ACTIVE = {"draft", "abgeschickt", "in_pruefung", "gespraech", "angebot"}
OFFENE_ABLAGE = ("vorgelegt", "draft")  # Fall-Ordner liegt in eingang/<id>/, sonst in stellen/<id>/

# Schema-Kontrakt: erlaubte Feldnamen (Drift-Schutz — 'datum_absage' statt 'absage_datum' verfaelscht den Funnel)
KNOWN_FIELDS = {
    "id", "firma", "rolle", "status", "datum", "standort", "quelle", "notiz", "anzeige", "dossier", "verlauf",
    "datum_eingereicht", "datum_ist_einreichung", "datum_cv_tailor", "iter", "gespraech_termin", "debrief",
    "absage_datum", "stadium", "begruendung", "fit_v2", "zweitpruefung", "eintritt",
}
# Pflichtfelder pro Status (ueber die Basisfelder id/firma/rolle/status hinaus)
REQUIRED_BY_STATUS = {
    "abgesagt": ("absage_datum", "stadium", "begruendung"),
    "aussortiert": ("datum", "begruendung"),
    "abgeschickt": ("datum_eingereicht",),
    "in_pruefung": ("datum_eingereicht",),
    "gespraech": ("gespraech_termin",),
    "zurueckgezogen": ("begruendung",),
}
EREIGNISSE = {"vorgelegt", "go", "nogo", "versand", "eingang", "nachfass", "einladung", "gespraech", "debrief",
              "absage", "rueckzug", "zweitpruefung", "nachtrag", "angebot"}

STELLEN_DIR = ROOT / "stellen"
EINGANG_DIR = ROOT / "eingang"
FALL_ROOTS = (STELLEN_DIR, EINGANG_DIR)

# Erlaubte Dateinamen in einem Fall-Ordner. Versandte Dateien (Anschreiben, CV) behalten ihren Namen.
FALL_DATEIEN = re.compile(
    r"^([a-z0-9][a-z0-9-]*--(anzeige|recherche|personen)--\d{4}-\d{2}-\d{2}\.(md|pdf)|bewertung\.md|journal\.md|"
    r"(absage|rueckmeldung|einladung|nachfass|offerte|quelle|gespraech|analyse)[_-].+|"
    r"Motivationsschreiben-.+|Portalantworten-.+|CV[-_ ].+|.*Anschreiben.*|anschreiben.*|cv.*\.pdf|"
    r"case/.*|archiv/.*)$", re.I)


def fall_ordner(fid):
    """Ordner eines Falls: eingang/<id>/ (offen) oder stellen/<id>/."""
    for r in FALL_ROOTS:
        if (r / str(fid)).is_dir():
            return r / str(fid)
    return STELLEN_DIR / str(fid)


def alle_fall_ordner():
    return sorted(p for r in FALL_ROOTS if r.exists() for p in r.iterdir() if p.is_dir() and not p.name.startswith("."))


def kerndateien(ordner, typ, endungen=("md",)):
    """Portable Kerndateien eines Typs (<id>--<typ>--JJJJ-MM-TT.<endung>); normalerweise genau eine."""
    out = []
    for endung in endungen:
        out.extend(ordner.glob(f"{ordner.name}--{typ}--????-??-??.{endung}"))
    return sorted(set(out))


def load():
    with open(DATA, encoding="utf-8") as f:
        return json.load(f)


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()


def ensure_ids(data):
    """Fehlende IDs deterministisch vergeben (Slug aus Firma + ersten Rollen-Woertern)."""
    apps = data["applications"]
    existing = {a["id"] for a in apps if a.get("id")}
    changed = False
    for a in apps:
        if a.get("id"):
            continue
        role_words = slugify(a.get("rolle") or "").split("-")[:4]
        base = "-".join([slugify(a["firma"])] + [w for w in role_words if w])[:60].rstrip("-")
        candidate, n = base, 2
        while candidate in existing:
            candidate, n = f"{base}-{n}", n + 1
        a_new = {"id": candidate}
        a_new.update(a)
        a.clear()
        a.update(a_new)
        existing.add(candidate)
        changed = True
    return changed


def cell(v):
    if not v:
        return "—"
    return str(v).replace("|", "\\|").replace("\n", " ").strip()


def gen_applications(data):
    apps = data["applications"]
    schema = data.get("status_schema", {})
    L = ["# Bewerbungs-Tracker", "",
         f"**Stand:** {TODAY.isoformat()} · **generiert aus `data/pipeline.json`** — nicht von Hand editieren "
         "(Änderungen dort vornehmen, dann `python3 scripts/jobcoach.py`).", ""]
    if schema:
        L += ["**Status-Schema:**", ""] + [f"- {EMOJI.get(k, k)} — {v}" for k, v in schema.items()] + [""]
    L += ["---", ""]
    vorgelegt = [a for a in apps if a["status"] == "vorgelegt"]
    if vorgelegt:
        L += ["## Vorgelegt — Entscheid offen", "", "| Firma | Rolle | Datum | Herkunft / Empfehlung |", "|---|---|---|---|"]
        for a in sorted(vorgelegt, key=lambda x: x.get("datum") or "", reverse=True):
            L.append(f"| **{cell(a['firma'])}** | {cell(a.get('rolle'))} | {cell(a.get('datum'))} | {cell(a.get('notiz'))} |")
        L.append("")
    L += ["## Aktive Pipeline", "", "| Firma | Rolle | Status | Eingereicht | Verlauf / Anmerkung |", "|---|---|---|---|---|"]
    for a in apps:
        if a["status"] in ACTIVE:
            L.append(f"| **{cell(a['firma'])}** | {cell(a.get('rolle'))} | {EMOJI.get(a['status'], a['status'])} | "
                     f"{cell(a.get('datum_eingereicht'))} | {cell(a.get('notiz'))} |")
    L += ["", "## Aussortiert (Pre-Screen NoGo)", "", "| Firma | Rolle | Datum | Begründung |", "|---|---|---|---|"]
    for a in apps:
        if a["status"] == "aussortiert":
            L.append(f"| **{cell(a['firma'])}** | {cell(a.get('rolle'))} | {cell(a.get('datum'))} | {cell(a.get('begruendung'))} |")
    L.append("")
    zurueck = [a for a in apps if a["status"] == "zurueckgezogen"]
    if zurueck:
        L += ["## Zurückgezogen", "", "| Firma | Rolle | Begründung |", "|---|---|---|"]
        L += [f"| **{cell(a['firma'])}** | {cell(a.get('rolle'))} | {cell(a.get('begruendung'))} |" for a in zurueck]
        L.append("")
    L += ["## Archiv (abgesagt)", "", "| Firma | Rolle | Bewerbung | Absage | Stadium | Begründung |", "|---|---|---|---|---|---|"]
    for a in apps:
        if a["status"] == "abgesagt":
            L.append(f"| **{cell(a['firma'])}** | {cell(a.get('rolle'))} | {cell(a.get('datum_eingereicht'))} | "
                     f"{cell(a.get('absage_datum'))} | {cell(a.get('stadium'))} | {cell(a.get('begruendung'))} |")
    L.append("")
    if NARRATIVE.exists():
        L += [NARRATIVE.read_text(encoding="utf-8").rstrip(), ""]
    VIEWS.mkdir(exist_ok=True)
    APPS_MD.write_text("\n".join(L), encoding="utf-8")
    return {"aktiv": sum(1 for a in apps if a["status"] in ACTIVE),
            "aussortiert": sum(1 for a in apps if a["status"] == "aussortiert"),
            "abgesagt": sum(1 for a in apps if a["status"] == "abgesagt")}


def stale(data):
    out = []
    for a in data["applications"]:
        if a.get("status") not in ("abgeschickt", "in_pruefung"):
            continue
        d = a.get("datum_eingereicht") or a.get("datum_cv_tailor")
        if not d or len(d) != 10:
            continue
        days = (TODAY - datetime.date.fromisoformat(d)).days
        if days >= STALE_DAYS:
            out.append((days, a["firma"]))
    return sorted(out, reverse=True)


def check_schema(data):
    """Feld-Kontrakt: unbekannte Felder (Tippfehler-Drift) und fehlende Pflichtfelder pro Status."""
    out = []
    for a in data["applications"]:
        wer = f"{a.get('firma', '?')} ({a.get('id', '?')})"
        unknown = set(a) - KNOWN_FIELDS
        if unknown:
            out.append(f"SCHEMA: unbekannte Felder {sorted(unknown)} bei {wer} — Tippfehler oder KNOWN_FIELDS ergänzen.")
        if a.get("status") not in EMOJI:
            out.append(f"SCHEMA: unbekannter Status '{a.get('status')}' bei {wer}.")
        for f in REQUIRED_BY_STATUS.get(a.get("status"), ()):
            if not a.get(f):
                out.append(f"SCHEMA: Pflichtfeld '{f}' fehlt bei {wer} (Status '{a.get('status')}').")
    return out


def check_datenlose_aktive(data):
    """Aktive Bewerbung ohne pruefbares Datum entgeht dem Stale-Waechter still."""
    out = []
    for a in data["applications"]:
        if a.get("status") in ("abgeschickt", "in_pruefung"):
            d = a.get("datum_eingereicht") or a.get("datum_cv_tailor")
            if not d or len(str(d)) != 10:
                out.append(f"AKTIV OHNE DATUM: {a['firma']} — Stale-Regel nicht prüfbar; Datum nachtragen oder als zurueckgezogen markieren.")
    return out


def check_exante(data):
    """Ex-ante-Protokoll (spec/PRESCREEN.md, Schritt 2): jede Bewerbung nach dem Go traegt fit_v2,
    ausgefuellt VOR dem Versand. Nur so laesst sich spaeter pruefen, ob das Raster etwas vorhersagt."""
    out = []
    for a in data["applications"]:
        if a.get("status") in ("aussortiert", "vorgelegt") or a.get("fit_v2"):
            continue
        zusatz = " (vor Versand ausfüllen)" if a.get("status") == "draft" else ""
        out.append(f"EX-ANTE FEHLT: {a['firma']} ({a.get('id')}) — fit_v2 nicht kodiert{zusatz} (spec/PRESCREEN.md, Schritt 2).")
    return out


def check_anzeigen(data):
    """Anzeige muss existieren und den portablen Namen im Fall-Ordner tragen, der dem Status entspricht:
    eingang/<id>/<id>--anzeige--<erfasst>.md bei vorgelegt und draft, sonst stellen/<id>/…"""
    out = []
    for a in data["applications"]:
        status, anzeige, fid = a.get("status"), a.get("anzeige"), a.get("id")
        if not anzeige:
            if status in ACTIVE:
                out.append(f"Anzeige-Pfad fehlt in pipeline.json: {a['firma']} ({fid or '?'})")
            continue
        if not (ROOT / anzeige).exists():
            treffer = kerndateien(fall_ordner(fid), "anzeige", ("md", "pdf"))
            out.append(f"Anzeige nicht gefunden: {anzeige} ({a['firma']})"
                       + (f" — Datei liegt in {treffer[0].relative_to(ROOT)}, Feld 'anzeige' nachführen." if treffer else ""))
            continue
        wurzel = "eingang" if status in OFFENE_ABLAGE else "stellen"
        if not re.fullmatch(rf"{wurzel}/{re.escape(str(fid))}/{re.escape(str(fid))}--anzeige--\d{{4}}-\d{{2}}-\d{{2}}\.(md|pdf)", anzeige):
            out.append(f"Anzeige braucht den portablen Namen {wurzel}/{fid}/{fid}--anzeige--<erfasst>.md "
                       f"(Status '{status}'): {anzeige} — `python3 scripts/status.py` verschiebt den Ordner.")
    return out


def check_anzeigen_waisen(data):
    """Jeder Fall-Ordner gehoert zu einem Datensatz, jede Datei darin folgt der Namenskonvention
    (formatunabhaengig: eine PDF zaehlt wie eine MD)."""
    out = []
    ids = {a.get("id") for a in data["applications"]}
    for d in alle_fall_ordner():
        if d.name not in ids:
            out.append(f"FALL-ORDNER OHNE DATENSATZ: {d.parent.name}/{d.name}/ — keine id dieses Namens.")
        for f in d.rglob("*"):
            if f.is_file() and not f.name.startswith(".") and not FALL_DATEIEN.match(str(f.relative_to(d))):
                out.append(f"Datei ausserhalb der Fall-Namenskonvention: {d.parent.name}/{d.name}/{f.relative_to(d)} "
                           "(erlaubt siehe FALL_DATEIEN in scripts/jobcoach.py).")
    return out


def check_publiziert(data):
    """Jede abgelegte Anzeige traegt im Kopf «**Publiziert:**» mit Datum, relativer Angabe oder «unbekannt»
    (Grundlage fuer das Anzeigen-Alter im Cockpit und fuer den Marktreport)."""
    out = []
    for a in data["applications"]:
        pfad = ROOT / a["anzeige"] if a.get("anzeige") else None
        if not pfad or not pfad.is_file() or pfad.suffix != ".md":
            continue  # check_anzeigen meldet fehlende Anzeigen
        if "**Publiziert:**" not in pfad.read_text(encoding="utf-8", errors="ignore")[:3000]:
            out.append(f"Anzeige ohne Pflichtfeld 'Publiziert': {a['anzeige']} ({a['firma']}).")
    return out


def check_eingang(data):
    """Im Eingang liegen nur Fall-Ordner mit Status vorgelegt oder draft. Lose Dateien hat Alex abgelegt (Absage,
    Einladung, neue Anzeige); der Pflegelauf sortiert sie ein. `scripts/status.py` verschiebt Ordner."""
    out = []
    if not EINGANG_DIR.exists():
        return out
    status_von = {a.get("id"): a.get("status") for a in data["applications"]}
    for f in sorted(EINGANG_DIR.iterdir()):
        if f.name.startswith(".") or f.name == "README.md":
            continue
        if not f.is_dir():
            out.append(f"EINGANG: lose Datei {f.relative_to(ROOT)} — in den passenden Fall-Ordner sortieren "
                       "(mit Datum benennen, Ereignis erfassen) oder als neue Anzeige prüfen.")
        elif status_von.get(f.name) not in OFFENE_ABLAGE:
            out.append(f"EINGANG: Ordner {f.name}/ gehört nicht in den Eingang (Status "
                       f"'{status_von.get(f.name, 'kein Datensatz')}') — nach stellen/{f.name}/ verschieben.")
    return out


def check_go_recherche():
    """Go ohne Firmen-Recherche — deterministisch ueber scripts/offene_auftraege.py."""
    try:
        import offene_auftraege
        return offene_auftraege.warnungen()
    except Exception as e:
        return [f"Prüfung Go ohne Recherche lief nicht: {e}"]


def check_go_ohne_recherche(data=None):
    """Gleiche Pruefung wie check_go_recherche (eine Quelle, keine doppelten Befunde)."""
    return check_go_recherche()


def check_volltext_ablage(data):
    """Jeder Volltext-NoGo im Sichtungs-Log braucht Anzeigendatei UND Datensatz. Anlass: geprueft und begruendet
    abgelehnt, danach nirgends abgelegt — die Zweitpruefung der Aussortierten fand die Faelle nicht mehr."""
    log = ROOT / "data" / "screening_log.json"
    if not log.exists():
        return []
    d = json.loads(log.read_text(encoding="utf-8"))

    def norm(x):
        t = (x or "").lower()
        for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("é", "e"), ("è", "e"), ("à", "a"), ("ç", "c")):
            t = t.replace(a, b)
        return t

    def woerter(x):
        return {w for w in re.findall(r"[a-z0-9]+", norm(x)) if len(w) > 2}

    pf = [(re.sub(r"[^a-z0-9]", "", norm(a.get("firma"))), re.sub(r"[^a-z0-9]", "", norm(a.get("rolle"))),
           woerter(a.get("rolle"))) for a in data["applications"]]
    ids = {a.get("id") for a in data["applications"]}
    fehlt = []
    for r in d.get("gesichtet", []):
        if r.get("entscheid") != "volltext-nogo" or r.get("erledigt"):
            continue
        if r.get("pipeline_id") in ids or (r.get("anzeige") and (ROOT / r["anzeige"]).is_file()):
            continue
        f, ro, rw = re.sub(r"[^a-z0-9]", "", norm(r.get("firma"))), re.sub(r"[^a-z0-9]", "", norm(r.get("rolle"))), woerter(r.get("rolle"))
        if not f:
            continue
        # Firma UND Rolle muessen passen: der reine Firmenvergleich hielt jede neue Stelle einer Firma fuer abgelegt
        if any(f[:12] in pfa or pfa[:12] in f for pfa, pro, prw in pf
               if (ro == pro or (rw and len(rw & prw) / len(rw | prw) >= 0.6))):
            continue
        fehlt.append(f"{r.get('firma')} — {r.get('rolle')} ({r.get('datum')})")
    if not fehlt:
        return []
    return ([f"VOLLTEXT OHNE ABLAGE: {len(fehlt)} im Volltext geprüfte NoGos haben keinen Datensatz in pipeline.json "
             "(und damit keine Anzeigendatei) — nachtragen:"]
            + ["    – " + x for x in fehlt[:12]] + ([f"    … und {len(fehlt) - 12} weitere"] if len(fehlt) > 12 else []))


def check_screening_log():
    """Das Sichtungs-Log ist die Grundlage des Delta-Laufs. Gemeldet: Tag mit Abfrage-Laeufen, aber ohne
    Sichtung (naechster Sweep startet im Vollscan); letzter Lauf > 3 Tage her; Sichtung ohne `gefunden_ueber`."""
    pfad = ROOT / "data" / "screening_log.json"
    if not pfad.exists():
        return ["Sichtungs-Log fehlt (data/screening_log.json) — der Delta-Lauf hat keine Grundlage."]
    d = json.loads(pfad.read_text(encoding="utf-8"))
    laeufe, gesichtet = d.get("laeufe", []), d.get("gesichtet", [])
    out = []
    tage_mit_sichtung = {e.get("datum") for e in gesichtet}
    for tag in sorted({l.get("datum") for l in laeufe} - tage_mit_sichtung):
        kanaele = sorted({l.get("kanal", "?") for l in laeufe if l.get("datum") == tag})
        out.append(f"Screening-Lauf am {tag} ohne eine einzige Sichtung im Log ({', '.join(kanaele)}) — "
                   "der nächste Lauf startet dort wieder im Vollscan.")
    if laeufe:
        letzter = max(l.get("datum", "") for l in laeufe)
        alter = (TODAY - datetime.date.fromisoformat(letzter)).days
        if alter > 3:
            out.append(f"Letzter Screening-Lauf ist {alter} Tage her ({letzter}) — der Morgen-Sweep läuft werktags, hier fehlt etwas.")
    ohne_begriff = [e for e in gesichtet if not e.get("gefunden_ueber")]
    if ohne_begriff:
        out.append(f"{len(ohne_begriff)} Sichtungen ohne Feld `gefunden_ueber` — ihr Abfrage-Ertrag ist nicht messbar.")
    return out


def check_screening_sweeps():
    """Jeder Sweep gegen den Soll-Katalog (spec/SWEEP.md). Gemeldet: gestern kein einziger Sweep (ein einzelner
    fehlender Sweep ist kein Befund, der naechste holt per Delta nach); Sweep von heute/gestern unvollstaendig
    ohne laufende Session; Notiz fehlt, ohne Pflichtsektion oder mit Platzhaltern; Laeufe/Sichtungen ohne Zuordnung."""
    try:
        import screening_sweep as _sw
    except Exception as e:
        return [f"screening_sweep.py nicht ladbar: {e}"]
    log = ROOT / "data" / "screening_log.json"
    if not log.exists() or not Path(_sw.KATALOG).exists():
        return ["Sweep-Prüfung: Log oder Katalog fehlt (data/screening_log.json, data/screening_kanaele.json)."]
    d = json.loads(log.read_text(encoding="utf-8"))
    _, aktive = _sw.katalog()
    out = []
    uhr = jetzt()
    gestern = (TODAY - datetime.timedelta(days=1)).isoformat()
    if not any(x.get("datum") == gestern for x in d.get("sweeps", [])):
        out.append(f"KEIN SWEEP GESTERN ({gestern}): den ganzen Tag kein Durchgang — Task prüfen, falls der Rechner lief.")
    for delta in (1, 0):
        tag = (TODAY - datetime.timedelta(days=delta)).isoformat()
        for art, faellig_ab in (("morgen", 12), ("mittag", 15), ("nachmittag", 19)):
            if delta == 0 and uhr.hour < faellig_ab:
                continue  # heute noch nicht faellig
            sid = f"{tag}-{art}"
            s = next((x for x in d.get("sweeps", []) if x.get("id") == sid), None)
            if not s:
                continue
            erl, feh = _sw.soll_ist(d, s, aktive)
            soll = len(erl) + len(feh)
            laeuft = s.get("sessions") and s["sessions"][-1].get("ende") is None
            if s.get("status") != "abgeschlossen" and not laeuft:
                out.append(f"SWEEP UNVOLLSTÄNDIG: {sid} — {len(erl)}/{soll} Abfragen "
                           f"({round(100 * len(erl) / soll) if soll else 0} %), Status {s.get('status')}, {len(feh)} fehlend "
                           f"(z.B. {', '.join(a['id'] for a in feh[:5])}). Der nächste Sweep holt nach.")
            notiz = ROOT / "notes" / f"{tag}_screening_{art}.md"
            if s.get("status") in ("abgeschlossen", "abgebrochen"):
                if not notiz.exists():
                    out.append(f"NOTIZ FEHLT: notes/{notiz.name} — Sweep {sid} ist {s['status']}, aber ohne Protokoll.")
                else:
                    txt = notiz.read_text(encoding="utf-8")
                    fehlend = [p for p in _sw.PFLICHTSEKTIONEN if p not in txt]
                    platz = [p for p in _sw.PLATZHALTER if p in txt]
                    if fehlend:
                        out.append(f"NOTIZ UNVOLLSTÄNDIG: notes/{notiz.name} ohne Sektion(en) {', '.join(fehlend)}.")
                    if platz:
                        out.append(f"NOTIZ MIT SKELETT-PLATZHALTERN: notes/{notiz.name} enthält noch {len(platz)} "
                                   f"unausgefüllte Stelle(n) ({platz[0][:40]}…).")
    ohne = [l for l in d.get("laeufe", []) if not l.get("abfrage_id") and l.get("kanal") != "manuell"
            and not (l.get("abfrage") or "").startswith("adhoc:")]
    if ohne:
        out.append(f"{len(ohne)} Abfrage-Läufe ohne Katalog-ID — sie zählen nicht zur Abdeckung.")
    ohne_s = [e for e in d.get("gesichtet", []) if not e.get("lauf_id")]
    if ohne_s:
        out.append(f"{len(ohne_s)} Sichtungen ohne Sweep-Zuordnung — ohne offenen Sweep eingetragen.")
    return out


def check_verlauf(data):
    """Verlauf je Fall (die Spur, was wann geschah): Status ohne passendes Ereignis, Absage-Datei ohne Ereignis
    und umgekehrt, vergangenes Gespraech ohne Debrief-Datei, unbekannte Ereignisse."""
    out = []
    erwartet = {"aussortiert": "nogo", "zurueckgezogen": "rueckzug", "abgesagt": "absage"}
    for a in data["applications"]:
        st, vl, fid = a.get("status"), a.get("verlauf") or [], a.get("id")
        arten = {e.get("ereignis") for e in vl}
        ordner = fall_ordner(fid)
        if st in ("abgeschickt", "in_pruefung", "gespraech", "angebot", "abgesagt") and "versand" not in arten:
            out.append(f"VERLAUF: {fid} ist '{st}', aber ohne Ereignis 'versand'. "
                       f"`python3 scripts/ereignis.py {fid} versand --datum <JJJJ-MM-TT> --quelle <Datei>`.")
        if st in erwartet and erwartet[st] not in arten:
            out.append(f"VERLAUF: {fid} ist '{st}', aber ohne Ereignis '{erwartet[st]}'.")
        if ordner.exists():
            absage_dateien = list(ordner.glob("absage_*.md"))
            if "absage" in arten and not absage_dateien:
                vakanz = [b for b in ordner.glob("rueckmeldung_*.md")
                          if re.search(r"nicht besetzt|vakanz", b.read_text(encoding="utf-8", errors="ignore"), re.I)]
                if not vakanz:
                    out.append(f"VERLAUF: {fid} hat Ereignis 'absage', aber keine absage_<datum>.md im Fall-Ordner.")
            if absage_dateien and "absage" not in arten:
                out.append(f"VERLAUF: {ordner.relative_to(ROOT)}/ enthält eine Absage-Datei, aber kein Ereignis 'absage' (Status '{st}').")
            # Vorbereitet, aber nie gefuehrt: Ereignis 'nachtrag' am Gespraechsdatum mit Notiz «kein Gespraech …»
            entfallen = {e.get("datum") for e in vl if e.get("ereignis") == "nachtrag"
                         and (e.get("notiz") or "").lower().replace("ä", "ae").startswith("kein gespraech")}
            for g in ordner.glob("gespraech_*_vorbereitung.md"):
                m = re.search(r"gespraech_(\d{4}-\d{2}-\d{2})_(.+?)_vorbereitung", g.name)
                if not m or m.group(1) in entfallen:
                    continue
                if datetime.date.fromisoformat(m.group(1)) < TODAY and not list(ordner.glob(f"gespraech_{m.group(1)}_*debrief.md")):
                    out.append(f"VERLAUF: {fid} — Gespräch {m.group(1)} ({m.group(2)}) vergangen, kein Debrief im Fall-Ordner.")
        for e in vl:
            if e.get("ereignis") not in EREIGNISSE:
                out.append(f"VERLAUF: {fid} — unbekanntes Ereignis '{e.get('ereignis')}'.")
    return out


def check_debriefs(data):
    """Status 'gespraech' mit vergangenem Termin braucht eine verlinkte Debrief-Notiz (Feld `debrief`)."""
    out = []
    for a in data["applications"]:
        if a.get("status") != "gespraech":
            continue
        t = a.get("gespraech_termin")
        if not t or len(t) != 10:
            out.append(f"Gespräch ohne Termin-Feld (gespraech_termin): {a['firma']}")
            continue
        if datetime.date.fromisoformat(t) <= TODAY:
            d = a.get("debrief")
            if not d:
                out.append(f"DEBRIEF OFFEN: {a['firma']} ({a.get('id')}) — Gespräch am {t}, keine Debrief-Notiz verlinkt.")
            elif not (ROOT / d).exists():
                out.append(f"Debrief-Pfad existiert nicht: {d} ({a['firma']})")
    return out


def check_konsistenz(data):
    """Querverweise Datei <-> Datensatz, schlank: doppelte id, aktiver Fall doppelt (gleiche Firma + Rolle),
    Absage-Datei im Fall-Ordner bei anderem Status, Eingangsbestaetigung im Ordner bei Status 'abgeschickt'.
    Anlass: Rueckmeldungen lagen im Ordner, der Status wurde nie nachgefuehrt."""
    out = []
    apps = data["applications"]
    for i, n in collections.Counter(a.get("id") for a in apps).items():
        if n > 1:
            out.append(f"DOPPELTE ID: '{i}' kommt {n}x in pipeline.json vor — zusammenführen, nie beide stehen lassen.")

    def nk(a):
        f, r = (re.sub(r"[^a-z0-9]", "", slugify(a.get(k) or "")) for k in ("firma", "rolle"))
        return f[:8] + "|" + r

    gruppen = collections.defaultdict(list)
    for a in apps:
        if a.get("status") in ACTIVE:
            gruppen[nk(a)].append(a.get("id"))
    for v in gruppen.values():
        if len(v) > 1:
            out.append(f"DOPPELTER AKTIVER FALL: {', '.join(v)} — gleiche Firma und Rolle, beide aktiv.")
    for a in apps:
        d, st = fall_ordner(a.get("id")), a.get("status")
        if not d.is_dir():
            continue
        if st != "abgesagt" and list(d.glob("absage_*.md")):
            out.append(f"ABSAGE OHNE STATUS: {a.get('id')} — Absage liegt in {d.relative_to(ROOT)}/, Status ist '{st}'.")
        if st == "abgeschickt":
            for p in d.glob("rueckmeldung_*.md"):
                if re.search(r"Eingangsbest|Zwischenbescheid", p.read_text(encoding="utf-8", errors="ignore")[:600]):
                    out.append(f"STATUS VERALTET: {a.get('id')} ist 'abgeschickt', aber {p.relative_to(ROOT)} "
                               "belegt eine Bestätigung der Firma → 'in_pruefung'.")
                    break
    return out


def check_umbau():
    """Wirkungskontrolle des Sweep-Umbaus (scripts/umbau_kontrolle.py): Kandidaten duerfen nicht einbrechen."""
    try:
        import umbau_kontrolle
        return umbau_kontrolle.warnungen()
    except Exception as e:
        return [f"Wirkungskontrolle Umbau lief nicht: {e}"]


def funnel(data):
    """Funnel: 'Gespraech erreicht' = gespraech/angebot oder Absage mit Gespraechs-Stadium ('Pre-Shortlist'/'Dossier'
    = keine Konversion). Absagen ohne stadium werden als 'Stadium unbekannt' ausgewiesen."""
    apps = data["applications"]
    submitted = [a for a in apps if a["status"] not in ("aussortiert", "draft", "vorgelegt", "zurueckgezogen")
                 or (a["status"] == "zurueckgezogen" and a.get("datum_eingereicht"))]
    gespraech, unknown = [], []
    for a in submitted:
        if a["status"] in ("gespraech", "angebot"):
            gespraech.append(a["firma"])
        elif a["status"] == "abgesagt":
            st = (a.get("stadium") or "").lower()
            if not st:
                unknown.append(a["firma"])
            elif st.startswith("pre-shortlist") or "kein gespräch" in st or "dossier" in st:
                pass
            elif any(k in st for k in ("gespräch", "runde")):
                gespraech.append(a["firma"])
    angebote = [a["firma"] for a in apps if a["status"] == "angebot"]
    return len(submitted), gespraech, angebote, unknown


def gen_status(data, warnings, st):
    """Session-Einstieg STATUS.md (Cockpit, Zahlen, Gespraeche, Befunde kurz) und WARNINGS.md (vollstaendig)."""
    apps = data["applications"]
    by = {}
    for a in apps:
        by.setdefault(a["status"], []).append(a)
    n_sub, gespraech, angebote, unknown = funnel(data)
    L = ["# STATUS — Kurz-Snapshot für den Session-Einstieg", "",
         f"**Stand:** {TODAY.isoformat()} · generiert aus `data/pipeline.json` (`python3 scripts/jobcoach.py`) — "
         "nicht von Hand editieren. Voll-Tracker: `APPLICATIONS.md`.", ""]
    try:
        import cockpit
        L += [cockpit.block(), ""]
    except Exception as e:
        L += ["## Bei dir liegt", "", f"(Cockpit nicht erzeugbar: {e})", ""]
    L += ["## Zahlen", "",
          f"- Aktiv: **{sum(len(by.get(s, [])) for s in ACTIVE)}** ("
          + " · ".join(f"{EMOJI[s]} {len(by[s])}" for s in ("draft", "abgeschickt", "in_pruefung", "gespraech", "angebot") if by.get(s)) + ")",
          f"- Vorgelegt, Entscheid offen: **{len(by.get('vorgelegt', []))}** · vollständige Liste in `APPLICATIONS.md`",
          f"- Aussortiert: {len(by.get('aussortiert', []))} · Abgesagt: {len(by.get('abgesagt', []))} · "
          f"Zurückgezogen: {len(by.get('zurueckgezogen', []))}",
          f"- **Funnel:** {n_sub} eingereicht → {len(gespraech)} Gespräch erreicht → {len(angebote)} Angebot(e)"
          + (f" · Stadium unbekannt: {', '.join(unknown)}" if unknown else ""), ""]
    laufend = by.get("gespraech", []) + by.get("angebot", [])
    if laufend:
        L += ["## Laufende Gespräche", ""]
        for a in laufend:
            L.append(f"- **{a['firma']}** — {a.get('rolle')} · {EMOJI[a['status']]} · Termin: {a.get('gespraech_termin') or 'offen'} · "
                     f"Debrief: {a.get('debrief') or '**offen**'}")
        L.append("")
    pflege = list(warnings)
    if st:
        pflege.append("Stale (>%dd ohne Rückmeldung): " % STALE_DAYS + "; ".join(f"{f} ({d}d)" for d, f in st))
    W = ["# WARNINGS — vollständige Pflege-Wächter-Befunde", "",
         f"**Stand:** {TODAY.isoformat()} · generiert mit `python3 scripts/jobcoach.py` — nicht von Hand editieren.", ""]
    if pflege:
        W += [f"    - {w.strip().lstrip('–').strip()}" if w.startswith(" ") else f"- ⚠ {w}" for w in pflege]
    else:
        W.append("- keine Befunde")
    W.append("")
    WARNINGS_MD.write_text("\n".join(W), encoding="utf-8")
    L += ["## Wächter-Befunde", ""]
    haupt = [w for w in pflege if not w.startswith(" ")]
    if haupt:
        L.append(f"- ⚠ **{len(haupt)} Befundgruppen** · vollständig in `WARNINGS.md`")
        L += [f"- {w}" for w in haupt[:5]]
        if len(haupt) > 5:
            L.append(f"- … {len(haupt) - 5} weitere Befundgruppen in `WARNINGS.md`")
    else:
        L.append("- keine Befunde")
    L.append("")
    STATUS_MD.write_text("\n".join(L), encoding="utf-8")


def main():
    data = load()
    if any(not a.get("id") for a in data.get("applications", [])):
        from pipeline_tx import Konflikt, transaktion
        try:
            with transaktion("jobcoach.py: fehlende IDs vergeben") as current:
                changed = ensure_ids(current)
            data = current
        except Konflikt as exc:
            raise SystemExit(f"KONFLIKT: {exc}")
        if changed:
            print("pipeline.json: fehlende IDs transaktional vergeben und zurückgeschrieben.")
    counts = gen_applications(data)
    print(f"APPLICATIONS.md generiert: {counts['aktiv']} aktiv, {counts['aussortiert']} aussortiert, {counts['abgesagt']} abgesagt.")
    st = stale(data)
    print(("Stale (>%dd): " % STALE_DAYS + "; ".join(f"{f} ({d}d)" for d, f in st)) if st
          else f"Keine stale Bewerbungen (>{STALE_DAYS} Tage).")
    warnings = (check_schema(data) + check_exante(data) + check_datenlose_aktive(data)
                + check_anzeigen(data) + check_anzeigen_waisen(data) + check_publiziert(data) + check_eingang(data)
                + check_go_recherche() + check_volltext_ablage(data) + check_screening_log() + check_screening_sweeps()
                + check_verlauf(data) + check_debriefs(data) + check_konsistenz(data) + check_umbau())
    gen_status(data, warnings, st)
    print("STATUS.md und WARNINGS.md generiert (Kurz-Snapshot + vollständige Wächterdetails).")
    if warnings:
        print("\nPflege-Wächter:")
        for w in warnings:
            print(f"  ⚠ {w}")
    else:
        print("Pflege-Wächter: keine Befunde.")


if __name__ == "__main__":
    main()
