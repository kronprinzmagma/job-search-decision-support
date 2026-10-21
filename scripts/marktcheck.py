#!/usr/bin/env python3
"""Marktcheck – monatliche Marktbeobachtung nach spec/MARKT.md (Blöcke A bis D).

Zweck: einmal im Monat festhalten, welche KI-Fähigkeiten die neuen Anzeigen verlangen (Block A), wer die
Stellen bekommt, die Alex wollte (Block B, nur pseudonymisiert und aggregiert), wo Alex' Beleglage dagegen
trägt oder eine Lücke hat (Block C) und wie die eigene Pipeline im selben Zeitraum lief (Block D).

Ehrlich zur Methode: Im Betrieb kodiert das Modell jede Anzeige blind nach spec/ki_kodierschema.json, ein
zweites Modell kodiert mindestens 20 % nach, die Übereinstimmung wird gemessen (--zweitkodierung). Dieses
Skript ist die deterministische Demo-Variante: Es ordnet Sätze aus Aufgaben und Profil per Stichwort den
Kategorien zu. Das macht Ablauf, Tabellen und Schutzregeln prüfbar, ersetzt aber kein Urteil: Wissen gegen
Tätigkeit, Zielzustände oder Umschreibungen ohne Stichwort erkennt es nicht.

Quellen (nur lesen):
  stellen/*/ und eingang/*/   Anzeigen <id>--anzeige--<datum>.md, Datum = Erfassung
  spec/ki_kodierschema.json   Kategorien, Stichworte, KI- und Wunsch-Signale (Regelwerk, eingefroren)
  persona/belege.json         Beleglage der Persona je Kategorie und Vergleichswerte für Block B
  data/besetzung.json         Block B (Demo: erzeugt von scripts/init_demo.py), Format unten
  data/pipeline.json          Block B (Stadium, Absagen) und Block D (über scripts/marktreport.py)
  demo/texte/marktbericht.md  Vorlage des Monatsberichts

Format data/besetzung.json: Liste, ein Eintrag je gefundener Besetzung einer Stelle mit Absage an Alex:
  {"pseudonym": "P001", "fall_id": "<id aus pipeline.json>", "firma": "…", "rolle": "…",
   "erhoben_am": "JJJJ-MM-TT", "jahre_rollentyp": 4, "vorbranche": "Versicherung",
   "vorstufe": "Product Owner | Senior PO/PM | Lead/Head of Product | andere Funktion",
   "abschluss": "Informatik/Technik | Wirtschaft | andere | unbekannt", "ki_belege": true,
   "wechsel": "intern | extern"}
  Unbekanntes bleibt null. Nicht gefundene Stellen stehen nicht in der Datei. Keine Namen, Profil-Links,
  Fotos oder Freitexte über Personen; der Schlüssel Pseudonym → Person liegt ausserhalb des Repos.
  Ausgewiesen wird nur aggregiert: Gruppen und Zellen unter 5 Fällen nicht, ein Median erst ab 10.

Aufruf:
  python3 scripts/marktcheck.py                          # Vormonat, Bericht auf stdout
  python3 scripts/marktcheck.py --monat 2025-03 --schreiben   # nach notes/2025-03_marktbeobachtung.md
  python3 scripts/marktcheck.py --von 2025-03-01 --bis 2025-04-25
  python3 scripts/marktcheck.py --zweitkodierung data/zweitkodierung_2025-03.json   # Kappa je Kategorie
"""
import argparse
import datetime as dt
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from heute import heute  # noqa: E402
from analyse_fit_v2 import wilson  # noqa: E402
import marktreport  # noqa: E402

SCHEMA = ROOT / "spec" / "ki_kodierschema.json"
BELEGE = ROOT / "persona" / "belege.json"
BESETZUNG = ROOT / "data" / "besetzung.json"
VORLAGE = ROOT / "demo" / "texte" / "marktbericht.md"
NOTES = ROOT / "notes"

MIN_GRUPPE = 5      # Block B: kleinere Gruppen und Zellen werden nicht ausgewiesen
MIN_MEDIAN = 10     # Median erst ab so vielen Fällen
MIN_ANTEIL = 10     # Block A: unter so vielen Anzeigen keine Anteile, nur Anzahl
SCHWELLE = 0.10     # Nachfrage, ab der eine Lücke Gewicht hat
KAPPA_ZIEL = 0.70

