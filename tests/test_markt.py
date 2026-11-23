"""Gruppe Markt: Kodierschema, Stichwort-Kodierung, Monatsnotiz, Block B (Schutzregeln), Zweitkodierung."""
import json
import re
import shutil
import sys

from conftest import REPO, run

sys.path.insert(0, str(REPO / "scripts"))
import marktcheck as mc  # noqa: E402

SCHEMA = mc.schema_laden(REPO / "spec" / "ki_kodierschema.json")
BAUSTEINE = json.loads((REPO / "demo" / "texte" / "ki_anforderungen.json").read_text(encoding="utf-8"))["bausteine"]
KI_IDS = [k["id"] for k in SCHEMA["kategorien"] if k["id"] != "K00"]

# Eine Beispielzeile je Kategorie (erfunden, Anzeigen-Wortlaut, absichtlich ohne Umlaute wie in der Demo)
BEISPIEL = {
    "K01": "Du identifizierst und priorisierst KI-Use-Cases fuer das Kundenportal.",
    "K02": "Du bringst die KI-Funktionen vom Pilot in den produktiven Betrieb.",
    "K03": "Du definierst Testfälle und Metriken für die Antworten unseres LLM.",
    "K04": "Du stellst die Datenqualitaet fuer unsere KI-Vorhaben sicher.",
    "K05": "Du konzipierst KI-Agenten für den Kundenservice.",
    "K06": "Du konzipierst Schulungen zu generativer KI für alle Fachbereiche.",
    "K07": "Du stellst die Einhaltung des EU AI Act sicher.",
    "K08": "Du trainierst ML-Modelle in Python.",
    "K09": "Ausgepraegte KI-Affinitaet.",
}


def anzeige(firma="", aufgaben=(), profil=()):
    return ("# Rolle – Firma\n\n**Quelle:** Demo\n\n---\n\n" + firma + "\n\n## Deine Aufgaben\n\n"
            + "\n".join(f"- {a}" for a in aufgaben) + "\n\n## Dein Profil\n\n" + "\n".join(f"- {p}" for p in profil)
            + "\n\n## Für cv-tailor\n\nKI-Agenten und Prompts (dieser Abschnitt wird nicht kodiert).\n")


def demo_markt(demo):
    """Demo-Kopie um die Vorlagen ergänzen (conftest kopiert demo/ nicht mit)."""
    shutil.copytree(REPO / "demo", demo / "demo", dirs_exist_ok=True)
    return demo


def abschnitt_b(txt):
    return txt.split("## B –")[1].split("## C –")[0]


# --- Schema und Kodierung ----------------------------------------------------------------------------

def test_beispielzeile_je_kategorie():
    assert set(BEISPIEL) == set(KI_IDS)
    for kid, satz in BEISPIEL.items():
        assert kid in mc.kodiere_satz(satz, SCHEMA), (kid, satz)


def test_beispiele_treffen_gegenbeispiele_nicht():
    for k in SCHEMA["kategorien"]:
        if k["id"] == "K00":
            continue
        for b in k["beispiele_im_anzeigentext"]:
            assert k["id"] in mc.kodiere_satz(b, SCHEMA), (k["id"], b)
        for g in k["gegenbeispiele"]:
            assert k["id"] not in mc.kodiere_satz(g, SCHEMA), (k["id"], g)


def test_bausteine_treffen_ihre_kategorie():
    je = {}
    for b in BAUSTEINE:
        je[b["kategorie_id"]] = je.get(b["kategorie_id"], 0) + 1
        if b["abschnitt"] == "firma":
            kod = mc.kodiere_anzeige(anzeige(firma=b["satz"], aufgaben=["Du verantwortest die Roadmap."]), SCHEMA)
            assert kod["codes"] == ["K00"], b
        else:
            teil = {"aufgaben": [b["satz"]]} if b["abschnitt"] == "aufgaben" else {"profil": [b["satz"]]}
            assert b["kategorie_id"] in mc.kodiere_anzeige(anzeige(**teil), SCHEMA)["codes"], b
    assert set(je) == set(KI_IDS) | {"K00"} and all(2 <= n <= 3 for n in je.values()), je


