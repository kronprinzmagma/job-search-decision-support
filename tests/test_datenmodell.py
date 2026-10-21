"""Gruppe Datenmodell: Sperre, Statuswechsel, Verlauf, Dublettencheck, Cockpit und Views."""
import json
import os
import subprocess
import sys
import time

from conftest import HEUTE, run


def pipeline(demo):
    return json.loads((demo / "data" / "pipeline.json").read_text(encoding="utf-8"))


def fall(demo, fid):
    return next(a for a in pipeline(demo)["applications"] if a["id"] == fid)


def ids_mit(demo, status):
    return [a["id"] for a in pipeline(demo)["applications"] if a["status"] == status]


def py(demo, code):
    """Python-Schnipsel in der Demo-Kopie ausfuehren (Module aus deren scripts/)."""
    env = {**os.environ, "JC_HEUTE": HEUTE, "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, 'scripts')\n" + code],
                          cwd=demo, env=env, capture_output=True, text=True, timeout=60)


# --- Sperre --------------------------------------------------------------------------------------

def test_sperre_konflikt_bei_geaenderter_mtime(demo):
    vorher = (demo / "data" / "pipeline.json").read_text(encoding="utf-8")
    r = py(demo, """
import os, pipeline_tx
try:
    with pipeline_tx.transaktion("test") as d:
        d["applications"][0]["notiz"] = "UEBERSCHRIEBEN"
        st = pipeline_tx.DATA.stat()
        os.utime(pipeline_tx.DATA, ns=(st.st_atime_ns, st.st_mtime_ns + 5_000_000_000))  # andere Session schreibt
except pipeline_tx.Konflikt as k:
    print("KONFLIKT", k)
print("SPERRE", pipeline_tx.LOCK.exists())
""")
    assert "KONFLIKT" in r.stdout, r.stderr
    assert "SPERRE False" in r.stdout  # Sperre wird auch im Fehlerfall freigegeben
    assert (demo / "data" / "pipeline.json").read_text(encoding="utf-8") == vorher


def test_sperre_konflikt_bei_frischer_sperre(demo):
    lock = demo / "data" / ".pipeline.lock"
    lock.write_text("2025-04-25T18:00:00 | pid 1 | andere Session\n", encoding="utf-8")
    vorher = (demo / "data" / "pipeline.json").read_text(encoding="utf-8")
    fid = ids_mit(demo, "in_pruefung")[0]
    r = run(demo, "ereignis.py", fid, "nachfass", "--notiz", "test")
    assert r.returncode != 0 and "KONFLIKT" in (r.stdout + r.stderr)
    assert (demo / "data" / "pipeline.json").read_text(encoding="utf-8") == vorher
    assert lock.exists()  # fremde Sperre bleibt unangetastet
    assert "GESPERRT" in run(demo, "pipeline_tx.py", "status").stdout


def test_verwaiste_sperre_wird_uebernommen(demo):
    lock = demo / "data" / ".pipeline.lock"
    lock.write_text("alt\n", encoding="utf-8")
    alt = time.time() - 30 * 60
    os.utime(lock, (alt, alt))
    fid = ids_mit(demo, "in_pruefung")[0]
    r = run(demo, "ereignis.py", fid, "nachfass", "--notiz", "test")
    assert r.returncode == 0, r.stderr
    assert "verwaiste Sperre" in r.stderr
    assert not lock.exists()


def test_screening_log_sperre(demo):
    (demo / "data" / ".screening_log.lock").write_text("fremd\n", encoding="utf-8")
    r = py(demo, """
import screening_log_tx
try:
    with screening_log_tx.transaktion("test") as d:
        pass
except screening_log_tx.Konflikt:
    print("KONFLIKT")
""")
    assert "KONFLIKT" in r.stdout, r.stderr


# --- status.py -----------------------------------------------------------------------------------

def test_go_legt_ordner_in_eingang(demo):
    fid = ids_mit(demo, "aussortiert")[0]  # liegt in stellen/; Go nach Zweitpruefung
    assert (demo / "stellen" / fid).is_dir()
    r = run(demo, "status.py", fid, "draft")
    assert r.returncode == 0, r.stdout + r.stderr
    assert (demo / "eingang" / fid).is_dir() and not (demo / "stellen" / fid).exists()
    a = fall(demo, fid)
    assert a["status"] == "draft"
    assert a["anzeige"].startswith(f"eingang/{fid}/") and a["dossier"] == f"eingang/{fid}"
    assert a["verlauf"][-1]["ereignis"] == "go"
    assert all(not str(e.get("quelle", "")).startswith(f"stellen/{fid}/") for e in a["verlauf"])