# Abschnitte, die kodiert werden (Aufgaben und Anforderungen); alles andere ist Firmenteil o. ä.
ABSCHNITT_RE = re.compile(r"aufgabe|profil|anforderung|mitbring|taetigkeit|qualifikation|requirement|"
                          r"responsibilit|about you|you will|what you")
AUSLASSEN_RE = re.compile(r"cv-tailor|benefits|wir bieten|bewerbung")
ANZEIGE_RE = re.compile(r"--anzeige--(\d{4}-\d{2}-\d{2})\.md$")


# --- Kodierung (Block A) -------------------------------------------------------------------------

def norm(s):
    """Klein, Umlaute ausgeschrieben (ä→ae), ohne Akzente: «prüfst» und «pruefst» werden gleich."""
    s = (s or "").lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


def schema_laden(pfad=SCHEMA):
    roh = json.loads(Path(pfad).read_text(encoding="utf-8"))
    terme = []
    for t in roh["ki_signal"]:
        t = norm(t)   # kurze Kürzel (KI, AI, ML) nur als ganzes Wort, längere auch als Wortanfang
        terme.append(r"(?<![a-z0-9])" + re.escape(t) + (r"(?![a-z0-9])" if len(t) <= 5 else ""))
    return {"roh": roh, "signal": re.compile("|".join(terme)),
            "wunsch": [norm(w) for w in roh["wunsch_signal"]],
            "kategorien": [dict(k, _st=[norm(x) for x in k["stichworte"]]) for k in roh["kategorien"]],
            "namen": {k["id"]: k["name"] for k in roh["kategorien"]}}


def kodiere_satz(satz, schema):
    """Kategorien eines Satzes. Ohne KI-Bezug im Satz selbst: keine (Regel 2 des Schemas)."""
    n = norm(satz)
    if not schema["signal"].search(n):
        return set()
    return {k["id"] for k in schema["kategorien"] if any(st in n for st in k["_st"])}


def ist_wunsch(satz, schema):
    n = norm(satz)
    return any(w in n for w in schema["wunsch"])


def relevante_saetze(text):
    """Sätze aus Aufgaben und Profil. Ohne Abschnitts-Überschriften: der ganze Text ohne Kopfzeilen."""
    zeilen = text.splitlines()
    mit_abschnitten = any(z.startswith("## ") for z in zeilen)
    aktiv = not mit_abschnitten
    saetze = []
    for z in zeilen:
        if z.startswith("## "):
            h = norm(z[3:])
            aktiv = bool(ABSCHNITT_RE.search(h)) and not AUSLASSEN_RE.search(h)
            continue
        z = z.strip()
        if not aktiv or not z or z.startswith(("#", "**", ">", "---")):
            continue
        z = re.sub(r"^[-*•]\s+", "", z)
        saetze += [s for s in re.split(r"(?<=[.!?])\s+", z) if s]
    return saetze


def kodiere_anzeige(text, schema):
    """{codes, nur_wunsch, ki_ohne_code}. Mehrfachkodierung erlaubt; keine Kategorie → K00."""
    muss, wunsch, ki_ohne = set(), set(), False
    for s in relevante_saetze(text):
        c = kodiere_satz(s, schema)
        if not c and schema["signal"].search(norm(s)):
            ki_ohne = True
        (wunsch if ist_wunsch(s, schema) else muss).update(c)
    codes = muss | wunsch
    return {"codes": sorted(codes) or ["K00"], "nur_wunsch": sorted(wunsch - muss),
            "ki_ohne_code": ki_ohne and not codes}


def anzeigen(von=None, bis=None):
    """Je Fall die zuerst erfasste Anzeige im Zeitraum: [(id, datum, pfad)]."""
    je_fall = {}
    for wurzel in ("stellen", "eingang"):
        for p in sorted((ROOT / wurzel).glob("*/*--anzeige--*.md")):
            m = ANZEIGE_RE.search(p.name)
            if not m:
                continue
            d = dt.date.fromisoformat(m.group(1))
            fid = p.parent.name
            if fid not in je_fall or d < je_fall[fid][1]:
                je_fall[fid] = (fid, d, p)
    return sorted((x for x in je_fall.values() if (not von or x[1] >= von) and (not bis or x[1] <= bis)),
                  key=lambda x: (x[1], x[0]))


def kodieren(liste, schema):
    return {fid: kodiere_anzeige(p.read_text(encoding="utf-8"), schema) for fid, _, p in liste}


# --- Hilfen ----------------------------------------------------------------------------------------

