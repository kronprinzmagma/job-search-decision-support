"""Tests der Gruppe Screening: Sweep-Mechanik, Sichtungs-Log, Publiziert-Datum, Vorscan."""
import json
import sys
from datetime import date
from pathlib import Path

from conftest import REPO, run

sys.path.insert(0, str(REPO / "scripts"))
import publiziert  # noqa: E402
import screening_sweep as sw  # noqa: E402
import vorscan_regeln as vr  # noqa: E402

MORGEN = "2025-04-26T08:05:00"


def _log(demo):
    return json.loads((demo / "data" / "screening_log.json").read_text(encoding="utf-8"))


def _audit(demo):
    return json.loads((demo / "data" / "lauf_audit.json").read_text(encoding="utf-8"))


def _katalog(demo):
    return json.loads((demo / "data" / "screening_kanaele.json").read_text(encoding="utf-8"))


# --- soll_ist / Abdeckung ------------------------------------------------------------------------

AKTIVE = [{"id": "pt-a", "kanal": "portal"}, {"id": "ns-a", "kanal": "netzwerk-suche"},
          {"id": "zp-a", "kanal": "zielportal"}]


def _lauf(aid, status, notiz="", sid="S"):
    return {"lauf_id": sid, "abfrage_id": aid, "status": status, "notiz": notiz}


def test_soll_ist_abdeckung_und_tageszeit():
    d = {"laeufe": [_lauf("pt-a", "ok"), _lauf("ns-a", "nicht-erreichbar", "JS-Geruest"),
                    _lauf("zp-a", "uebersprungen"), _lauf("ns-a", "ok", sid="ANDERER")]}
    erledigt, fehlend = sw.soll_ist(d, {"id": "S", "art": "morgen"}, AKTIVE)
    assert set(erledigt) == {"pt-a", "ns-a"}
    assert [a["id"] for a in fehlend] == ["zp-a"]           # uebersprungen zaehlt nicht
    # Mittag ohne Ziel-/Behoerdenportale: dasselbe Log ist dort vollstaendig
    _, fehlend = sw.soll_ist(d, {"id": "S", "art": "mittag"}, AKTIVE)
    assert fehlend == []
    # nach abgebrochenem Morgen-Sweep holt der Mittag die Portale nach
    _, fehlend = sw.soll_ist(d, {"id": "S", "art": "mittag", "mit_portalen": True}, AKTIVE)
    assert [a["id"] for a in fehlend] == ["zp-a"]


def test_teilweise_zaehlt_nur_mit_technik():
    s = {"id": "S", "art": "mittag"}
    ohne = {"laeufe": [_lauf("pt-a", "teilweise", "nur Seite 1 gelesen"), _lauf("ns-a", "ok")]}
    assert [a["id"] for a in sw.soll_ist(ohne, s, AKTIVE)[1]] == ["pt-a"]
    mit = {"laeufe": [_lauf("pt-a", "teilweise", "TECHNIK: Seite 3 liefert Fehler 502"), _lauf("ns-a", "ok")]}
    assert sw.soll_ist(mit, s, AKTIVE)[1] == []
    # ein spaeterer Eintrag ohne TECHNIK ersetzt den frueheren ok-Eintrag
    spaeter = {"laeufe": [_lauf("pt-a", "ok"), _lauf("pt-a", "teilweise", "abgekuerzt"), _lauf("ns-a", "ok")]}
    assert [a["id"] for a in sw.soll_ist(spaeter, s, AKTIVE)[1]] == ["pt-a"]


def test_aktive_am_neue_abfrage_zaehlt_nicht_rueckwirkend():
    d = {"laeufe": [{"abfrage_id": "pt-a", "datum": "2025-04-01"}, {"abfrage_id": "ns-a", "datum": "2025-04-10"}]}
    soll = sw.aktive_am(d, {"id": "S", "datum": "2025-04-05", "art": "morgen"}, AKTIVE)
    assert [a["id"] for a in soll] == ["pt-a", "zp-a"]       # ns-a erst ab 04-10, zp-a nie abgefragt = faellig