def test_firmenteil_ohne_ki_bezug_und_wunsch():
    ohne = mc.kodiere_anzeige(anzeige(firma="Wir setzen seit Jahren auf KI und Agenten.",
                                      aufgaben=["Du priorisierst das Backlog."]), SCHEMA)
    assert ohne["codes"] == ["K00"]
    w = mc.kodiere_anzeige(anzeige(profil=["Erfahrung mit der Evaluation von KI-Ergebnissen von Vorteil."]), SCHEMA)
    assert w["codes"] == ["K03"] and w["nur_wunsch"] == ["K03"]
    muss = mc.kodiere_anzeige(anzeige(aufgaben=[BEISPIEL["K03"]],
                                      profil=["Erfahrung mit der Evaluation von KI-Ergebnissen von Vorteil."]), SCHEMA)
    assert muss["nur_wunsch"] == []
    leer = mc.kodiere_anzeige(anzeige(aufgaben=["Du arbeitest mit KI."]), SCHEMA)
    assert leer["codes"] == ["K00"] and leer["ki_ohne_code"]


def test_belege_decken_alle_kategorien():
    b = json.loads((REPO / "persona" / "belege.json").read_text(encoding="utf-8"))
    assert set(b["kategorien"]) == set(KI_IDS)
    assert {x["status"] for x in b["kategorien"].values()} <= {"belegt", "teilweise", "luecke"}


def test_uebereinstimmung():
    a = {"x": ["K01", "K02"], "y": ["K00"], "z": ["K09"]}
    gleich = mc.uebereinstimmung(a, dict(a), ["K01", "K02", "K09", "K00"])
    assert gleich["n"] == 3 and gleich["jaccard"] == 1.0 and set(gleich["kappa"].values()) == {1.0}
    b = {"x": ["K01"], "y": ["K00"], "z": ["K09"], "fremd": ["K05"]}
    u = mc.uebereinstimmung(a, b, ["K01", "K02"])
    assert u["n"] == 3 and abs(u["jaccard"] - (0.5 + 1 + 1) / 3) < 1e-9
    assert u["kappa"]["K01"] == 1.0 and abs(u["kappa"]["K02"]) < 1e-9


# --- Lauf auf den Demo-Daten ---------------------------------------------------------------------------

def anzahl(txt, kid):
    return int(re.search(rf"\({kid}\) \| (\d+) \|", txt).group(1))


def test_lauf_auf_demo_erzeugt_notiz(demo):
    demo_markt(demo)
    vorher = run(demo, "marktcheck.py", "--monat", "2025-03")
    assert vorher.returncode == 0, vorher.stderr
    # In März-Anzeigen ohne K05/K07 je einen Baustein-Satz einmischen: die Zählung muss genau so steigen
    ohne = [p for p in sorted(demo.glob("stellen/*/*--anzeige--2025-03-*.md"))
            if not {"K05", "K07"} & set(mc.kodiere_anzeige(p.read_text(encoding="utf-8"), SCHEMA)["codes"])][:6]
    saetze = {b["kategorie_id"]: b["satz"] for b in BAUSTEINE if b["kategorie_id"] in ("K05", "K07")
              and b["abschnitt"] == "aufgaben"}
    for i, p in enumerate(ohne):
        t = p.read_text(encoding="utf-8")
        satz = saetze["K05" if i % 2 else "K07"]
        assert "## Deine Aufgaben\n\n" in t
        p.write_text(t.replace("## Deine Aufgaben\n\n", f"## Deine Aufgaben\n\n- {satz}\n", 1), encoding="utf-8")
    abgesagt = [f for f in pipeline(demo) if f["status"] == "abgesagt"]
    schreibe_besetzung(demo, [_profil(i, fall_id=f["id"], firma=f["firma"], rolle=f["rolle"])
                              for i, f in enumerate(abgesagt[:6], 1)])
    r = run(demo, "marktcheck.py", "--monat", "2025-03", "--schreiben")
    assert r.returncode == 0, r.stderr
    txt = (demo / "notes" / "2025-03_marktbeobachtung.md").read_text(encoding="utf-8")
    for teil in ("# Marktbeobachtung 2025-03", "## A – Nachfrage", "## B – Besetzung", "## C – Position",
                 "## D – Eigenanalyse", "## Was die Zahlen nicht hergeben", "2025-03-01 bis 2025-03-31"):
        assert teil in txt, teil
    assert "{" not in txt and "}" not in txt                      # alle Platzhalter ersetzt
    assert len(ohne) == 6
    assert anzahl(txt, "K05") == anzahl(vorher.stdout, "K05") + 3   # genau die eingemischten Sätze
    assert anzahl(txt, "K07") == anzahl(vorher.stdout, "K07") + 3
    assert "| Merkmal | Gruppe (n = 6) |" in abschnitt_b(txt)
    assert "| Beispiele |" in txt and "95 %-Wilson" in txt
    assert "| Fälle im Zeitraum (Volltext bewertet) |" in txt
    # ohne --schreiben: dieselbe Notiz auf stdout, nichts geschrieben
    r = run(demo, "marktcheck.py", "--monat", "2025-03")
    assert r.returncode == 0 and r.stdout == txt