def prozent(x):
    return f"{x * 100:.0f} %"


def zelle(k):
    """Personenzahl in Block B: unter MIN_GRUPPE wird nicht ausgewiesen."""
    return str(k) if k >= MIN_GRUPPE else f"unter {MIN_GRUPPE}"


def verteilung(werte):
    """«Wert: n · …»; Ausprägungen unter MIN_GRUPPE werden zusammengefasst und nicht beziffert."""
    c = Counter(w for w in werte if w is not None)
    gross = [(w, k) for w, k in sorted(c.items(), key=lambda x: (-x[1], str(x[0]))) if k >= MIN_GRUPPE]
    rest = sum(k for w, k in c.items() if k < MIN_GRUPPE)
    teile = [f"{w}: {k}" for w, k in gross]
    if rest:
        teile.append(f"übrige Ausprägungen: {zelle(rest)}")
    return " · ".join(teile) or "–"


def name(schema, kid):
    return f"{schema['namen'].get(kid, kid)} ({kid})"


# --- Block A: Nachfrage ----------------------------------------------------------------------------

def tabelle_nachfrage(schema, kod, vormonat):
    n = len(kod)
    ids = [k["id"] for k in schema["kategorien"]]
    z = ["| Kategorie | Anzeigen | Anteil | 95 %-Wilson | davon nur Wunsch | Vormonat | Beispiele |",
         "|---|---:|---:|---|---:|---:|---|"]
    for kid in ids:
        treffer = [f for f, k in kod.items() if kid in k["codes"]]
        wunsch = sum(1 for f in treffer if kid in kod[f]["nur_wunsch"])
        k = len(treffer)
        if n >= MIN_ANTEIL:
            lo, hi = wilson(k, n)
            anteil, wi = prozent(k / n), f"{lo * 100:.0f}–{hi * 100:.0f} %"
        else:
            anteil, wi = "–", "–"
        vm = "–"
        if vormonat is not None and len(vormonat) >= MIN_ANTEIL:
            vm = prozent(sum(1 for x in vormonat.values() if kid in x["codes"]) / len(vormonat))
        bsp = ", ".join(f"`{f}`" for f in treffer[:2]) or "–"
        z.append(f"| {name(schema, kid)} | {k} | {anteil} | {wi} | {wunsch} | {vm} | {bsp} |")
    mit_ki = sum(1 for x in kod.values() if x["codes"] != ["K00"])
    ohne = sum(1 for x in kod.values() if x["ki_ohne_code"])
    z += ["", f"- **Anzeigen mit KI-Anforderung:** {mit_ki} von {n} (mindestens eine Kategorie K01–K09).",
          f"- **KI erwähnt, keiner Kategorie zugeordnet:** {ohne} (im Betrieb: Code «NEU» prüfen)."]
    if n < MIN_ANTEIL:
        z.append(f"- Unter {MIN_ANTEIL} Anzeigen: keine Anteile, nur Anzahl.")
    z.append("- Wilson-Intervalle sind eine Untergrenze der Unsicherheit, nicht ihr Mass: Die Anzeigen stammen "
             "aus den eigenen Suchbegriffen und Kanälen, nicht aus einer Zufallsstichprobe.")
    return "\n".join(z), mit_ki


# --- Block B: Besetzung (pseudonymisiert, aggregiert) -----------------------------------------------

def branche_der_stelle(fall):
    """Branche aus dem Fall (Feld «branche»), sonst aus der Demo-Welt; unbekannt bleibt unbekannt."""
    if fall.get("branche"):
        return fall["branche"]
    try:
        import init_demo
        return init_demo.F.get(fall.get("firma"), (None, None))[1]
    except ImportError:
        return None