def test_audit_alle_sweeps_der_demo(demo):
    r = run(demo, "screening_log.py", "audit", "--aktualisieren", "--alle")
    assert r.returncode == 0, r.stdout + r.stderr
    sweeps = _log(demo)["sweeps"]
    audit = _audit(demo)
    assert len(audit) == len(sweeps)
    for rec in audit:
        assert rec["soll"] == (28 if rec["art"] == "morgen" else 18)
        assert rec["ist"] <= rec["soll"]
        if rec["status"] == "abgeschlossen":
            assert rec["abdeckung"] == 1.0 and rec["fehlend"] == [], rec
            assert rec["format_ok"] is True, rec          # Demo-Notizen haben alle Pflichtsektionen
        else:
            assert rec["abdeckung"] < 1.0 and rec["fehlend"]
    assert [r["sweep"] for r in audit[:3]] == ["2025-03-03-morgen", "2025-03-03-nachmittag", "2025-03-04-morgen"]


# --- CLI im Demo-Stand ---------------------------------------------------------------------------

def test_cli_im_demo_stand(demo):
    r = run(demo, "screening_log.py", "sweeps")
    assert r.returncode == 0 and "| 2025-04-25-morgen | abgeschlossen | 1 | 28/28 | 100 % |" in r.stdout
    r = run(demo, "screening_log.py", "bericht", "2025-04-25-mittag")
    assert r.returncode == 0
    assert all(p in r.stdout for p in sw.PFLICHTSEKTIONEN)
    assert "alle 18 Abfragen" in r.stdout                      # Soll des Mittags ohne Portale
    r = run(demo, "screening_log.py", "status")
    assert r.returncode == 0 and "nachmittag  abgeschlossen   18/18" in r.stdout
    r = run(demo, "screening_log.py", "delta", "--tage", "1")
    assert r.returncode == 0 and "Anzeigen seit 2025-04-24" in r.stdout
    r = run(demo, "screening_log.py", "ertrag")
    assert r.returncode == 0 and "ERTRAG JE ABFRAGE" in r.stdout


def test_check_bekannt_pruefen_neu(demo):
    e = next(x for x in _log(demo)["gesichtet"] if x["entscheid"] == "kandidat")
    r = run(demo, "screening_log.py", "check", f"{e['firma']}|{e['rolle']}")
    assert r.returncode == 1 and r.stdout.startswith("BEKANNT")
    r = run(demo, "screening_log.py", "check", f"{e['firma']}|Chief Happiness Officer")
    assert r.returncode == 0 and r.stdout.startswith("NEU") and "gleiche Firma, andere Rolle" in r.stdout
    r = run(demo, "screening_log.py", "check", "Unbekannte Firma AG|Product Owner")
    assert r.returncode == 0 and r.stdout.strip() == "NEU        | Unbekannte Firma AG | Product Owner"


# --- Sweep-Regeln ---------------------------------------------------------------------------------

def test_parallele_session_ohne_ende_blockiert_neustart(demo):
    assert run(demo, "screening_log.py", "start", "morgen", jetzt=MORGEN).returncode == 0
    r = run(demo, "screening_log.py", "start", "morgen", jetzt="2025-04-26T08:30:00")
    assert r.returncode == 4 and "Session ohne 'ende'" in r.stdout
    assert len(_log(demo)["sweeps"][-1]["sessions"]) == 1
    # nach der Schwelle gilt die Session als verwaist: Fortsetzen erlaubt
    r = run(demo, "screening_log.py", "start", "morgen", jetzt="2025-04-26T09:10:00")
    assert r.returncode == 0 and "SWEEP FORTSETZEN" in r.stdout


def test_ok_mit_wenig_sichtungen_wird_abgewiesen(demo):
    run(demo, "screening_log.py", "start", "morgen", jetzt=MORGEN)
    r = run(demo, "screening_log.py", "abfrage", "ns-zh-a|ok|2|", jetzt=MORGEN)
    assert r.returncode == 1 and "ueblich ~" in r.stdout and "BESTAND KLEINER" in r.stdout
    assert not [l for l in _log(demo)["laeufe"] if l["lauf_id"] == "2025-04-26-morgen"]
    r = run(demo, "screening_log.py", "abfrage", "ns-zh-a|ok|2|BESTAND KLEINER: Seite zeigt 2 Treffer", jetzt=MORGEN)
    assert r.returncode == 0 and "1/28 abgedeckt" in r.stdout
    # «teilweise» ohne TECHNIK: wird geloggt, zaehlt aber nicht
    r = run(demo, "screening_log.py", "abfrage", "ns-zh-b|teilweise|9|Seite 2 ausgelassen", jetzt=MORGEN)
    assert r.returncode == 0 and "zaehlt nicht als abgedeckt" in r.stdout and "1/28 abgedeckt" in r.stdout