def pipeline(demo):
    return json.loads((demo / "data" / "pipeline.json").read_text(encoding="utf-8"))["applications"]


def schreibe_besetzung(demo, eintraege):
    (demo / "data" / "besetzung.json").write_text(json.dumps(eintraege, ensure_ascii=False), encoding="utf-8")


def _besetzung(demo, eintraege):
    schreibe_besetzung(demo, eintraege)
    r = run(demo, "marktcheck.py", "--monat", "2025-03")
    assert r.returncode == 0, r.stderr
    return abschnitt_b(r.stdout)


def _profil(i, **kw):
    """Ein erfundener Eintrag im Format von data/besetzung.json (Docstring scripts/marktcheck.py)."""
    b = {"pseudonym": f"P{i:03d}", "fall_id": f"demo-fall-{i}", "firma": "Kalvit Software AG",
         "rolle": "Senior Product Owner", "erhoben_am": "2025-03-20", "jahre_rollentyp": 4,
         "vorbranche": "B2B-Software", "vorstufe": "Senior PO/PM", "abschluss": "Wirtschaft", "ki_belege": True,
         "wechsel": "extern"}
    b.update(kw)
    return b


def test_besetzung_gruppen_unter_5_werden_nicht_ausgewiesen(demo):
    demo_markt(demo)
    eintraege = [_profil(i) for i in range(1, 6)]
    eintraege.append(_profil(6, wechsel="intern", abschluss="Informatik/Technik", vorstufe="Product Owner",
                             jahre_rollentyp=9))
    b = _besetzung(demo, eintraege)
    assert "| Interner Wechsel | unter 5 |" in b
    assert "| Abschluss Informatik/Technik | unter 5 |" in b
    assert "Senior PO/PM: 5 · übrige Ausprägungen: unter 5" in b
    assert "Product Owner:" not in b                                   # Ausprägung mit 1 Fall nicht beziffert
    assert "Median erst ab 10" in b and not re.search(r"Median \d", b)   # unter 10 Fällen kein Median
    assert "zu wenig Fälle für einen Vergleich" in b                   # kein Stadium mit 5 Fällen
    assert "| Aus der Branche der Stelle | 6 von 6 | 6 von 6 | kein Abstand erkennbar |" in b
    # unter 5 gefundenen Besetzungen: gar keine Tabelle
    spaeter = _profil(5, erhoben_am="2025-04-10")                      # nach dem Berichtszeitraum erhoben
    b = _besetzung(demo, [_profil(i) for i in range(1, 5)] + [spaeter])
    assert "Zu wenig Fälle für eine Auswertung" in b and "| Merkmal |" not in b
    assert re.search(r"gefunden \(erhoben bis 2025-03-31\): unter 5", b)


def test_zweitkodierung_cli(demo):
    demo_markt(demo)
    ids = sorted(p.parent.name for p in demo.glob("stellen/*/*--anzeige--2025-03-*.md"))[:4]
    (demo / "data" / "zweit.json").write_text(json.dumps({i: ["K00"] for i in ids}), encoding="utf-8")
    r = run(demo, "marktcheck.py", "--zweitkodierung", demo / "data" / "zweit.json")
    assert r.returncode == 0, r.stderr
    assert "4 gemeinsame Anzeigen" in r.stdout and "Kappa" in r.stdout
