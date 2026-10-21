#!/usr/bin/env python3
"""init_demo — erzeugt die komplette Demo-Welt fuer die Persona Alex Müller.

    python3 scripts/init_demo.py            # schreibt data/, stellen/, eingang/, notes/, feedback/
    python3 scripts/init_demo.py --pruefen  # erzeugt in ein Temp-Verzeichnis und vergleicht (Determinismus)

Alles ist erfunden: Firmen, Anzeigen, Begruendungen, Termine. Der Zeitraum (2025-03-03 bis 2025-04-25)
ist bewusst synthetisch. Fester Seed, keine Systemzeit: zwei Laeufe erzeugen byte-identische Dateien.

Erzeugt nur Rohdaten (was im Betrieb Sweeps, Kandidaten-Chat und Pflegelauf schreiben). Alles Abgeleitete
(Audit je Sweep, Views, Reports, Retro) rechnen danach die echten Skripte: scripts/demo.sh.
"""
import argparse
import datetime as dt
import filecmp
import json
import random
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = 20250303
START = dt.date(2025, 3, 3)
ENDE = dt.date(2025, 4, 25)
UMBAU = dt.date(2025, 4, 7)          # ab hier: Vorscan fuer das Jobportal, schlanke Arbeitskarte
DREI_SWEEPS_AB = dt.date(2025, 3, 17)  # vorher nur morgen + nachmittag

# --- Welt ------------------------------------------------------------------------------------------

# Ort -> Pendelzeit ab Zuerich HB in Minuten (Persona: hoechstens 60)
ORTE = {"Zürich": 0, "Schlieren": 15, "Dübendorf": 15, "Kloten": 15, "Baden": 20, "Winterthur": 25,
        "Zug": 25, "Aarau": 35, "Luzern": 45, "Basel": 55, "Bern": 58, "St. Gallen": 65,
        "Lausanne": 130, "Genf": 170}

# (Name, Branche, Ort, Typ). Typ steuert, wie das Screening die Firma behandelt.
FIRMEN = [
    ("Quendor Versicherungen AG", "Versicherung", "Zürich", "ziel"),
    ("Brivana Privatbank AG", "Bank", "Zürich", "ziel"),
    ("Sanuvia Health AG", "Krankenversicherung", "Winterthur", "ziel"),
    ("Mirvel Medien AG", "Medien", "Zürich", "ziel"),
    ("Kalvit Software AG", "B2B-Software", "Zürich", "ziel"),
    ("Varella Energie AG", "Energie", "Baden", "ziel"),
    ("Vendaro Retail AG", "Detailhandel", "Zürich", "ziel"),
    ("Pelvio Mobility AG", "Mobilität", "Bern", "ziel"),
    ("Fendrix Analytics AG", "Daten und Analytik", "Baden", "normal"),
    ("Trellin Immobilien AG", "Immobilien", "Zug", "normal"),
    ("Quelvia Pharma AG", "Pharma", "Basel", "normal"),
    ("Lernovi Bildung AG", "Bildung", "Zürich", "normal"),
    ("Orvana Reisen AG", "Tourismus", "Luzern", "normal"),
    ("Kombira Versand AG", "E-Commerce", "Dübendorf", "normal"),
    ("Ristra Finanztechnik AG", "Fintech", "Zug", "normal"),
    ("Telvaro Kommunikation AG", "Telekommunikation", "Zürich", "normal"),
    ("Veltrima Gesundheitsdienste AG", "Gesundheit", "St. Gallen", "normal"),
    ("Sorvik Logistik AG", "Logistik", "Kloten", "normal"),
    ("Amberlin Versicherung AG", "Versicherung", "Lausanne", "normal"),
    ("Cirrova Cloud AG", "Cloud-Dienste", "Schlieren", "normal"),
    ("Hovald Bau AG", "Bau", "Aarau", "physisch"),
    ("Mastrova Industrie AG", "Maschinenbau", "Aarau", "physisch"),
    ("Tuskora Lebensmittel AG", "Lebensmittel", "Luzern", "physisch"),
    ("Kandora Consulting AG", "Beratung", "Zürich", "beratung"),
    ("Pixavo Agentur GmbH", "Digitalagentur", "Zürich", "beratung"),
    ("Talentbrücke Personal AG", "Personalvermittlung", "Zürich", "vermittler"),
    ("Jobvera Staffing AG", "Personalvermittlung", "Zug", "vermittler"),
    ("Spielora Gaming AG", "Glücksspiel", "Zürich", "ausschluss"),
    ("Stadtverwaltung Nordtal", "Verwaltung", "Winterthur", "behoerde"),
    ("Kantonale Verwaltung Altmark", "Verwaltung", "Aarau", "behoerde"),
]
F = {f[0]: f for f in FIRMEN}

# (Titel, Art). Art steuert den Vorfilter.
ROLLEN = [
    ("Senior Product Owner", "po"), ("Product Owner Kundenportal", "po"), ("Product Owner Self-Service", "po"),
    ("Lead Product Owner Plattform", "lead"), ("Product Owner Mobile App", "po"), ("Head of Product", "head"),
    ("Senior Product Manager", "pm"), ("Product Manager KI-Anwendungen", "ki"), ("Product Manager Data Platform", "pm"),
    ("Digital Product Lead", "lead"), ("Product Owner Payments", "payment"), ("Junior Product Owner", "junior"),
    ("Praktikum Produktmanagement", "junior"), ("Software Engineer Backend", "eng"), ("Data Engineer", "eng"),
    ("Solution Architect", "eng"), ("Scrum Master", "nicht"), ("Business Analyst", "nicht"),
    ("UX Designer", "nicht"), ("Projektleiter Digitalisierung", "nicht"), ("Product Manager Hardware", "physisch"),
    ("Requirements Engineer", "nicht"),
]
ROLLEN_GEWICHT = {"po": 5, "lead": 2, "head": 1, "pm": 4, "ki": 2, "payment": 1, "junior": 7, "eng": 22,
                  "nicht": 20, "physisch": 5}
# Zusaetze, damit dieselbe Firma mehrere verschiedene Anzeigen derselben Rollenfamilie haben kann
ZUSAETZE = ["", "", "", " Digital Channels", " Kundenerlebnis", " B2B", " Plattform-Services", " Daten", " Prozesse", " (80–100 %)"]

# Abfrage-Katalog (Soll je Sweep). Kanalnamen sind generisch: portal = grosses Jobportal,
# netzwerk-* = Suche und Empfehlungen im Berufsnetzwerk, zielportal = Karriereseite einer Zielfirma.
KATALOG = (
    [("portal", f"pt-{b}", n) for b, n in [
        ("a-product-owner", "Jobportal: «Product Owner», 24 h, Region Zürich"),
        ("a-senior-product-owner", "Jobportal: «Senior Product Owner», 24 h"),
        ("a-product-manager", "Jobportal: «Product Manager», 24 h"),
        ("a-head-of-product", "Jobportal: «Head of Product», 7 Tage"),
        ("b-ki-produkt", "Jobportal: «KI» UND «Produkt», 24 h"),
        ("b-digital-product", "Jobportal: «Digital Product», 24 h"),
        ("c-plattform", "Jobportal: «Plattform» UND «Owner», 24 h"),
        ("c-produktverantwortung", "Jobportal: «Produktverantwortung», 24 h"),
        ("d-lead-po", "Jobportal: «Lead Product Owner», 7 Tage"),
        ("d-product-lead", "Jobportal: «Product Lead», 24 h"),
        ("e-data-product", "Jobportal: «Data Product», 24 h"),
        ("e-ai-product-manager", "Jobportal: «AI Product Manager», 24 h"),
    ]]
    + [("netzwerk-suche", f"ns-{b}", n) for b, n in [
        ("zh-a", "Netzwerk-Suche: Product Owner, Zürich, letzte 24 h"),
        ("zh-b", "Netzwerk-Suche: Product Manager, Zürich, letzte 24 h"),
        ("zh-c", "Netzwerk-Suche: Head of Product, Zürich, letzte Woche"),
        ("be-a", "Netzwerk-Suche: Product Owner, Bern, letzte 24 h"),
        ("be-b", "Netzwerk-Suche: Product Manager, Bern, letzte 24 h"),
    ]]
    + [("netzwerk-empfehlung", "ne-empfehlungen", "Netzwerk: Empfehlungen «Für dich»")]
    + [("zielportal", "zp-" + f[0].split()[0].lower(), f"Karriereseite {f[0]}") for f in FIRMEN if f[3] == "ziel"]
    + [("behoerdenportal", "bp-nordtal", "Stellenportal Stadtverwaltung Nordtal"),
       ("behoerdenportal", "bp-altmark", "Stellenportal Kantonale Verwaltung Altmark")]
)
AUSRANGIERT = [("portal", "pt-x-projektleiter", "Jobportal: «Projektleiter Digital», 24 h",
                "2025-03-14: in zwei Wochen 0 Kandidaten, 41 Sichtungen, alles Nicht-Rollen"),
               ("netzwerk-suche", "ns-ost", "Netzwerk-Suche: Product Owner, Ostschweiz",
                "2025-03-21: Region liegt ausserhalb der Pendelzeit, 0 Kandidaten")]