def test_versand_ohne_recherche_bricht_ab_mit_recherche_nach_stellen(demo):
    fid = ids_mit(demo, "vorgelegt")[0]
    assert run(demo, "status.py", fid, "draft").returncode == 0
    assert (demo / "eingang" / fid).is_dir()
    brief = demo / "eingang" / fid / "Motivationsschreiben-Alex Müller-Test.md"
    brief.write_text("# Test\n", encoding="utf-8")
    quelle = f"eingang/{fid}/{brief.name}"

    r = run(demo, "status.py", fid, "abgeschickt", "--quelle", quelle)
    assert r.returncode != 0 and "Recherche" in (r.stdout + r.stderr)
    assert fall(demo, fid)["status"] == "draft" and (demo / "eingang" / fid).is_dir()

    (demo / "eingang" / fid / f"{fid}--recherche--{HEUTE}.md").write_text(f"# Recherche\n\n**Stand:** {HEUTE}\n", encoding="utf-8")
    r = run(demo, "status.py", fid, "abgeschickt", "--quelle", quelle)
    assert r.returncode != 0 and "personen" in (r.stdout + r.stderr)   # Personen-Recherche fehlt noch

    (demo / "eingang" / fid / f"{fid}--personen--{HEUTE}.md").write_text(f"# Personen\n\n**Stand:** {HEUTE}\n", encoding="utf-8")
    r = run(demo, "status.py", fid, "abgeschickt", "--quelle", quelle)
    assert r.returncode == 0, r.stdout + r.stderr
    assert (demo / "stellen" / fid).is_dir() and not (demo / "eingang" / fid).exists()
    a = fall(demo, fid)
    assert a["status"] == "abgeschickt" and a["datum_eingereicht"] == HEUTE
    assert a["verlauf"][-1]["ereignis"] == "versand"
    assert a["verlauf"][-1]["quelle"] == f"stellen/{fid}/{brief.name}"
    assert a["anzeige"].startswith(f"stellen/{fid}/")


def test_status_pflichtfelder(demo):
    fid = ids_mit(demo, "in_pruefung")[0]
    r = run(demo, "status.py", fid, "abgesagt", "--quelle", fall(demo, fid)["anzeige"])
    assert r.returncode != 0 and "--stadium" in r.stderr


# --- ereignis.py ---------------------------------------------------------------------------------

def test_ereignis_schreibt_und_lehnt_duplikat_ab(demo):
    fid = ids_mit(demo, "in_pruefung")[0]
    n0 = len(fall(demo, fid)["verlauf"])
    r = run(demo, "ereignis.py", fid, "nachfass", "--datum", HEUTE, "--notiz", "Telefon")
    assert r.returncode == 0, r.stderr
    vl = fall(demo, fid)["verlauf"]
    assert len(vl) == n0 + 1 and any(e["ereignis"] == "nachfass" and e["datum"] == HEUTE for e in vl)
    r = run(demo, "ereignis.py", fid, "nachfass", "--datum", HEUTE)
    assert "existiert schon" in r.stdout
    assert len(fall(demo, fid)["verlauf"]) == n0 + 1


def test_ereignis_quelle_pflicht(demo):
    fid = ids_mit(demo, "abgeschickt")[0]
    r = run(demo, "ereignis.py", fid, "eingang")
    assert r.returncode != 0 and "--quelle" in r.stderr


# --- Dublettencheck, vorgelegt, offene Auftraege, Sync -----------------------------------------------

def test_dublettencheck(demo):
    a = pipeline(demo)["applications"][0]
    r = run(demo, "dublettencheck.py", a["firma"], a["rolle"])
    assert r.returncode == 1 and "TREFFER" in r.stdout and a["id"] in r.stdout
    r = run(demo, "dublettencheck.py", "Zyrtak Holding AG", "Chief Llama Officer")
    assert r.returncode == 0 and r.stdout.startswith("NEU ")