def tabelle_besetzung(besetzung, faelle, belege, bis):
    """Block B nur aggregiert: Gruppen und Zellen unter MIN_GRUPPE werden nicht ausgewiesen."""
    if besetzung is None:
        return "Keine Besetzungsdaten (`data/besetzung.json` fehlt)."
    je_fall = {f["id"]: f for f in faelle}
    gesucht = [f for f in faelle if f.get("status") == "abgesagt"]
    g = [dict(b, _fall=je_fall.get(b.get("fall_id"), {})) for b in besetzung
         if str(b.get("erhoben_am") or "")[:10] <= bis.isoformat()]
    for b in g:
        b["_stadium"] = ("gespraech" if "einladung" in marktreport.ereignisse(b["_fall"]) else "dossier") \
            if b["_fall"] else "unbekannt"
        b["_branche"] = branche_der_stelle(b["_fall"] or {"firma": b.get("firma")})
    ohne = max(len(gesucht) - len(g), 0)
    kopf = (f"Stellen mit Absage: {len(gesucht)} · Besetzung gefunden (erhoben bis {bis.isoformat()}): "
            f"{zelle(len(g))} · ohne Fund (offen oder nicht auffindbar, nicht geraten): {ohne}.")
    n = len(g)
    if n < MIN_GRUPPE:
        return kopf + f"\n\nZu wenig Fälle für eine Auswertung: berichtet wird erst ab {MIN_GRUPPE} gefundenen Besetzungen."
    v = belege["vergleich"]
    jahre = sorted(b["jahre_rollentyp"] for b in g if b.get("jahre_rollentyp") is not None)
    mehr = sum(1 for j in jahre if j > v["jahre_rollentyp"])
    techn = sum(1 for b in g if b.get("abschluss") == "Informatik/Technik")
    ki = sum(1 for b in g if b.get("ki_belege"))
    mit_branche = [b for b in g if b["_branche"]]
    branche = sum(1 for b in mit_branche if b.get("vorbranche") == b["_branche"])
    alex_branche = sum(1 for b in mit_branche if b["_branche"] in v["branchen"])
    intern = sum(1 for b in g if b.get("wechsel") == "intern")

    def mehrheit(k, basis, text_ja, text_nein="kein Abstand erkennbar"):
        if 0 < k < MIN_GRUPPE:
            return "nicht auswertbar (Zelle unter 5)"
        return text_ja if k * 2 > basis else text_nein

    z = [kopf, "", "| Merkmal | Gruppe (n = %d) | Alex | Abstand |" % n, "|---|---|---|---|"]
    if len(jahre) >= MIN_MEDIAN:
        m = len(jahre) // 2
        median = jahre[m] if len(jahre) % 2 else (jahre[m - 1] + jahre[m]) / 2
        z.append(f"| Jahre im Rollentyp | Median {median:g} · mehr als Alex: {zelle(mehr)} | {v['jahre_rollentyp']} "
                 f"| Alex {v['jahre_rollentyp'] - median:+g} Jahre gegenüber dem Median |")
    else:
        z.append(f"| Jahre im Rollentyp | mehr als Alex: {zelle(mehr)} (Median erst ab {MIN_MEDIAN}) "
                 f"| {v['jahre_rollentyp']} | {mehrheit(mehr, len(jahre), 'Gruppe meist erfahrener')} |")
    z += [f"| Vorherige Stufe | {verteilung(b.get('vorstufe') for b in g)} | {v['vorstufe']} | – |",
          f"| Abschluss Informatik/Technik | {zelle(techn)} | {v['abschluss']} "
          f"| {mehrheit(techn, n, 'Lücke: Mehrheit mit technischem Abschluss')} |",
          f"| KI-Belege im Profil | {zelle(ki)} | {'ja' if v['ki_belege'] else 'nein'} "
          f"| {mehrheit(ki, n, 'gleichauf' if v['ki_belege'] else 'Lücke: Mehrheit mit KI-Belegen')} |"]
    if len(mit_branche) >= MIN_GRUPPE:
        abstand = (mehrheit(branche, len(mit_branche), "Lücke: Branchennähe")
                   if alex_branche * 2 <= len(mit_branche) else "kein Abstand erkennbar")
        z.append(f"| Aus der Branche der Stelle | {zelle(branche)} von {len(mit_branche)} "
                 f"| {alex_branche} von {len(mit_branche)} | {abstand} |")
    z.append(f"| Interner Wechsel | {zelle(intern)} | {v['wechsel']} "
             f"| {mehrheit(intern, n, 'strukturell: intern besetzt, über das Profil nicht erreichbar')} |")
    st = Counter(b["_stadium"] for b in g)
    if min(st.get("gespraech", 0), st.get("dossier", 0)) < MIN_GRUPPE:
        z += ["", "- Nach Stadium (Absage nach Gespräch gegen Dossier-Absage): zu wenig Fälle für einen Vergleich."]
    else:
        z += ["", f"- Nach Stadium: Absage nach Gespräch {st['gespraech']}, nach Dossier {st['dossier']}."]
    z.append("- Ein gefundenes Profil zeigt, wer genommen wurde, nicht warum. Interne Besetzungen bleiben oft unsichtbar.")
    return "\n".join(z)