NUR_MORGENS = {"zielportal", "behoerdenportal"}
# Bewaehrter Weg je Kanal: wie die Liste zuletzt vollstaendig gelesen wurde (Methodengedaechtnis im Log)
WEG = {"portal": "nach Datum sortiert, alle Seiten bis zum ersten Treffer aelter als das Fenster",
       "netzwerk-suche": "Filter «letzte 24 h», Liste bis zum Ende gescrollt, «mehr anzeigen» bis leer",
       "netzwerk-empfehlung": "Empfehlungsliste vollstaendig, nur Stellen mit Ort in der Ortstabelle",
       "zielportal": "Stellenliste der Karriereseite ohne Filter, alle Eintraege mit Datum verglichen",
       "behoerdenportal": "Rubrik Informatik und Digitales, alle Eintraege"}

# Volltext-NoGo: tragender Ausschluss (weich = Urteil, das die Zweitpruefung nochmals ansieht)
VOLLTEXT_NOGO = [
    "Ausschluss 5 (Rueckschritt): kein Produktmandat, Roadmap liegt beim Business Owner, Rolle setzt Tickets um",
    "Ausschluss 6 (Kernfaehigkeits-Luecke): mehrjaehrige Erfahrung mit Kernbankensystemen gefordert, bei Alex unbelegt",
    "Domaenenluecke: tiefes Pharma-Regulatorik-Wissen (GxP) als Muss-Kriterium, bei Alex nicht vorhanden",
    "Level-/Fuehrungsluecke: Fuehrung von Fuehrungskraeften (3 Teamleads) verlangt, Alex nur interimistisch",
    "Ausschluss 3 (kein Homeoffice): 100% vor Ort laut Volltext, Hybrid nur in Ausnahmefaellen",
    "Payment-Fachwissen gefordert (Zahlungsverkehr, Acquiring), benannter Faehigkeits-Ausschluss",
    "Rollen-Praeferenz: Schwerpunkt UI-Design in Figma, Produktverantwortung nur nominell",
    "Kompetenzdistanz (Schritt 2): Chance tief, Informatik-Studium als hartes Formalkriterium",
]
KANDIDAT_GRUND = [
    "Volltext geprueft: Roadmap-Hoheit, Plattformprodukt, regulierte Branche — Schritt 1 passt, Chance mittel",
    "Volltext geprueft: Self-Service-Portal, Teamfuehrung, KI-Anteil — Schritt 1 passt, Chance hoch",
    "Volltext geprueft: Produktverantwortung B2B, Abo-Modell — Schritt 1 passt, Chance mittel",
    "Volltext geprueft: KI-Anwendungen im Bestandsprodukt, Anbieter-Evaluation — Schritt 1 passt, Chance hoch",
]
NOGO_ALEX = [
    "Entscheid Alex {d}: Pendelzeit im Alltag zu hoch, trotz Hybrid",
    "Entscheid Alex {d}: Produkt zu nah an der aktuellen Stelle, kein Lernschritt",
    "Entscheid Alex {d}: Team im Umbau, Rolle soll erst in sechs Monaten definiert werden",
]


def gewichtete_rolle(rnd):
    pool = [r for r in ROLLEN for _ in range(ROLLEN_GEWICHT[r[1]])]
    return rnd.choice(pool)


def firma_fuer(rnd, rolle_art):
    if rolle_art in ("po", "lead", "head", "pm", "ki") and rnd.random() < 0.55:
        pool = [f for f in FIRMEN if f[3] in ("ziel", "normal")]
    else:
        pool = [f for f in FIRMEN if f[3] != "behoerde"]
    return rnd.choice(pool)


def vorfilter_grund(firma, rolle_art, ort):
    """Rauschregel auf Listenebene (dieselben Klassen wie scripts/vorscan_regeln.py). None = Volltext noetig."""
    typ = F[firma][3]
    if typ == "vermittler":
        return "Vermittler (Personalvermittlung, kein Arbeitgeber)"
    if typ == "beratung":
        return "Ausschluss 4 (Beratung/Agentur)"
    if typ == "ausschluss":
        return "Firmen-Ausschluss (Persona: keine Glücksspielbranche)"
    if rolle_art == "junior":
        return "Ausschluss 1 (Junior/Praktikum)"
    if rolle_art == "eng":
        return "Engineering-/Entwicklerrolle"
    if rolle_art == "physisch" or typ == "physisch":
        return "Physisches Produkt (Hardware, Maschinen, Lebensmittel)"
    if rolle_art == "nicht":
        return "Nicht-Rolle: kein Produktmandat (Listenebene)"
    if ORTE[ort] > 60:
        return f"Ausschluss 2 (Distanz): {ort}, Pendelzeit {ORTE[ort]} Min."
    return None


# --- Erzeugung ---------------------------------------------------------------------------------------

def tage():
    d = START
    while d <= ENDE:
        if d.weekday() < 5 or (d.weekday() == 5 and d > DREI_SWEEPS_AB):
            yield d
        d += dt.timedelta(days=1)


def arten(d):
    if d.weekday() == 5:
        return ["morgen"]
    return ["morgen", "mittag", "nachmittag"] if d >= DREI_SWEEPS_AB else ["morgen", "nachmittag"]


START_ZEIT = {"morgen": (8, 4), "mittag": (11, 3), "nachmittag": (15, 6)}


def iso(d, h, m, s=0):
    return dt.datetime(d.year, d.month, d.day, h, m, s).isoformat(timespec="seconds")


def publiziert_roh(rnd, d, kanal, abfrage):
    """Alter der Anzeige beim Fund, passend zum Suchfenster der Abfrage."""
    if kanal in NUR_MORGENS:
        alter = rnd.choice([0, 1, 1, 2, 3, 5, 8, 12])          # Karriereseiten: ohne Zeitfilter
    elif "7 Tage" in abfrage or "Woche" in abfrage:
        alter = rnd.choice([0, 1, 2, 3, 4, 6])
    else:
        alter = rnd.choice([0, 0, 0, 0, 1])                    # 24-Stunden-Fenster
    if alter == 0:
        return f"vor {rnd.randint(1, 9)} Stunden", d
    if alter == 1:
        return "Gestern", d - dt.timedelta(days=1)
    if rnd.random() < 0.5:
        return f"vor {alter} Tagen", d - dt.timedelta(days=alter)
    p = d - dt.timedelta(days=alter)
    return p.isoformat(), p


TEXTE = ROOT / "demo" / "texte"