def test_add_volltext_fall_braucht_abgelegte_anzeige(demo):
    run(demo, "screening_log.py", "start", "morgen", jetzt=MORGEN)
    zeile = "Mirvel Medien AG|Head of Product Leserplattform|Zürich|netzwerk-suche|kandidat|Volltext geprueft|ns-zh-a|Gestern"
    r = run(demo, "screening_log.py", "add", zeile, jetzt=MORGEN)
    assert "ABGELEHNT (Ablage)" in r.stdout
    fid = "mirvel-medien-head-of-product-leserplattform"
    pfad = f"eingang/{fid}/{fid}--anzeige--2025-04-26.md"
    (demo / pfad).parent.mkdir(parents=True)
    (demo / pfad).write_text("# Head of Product\n\n**Publiziert:** Gestern (Abruf 2025-04-26)\n", encoding="utf-8")
    r = run(demo, "screening_log.py", "add", f"{zeile}|{pfad}", jetzt=MORGEN)
    assert f"Datensatz {fid} angelegt (vorgelegt)" in r.stdout
    e = _log(demo)["gesichtet"][-1]
    assert (e["entscheid"], e["publiziert"], e["lauf_id"], e["anzeige"]) == ("kandidat", "2025-04-25", "2025-04-26-morgen", pfad)
    apps = json.loads((demo / "data" / "pipeline.json").read_text(encoding="utf-8"))["applications"]
    assert next(a for a in apps if a["id"] == fid)["status"] == "vorgelegt"
    r = run(demo, "screening_log.py", "add", "Firma AG|12 weitere Stellen|Zürich|portal|vorfilter|Junior", jetzt=MORGEN)
    assert "ABGELEHNT (Sammelzeile)" in r.stdout


# --- kompletter Sweep am Folgetag -----------------------------------------------------------------