# --- Block C: Position -----------------------------------------------------------------------------

STATUS_TEXT = {"belegt": "belegt", "teilweise": "teilweise", "luecke": "Lücke"}


def einordnung(status, anteil):
    if status == "belegt":
        return "trägt"
    if status == "teilweise":
        return "Beleg schärfen" if anteil >= SCHWELLE else "beobachten"
    return "Lücke mit Gewicht" if anteil >= SCHWELLE else "Lücke, kaum verlangt"


def tabelle_position(schema, kod, belege):
    n = len(kod) or 1
    z = ["| Kategorie | Nachfrage | Beleglage Alex | Einordnung |", "|---|---:|---|---|"]
    massnahmen = []
    for k in schema["kategorien"]:
        kid = k["id"]
        if kid == "K00":
            continue
        b = belege["kategorien"].get(kid, {"status": "luecke", "beleg": "nicht erfasst", "massnahme": ""})
        treffer = sum(1 for x in kod.values() if kid in x["codes"])
        wunsch = sum(1 for x in kod.values() if kid in x["nur_wunsch"])
        e = einordnung(b["status"], treffer / n)
        z.append(f"| {name(schema, kid)} | {treffer} von {len(kod)} | {STATUS_TEXT[b['status']]}: {b['beleg']} | {e} |")
        if e in ("Lücke mit Gewicht", "Beleg schärfen") and b.get("massnahme"):
            massnahmen.append((-treffer, kid, f"- **{k['name']}** ({e}; verlangt in {treffer} von {len(kod)} "
                                              f"Anzeigen, davon {wunsch} nur als Wunsch): {b['massnahme']}"))
    m = [x[2] for x in sorted(massnahmen)] or ["- Keine: im Zeitraum keine Lücke mit Gewicht."]
    m.append("- Vor jeder Massnahme die Nullmessung festhalten (spec/MARKT.md). Entscheid bei Alex.")
    return "\n".join(z), "\n".join(m)


# --- Block D: Eigenanalyse -------------------------------------------------------------------------

def tabelle_eigen(von, bis):
    _, faelle = marktreport.laden()
    im = [f for f in faelle if f.get("datum") and von.isoformat() <= f["datum"][:10] <= bis.isoformat()]
    bew = [f for f in im if marktreport.beworben(f)]
    einl = [f for f in bew if "einladung" in marktreport.ereignisse(f) or f.get("status") in ("gespraech", "angebot")]
    absage = [f for f in bew if f.get("status") == "abgesagt"]
    ohne = [f for f in absage if "einladung" not in marktreport.ereignisse(f)]
    z = ["| Stufe | Anzahl |", "|---|---:|",
         f"| Fälle im Zeitraum (Volltext bewertet) | {len(im)} |",
         f"| aussortiert | {sum(1 for f in im if f.get('status') == 'aussortiert')} |",
         f"| Entscheid offen (vorgelegt, draft) | {sum(1 for f in im if f.get('status') in ('vorgelegt', 'draft'))} |",
         f"| beworben | {len(bew)} |", f"| Einladung zum Gespräch | {len(einl)} |",
         f"| Absage (davon ohne Gespräch) | {len(absage)} ({len(ohne)}) |",
         f"| Angebot | {sum(1 for f in bew if f.get('status') == 'angebot')} |"]
    gruende = Counter()
    for f in im:
        if f.get("status") == "aussortiert":
            b = marktreport.blocker(f.get("begruendung", ""))
            gruende[b[0] if b else "nicht klassifiziert"] += 1
    if gruende:
        z += ["", "Häufigste Ausschlussgründe im Volltext: "
              + " · ".join(f"{g} {k}" for g, k in gruende.most_common(3)) + "."]
    z.append("Kohorte = Fälle mit Datum im Zeitraum; Ergebnisse fliessen nach. Nur abgeschlossene Kohorten vergleichen.")
    return "\n".join(z)


# --- Zweitkodierung --------------------------------------------------------------------------------