def text(name, **felder):
    """Demo-Textvorlage aus demo/texte/ mit str.format fuellen (Platzhalter in geschweiften Klammern)."""
    return (TEXTE / f"{name}.md").read_text(encoding="utf-8").format(**felder)


def lang(d):
    return f"{d.day}. {MONATE[d.month - 1]} {d.year}"


KI_BAUSTEINE = [b for b in json.loads((TEXTE / "ki_anforderungen.json").read_text(encoding="utf-8"))["bausteine"]
                if b.get("abschnitt") in ("aufgaben", "profil")]

MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober",
          "November", "Dezember"]


def brief(a, d):
    """Motivationsschreiben-Entwurf aus demo/texte/anschreiben.md: baut auf Recherche und Personen-Recherche auf."""
    go = next(e["datum"] for e in a["verlauf"] if e["ereignis"] == "go")   # Recherchen entstehen beim Go
    return text("anschreiben", firma=a["firma"], rolle=a["rolle"], ort=F[a["firma"]][2], id=a["id"],
                datum_lang=lang(d), datum_recherche=go)


def slug(s):
    import re
    import unicodedata
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()


class Welt:
    def __init__(self, root: Path):
        self.root = root
        self.rnd = random.Random(SEED)
        self.gesichtet, self.laeufe, self.sweeps = [], [], []
        self.apps = []
        self.dateien = {}           # relativer Pfad -> Text
        self.bekannt = {}           # (firma, rolle) -> erster Kanal
        self.zuletzt = []           # (datum, (firma, rolle), kanal) der letzten zwei Tage, fuer Dubletten
        self.ids = set()
        self.wartend = []           # Kandidaten, die auf den Entscheid von Alex warten: (fall, faellig_am)
        self.offen_volltext = []

    # -- Katalog
    def katalog(self):
        abfragen = []
        for kanal, aid, name in KATALOG:
            abfragen.append({"id": aid, "kanal": kanal, "name": name, "abfrage": name.split(": ", 1)[-1],
                             "url": "", "filter": "Region Zürich +60 Min." if kanal == "portal" else "",
                             "hinweis": "", "netz": "vorscan" if kanal == "portal" else "browser", "aktiv": True})
        for kanal, aid, name, grund in AUSRANGIERT:
            abfragen.append({"id": aid, "kanal": kanal, "name": name, "abfrage": name.split(": ", 1)[-1],
                             "url": "", "filter": "", "hinweis": "", "netz": "browser", "aktiv": False,
                             "ausrangiert": grund})
        return {"version": "2025-03-21", "stand": "2025-03-21", "quelle": "spec/SUCHBEGRIFFE.md",
                "regeln": ["Ein Sweep ist erst abgeschlossen, wenn JEDE aktive Abfrage einen Status hat "
                           "(ok, leer, teilweise mit TECHNIK:, nicht-erreichbar). «uebersprungen» zaehlt nicht.",
                           "Ausrangieren = aktiv:false mit Datum und Grund, nie loeschen.",
                           "Ziel- und Behoerdenportale nur im Morgen-Sweep (aendern sich selten)."],
                "abfragen": abfragen}

    def aktive(self, d, art, mit_portalen=False):
        out = []
        for kanal, aid, name in KATALOG:
            if art != "morgen" and kanal in NUR_MORGENS and not mit_portalen:
                continue
            out.append((kanal, aid, name))
        for kanal, aid, name, grund in AUSRANGIERT:
            if d.isoformat() < grund[:10]:
                out.append((kanal, aid, name))
        return out

    # -- Sweeps
    def lauf(self):
        abbruch_tage = {dt.date(2025, 3, 11): "nachmittag", dt.date(2025, 3, 26): "nachmittag",
                        dt.date(2025, 4, 16): "mittag"}
        nachholen = False
        for d in tage():
            for art in arten(d):
                mit_portalen = nachholen and art != "morgen"
                abbrechen = abbruch_tage.get(d) == art
                self.sweep(d, art, mit_portalen, abbrechen)
                nachholen = abbrechen and art == "morgen"
            self.entscheide(d)
            self.verlaeufe(d)
            if d.weekday() == 5:
                self.wochen_review(d)

    def wochen_review(self, d):
        """Samstag: weiche Ausschluesse der Woche gegen den Volltext gegenpruefen (wie review_aussortierte.py)."""
        weich = ("Ausschluss 5", "Ausschluss 6", "Domaenenluecke", "Level-", "Rollen-Praeferenz", "Kompetenzdistanz")
        for a in self.apps:
            if (a["status"] != "aussortiert" or a.get("zweitpruefung") or a["datum"] > d.isoformat()
                    or not a.get("begruendung", "").startswith(weich)):
                continue
            # Fruehere Rueckgaben hat Alex laengst entschieden; offen ist nur, was der letzte Review zurueckgab.
            letzter = d + dt.timedelta(days=7) > ENDE
            ergebnis = "an-alex" if self.rnd.random() < 0.08 and letzter else "bestaetigt"
            a["zweitpruefung"] = {"datum": d.isoformat(), "ergebnis": ergebnis}
            self.ereignis(a, d, "zweitpruefung", a["anzeige"],
                          "Volltext erneut gelesen, Ausschluss traegt" if ergebnis == "bestaetigt"
                          else "Zweifel: Ausschluss nicht eindeutig belegt, an Alex")

    def sweep(self, d, art, mit_portalen, abbrechen):
        rnd = self.rnd
        sid = f"{d.isoformat()}-{art}"
        h, m = START_ZEIT[art]
        m += rnd.randint(0, 9)
        schlank = d >= UMBAU
        soll = self.aktive(d, art, mit_portalen)
        dauer = rnd.randint(22, 40) if schlank else rnd.randint(38, 72)
        s = {"id": sid, "datum": d.isoformat(), "art": art, "status": "abgeschlossen",
             "katalog_version": "2025-03-21" if d >= dt.date(2025, 3, 21) else "2025-03-03",
             "soll": len(soll), "start": iso(d, h, m), "ende": None, "sessions": [], "notiz": ""}
        if mit_portalen:
            s["mit_portalen"] = True
        t = dt.datetime(d.year, d.month, d.day, h, m)
        modell = "sonnet" if schlank else "opus"
        if abbrechen:
            # Session bricht nach gut der Haelfte ab (Rechner im Ruhezustand); der naechste Sweep holt nach.
            soll = soll[: len(soll) * 3 // 5]
            s["status"] = "abgebrochen"
            s["notiz"] = "Session ohne Ende (Rechner im Ruhezustand), naechster Sweep holt nach"
        neue = max(0, int(rnd.gauss(30 if art == "morgen" else 16, 6)))
        if d.weekday() == 5:
            neue //= 2
        # neue Anzeigen verteilen sich nach Kanalvolumen: Karriereseiten bringen selten Neues
        gewichte = [{"portal": 5, "netzwerk-suche": 4, "netzwerk-empfehlung": 2, "zielportal": 0.3,
                     "behoerdenportal": 0.8}[k] for k, _, _ in soll]
        verteilung = rnd.choices(range(len(soll)), weights=gewichte, k=neue)
        for i, (kanal, aid, name) in enumerate(soll):
            t += dt.timedelta(minutes=dauer / max(1, len(soll)))
            st, notiz, ges = "ok", "", None
            notiz = WEG[kanal]
            if kanal == "portal" and schlank:
                notiz = "Vorscan: Trefferliste mechanisch uebernommen, Unklare im Volltext"
            if rnd.random() < 0.035 and kanal != "portal":
                st, notiz = "nicht-erreichbar", "Seite laedt nur das Geruest (JavaScript), zwei Versuche, kein Volltext"
            elif rnd.random() < 0.02:
                st, notiz = "teilweise", "TECHNIK: Seite 3 der Trefferliste liefert Fehler 502, Seiten 1-2 gelesen"
            n_neu = sum(1 for v in verteilung if v == i)
            if st != "nicht-erreichbar":
                basis = {"portal": 28, "netzwerk-suche": 22, "netzwerk-empfehlung": 12, "zielportal": 7,
                         "behoerdenportal": 11}[kanal]
                ges = max(n_neu, int(rnd.gauss(basis, basis / 4)))
                if ges == 0:
                    st = "leer"
            self.laeufe.append({"kanal": kanal, "abfrage": name, "filter": "", "gesichtet": str(ges) if ges is not None else st.upper(),
                                "notiz": notiz, "datum": d.isoformat(), "lauf_id": sid, "abfrage_id": aid,
                                "status": st, "gesichtet_n": ges, "zeit": t.strftime("%H:%M:%S")})
            if st == "nicht-erreichbar":
                continue
            for _ in range(n_neu):
                self.sichtung(d, sid, t, kanal, name)
        ende = t + dt.timedelta(minutes=2)
        s["sessions"].append({"start": s["start"], "ende": None if abbrechen else ende.isoformat(timespec="seconds"),
                              "modell": modell, "pid_hinweis": ""})
        if not abbrechen:
            s["ende"] = ende.isoformat(timespec="seconds")
        else:
            s["sessions"][-1]["ende"] = (t + dt.timedelta(minutes=1)).isoformat(timespec="seconds")
            s["ende"] = s["sessions"][-1]["ende"]
        self.sweeps.append(s)

    def sichtung(self, d, sid, t, kanal, abfrage):
        rnd = self.rnd
        if kanal in NUR_MORGENS:
            if kanal == "zielportal":
                firma = next(f for f in FIRMEN if f[3] == "ziel" and f[0].split()[0].lower() in abfrage.lower())
            else:
                firma = next(f for f in FIRMEN if f[0] in abfrage)
            for _ in range(8):
                titel, art = rnd.choice([r for r in ROLLEN if r[1] in ("po", "pm", "nicht", "eng", "lead")])
                titel += rnd.choice(ZUSAETZE)
                if (firma[0], titel) not in self.bekannt:
                    break
        else:
            # ein Teil der Treffer ist dieselbe Anzeige ueber einen zweiten Kanal (Dublette), meist Stunden spaeter
            frisch = [z for z in self.zuletzt if (d - z[0]).days <= 1 and z[2] != kanal]
            if frisch and rnd.random() < 0.12:
                _, (fn, titel), erster = rnd.choice(frisch)
                self.eintrag(d, sid, t, fn, titel, F[fn][2], kanal, "dublette",
                             f"Dublette: bereits gesichtet ueber {erster}", abfrage, None)
                return
            for _ in range(8):
                titel, art = gewichtete_rolle(rnd)
                titel += rnd.choice(ZUSAETZE)
                firma = firma_fuer(rnd, art)
                if (firma[0], titel) not in self.bekannt:
                    break
        fn, ort = firma[0], firma[2]
        if (fn, titel) in self.bekannt:
            return  # schon bekannt: der Delta-Filter loggt nur Neues
        self.bekannt[(fn, titel)] = kanal
        self.zuletzt = [z for z in self.zuletzt if (d - z[0]).days <= 1] + [(d, (fn, titel), kanal)]
        roh, pub = publiziert_roh(rnd, d, kanal, abfrage)
        grund = vorfilter_grund(fn, art, ort)
        if grund:
            self.eintrag(d, sid, t, fn, titel, ort, kanal, "vorfilter", grund, abfrage, (roh, pub))
            return
        if rnd.random() < 0.06:
            self.eintrag(d, sid, t, fn, titel, ort, kanal, "geschlossen",
                         "Anzeige beim Volltext-Abruf nicht mehr verfuegbar (Fehlerseite des Portals)", abfrage, (roh, pub))
            return
        if d == ENDE and t.hour >= 15:
            self.eintrag(d, sid, t, fn, titel, ort, kanal, "offen", "Volltext ausstehend (Sweep-Ende)", abfrage, (roh, pub))
            return
        if F[fn][3] == "ziel" or art in ("lead", "head", "ki") or rnd.random() < 0.3:
            ok = art != "payment" and rnd.random() < 0.3
        else:
            ok = False
        if ok:
            grund = rnd.choice(KANDIDAT_GRUND)
            e = self.eintrag(d, sid, t, fn, titel, ort, kanal, "kandidat", grund, abfrage, (roh, pub))
            self.fall_vorgelegt(e, roh)
        else:
            branche = F[fn][1]
            pool = [g for g in VOLLTEXT_NOGO if not ("Kernbanken" in g and branche not in ("Bank", "Fintech"))
                    and not ("Pharma" in g and branche != "Pharma") and "Payment" not in g]
            grund = VOLLTEXT_NOGO[5] if art == "payment" else rnd.choice(pool)
            e = self.eintrag(d, sid, t, fn, titel, ort, kanal, "volltext-nogo", grund, abfrage, (roh, pub))
            self.fall_nogo(e, roh)

    def eintrag(self, d, sid, t, firma, rolle, ort, kanal, entscheid, grund, abfrage, pub):
        e = {"firma": firma, "rolle": rolle, "ort": ort, "kanal": kanal, "entscheid": entscheid, "grund": grund,
             "datum": d.isoformat(), "gefunden_ueber": abfrage, "lauf_id": sid, "zeit": t.strftime("%H:%M:%S")}
        if pub:
            e["publiziert_roh"] = pub[0]
            e["publiziert"] = pub[1].isoformat()
        self.gesichtet.append(e)
        return e

    # -- Faelle
    def neue_id(self, firma, rolle):
        basis = "-".join([slug(firma.replace(" AG", "").replace(" GmbH", ""))] + slug(rolle).split("-")[:4])[:60]
        k, n = basis, 2
        while k in self.ids:
            k, n = f"{basis}-{n}", n + 1
        self.ids.add(k)
        return k

    def anzeige(self, fid, e, roh, wurzel):
        firma, rolle = e["firma"], e["rolle"]
        branche, ort = F[firma][1], e["ort"]
        r = random.Random(fid)
        aufgaben = r.sample([
            "Du verantwortest die Roadmap des Produkts und priorisierst gemeinsam mit den Stakeholdern.",
            "Du fuehrst ein crossfunktionales Team aus Entwicklung, Design und Daten.",
            "Du entwickelst unser Kundenportal zur Self-Service-Plattform weiter.",
            "Du stellst sicher, dass Datenschutz und Barrierefreiheit von Anfang an mitgedacht werden.",
            "Du definierst Produktkennzahlen und steuerst danach.",
            "Du arbeitest eng mit Fachbereichen zusammen und uebersetzt ihre Anforderungen in Produktentscheide.",
            "Du verhandelst Prioritaeten mit internen Kunden und externen Partnern.",
        ], 4)
        profil = r.sample([
            "Mehrjaehrige Erfahrung als Product Owner oder Product Manager",
            "Erfahrung mit agilen Methoden (Scrum, Kanban, SAFe)",
            "Sicheres Auftreten gegenueber Fachbereichen und Geschaeftsleitung",
            "Erfahrung in einem regulierten Umfeld von Vorteil",
            "Sehr gute Deutsch- und Englischkenntnisse",
            "Freude an komplexen Fachdomaenen und an klaren Entscheiden",
            "Abgeschlossenes Studium in Wirtschaft, Informatik oder vergleichbar",
        ], 4)
        # verlangte KI-Faehigkeiten (Block A der Marktbeobachtung kodiert sie): KI-Rollen fast immer, sonst oft
        n_ki = r.choice([2, 3]) if "KI" in rolle or "Data" in rolle else r.choice([0, 0, 1, 1, 2])
        for b in r.sample(KI_BAUSTEINE, n_ki):
            (aufgaben if b["abschnitt"] == "aufgaben" else profil).append(b["satz"])
        txt = (f"# {rolle} — {firma}\n\n"
               f"**Quelle:** {e['gefunden_ueber']} (Kanal {e['kanal']}), verbatim abgerufen {e['datum']}\n"
               f"**Abruf:** {e['datum']}\n"
               f"**Publiziert:** {roh} (Abruf {e['datum']})\n"
               f"**Ort:** {ort} · **Pensum:** 80–100 % · **Arbeitsform:** hybrid\n\n"
               f"> Demo-Anzeige: erfunden fuer die Persona Alex Müller.\n\n---\n\n"
               f"{firma} ist ein Unternehmen aus der Branche {branche} mit Sitz in {ort}.\n\n"
               f"## Deine Aufgaben\n\n" + "\n".join(f"- {a}" for a in aufgaben) +
               "\n\n## Dein Profil\n\n" + "\n".join(f"- {p}" for p in profil) +
               "\n\n## Für cv-tailor\n\nDieser Abschnitt bleibt leer: die Anzeige oben ist der unveraenderte Input.\n")
        pfad = f"{wurzel}/{fid}/{fid}--anzeige--{e['datum']}.md"
        self.dateien[pfad] = txt
        return pfad

    def fall_nogo(self, e, roh):
        fid = self.neue_id(e["firma"], e["rolle"])
        note = f"notes/{e['lauf_id'][:10]}_screening_{e['lauf_id'][11:]}.md"
        pfad = self.anzeige(fid, e, roh, "stellen")
        self.apps.append({"id": fid, "firma": e["firma"], "rolle": e["rolle"], "status": "aussortiert",
                          "datum": e["datum"], "standort": e["ort"], "quelle": note, "anzeige": pfad,
                          "dossier": f"stellen/{fid}", "begruendung": e["grund"],
                          "verlauf": [{"datum": e["datum"], "ereignis": "nogo", "quelle": note,
                                       "notiz": e["grund"][:200]}]})
        e["pipeline_id"] = fid
        e["anzeige"] = pfad

    def fall_vorgelegt(self, e, roh):
        fid = self.neue_id(e["firma"], e["rolle"])
        note = f"notes/{e['lauf_id'][:10]}_screening_{e['lauf_id'][11:]}.md"
        pfad = self.anzeige(fid, e, roh, "eingang")
        a = {"id": fid, "firma": e["firma"], "rolle": e["rolle"], "status": "vorgelegt", "datum": e["datum"],
             "standort": e["ort"], "quelle": note, "anzeige": pfad, "dossier": f"eingang/{fid}",
             "notiz": f"Vom Sweep vorgelegt; Go/NoGo offen. {e['grund']}",
             "verlauf": [{"datum": e["datum"], "ereignis": "vorgelegt", "quelle": note,
                          "notiz": "Als Kandidat vorgelegt; Entscheid bei Alex offen."}]}
        self.apps.append(a)
        e["pipeline_id"] = fid
        e["anzeige"] = pfad
        # Alex entscheidet meist am selben oder naechsten Tag; die letzten Tage bleiben teils offen.
        tage_bis = self.rnd.choice([0, 0, 1, 1, 2])
        self.wartend.append((a, dt.date.fromisoformat(e["datum"]) + dt.timedelta(days=tage_bis)))

    def umziehen(self, a, wurzel):
        alt = a["dossier"].split("/", 1)[0]
        if alt == wurzel:
            return
        for p in [p for p in self.dateien if p.startswith(f"{alt}/{a['id']}/")]:
            self.dateien[wurzel + p[len(alt):]] = self.dateien.pop(p)
        um = lambda v: (wurzel + v[len(alt):]) if isinstance(v, str) and v.startswith(f"{alt}/{a['id']}") else v
        a["dossier"], a["anzeige"] = um(a["dossier"]), um(a["anzeige"])
        for ev in a["verlauf"]:
            ev["quelle"] = um(ev["quelle"])

    def ereignis(self, a, d, art, quelle, notiz=""):
        a["verlauf"].append({"datum": d.isoformat(), "ereignis": art, "quelle": quelle, "notiz": notiz[:200]})

    def entscheide(self, d):
        rest = []
        for a, faellig in self.wartend:
            gefunden = dt.date.fromisoformat(a["datum"])
            if faellig > d or gefunden >= ENDE - dt.timedelta(days=1):
                rest.append((a, faellig))
                continue
            if self.rnd.random() < 0.6:
                self.go(a, d)
            else:
                grund = self.rnd.choice(NOGO_ALEX).format(d=d.isoformat())
                a["status"] = "aussortiert"
                a["begruendung"] = grund
                self.umziehen(a, "stellen")
                self.ereignis(a, d, "nogo", "notes/" + d.isoformat() + "_kandidaten.md", grund)
                a["notiz"] += f" || Nachtrag {d.isoformat()} (status.py): vorgelegt → aussortiert"
        self.wartend = rest

    def go(self, a, d):
        rnd = self.rnd
        a["status"] = "draft"
        a["notiz"] += f" || Nachtrag {d.isoformat()} (status.py): vorgelegt → draft"
        self.ereignis(a, d, "go", "notes/" + d.isoformat() + "_kandidaten.md", "Go von Alex im Kandidaten-Chat")
        fid = a["id"]
        felder = dict(firma=a["firma"], rolle=a["rolle"], ort=F[a["firma"]][2], branche=F[a["firma"]][1], id=fid,
                      datum=d.isoformat())
        self.dateien[f"eingang/{fid}/{fid}--recherche--{d.isoformat()}.md"] = text("recherche", **felder)
        self.dateien[f"eingang/{fid}/{fid}--personen--{d.isoformat()}.md"] = text("personen", **felder)
        # fit_v2: Raster Schritt 2 vor dem Versand (ex ante); A = Anforderungs-Fit, B = Domaenennaehe
        A = rnd.choice([1, 2, 2]) if F[a["firma"]][3] == "ziel" else rnd.choice([0, 1, 1, 2])
        B = rnd.choice([0, 1, 2])
        kanal = rnd.choice(["+", "0", "0", "-"])
        verdikt = "hoch" if A + B >= 3 else ("mittel" if A + B == 2 else "tief")
        a["fit_v2"] = {"datum": d.isoformat(), "ex_ante": True, "A": A,
                       "A_begruendung": "Muss-Kriterien der Anzeige gegen persona/PROFILE.md geprueft (Demo)",
                       "B": B, "B_begruendung": "Branchen- und Aktivitaetsnaehe gegen belegte Stationen (Demo)",
                       "kanal": kanal, "verdikt": verdikt, "ergebnis": "offen",
                       "methode": "ex ante vor dem Versand, Raster spec/PRESCREEN.md"}
        a["_plan"] = {"versand": d + dt.timedelta(days=rnd.choice([1, 2, 3, 4])),
                      "einladung": (A * 0.28 + B * 0.08 + (0.15 if kanal == "+" else 0)) > rnd.random()}

    def verlaeufe(self, d):
        rnd = self.rnd
        for a in self.apps:
            p = a.get("_plan")
            if not p:
                continue
            fid = a["id"]
            felder = dict(firma=a["firma"], rolle=a["rolle"], ort=F[a["firma"]][2], id=fid)
            if a["status"] == "draft" and p["versand"] <= d:
                if rnd.random() < 0.06:
                    a["status"] = "zurueckgezogen"
                    a["begruendung"] = "Entscheid Alex: Stelle wurde intern besetzt, laut Rueckruf der Firma"
                    a["fit_v2"]["ergebnis"] = "zurueckgezogen"
                    self.umziehen(a, "stellen")
                    self.ereignis(a, d, "rueckzug", a["anzeige"], a["begruendung"])
                    a.pop("_plan")
                    continue
                stamm = f"Motivationsschreiben-Alex Müller-{a['firma'].split()[0]}-{slug(a['rolle'])[:30]}-{d.strftime('%y%m%d')}"
                self.dateien[f"eingang/{fid}/{stamm}.md"] = brief(a, d)
                self.umziehen(a, "stellen")
                a["status"] = "abgeschickt"
                a["datum_eingereicht"] = d.isoformat()
                a["datum_ist_einreichung"] = True
                self.ereignis(a, d, "versand", f"stellen/{fid}/{stamm}.md", "Versand ueber das Bewerbungsportal der Firma")
                p["eingang"] = d + dt.timedelta(days=rnd.choice([0, 1, 2]))
                p["antwort"] = d + dt.timedelta(days=rnd.randint(6, 26))
                continue
            if a["status"] == "abgeschickt" and p.get("eingang") and p["eingang"] <= d:
                q = f"stellen/{fid}/rueckmeldung_{d.isoformat()}.md"
                self.dateien[q] = text("mail_eingangsbestaetigung", datum=d.isoformat(), **felder)
                a["status"] = "in_pruefung"
                self.ereignis(a, d, "eingang", q, "Eingangsbestaetigung")
            if a["status"] in ("abgeschickt", "in_pruefung") and p.get("antwort") and p["antwort"] <= d:
                if p["einladung"]:
                    termin = d + dt.timedelta(days=rnd.randint(3, 8))
                    q = f"stellen/{fid}/einladung_{d.isoformat()}.md"
                    self.dateien[q] = text("mail_einladung", datum=d.isoformat(), termin=termin.isoformat(), **felder)
                    self.ereignis(a, d, "einladung", q, f"Erstgespraech am {termin.isoformat()}")
                    a["status"] = "gespraech"
                    a["gespraech_termin"] = termin.isoformat()
                    a["fit_v2"]["ergebnis"] = "einladung"
                    self.dateien[f"stellen/{fid}/gespraech_{termin.isoformat()}_erstgespraech_vorbereitung.md"] = text(
                        "interview_vorbereitung", datum=(termin - dt.timedelta(days=1)).isoformat(),
                        termin=termin.isoformat(), **felder)
                    p["gespraech"] = termin
                    p["nach_gespraech"] = termin + dt.timedelta(days=rnd.randint(4, 9))
                    if rnd.random() < 0.45:
                        # zweite Runde mit Case: Aufgabe kommt nach dem Erstgespraech, Vorbereitung im Fall-Ordner
                        aufgabe = termin + dt.timedelta(days=1)
                        self.dateien[f"stellen/{fid}/case/vorbereitung_{aufgabe.isoformat()}.md"] = text(
                            "case_vorbereitung", datum=aufgabe.isoformat(), termin=p["nach_gespraech"].isoformat(), **felder)
                else:
                    q = f"stellen/{fid}/absage_{d.isoformat()}.md"
                    self.dateien[q] = text("mail_absage", datum=d.isoformat(), **felder)
                    a.update(status="abgesagt", absage_datum=d.isoformat(), stadium="Pre-Shortlist (Dossier, kein Gespräch)",
                             begruendung="Standardabsage ohne Begruendung nach Dossierpruefung")
                    a["fit_v2"]["ergebnis"] = "absage-dossier"
                    self.ereignis(a, d, "absage", q, "Dossier-Absage ohne Begruendung")
                    a.pop("_plan")
                continue
            if a["status"] == "gespraech" and p.get("gespraech") and p["gespraech"] <= d and not p.get("gefuehrt"):
                p["gefuehrt"] = True
                g = p["gespraech"]
                self.ereignis(a, g, "gespraech", f"stellen/{fid}/gespraech_{g.isoformat()}_erstgespraech_vorbereitung.md",
                              "Erstgespraech gefuehrt")
                if rnd.random() < 0.8:
                    q = f"stellen/{fid}/gespraech_{g.isoformat()}_erstgespraech_debrief.md"
                    self.dateien[q] = text("interview_debrief", termin=g.isoformat(), **felder)
                    a["debrief"] = q
                    self.ereignis(a, g, "debrief", q, "Debrief geschrieben")
            if a["status"] == "gespraech" and p.get("nach_gespraech") and p["nach_gespraech"] <= d:
                if rnd.random() < 0.3:
                    q = f"stellen/{fid}/offerte_{d.isoformat()}.md"
                    self.dateien[q] = text("mail_offerte", datum=d.isoformat(), **felder)
                    a["status"] = "angebot"
                    self.ereignis(a, d, "angebot", q, "Angebot erhalten")
                else:
                    q = f"stellen/{fid}/absage_{d.isoformat()}.md"
                    self.dateien[q] = text("mail_absage", datum=d.isoformat(), **felder)
                    a.update(status="abgesagt", absage_datum=d.isoformat(), stadium="nach Erstgespräch",
                             begruendung="Absage nach Erstgespraech: andere Kandidatin mit mehr Branchenerfahrung")
                    self.ereignis(a, d, "absage", q, "Absage nach Erstgespraech")
                a.pop("_plan")

    # -- Notizen
    def notizen(self):
        for s in self.sweeps:
            sicht = [e for e in self.gesichtet if e["lauf_id"] == s["id"]]
            laeufe = [l for l in self.laeufe if l["lauf_id"] == s["id"]]
            kand = [e for e in sicht if e["entscheid"] == "kandidat"]
            weg = [e for e in sicht if e["entscheid"] in ("vorfilter", "volltext-nogo", "dublette", "geschlossen")]
            ne = [l for l in laeufe if l["status"] in ("nicht-erreichbar", "teilweise")]
            L = [f"# Screening-Lauf {s['art'].capitalize()}, {s['datum']} (Sweep {s['id']})", "",
                 "## Abdeckung", "",
                 f"{len(laeufe)} von {s['soll']} Abfragen, Status {s['status']}." +
                 (f" {s['notiz']}." if s["notiz"] else ""), ""]
            L += [f"- {l['abfrage_id']} [{l['status']}]: {l['notiz']}" for l in ne] + ([""] if ne else [])
            L += ["## Kandidaten", ""]
            if not kand:
                L.append("Keine neuen Kandidaten.")
            for e in kand:
                L += [f"### {e['firma']} — {e['rolle']} ({e['ort']})",
                      f"Kanal: {e['kanal']} · Dublettencheck: NEU · Publiziert: {e.get('publiziert_roh', 'unbekannt')}",
                      f"Empfehlung: bewerben — Entscheid bei Alex. {e['grund']}", ""]
            L += ["", "## Weggefallen", "", f"{len(weg)} weg (Vorfilter, Volltext-NoGo, Dubletten, geschlossen).", "",
                  "## Befunde", "", "keine", "", "## Bei dir liegt", "",
                  (f"{len(kand)} Kandidat(en) mit Empfehlung, Entscheid bei Alex." if kand else "keine"), ""]
            self.dateien[f"notes/{s['datum']}_screening_{s['art']}.md"] = "\n".join(L)

    def kandidaten_notizen(self):
        """Protokoll des Kandidaten-Chats je Tag: jeder Entscheid von Alex mit Wortlaut, im selben Zug erfasst."""
        tage = {}
        for a in self.apps:
            for e in a["verlauf"]:
                if e["quelle"].endswith("_kandidaten.md") and e["ereignis"] in ("go", "nogo"):
                    tage.setdefault(e["datum"], []).append((a, e))
        for tag, eintraege in sorted(tage.items()):
            L = [f"# Kandidaten-Chat {tag}", "", "> Demo: erfundener Verlauf. Jeder Entscheid steht im selben Zug im Datensatz "
                 "(`scripts/status.py`).", "", "| Fall | Empfehlung | Entscheid Alex | erfasst |", "|---|---|---|---|"]
            for a, e in sorted(eintraege, key=lambda x: x[0]["id"]):
                wortlaut = "Go" if e["ereignis"] == "go" else e["notiz"].split(": ", 1)[-1]
                L.append(f"| `{a['id']}` · {a['firma']} — {a['rolle']} | bewerben | «{wortlaut}» | "
                         f"`status.py {a['id']} {'draft' if e['ereignis'] == 'go' else 'aussortiert'}` |")
            L += ["", "Nach jedem Go im selben Zug: Recherche und Personen-Recherche im Fall-Ordner (spec/RECHERCHE.md, "
                  "spec/PERSONEN.md).", ""]
            self.dateien[f"notes/{tag}_kandidaten.md"] = "\n".join(L)

    def lehren(self):
        """Vier Lehren-Dokumente im Format von feedback/ — erfundene Daten, echte Muster."""
        L = {
            "2025-03-11_datenverlust-parallele-sessions.md": (
                "# Datenverlust durch parallele Sessions\n\n**Datum:** 2025-03-11 · **Mechanik danach:** "
                "`scripts/pipeline_tx.py`, `scripts/screening_log_tx.py`\n\n"
                "## Was passiert ist\n\nZwei Sessions (Sweep und Kandidaten-Chat) lasen `data/pipeline.json` ein, "
                "arbeiteten parallel und schrieben am Ende ihren ganzen Stand zurueck. Die zweite ueberschrieb die "
                "Entscheide der ersten. Aufgefallen ist es erst, als ein Go im Cockpit wieder als offen erschien.\n\n"
                "## Ursache\n\nJede Session hielt eine eigene Kopie der Datei; niemand pruefte vor dem Schreiben, "
                "ob sich die Datei inzwischen geaendert hatte.\n\n## Regel\n\nEs gibt genau einen Schreibweg: "
                "`pipeline_tx.transaktion()`. Sperrdatei (exklusiv angelegt), Vergleich der Aenderungszeit vor dem "
                "Schreiben, atomares Ersetzen. Bei Konflikt wird nicht gewartet und nicht ueberschrieben, sondern "
                "abgebrochen und gemeldet.\n"),
            "2025-03-18_dublette-behauptet-nicht-geprueft.md": (
                "# Dublettencheck behauptet, nicht ausgefuehrt\n\n**Datum:** 2025-03-18 · **Mechanik danach:** "
                "`scripts/dublettencheck.py` (Pflicht vor jeder Vorlage)\n\n## Was passiert ist\n\nDer Sweep legte "
                "eine Stelle als neuen Kandidaten vor, die seit dem Vormittag als Draft im Repo lag. Im Bericht stand "
                "«Dublettencheck: NEU».\n\n## Ursache\n\nDie Arbeitskarte schrieb den Abgleich vor, aber nur als Text. "
                "Das Modell meldete den Schritt als erledigt, ohne ihn auszufuehren.\n\n## Regel\n\nEine Pruefung, die "
                "ein Modell nur behaupten kann, ist keine Pruefung. Der Abgleich ist ein Skript mit Exit-Code; kein "
                "Kandidat geht an Alex, bevor es gelaufen ist.\n"),
            "2025-03-25_bewertung-auf-paraphrase.md": (
                "# Go/NoGo auf einer Paraphrase\n\n**Datum:** 2025-03-25 · **Mechanik danach:** Hard-Gate Quelle in "
                "`AGENTS.md`, Kopfzeilen **Quelle/Abruf/Publiziert** in jeder Anzeige\n\n## Was passiert ist\n\nEine "
                "Empfehlung stuetzte sich auf eine Zusammenfassung der Anzeige statt auf den Volltext. Die "
                "Zusammenfassung liess das harte Kriterium «100 % vor Ort» weg.\n\n## Regel\n\nKeine Bewertung ohne "
                "vollstaendigen Volltext aus der Primaerquelle. Eine Paraphrase zaehlt nie als Quelle, auch keine "
                "eigene. Jede Empfehlung nennt die verbatim abgelegte Datei, auf der sie beruht.\n"),
            "2025-04-02_abruf-gescheitert-ist-kein-befund.md": (
                "# Gescheiterter Abruf als «Stelle weg» gemeldet\n\n**Datum:** 2025-04-02 · **Mechanik danach:** "
                "Status `nicht-erreichbar` mit Pflichtnotiz in `scripts/screening_sweep.py`\n\n## Was passiert ist\n\n"
                "Eine Karriereseite lieferte nur ein JavaScript-Geruest. Der Bericht meldete «Stelle nicht mehr "
                "ausgeschrieben». Die Stelle war online.\n\n## Regel\n\nEin gescheiterter Abruf ist ein Befund ueber den "
                "Abruf, nicht ueber die Welt. Gemeldet wird «konnte nicht abrufen» mit Weg und Fehlerbild; die Abfrage "
                "bleibt im naechsten Sweep faellig.\n"),
        }
        for name, txt in L.items():
            self.dateien[f"feedback/{name}"] = txt

    def massnahmen(self):
        return [
            {"id": "2025-03-16-log-sperre", "datum": "2025-03-16", "befund": "Zwei Sessions am selben Sweep, 9 Abfragen doppelt geloggt",
             "beleg": "data/lauf_audit.json, notes/2025-03-11_screening_nachmittag.md", "vorschlag": "Sperre auch fuer screening_log.json, Session ohne Ende blockiert Neustart",
             "zieldatei": "scripts/screening_log_tx.py", "metrik": "sweeps_doppelt", "wert_bei_vorschlag": 1,
             "entscheid": "umgesetzt", "entscheid_datum": "2025-03-16", "notiz": "Sperrmuster wie pipeline_tx"},
            {"id": "2025-03-23-ausrangieren", "datum": "2025-03-23", "befund": "Zwei Abfragen liefern seit zwei Wochen nur Rauschen",
             "beleg": "scripts/kanal_auswertung.py --tage 14", "vorschlag": "pt-x-projektleiter und ns-ost ausrangieren",
             "zieldatei": "data/screening_kanaele.json", "metrik": "abfragen_ohne_kandidat_14d", "wert_bei_vorschlag": 2,
             "entscheid": "umgesetzt", "entscheid_datum": "2025-03-23", "notiz": "aktiv:false mit Datum und Grund"},
            {"id": "2025-04-06-vorscan", "datum": "2025-04-06", "befund": "Ein Sweep liest rund 280 KB Regelwerk und faehrt das Jobportal im Browser",
             "beleg": "data/lauf_audit.json (dauer_min)", "vorschlag": "Vorscan ohne Modell fuer das Jobportal, schlanke Arbeitskarte spec/SWEEP.md",
             "zieldatei": "scripts/vorscan.py", "metrik": "dauer_min_median", "wert_bei_vorschlag": 54,
             "entscheid": "umgesetzt", "entscheid_datum": "2025-04-06", "notiz": "Wirkungskontrolle: scripts/umbau_kontrolle.py"},
            {"id": "2025-04-20-portale-mittag", "datum": "2025-04-20", "befund": "Zielportale aendern sich selten, werden aber dreimal taeglich gefahren",
             "beleg": "scripts/kanal_auswertung.py", "vorschlag": "Zielportale auch im Mittag-Sweep streichen",
             "zieldatei": "spec/SWEEP.md", "metrik": "kandidaten_zielportal_mittag", "wert_bei_vorschlag": 0,
             "entscheid": "abgelehnt", "entscheid_datum": "2025-04-20", "notiz": "Entscheid Alex: schon umgesetzt seit Katalog 2025-03-21, Befund doppelt"},
        ]

    def schreiben(self, ziel: Path):
        for wurzel in ("data", "stellen", "eingang", "notes", "feedback"):
            p = ziel / wurzel
            if p.exists():
                for f in sorted(p.rglob("*"), reverse=True):
                    if f.is_file() and not f.name.startswith(".gitkeep"):
                        f.unlink()
                    elif f.is_dir():
                        f.rmdir()
            p.mkdir(parents=True, exist_ok=True)
        for a in self.apps:
            a.pop("_plan", None)
        schema = {
            "vorgelegt": "Vom Screening-Sweep vorgelegt, Entscheid von Alex steht aus — wird im Kandidaten-Chat zu draft (Go) oder aussortiert (NoGo)",
            "draft": "Go bestaetigt, noch nicht abgeschickt (Stellen-Ordner liegt in eingang/)",
            "abgeschickt": "Bewerbung eingereicht, keine Rueckmeldung", "in_pruefung": "Bestaetigung erhalten, laeuft",
            "gespraech": "Interview-Phase", "abgesagt": "Absage erhalten", "zurueckgezogen": "Selbst gestoppt",
            "angebot": "Offerte vorliegend", "aussortiert": "Pre-Screen NoGo, nicht beworben"}
        pipeline = {"_doc": "EINZIGE QUELLE fuer den Status jedes Falls. Views erzeugt python3 scripts/jobcoach.py. "
                            "Nie die generierten .md von Hand editieren. Felder nie raten: Unbekanntes weglassen. "
                            "Demo-Daten, erfunden (scripts/init_demo.py).",
                    "status_schema": schema, "applications": self.apps}
        dump = lambda o: json.dumps(o, ensure_ascii=False, indent=1) + "\n"
        (ziel / "data" / "pipeline.json").write_text(dump(pipeline), encoding="utf-8")
        (ziel / "data" / "screening_log.json").write_text(
            dump({"gesichtet": self.gesichtet, "laeufe": self.laeufe, "sweeps": self.sweeps}), encoding="utf-8")
        (ziel / "data" / "screening_kanaele.json").write_text(dump(self.katalog()), encoding="utf-8")
        (ziel / "data" / "retro_massnahmen.json").write_text(dump(self.massnahmen()), encoding="utf-8")
        (ziel / "data" / "besetzung.json").write_text(dump(self.besetzung()), encoding="utf-8")
        (ziel / "data" / "vorscan").mkdir(exist_ok=True)
        (ziel / "data" / "vorscan" / "stand.json").write_text(dump(self.vorscan_stand()), encoding="utf-8")
        for rel, txt in sorted(self.dateien.items()):
            p = ziel / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(txt, encoding="utf-8")
        (ziel / "eingang" / ".gitkeep").touch()

    def besetzung(self):
        """Block B der Marktbeobachtung (spec/MARKT.md): wer hat die Stellen bekommen, die Alex abgesagt wurden?
        Synthetisch und pseudonymisiert: nur rollenrelevante Merkmale, kein Name, kein Link. Erhoben wird zwei bis
        vier Wochen nach der Absage; nicht jede Besetzung ist auffindbar (dann fehlt der Eintrag)."""
        rnd = random.Random(SEED + 2)
        out = []
        for a in sorted(self.apps, key=lambda x: x.get("absage_datum") or ""):
            if a["status"] != "abgesagt" or rnd.random() < 0.15:
                continue
            erhoben = min(dt.date.fromisoformat(a["absage_datum"]) + dt.timedelta(days=rnd.randint(10, 28)), ENDE)
            eigene_branche = rnd.random() < 0.65
            out.append({"pseudonym": f"P{len(out) + 1:03d}", "fall_id": a["id"], "firma": a["firma"], "rolle": a["rolle"],
                        "erhoben_am": erhoben.isoformat(),
                        "jahre_rollentyp": rnd.choice([5, 6, 7, 8, 8, 9, 10, 12]),
                        "vorbranche": F[a["firma"]][1] if eigene_branche else rnd.choice(
                            ["Versicherung", "Bank", "B2B-Software", "Beratung", "Telekommunikation"]),
                        "vorstufe": rnd.choice(["Lead/Head of Product", "Lead/Head of Product", "Senior PO/PM",
                                                "Senior PO/PM", "Senior PO/PM", "Product Owner", "andere Funktion"]),
                        "abschluss": rnd.choice(["Informatik/Technik", "Informatik/Technik", "Wirtschaft", "andere",
                                                 "unbekannt"]),
                        "ki_belege": rnd.random() < 0.6,
                        "wechsel": "intern" if rnd.random() < 0.25 else "extern"})
        return out

    def vorscan_stand(self):
        """Trefferlisten, wie sie der Vorscan fuer den naechsten Morgen-Sweep geholt haette (Fixture-Kanal)."""
        rnd = random.Random(SEED + 1)
        tag = ENDE + dt.timedelta(days=1)
        abfragen = {}
        bekannt = sorted(self.bekannt)
        for kanal, aid, name in KATALOG:
            if kanal != "portal":
                continue
            eintraege = []
            for i in range(rnd.randint(14, 30)):
                if rnd.random() < 0.7:
                    firma, rolle = rnd.choice(bekannt)
                else:
                    rolle, art = gewichtete_rolle(rnd)
                    firma = firma_fuer(rnd, art)[0]
                eintraege.append({"id": f"{aid}-{i:03d}", "firma": firma, "rolle": rolle, "ort": F[firma][2],
                                  "publiziert": (tag - dt.timedelta(days=rnd.choice([0, 0, 1, 2]))).isoformat(),
                                  "url": f"https://jobs.example.org/{aid}/{i:03d}"})
            if aid in ("pt-a-product-owner", "pt-b-ki-produkt"):
                for j, (firma, rolle) in enumerate([("Quendor Versicherungen AG", "Product Owner Schadenportal"),
                                                    ("Telvaro Kommunikation AG", "Product Manager KI-Assistent")][:1 + (aid == "pt-b-ki-produkt")]):
                    eintraege.append({"id": f"{aid}-neu{j}", "firma": firma, "rolle": rolle, "ort": F[firma][2],
                                      "publiziert": tag.isoformat(), "url": f"https://jobs.example.org/{aid}/neu{j}"})
            abfragen[aid] = {"status": "ok", "kanal": kanal, "zeit": f"{tag.isoformat()}T07:45:12", "fenster_s": 86400,
                             "abrufe": 1 + len(eintraege) // 20, "seiten": 1 + len(eintraege) // 20,
                             "treffer": len(eintraege), "eintraege": eintraege}
        return {"zeit": f"{tag.isoformat()}T07:46:03", "quelle": "Fixture-Kanal (Demo, kein echtes Portal)",
                "abfragen": abfragen, "dauer_s": 41, "fehler": 0}


def erzeugen(ziel: Path):
    w = Welt(ziel)
    w.lauf()
    w.notizen()
    w.kandidaten_notizen()
    w.lehren()
    w.schreiben(ziel)
    return w


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pruefen", action="store_true", help="Determinismus pruefen: zweimal erzeugen und vergleichen")
    ap.add_argument("--ziel", type=Path, default=ROOT)
    a = ap.parse_args(argv)
    if a.pruefen:
        with tempfile.TemporaryDirectory() as t1, tempfile.TemporaryDirectory() as t2:
            erzeugen(Path(t1)); erzeugen(Path(t2))
            abw = []
            for f in sorted(Path(t1).rglob("*")):
                if f.is_file():
                    g = Path(t2) / f.relative_to(t1)
                    if not g.exists() or not filecmp.cmp(f, g, shallow=False):
                        abw.append(str(f.relative_to(t1)))
            print("deterministisch" if not abw else f"ABWEICHUNG in {len(abw)} Dateien: {abw[:5]}")
            return 1 if abw else 0
    w = erzeugen(a.ziel)
    st = {}
    for x in w.apps:
        st[x["status"]] = st.get(x["status"], 0) + 1
    ent = {}
    for e in w.gesichtet:
        ent[e["entscheid"]] = ent.get(e["entscheid"], 0) + 1
    print(f"Demo erzeugt: {len(w.sweeps)} Sweeps, {len(w.laeufe)} Abfrage-Laeufe, {len(w.gesichtet)} Sichtungen {ent}")
    print(f"              {len(w.apps)} Faelle {st}, {len(w.dateien)} Dateien")
    return 0


if __name__ == "__main__":
    sys.exit(main())