def test_kompletter_sweep_am_folgetag(demo):
    # Fixture-Kanal um zwei Neuzugaenge ergaenzen: einer faellt per Regel weg, einer ist unklar
    stand_p = demo / "data" / "vorscan" / "stand.json"
    stand = json.loads(stand_p.read_text(encoding="utf-8"))
    q = stand["abfragen"]["pt-a-product-owner"]
    for i, (firma, rolle, ort) in enumerate([("Spielora Gaming AG", "Product Owner Casino-App", "Zürich"),
                                             ("Cirrova Cloud AG", "Product Owner Entwicklerplattform", "Schlieren")]):
        q["eintraege"].append({"id": f"pt-a-product-owner-9{i}", "firma": firma, "rolle": rolle, "ort": ort,
                               "publiziert": "2025-04-26", "url": f"https://jobs.example.org/x/9{i}"})
    q["treffer"] = len(q["eintraege"])
    stand_p.write_text(json.dumps(stand, ensure_ascii=False), encoding="utf-8")
    vorher = len(_log(demo)["gesichtet"])

    r = run(demo, "screening_log.py", "start", "morgen", "--modell", "sonnet", jetzt=MORGEN)
    assert r.returncode == 0 and "SWEEP NEU       2025-04-26-morgen — Soll: 28" in r.stdout
    r = run(demo, "vorscan.py", "uebernehmen", jetzt="2025-04-26T08:06:00")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "12 Abfragen abgedeckt" in r.stdout
    unklar = r.stdout.split("UNKLAR", 1)[1]
    assert "Cirrova Cloud AG|Product Owner Entwicklerplattform|Schlieren|pt-a-product-owner" in unklar
    assert "Spielora Gaming AG" not in unklar
    d = _log(demo)
    neu = [e for e in d["gesichtet"][vorher:] if e["lauf_id"] == "2025-04-26-morgen"]
    assert all(e["entscheid"] == "vorfilter" and e["grund"].endswith("(Vorscan-Regel)") for e in neu)
    spielora = next(e for e in neu if e["firma"] == "Spielora Gaming AG")
    assert spielora["grund"].startswith("Firmen-Ausschluss") and spielora["kanal"] == "portal"
    assert not any(e["firma"] == "Cirrova Cloud AG" and e["rolle"].endswith("Entwicklerplattform") for e in neu)
    portal = [l for l in d["laeufe"] if l["lauf_id"] == "2025-04-26-morgen"]
    assert len(portal) == 12 and all(l["notiz"].startswith("BESTAND KLEINER:") for l in portal)
    # Unklare entscheidet das Modell; hier: Volltext ausstehend
    r = run(demo, "screening_log.py", "add",
            "Cirrova Cloud AG|Product Owner Entwicklerplattform|Schlieren|portal|offen|Volltext ausstehend|pt-a-product-owner|2025-04-26",
            jetzt="2025-04-26T08:10:00")
    assert r.returncode == 0
    # restliche Abfragen; Vorscan-Abfragen sind schon abgedeckt
    r = run(demo, "screening_log.py", "naechste", "--alle", jetzt="2025-04-26T08:11:00")
    offen = [z for z in r.stdout.splitlines() if z and not z.startswith((" ", "#", ".", "Loggen"))]
    rest = [a["id"] for a in _katalog(demo)["abfragen"] if a.get("aktiv") and a["kanal"] != "portal"]
    assert offen == rest and len(rest) == 16
    r = run(demo, "screening_log.py", "abfrage", *[f"{aid}|ok|25|Liste vollstaendig gelesen" for aid in rest],
            jetzt="2025-04-26T08:30:00")
    assert r.returncode == 0 and "28/28 abgedeckt, 0 offen" in r.stdout
    r = run(demo, "screening_log.py", "ende", jetzt="2025-04-26T08:35:00")
    assert r.returncode == 0 and "SWEEP ABGESCHLOSSEN 2025-04-26-morgen" in r.stdout
    rec = _audit(demo)[-1]
    assert rec["sweep"] == "2025-04-26-morgen" and rec["status"] == "abgeschlossen"
    assert (rec["soll"], rec["ist"], rec["abdeckung"], rec["dauer_min"], rec["offen"]) == (28, 28, 1.0, 30, 1)
    assert run(demo, "screening_log.py", "start", "morgen", jetzt="2025-04-26T09:00:00").returncode == 3
    r = run(demo, "screening_log.py", "bericht", "--schreiben", jetzt="2025-04-26T08:36:00")
    assert r.returncode == 0
    notiz = (demo / "notes" / "2025-04-26_screening_morgen.md").read_text(encoding="utf-8")
    assert sw.GEN_START in notiz and "Cirrova Cloud AG — Product Owner Entwicklerplattform (portal, seit 2025-04-26)" in notiz


def test_vorscan_veraltet_und_fehlend(demo):
    run(demo, "screening_log.py", "start", "mittag", jetzt="2025-04-26T12:00:00")
    r = run(demo, "vorscan.py", "uebernehmen", "--probe", jetzt="2025-04-26T12:01:00")
    assert r.returncode == 4 and "VERALTET" in r.stdout
    r = run(demo, "vorscan.py", "uebernehmen", jetzt="2025-04-26T12:01:00")
    assert r.returncode == 0 and "12 Abfragen als nicht erreichbar geloggt" in r.stdout
    laeufe = [l for l in _log(demo)["laeufe"] if l["lauf_id"] == "2025-04-26-mittag"]
    assert len(laeufe) == 12 and all(l["status"] == "nicht-erreichbar" and l["notiz"].startswith("TECHNIK:") for l in laeufe)
    (demo / "data" / "vorscan" / "stand.json").unlink()
    assert run(demo, "vorscan.py", "uebernehmen", jetzt="2025-04-26T12:02:00").returncode == 4


# --- Vorscan-Regeln -------------------------------------------------------------------------------

def test_vorscan_pruefen_findet_keine_falsch_vorgefilterten(demo):
    r = run(demo, "vorscan.py", "pruefen")
    assert r.returncode == 0, r.stdout
    assert "Faelschlich vorgefiltert (Kandidat/Volltext/offen, ohne Firmen-Ausschluss): 0" in r.stdout
    gefangen = int(r.stdout.split("abgefangen: ")[1].split(" ")[0])
    assert gefangen > 0 and "FEHLT" not in r.stdout
    assert run(demo, "vorscan.py", "scan").returncode == 0


