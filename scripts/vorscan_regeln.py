"""Firmen-, Orts- und Titelregeln fuer den Vorscan (Kosten sparen ohne Qualitaetseinbusse).

Bildet NUR die Rauschregeln ab, die spec/SWEEP.md «Listenebene» erlaubt: Firmen-Ausschluss der Persona
(Gluecksspiel), Vermittler, Beratung/Agentur, Distanz laut Ortstabelle, Junior/Praktikum, physisches Produkt,
Engineering- und Entwicklerrollen, offensichtliche Nicht-Rollen. Alles Unklare entscheidet weiterhin das
Modell. Schutzwoerter (SCHUTZ) im Titel heissen immer: Modell entscheidet (Ausnahme: Junior/Praktikum, das
ist nie eine Zielrolle).

Reihenfolge in `entscheid`: erst was am Arbeitgeber oder Ort haengt (titelunabhaengig), dann Junior, dann
die Schutzwoerter, zuletzt die Titelregeln.

Validierung gegen das ganze Sichtungs-Log: `python3 scripts/vorscan.py pruefen` — Pflicht nach jeder
Regelaenderung (0 faelschlich vorgefilterte Kandidaten-, Volltext- und Offen-Faelle).
"""
import re
import unicodedata
from pathlib import Path

PRESCREEN = Path(__file__).resolve().parent.parent / "spec" / "PRESCREEN.md"