def test_vorgelegt_exit_code(demo):
    offen = ids_mit(demo, "vorgelegt")
    r = run(demo, "vorgelegt.py")
    assert r.returncode == 1 and f"VORGELEGT: {len(offen)}" in r.stdout
    assert all(i in r.stdout for i in offen)
    p = demo / "data" / "pipeline.json"
    d = pipeline(demo)
    d["applications"] = [a for a in d["applications"] if a["status"] != "vorgelegt"]
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    r = run(demo, "vorgelegt.py")
    assert r.returncode == 0 and "VORGELEGT: 0" in r.stdout


def test_offene_auftraege(demo):
    assert run(demo, "offene_auftraege.py").returncode == 0
    fid = ids_mit(demo, "draft")[0]
    for f in (demo / "eingang" / fid).glob(f"{fid}--recherche--*.md"):
        f.unlink()
    r = run(demo, "offene_auftraege.py")
    assert r.returncode == 1 and fid in r.stdout


def test_sync_screening_candidates(demo):
    p = demo / "data" / "screening_log.json"
    log = json.loads(p.read_text(encoding="utf-8"))
    log["gesichtet"].append({"firma": "Zyrtak Holding AG", "rolle": "Lead Product Owner Plattform", "ort": "Zürich",
                             "kanal": "portal", "entscheid": "kandidat", "grund": "Test", "datum": HEUTE,
                             "gefunden_ueber": "Test", "lauf_id": f"{HEUTE}-nachmittag", "zeit": "15:30:00"})
    p.write_text(json.dumps(log, ensure_ascii=False), encoding="utf-8")
    r = run(demo, "sync_screening_candidates.py")
    assert r.returncode == 0 and "Zyrtak" in r.stdout and "Vorschau" in r.stdout
    assert run(demo, "sync_screening_candidates.py", "--apply").returncode == 0
    neu = [a for a in pipeline(demo)["applications"] if a["firma"] == "Zyrtak Holding AG"]
    assert len(neu) == 1 and neu[0]["status"] == "vorgelegt" and neu[0]["verlauf"][0]["ereignis"] == "vorgelegt"
    assert "Keine Log-Kandidaten" in run(demo, "sync_screening_candidates.py").stdout


# --- Cockpit und Views ---------------------------------------------------------------------------

def test_cockpit_zeigt_vorgelegte(demo):
    r = run(demo, "cockpit.py")
    assert r.returncode == 0, r.stderr
    assert "## Bei dir liegt" in r.stdout and "## Heute gelaufen" in r.stdout
    offen = ids_mit(demo, "vorgelegt")
    assert offen and all(f"`{i}`" in r.stdout for i in offen)


def test_jobcoach_erzeugt_views(demo):
    r = run(demo, "jobcoach.py")
    assert r.returncode == 0, r.stdout + r.stderr
    for name in ("STATUS.md", "APPLICATIONS.md", "WARNINGS.md"):
        assert (demo / "views" / name).is_file(), name
    status = (demo / "views" / "STATUS.md").read_text(encoding="utf-8")
    assert status.index("## Bei dir liegt") < status.index("## Zahlen") < status.index("## Wächter-Befunde")
    assert f"**Stand:** {HEUTE}" in status
    apps = (demo / "views" / "APPLICATIONS.md").read_text(encoding="utf-8")
    assert "## Vorgelegt — Entscheid offen" in apps and "## Aktive Pipeline" in apps
    # Generator (init_demo/status.py) und Waechter sind konsistent: keine Ablage- oder Schema-Befunde
    warn = (demo / "views" / "WARNINGS.md").read_text(encoding="utf-8")
    for marke in ("SCHEMA", "EX-ANTE", "portablen Namen", "EINGANG", "GO OHNE RECHERCHE", "VOLLTEXT OHNE ABLAGE",
                  "Namenskonvention", "nicht ladbar"):
        assert marke not in warn, marke


def test_jobcoach_meldet_schema_und_eingang(demo):
    d = pipeline(demo)
    a = next(x for x in d["applications"] if x["status"] == "in_pruefung")
    a["datum_absage"] = "2025-04-01"  # Tippfehler-Drift
    (demo / "data" / "pipeline.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    (demo / "eingang" / "lose_mail.md").write_text("Absage\n", encoding="utf-8")
    r = run(demo, "jobcoach.py")
    assert "SCHEMA: unbekannte Felder ['datum_absage']" in r.stdout
    assert "EINGANG: lose Datei eingang/lose_mail.md" in r.stdout