def test_vorscan_regeln():
    e = vr.entscheid
    assert e("Spielora Gaming AG", "Head of Product", "Zürich")[1].startswith("Firmen-Ausschluss")
    assert e("Talentbrücke Personal AG", "Senior Product Owner", "Zürich")[1].startswith("Vermittler")
    assert e("Kandora Consulting AG", "Product Owner", "Zürich")[1].startswith("Ausschluss 4")
    assert e("Veltrima Gesundheitsdienste AG", "Product Owner", "St. Gallen")[1].startswith("Ausschluss 2")
    assert e("Kalvit Software AG", "Junior Product Owner", "Zürich")[1].startswith("Ausschluss 1")
    assert e("Mastrova Industrie AG", "Senior Product Owner", "Aarau")[1].startswith("Physisches Produkt")
    assert e("Kalvit Software AG", "Data Engineer", "Zürich") == ("vorfilter", "Engineering-/Entwicklerrolle")
    assert e("Kalvit Software AG", "Scrum Master", "Zürich")[1].startswith("Nicht-Rolle")
    # Schutzwoerter: Modell entscheidet
    assert e("Kalvit Software AG", "Data Engineer Plattform", "Zürich") == ("unklar", "")
    assert e("Kalvit Software AG", "Product Owner Payments", "Zürich") == ("unklar", "")
    assert e("Quendor Versicherungen AG", "Senior Product Owner", "Zürich") == ("unklar", "")
    assert vr.DISTANZ_ORTE == {"st gallen", "lausanne", "genf"}


# --- publiziert -----------------------------------------------------------------------------------

def test_publiziert_parse_varianten():
    b = date(2025, 4, 10)
    p = publiziert.parse
    assert p("2025-04-02", b) == date(2025, 4, 2)
    assert p("02 April 2025", b) == date(2025, 4, 2)
    assert p("2. April 2025", b) == date(2025, 4, 2)
    assert p("02.04.2025", b) == date(2025, 4, 2)
    assert p("Fri Apr 04 02:01:00 UTC 2025", b) == date(2025, 4, 4)
    assert p('"datePosted": "2025-04-03"', b) == date(2025, 4, 3)
    assert p("eine Woche vor dem 2025-04-09", b) == date(2025, 4, 2)
    assert p("vor 4 Stunden", b) == b
    assert p("Gestern", b) == date(2025, 4, 9)
    assert p("Heute", b) == b
    assert p("3 days ago", b) == date(2025, 4, 7)
    assert p("1 week ago", b) == date(2025, 4, 3)
    assert p("2 months ago", b) == date(2025, 2, 9)
    assert p("Netzwerk «1 week ago», Abruf 2025-04-01") == date(2025, 3, 25)   # gegen das Abrufdatum
    assert p("ca. vor 3 Tagen", b) == date(2025, 4, 7)
    assert p("2025-04-02, Bewerbungsfrist 2025-05-01", b) == date(2025, 4, 2)
    assert p("Bewerbungsfrist 2025-05-01", b) is None
    assert p("unbekannt", b) is None and p("", b) is None and p("irgendwann", b) is None
    assert p("2025-04-20", b) is None                                         # nach dem Bezug: unplausibel
    assert p("Gestern") is None                                               # relativ ohne Bezug
    assert publiziert.alter_text(date(2025, 4, 1), b) == "über eine Woche alt (9 Tage)"
    assert publiziert.alter_text(date(2025, 4, 9), b) == "1 Tag"
    assert publiziert.alter_text(None, b) == "unbekannt"


def test_publiziert_aus_anzeige(demo):
    a = next(x for x in json.loads((demo / "data" / "pipeline.json").read_text(encoding="utf-8"))["applications"]
             if x["status"] == "aussortiert")
    datei = publiziert.anzeige_datei(demo, a["id"])
    assert datei and datei.name.startswith(a["id"] + "--anzeige--")
    pub, roh = publiziert.aus_anzeige(datei)
    assert roh and pub is not None and pub <= date.fromisoformat(datei.stem.rsplit("--", 1)[1])