def n(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " " + re.sub(r"[^a-z0-9]+", " ", s) + " "


# Firmen-Ausschluss der Persona: spec/PRESCREEN.md nennt die Branche, hier steht die Erkennung im
# Firmennamen. (Grund, Branche wie in PRESCREEN.md, Regex). `vorscan.py pruefen` meldet, wenn PRESCREEN.md
# eine Branche nennt, die hier fehlt, oder wenn ein im Log so aussortierter Arbeitgeber nicht erkannt wird.
FIRMEN_AUS = [
    ("Firmen-Ausschluss Glücksspiel", "Glücksspiel",
     r" (\w*casino\w*|spielbank\w*|lotterie\w*|lotto\w*|\w*wetten|sportwett\w*|wettanbiet\w*|glucksspiel\w*|"
     r"gluecksspiel\w*|poker\w*|betting|gambling|spielora) "),
]
VERMITTLER_FIRMA = (r" (personal|personalberatung|personaldienst\w*|personalvermittlung|stellenvermittlung|staffing|"
                    r"recruit\w*|headhunt\w*|executive search|temporar\w*|talent\w*|jobvermittl\w*|interim management) ")
BERATUNG_FIRMA = r" (\w*consulting|consultants?|\w*beratung|beratungs\w*|advisory|\w*agentur|agency|digitalagentur) "
PHYSISCH_FIRMA = (r" (bau|hochbau|tiefbau|holzbau|bauunternehm\w*|industrie|industries|maschinen\w*|\w*maschinenbau|"
                  r"anlagenbau|lebensmittel\w*|nahrungsmittel\w*|food|textil\w*|moebel\w*|mobel\w*) ")

# Junior/Praktikum/Ausbildung: nie eine Zielrolle (Ausschluss 1), gilt auch bei Schutzwoertern
JUNIOR = (" (junior|praktik\\w*|praktikum|intern|internship|lernende\\w*|lehrstelle|lehre als|ausbildung|"
          "werkstudent\\w*|trainee|azubi|student\\w*|stage|stagiaire|einsteiger\\w*|berufseinst\\w*) ")

# eindeutige Nicht-Rollen im Titel (greifen nur ohne Schutzwort)
TITEL_NEG = [
    ("Engineering-/Entwicklerrolle",
     r" (\w*engineer|\w*engineers|\w*engineering|\w*architect|\w*architekt\w*|entwickler\w*|\w*developer|programmier\w*|"
     r"\w*ingenieur\w*|devops|sre|site reliability|backend|frontend|fullstack|full stack|data scientist|tester|"
     r"informatiker\w*|systemadministrator\w*) "),
    ("Physisches Produkt (Hardware, Maschinen, Lebensmittel)",
     r" (hardware|maschinen\w*|lebensmittel\w*|nahrungsmittel\w*|textil\w*|bauleit\w*|bauprojekt\w*|\w*techniker\w*|"
     r"elektro\w*|mechani\w*|produktion\w*|fertigung\w*) "),
    ("Nicht-Rolle: kein Produktmandat (Scrum, Analyse, Design, Projektleitung)",
     r" (scrum master|agile coach|business analyst\w*|requirements|\w*designer\w*|ux|ui|projektleiter\w*|"
     r"projektleiterin|projektleitung|projektmanager\w*|project manager|pmo|release manager|service manager|"
     r"test manager|qualitatsmanag\w*) "),
    ("Nicht-Rolle: Fachfunktion ohne Produktbezug (Finanzen, Verkauf, HR, Administration)",
     r" (buchhalt\w*|controller\w*|controlling|treuhand\w*|accountant|payroll|lohn\w*|recruiter|hr business partner|"
     r"personalfach\w*|jurist\w*|legal counsel|sachbearbeiter\w*|kaufmann|kauffrau|administrat\w*|sekretar\w*|"
     r"assistent\w*|assistant|verkauf\w*|aussendienst\w*|sales|key account\w*|account manager|kundenberater\w*|"
     r"kundendienst\w*|callcenter|call center|filialleit\w*|logisti\w*|lager\w*|chauffeur\w*) "),
]
# Schutzwoerter: kommt eines davon im Titel vor, entscheidet nie das Skript, sondern das Modell.
# Abgeleitet aus den Zielrollen in persona/PROFILE.md (Produktverantwortung, Plattform, KI).
SCHUTZ = (r" (products?|product owner\w*|produkt(?!ion)\w*|owner|plattform\w*|platform\w*|ki|ai|genai|roadmap|"
          r"backlog|innovation|portfolio|strateg\w*|transformation|self service|chapter|tribe) ")


def distanz_orte():
    """Orte mit Pendelzeit ueber 60 Min. (Ausschluss 2). Einzige Quelle: Ortstabelle in spec/PRESCREEN.md,
    Spalte «über 60 Min.». Fehlt die Tabelle: leere Menge (vorscan.py pruefen meldet es)."""
    try:
        txt = PRESCREEN.read_text(encoding="utf-8")
    except OSError:
        return frozenset()
    zellen = lambda l: [c.strip() for c in l.strip().strip("|").split("|")]
    for block in re.findall(r"(?:^\|.*\n?)+", txt, re.M):          # zusammenhaengende Tabellen
        zeilen = block.strip().splitlines()
        if len(zeilen) < 3 or not set("".join(zellen(zeilen[1]))) <= set("-: "):
            continue                                                # keine Kopfzeile mit Trennzeile
        spalte = next((j for j, c in enumerate(zellen(zeilen[0])) if re.search(r"(über|ueber) 60 min", c, re.I)), None)
        if spalte is None:
            continue
        orte = {n(o).strip() for z in zeilen[2:] if len(zellen(z)) > spalte for o in zellen(z)[spalte].split(",")}
        return frozenset(orte - {""})
    return frozenset()


DISTANZ_ORTE = distanz_orte()


def entscheid(firma, titel, ort, vermittler_bekannt=frozenset(), distanz_bekannt=frozenset()):
    """("vorfilter", Grund) oder ("unklar", ""). vermittler_bekannt/distanz_bekannt: aus dem Log gelernte
    Firmen und Orte (vorscan.gelernte_listen), normiert mit n()."""
    nf, nt, no = n(firma), n(titel), n(ort)
    for grund, _branche, rx in FIRMEN_AUS:
        if re.search(rx, nf):
            return ("vorfilter", grund)
    if nf.strip() in vermittler_bekannt or re.search(VERMITTLER_FIRMA, nf):
        return ("vorfilter", "Vermittler-Inserat (Personalvermittlung, kein Arbeitgeber)")
    if re.search(BERATUNG_FIRMA, nf):
        return ("vorfilter", "Ausschluss 4 (Beratung/Agentur)")
    if no.strip() and (no.strip() in DISTANZ_ORTE or no.strip() in distanz_bekannt):
        return ("vorfilter", f"Ausschluss 2 (Distanz): {ort.strip()}, Pendelzeit ueber 60 Min. (Ortstabelle)")
    if re.search(JUNIOR, nt):
        return ("vorfilter", "Ausschluss 1 (Junior/Praktikum)")
    if re.search(PHYSISCH_FIRMA, nf):
        return ("vorfilter", "Physisches Produkt (Arbeitgeber aus Bau, Industrie oder Lebensmitteln)")
    if re.search(SCHUTZ, nt):
        return ("unklar", "")
    for grund, rx in TITEL_NEG:
        if re.search(rx, nt):
            return ("vorfilter", grund)
    return ("unklar", "")