def uebereinstimmung(a, b, ids):
    """Cohen-Kappa je Kategorie über das Vorkommen je Anzeige und mittlere Jaccard-Ähnlichkeit."""
    gemeinsam = sorted(set(a) & set(b))
    n = len(gemeinsam)
    kappa = {}
    for kid in ids:
        x = [kid in a[f] for f in gemeinsam]
        y = [kid in b[f] for f in gemeinsam]
        if not n:
            kappa[kid] = None
            continue
        po = sum(1 for i, j in zip(x, y) if i == j) / n
        pa, pb = sum(x) / n, sum(y) / n
        pe = pa * pb + (1 - pa) * (1 - pb)
        kappa[kid] = 1.0 if pe == 1 else (po - pe) / (1 - pe)
    jac = [len(set(a[f]) & set(b[f])) / len(set(a[f]) | set(b[f])) if set(a[f]) | set(b[f]) else 1.0
           for f in gemeinsam]
    return {"n": n, "kappa": kappa, "jaccard": sum(jac) / n if n else None}


# --- Ablauf ----------------------------------------------------------------------------------------

def zeitraum(a):
    if a.von or a.bis:
        von = dt.date.fromisoformat(a.von) if a.von else dt.date(1900, 1, 1)
        bis = dt.date.fromisoformat(a.bis) if a.bis else heute()
        return von, bis, f"{von.isoformat()}_bis_{bis.isoformat()}", None
    if a.monat:
        von = dt.date.fromisoformat(a.monat + "-01")
    else:
        von = (heute().replace(day=1) - dt.timedelta(days=1)).replace(day=1)
    bis = (von.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
    vm_bis = von - dt.timedelta(days=1)
    return von, bis, von.strftime("%Y-%m"), (vm_bis.replace(day=1), vm_bis)


def bericht(a):
    if not VORLAGE.exists():
        sys.exit(f"Vorlage fehlt: {VORLAGE.relative_to(ROOT)}")
    schema = schema_laden()
    belege = json.loads(BELEGE.read_text(encoding="utf-8"))
    von, bis, label, vm = zeitraum(a)
    kod = kodieren(anzeigen(von, bis), schema)
    vormonat = kodieren(anzeigen(*vm), schema) if vm else None
    nachfrage, _ = tabelle_nachfrage(schema, kod, vormonat)
    position, massnahmen = tabelle_position(schema, kod, belege)
    besetzung = json.loads(BESETZUNG.read_text(encoding="utf-8")) if BESETZUNG.exists() else None
    _, faelle = marktreport.laden()
    text = VORLAGE.read_text(encoding="utf-8").format(
        monat=label, zeitraum=f"{von.isoformat()} bis {bis.isoformat()}", n_anzeigen=len(kod),
        tabelle_nachfrage=nachfrage, tabelle_besetzung=tabelle_besetzung(besetzung, faelle, belege, bis),
        tabelle_position=position, tabelle_eigen=tabelle_eigen(von, bis), massnahmen=massnahmen)
    return label, text


def main(argv=None):
    ap = argparse.ArgumentParser(description="Monatliche Marktbeobachtung (spec/MARKT.md)")
    ap.add_argument("--monat", help="JJJJ-MM (Standard: Vormonat)")
    ap.add_argument("--von", help="JJJJ-MM-TT, statt --monat")
    ap.add_argument("--bis", help="JJJJ-MM-TT, statt --monat")
    ap.add_argument("--schreiben", action="store_true", help="nach notes/<monat>_marktbeobachtung.md schreiben")
    ap.add_argument("--zweitkodierung", help="JSON {fall_id: [Kategorie-IDs]} gegen die Stichwort-Kodierung messen")
    a = ap.parse_args(argv)

    if a.zweitkodierung:
        schema = schema_laden()
        zweit = json.loads(Path(a.zweitkodierung).read_text(encoding="utf-8"))
        erst = {f: k["codes"] for f, k in kodieren(anzeigen(), schema).items()}
        ids = [k["id"] for k in schema["kategorien"]]
        u = uebereinstimmung(erst, zweit, ids)
        print(f"Zweitkodierung: {u['n']} gemeinsame Anzeigen, mittlere Jaccard-Ähnlichkeit "
              f"{u['jaccard']:.2f}" if u["n"] else "Zweitkodierung: keine gemeinsamen Anzeigen")
        for kid in ids:
            k = u["kappa"][kid]
            if k is not None:
                hinweis = "" if k >= KAPPA_ZIEL else "  → nur als Spanne beider Kodierer berichten"
                print(f"  {kid} {schema['namen'][kid]:<38} Kappa {k:5.2f}{hinweis}")
        return 0

    label, text = bericht(a)
    if a.schreiben:
        NOTES.mkdir(exist_ok=True)
        ziel = NOTES / f"{label}_marktbeobachtung.md"
        ziel.write_text(text, encoding="utf-8")
        print(f"Geschrieben: {ziel.relative_to(ROOT)}")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
