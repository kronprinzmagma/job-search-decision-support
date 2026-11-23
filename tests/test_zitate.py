"""Gruppe Belege: jede Absage-Begruendung zitiert die Anzeige woertlich, Skripte pruefen das Zitat."""
import json

from conftest import run

MORGEN = "2025-04-26T08:00:00"


def pipeline(demo):
    return json.loads((demo / "data" / "pipeline.json").read_text(encoding="utf-8"))


def speichern(demo, data):
    (demo / "data" / "pipeline.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def fall(demo, fid):
    return next(a for a in pipeline(demo)["applications"] if a["id"] == fid)


def erstes_modell_nogo(data):
    return next(a for a in data["applications"] if a["status"] == "aussortiert" and a.get("zitate"))


# --- zitatcheck.py -------------------------------------------------------------------------------

def test_demo_ist_vollstaendig_belegt(demo):
    r = run(demo, "zitatcheck.py")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "0 Verstoesse" in r.stdout
    data = pipeline(demo)
    nogo = [a for a in data["applications"] if a["status"] == "aussortiert"]
    # jedes NoGo hat entweder Zitate oder eine ausdrueckliche Ausnahme (nur Entscheide von Alex)
    assert all(a.get("zitate") or a.get("zitat_ausnahme") for a in nogo)
    assert all(a["begruendung"].startswith("Entscheid Alex") for a in nogo if a.get("zitat_ausnahme"))


def test_umschreibung_ist_ein_verstoss(demo):
    data = pipeline(demo)
    a = erstes_modell_nogo(data)
    a["zitate"] = ["Die Rolle verlangt Erfahrung im Zahlungsverkehr"]  # Umschreibung, nicht woertlich
    speichern(demo, data)
    r = run(demo, "zitatcheck.py")
    assert r.returncode == 1
    assert f"VERSTOSS {a['id']}: Zitat steht nicht woertlich in der Anzeige" in r.stdout
    assert "1 Verstoesse" in r.stderr
    # der Waechter meldet dasselbe im Cockpit
    run(demo, "jobcoach.py")
    assert f"NOGO OHNE BELEG: {a['firma']} ({a['id']})" in (demo / "views" / "WARNINGS.md").read_text(encoding="utf-8")


def test_fehlendes_oder_zu_kurzes_zitat(demo):
    data = pipeline(demo)
    nogo = [a for a in data["applications"] if a["status"] == "aussortiert" and a.get("zitate")]
    nogo[0].pop("zitate")
    nogo[1]["zitate"] = ["vor Ort"]
    speichern(demo, data)
    r = run(demo, "zitatcheck.py", nogo[0]["id"], nogo[1]["id"])
    assert r.returncode == 1
    assert f"{nogo[0]['id']}: kein Zitat aus der Anzeige" in r.stdout
    assert f"{nogo[1]['id']}: Zitat zu kurz" in r.stdout
    assert run(demo, "zitatcheck.py", "gibt-es-nicht").returncode == 2


def test_zeilenumbruch_im_zitat_ist_egal_anhang_zaehlt_nicht(demo):
    data = pipeline(demo)
    a = erstes_modell_nogo(data)
    anzeige = demo / a["anzeige"]
    a["zitate"] = [a["zitate"][0].replace(" ", "\n  ", 1)]
    speichern(demo, data)
    assert run(demo, "zitatcheck.py", a["id"]).returncode == 0
    # was nur im eigenen Anhang «Für cv-tailor» steht, ist kein Beleg aus der Anzeige
    anzeige.write_text(anzeige.read_text(encoding="utf-8") + "\nNur im Anhang: erfundener Ausschlussgrund\n",
                       encoding="utf-8")
    a["zitate"] = ["Nur im Anhang: erfundener Ausschlussgrund"]
    speichern(demo, data)
    assert run(demo, "zitatcheck.py", a["id"]).returncode == 1


# --- status.py -----------------------------------------------------------------------------------

def test_status_nogo_braucht_belegtes_zitat(demo):
    fid = next(a["id"] for a in pipeline(demo)["applications"] if a["status"] == "vorgelegt")
    anzeige = fall(demo, fid)["anzeige"]
    argumente = [fid, "aussortiert", "--quelle", anzeige, "--begruendung", "Ausschluss 6: Muss-Kriterium unbelegt"]

    r = run(demo, "status.py", *argumente)
    assert r.returncode != 0 and "--zitat" in r.stderr
    r = run(demo, "status.py", *argumente, "--zitat", "Mehrjaehrige Erfahrung mit Quantencomputern")
    assert r.returncode != 0 and "nicht woertlich" in r.stderr
    assert fall(demo, fid)["status"] == "vorgelegt"   # nichts geschrieben, Ordner nicht verschoben

    zeile = next(z for z in (demo / anzeige).read_text(encoding="utf-8").splitlines() if z.startswith("- "))
    zitat = zeile[2:40]
    r = run(demo, "status.py", *argumente, "--zitat", zitat)
    assert r.returncode == 0, r.stdout + r.stderr
    a = fall(demo, fid)
    assert a["status"] == "aussortiert" and a["zitate"] == [zitat] and "zitat_ausnahme" not in a
    assert run(demo, "zitatcheck.py", fid).returncode == 0


def test_status_ausnahme_nur_ausdruecklich(demo):
    fid = next(a["id"] for a in pipeline(demo)["applications"] if a["status"] == "vorgelegt")
    grund = "Entscheid Alex 2025-04-25: Pendelzeit im Alltag zu hoch"
    r = run(demo, "status.py", fid, "aussortiert", "--quelle", fall(demo, fid)["anzeige"],
            "--begruendung", grund, "--ohne-zitat", grund)
    assert r.returncode == 0, r.stdout + r.stderr
    a = fall(demo, fid)
    assert a["zitat_ausnahme"] == grund and "zitate" not in a
    assert run(demo, "zitatcheck.py", fid).returncode == 0
    # --zitat gilt nur fuer ein NoGo
    andere = next(x["id"] for x in pipeline(demo)["applications"] if x["status"] == "vorgelegt")
    r = run(demo, "status.py", andere, "draft", "--zitat", "irgendein langer Text")
    assert r.returncode != 0 and "nur fuer Status 'aussortiert'" in r.stderr


# --- screening_log.py add ------------------------------------------------------------------------

def test_sweep_nogo_ohne_belegtes_zitat_wird_abgelehnt(demo):
    run(demo, "screening_log.py", "start", "morgen", jetzt=MORGEN)
    fid = "mirvel-medien-head-of-product-leserplattform"
    pfad = f"stellen/{fid}/{fid}--anzeige--2025-04-26.md"
    (demo / pfad).parent.mkdir(parents=True)
    (demo / pfad).write_text("# Head of Product\n\n**Publiziert:** Gestern (Abruf 2025-04-26)\n\n---\n\n"
                             "## Dein Profil\n\n- Die Stelle ist zu 100 % vor Ort.\n", encoding="utf-8")
    zeile = (f"Mirvel Medien AG|Head of Product Leserplattform|Zürich|netzwerk-suche|volltext-nogo|"
             f"Ausschluss 3 (kein Homeoffice)|ns-zh-a|Gestern|{pfad}")
    r = run(demo, "screening_log.py", "add", zeile, jetzt=MORGEN)
    assert "ABGELEHNT (Beleg)" in r.stdout and "kein Zitat" in r.stdout
    r = run(demo, "screening_log.py", "add", zeile + "|kein Homeoffice moeglich", jetzt=MORGEN)
    assert "ABGELEHNT (Beleg)" in r.stdout and "nicht woertlich" in r.stdout
    assert not any(a["id"] == fid for a in pipeline(demo)["applications"])

    r = run(demo, "screening_log.py", "add", zeile + "|Die Stelle ist zu 100 % vor Ort", jetzt=MORGEN)
    assert f"Datensatz {fid} angelegt (aussortiert)" in r.stdout, r.stdout
    a = fall(demo, fid)
    assert a["zitate"] == ["Die Stelle ist zu 100 % vor Ort"]
    assert run(demo, "zitatcheck.py", fid).returncode == 0
