"""Gruppe Auswertung: Marktreport, Marktbild, Kanal-Auswertung, Zweitprüfung, Prozess-Retro, Umbau-Kontrolle, Fit-Analyse."""
import importlib.util
import json
import math

from conftest import run


def modul(demo, name):
    """Skript aus der Demo-Kopie als Modul laden (ROOT zeigt dann auf die Kopie, nie aufs Repo)."""
    spec = importlib.util.spec_from_file_location(f"{name}_{abs(hash(str(demo)))}", demo / "scripts" / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def pipeline(demo):
    return json.loads((demo / "data" / "pipeline.json").read_text(encoding="utf-8"))


# --- marktreport / marktbild / kanal_auswertung -------------------------------------------------

def test_marktreport_schreibt_trichter_und_ausschlussgruende(demo):
    r = run(demo, "marktreport.py")
    assert r.returncode == 0, r.stderr
    txt = (demo / "views" / "MARKTREPORT.md").read_text(encoding="utf-8")
    assert "## 1 — Der Trichter" in txt
    for stufe in ("Gesichtet (Listenebene)", "Volltext geprüft", "Als Kandidat vorgelegt", "Beworben", "Einladung"):
        assert stufe in txt
    assert "## 2 — Warum Stellen nicht in Frage kommen" in txt
    for grund in ("Vermittler / Aggregator", "Engineering-/Entwicklerrolle", "Benannter Fähigkeits-Ausschluss (Payment)",
                  "Fachwissen in fremder Domäne"):
        assert grund in txt
    assert "nicht klassifiziert" not in txt          # jede Demo-Begründung ist einer Kategorie zugeordnet
    assert "**Befund:**" in txt


def test_marktbild_kategorisiert_alle_vorfilter(demo):
    r = run(demo, "marktbild.py")
    assert r.returncode == 0, r.stderr
    vor = (demo / "views" / "MARKTBILD_VORFILTER.md").read_text(encoding="utf-8")
    assert "Sonstiges / nicht kategorisiert" not in vor
    assert (demo / "data" / "marktbild_vorfilter.csv").read_text(encoding="utf-8").startswith("Datum;Firma")
    voll = (demo / "views" / "MARKTBILD_VOLLTEXT.md").read_text(encoding="utf-8")
    assert "--anzeige--" in voll


def test_kanal_auswertung_laeuft(demo):
    r = run(demo, "kanal_auswertung.py", "--tage", "28")
    assert r.returncode == 0, r.stderr
    assert "## Kanal-Auswertung (2025-03-28 bis 2025-04-24, 28 Tage)" in r.stdout
    assert "| portal |" in r.stdout and "| zielportal |" in r.stdout
    assert "Karriere- und Behördenportale einzeln" in r.stdout


# --- review_aussortierte ------------------------------------------------------------------------

def test_review_listet_nur_weiche_faelle(demo):
    r = run(demo, "review_aussortierte.py", "--json")
    assert r.returncode == 0, r.stderr
    faelle = json.loads(r.stdout)
    assert faelle and all(f["art"] == "weich" for f in faelle)
    # harte Gates und Entscheide von Alex erscheinen nicht
    begr = " ".join(f["begruendung"] for f in faelle)
    assert "Entscheid Alex" not in begr and "Payment" not in begr and "Ausschluss 3" not in begr
    alle = json.loads(run(demo, "review_aussortierte.py", "--alle", "--json").stdout)
    assert {"hard", "weich"} <= {f["art"] for f in alle} and len(alle) > len(faelle)
    # faellig sind nur die Faelle seit dem letzten Wochen-Review; ueber alle gesehen kommen beide weichen Gruende vor
    weich = {f["grund"] for f in alle if f["art"] == "weich"}
    assert "Ausschluss 6 (Kernfähigkeits-Lücke)" in weich and "Kompetenzdistanz (Schritt 2)" in weich


def test_review_kategorie_regeln(demo):
    m = modul(demo, "review_aussortierte")
    assert m.kategorie("Kompetenzdistanz (Schritt 2): Chance tief")[0] == "weich"   # nicht «Distanz»
    assert m.kategorie("Ausschluss 2 (Distanz): St. Gallen, Pendelzeit 65 Min.")[0] == "hard"
    assert m.kategorie("Ausschluss 6 (Kernfaehigkeits-Luecke): bei Alex unbelegt") == ("weich", "Ausschluss 6 (Kernfähigkeits-Lücke)")
    assert m.kategorie("Ausschluss 6 ... Entscheid Alex 2025-04-01: Team im Umbau") == ("hard", "Entscheid Alex")
    assert m.kategorie("Nicht-Rolle: kein Produktmandat (Ausschluss 5 auf Listenebene)")[0] == "hard"
    assert m.kategorie("Firmen-Ausschluss (Persona: keine Glücksspielbranche)")[0] == "hard"


def test_review_markiere_schreibt_zweitpruefung(demo):
    fid = json.loads(run(demo, "review_aussortierte.py", "--json").stdout)[0]["id"]
    r = run(demo, "review_aussortierte.py", "--markiere", fid, "bestaetigt")
    assert r.returncode == 0, r.stdout + r.stderr
    a = next(a for a in pipeline(demo)["applications"] if a["id"] == fid)
    assert a["zweitpruefung"] == {"datum": "2025-04-25", "ergebnis": "bestaetigt"}
    assert not (demo / "data" / ".pipeline.lock").exists()
    assert fid not in {f["id"] for f in json.loads(run(demo, "review_aussortierte.py", "--json").stdout)}
    assert run(demo, "review_aussortierte.py", "--markiere", fid, "vielleicht").returncode == 2
    assert run(demo, "review_aussortierte.py", "--markiere", "gibt-es-nicht", "bestaetigt").returncode == 1


# --- analyse_fit_v2 -----------------------------------------------------------------------------

def test_fisher_exakt_bekannte_werte(demo):
    m = modul(demo, "analyse_fit_v2")
    assert math.isclose(m.fisher(3, 1, 1, 3), 34 / 70, rel_tol=1e-9)            # ≈ 0.4857
    assert math.isclose(m.fisher(1, 9, 11, 3), 0.002759, abs_tol=5e-6)           # Lehrbuchbeispiel
    assert math.isclose(m.fisher(1, 3, 3, 1), m.fisher(3, 1, 1, 3))              # symmetrisch
    assert math.isclose(m.fisher(2, 2, 2, 2), 1.0)


def test_wilson_intervall_referenz(demo):
    m = modul(demo, "analyse_fit_v2")
    lo, hi = m.wilson(5, 10)
    assert math.isclose(lo, 0.2366, abs_tol=1e-4) and math.isclose(hi, 0.7634, abs_tol=1e-4)
    lo, hi = m.wilson(0, 10)
    assert lo == 0.0 and math.isclose(hi, 0.2775, abs_tol=1e-4)
    assert m.wilson(0, 0) == (0.0, 0.0)


def test_analyse_fit_v2_schreibt_auswertung(demo):
    r = run(demo, "analyse_fit_v2.py", "--schreiben")
    assert r.returncode == 0, r.stderr
    assert "Basisrate Einladung" in r.stdout and "Fisher exakt (A=2 vs. A≤1)" in r.stdout
    txt = (demo / "data" / "analyse_v2" / "auswertung.md").read_text(encoding="utf-8")
    assert "## H2 — Anforderungs-Fit (A)" in txt and "Leave-one-out" in txt


# --- umbau_kontrolle ----------------------------------------------------------------------------

def test_umbau_kontrolle_warnungen_liste(demo):
    m = modul(demo, "umbau_kontrolle")
    w = m.warnungen()
    assert isinstance(w, list) and all(isinstance(x, str) for x in w)
    assert not any("lief nicht" in x for x in w)
    erg = m.messen()
    assert erg["vorher"]["modell"] == "opus" and erg["nachher"]["modell"] == "sonnet"
    assert erg["nachher"]["dauer_median"] < erg["vorher"]["dauer_median"]
    assert erg["nachher"]["vorscan_anteil"] > 0.9 and not erg["vorher"]["vorscan_anteil"]
    r = run(demo, "umbau_kontrolle.py")
    assert r.returncode in (0, 1) and "Urteil:" in r.stdout


# --- prozess_retro ------------------------------------------------------------------------------

def test_prozess_retro_schreibt_notiz_und_prueft_wirkung(demo):
    vorher = json.loads((demo / "data" / "retro_massnahmen.json").read_text(encoding="utf-8"))
    r = run(demo, "prozess_retro.py", heute="2025-04-20")
    assert r.returncode == 0, r.stderr
    txt = (demo / "notes" / "2025-04-20_prozessretro.md").read_text(encoding="utf-8")
    assert "Zeitraum 2025-04-13 bis 2025-04-19" in txt
    for teil in ("## Kennzahlen", "## Fundgeschwindigkeit", "## Die drei grössten Abweichungen",
                 "## Wirkungskontrolle früherer Massnahmen", "## Kanal-Auswertung", "## Bei dir liegt"):
        assert teil in txt
    # Kostenumbau der Vorwoche (2025-04-06-vorscan): Sweep-Dauer gesunken -> gewirkt
    zeile = next(z for z in txt.splitlines() if z.startswith("| 2025-04-06 "))
    assert "dauer_min_median" in zeile and "**gewirkt**" in zeile
    assert "2025-04-06-vorscan **gewirkt**" in txt
    nachher = json.loads((demo / "data" / "retro_massnahmen.json").read_text(encoding="utf-8"))
    neu = [m for m in nachher if m["id"] not in {v["id"] for v in vorher}]
    assert neu and all(m["entscheid"] == "offen" and m["datum"] == "2025-04-20" for m in neu)
    # zweiter Lauf am selben Tag legt keine Massnahme doppelt an, handgeschriebener Teil bleibt
    pfad = demo / "notes" / "2025-04-20_prozessretro.md"
    pfad.write_text(txt + "\n## Ursachen\n\nvon Hand ergänzt\n", encoding="utf-8")
    assert run(demo, "prozess_retro.py", heute="2025-04-20").returncode == 0
    assert len(json.loads((demo / "data" / "retro_massnahmen.json").read_text(encoding="utf-8"))) == len(nachher)
    assert "von Hand ergänzt" in pfad.read_text(encoding="utf-8")


def test_prozess_retro_liest_lauf_audit(demo):
    r = run(demo, "screening_log.py", "audit", "--aktualisieren", "--alle", heute="2025-04-20")
    assert r.returncode == 0, r.stdout + r.stderr
    assert (demo / "data" / "lauf_audit.json").exists()
    r = run(demo, "prozess_retro.py", heute="2025-04-20")
    assert r.returncode == 0, r.stderr
    txt = (demo / "notes" / "2025-04-20_prozessretro.md").read_text(encoding="utf-8")
    assert "nachgerechnet" not in txt and "| Sweeps gestartet / Soll (nur Info) | 16 / 16 |" in txt


def test_prozess_retro_markiere(demo):
    r = run(demo, "prozess_retro.py", "--markiere", "2025-04-20-portale-mittag", "offen", "neu zu entscheiden")
    assert r.returncode == 0, r.stdout
    m = next(x for x in json.loads((demo / "data" / "retro_massnahmen.json").read_text(encoding="utf-8"))
             if x["id"] == "2025-04-20-portale-mittag")
    assert m["entscheid"] == "offen" and m["entscheid_datum"] == "2025-04-25"
    assert run(demo, "prozess_retro.py", "--markiere", "2025-04-20-portale-mittag", "egal").returncode == 2
