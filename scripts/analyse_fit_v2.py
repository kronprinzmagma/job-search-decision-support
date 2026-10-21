#!/usr/bin/env python3
"""Auswertung des Fit-Rasters v2 (spec/PRESCREEN.md, Schritt 2) gegen das erreichte Selektionsergebnis.

Zielgrösse Y: Einladung zum Erstgespräch (1) vs. Dossier-Absage ohne Kontakt (0), Feld fit_v2.ergebnis.
Prädiktoren: A = Anforderungs-Fit (0-2), B = Domänen-/Aktivitätsnähe (0-2), Kanal (+/0/-), Verdikt v2.
Einzige Quelle: data/pipeline.json (Feld fit_v2 je Fall).

Reine Standardbibliothek — kein scipy. Fisher-Exakt und Wilson-Intervalle selbst gerechnet.
Aufruf:
  python3 scripts/analyse_fit_v2.py              # Auswertung auf stdout
  python3 scripts/analyse_fit_v2.py --schreiben  # zusätzlich nach data/analyse_v2/auswertung.md
"""
import json, math, sys
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIPE = ROOT / "data" / "pipeline.json"
OUT = ROOT / "data" / "analyse_v2" / "auswertung.md"

# Ergebnis-Werte (fit_v2.ergebnis) -> Y. Alles andere (offen, leer) gilt als zensiert.
Y_WERT = {"einladung": 1, "erstgespraech": 1, "absage-dossier": 0, "dossier": 0}
Z_95, Z_POWER_80 = 1.96, 0.8416


# --- Statistik-Hilfen -------------------------------------------------------
def wilson(k, n, z=Z_95):
    """Wilson-Konfidenzintervall für k Erfolge in n Versuchen."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def fisher(a, b, c, d):
    """Zweiseitiger exakter Test für [[a,b],[c,d]] (Summe aller Tafeln, die höchstens so wahrscheinlich sind)."""
    n = a + b + c + d; r1, r2, c1 = a + b, c + d, a + c
    if n == 0:
        return 1.0
    def pr(x):
        return (math.comb(r1, x) * math.comb(r2, c1 - x)) / math.comb(n, c1)
    obs = pr(a); tot = 0.0
    lo, hi = max(0, c1 - r2), min(r1, c1)
    for x in range(lo, hi + 1):
        p = pr(x)
        if p <= obs * (1 + 1e-9) + 1e-15:
            tot += p
    return min(1.0, tot)


def fallzahl_je_gruppe(p1, p2, z_a=Z_95, z_b=Z_POWER_80):
    """Nötige Fälle je Gruppe für 80 % Power bei alpha 0.05 (Normalapproximation, zwei Anteile)."""
    if p1 == p2:
        return None
    pq = (p1 + p2) / 2
    zaehler = (z_a * math.sqrt(2 * pq * (1 - pq)) + z_b * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return math.ceil(zaehler / (p1 - p2) ** 2)


def tab(rows, key):
    out = {}
    for r in rows:
        out.setdefault(r[key], [0, 0])[r["Y"]] += 1
    return out


def zeile(label, k, n):
    lo, hi = wilson(k, n)
    q = f"{k}/{n}" if n else "0/0"
    pct = f"{100*k/n:5.1f}%" if n else "    —"
    return f"| {label:24s} | {q:>6s} | {pct} | {100*lo:4.1f}–{100*hi:4.1f}% |"


def kontrast(rows, wahr):
    """(k1, n1, k0, n0, p) für «wahr» gegen den Rest."""
    hi_ = [r for r in rows if wahr(r)]; lo_ = [r for r in rows if not wahr(r)]
    k1, k0 = sum(r["Y"] for r in hi_), sum(r["Y"] for r in lo_)
    return k1, len(hi_), k0, len(lo_), fisher(k1, len(hi_) - k1, k0, len(lo_) - k0)


def quote(k, n):
    return f"{k}/{n} = {100*k/n:.1f}%" if n else "0/0"


# --- Population -------------------------------------------------------------
def population(D):
    rows, nicht_kodierbar = [], 0
    for a in D["applications"]:
        f = a.get("fit_v2")
        if not f:
            continue
        if f.get("A") is None:
            nicht_kodierbar += 1
            continue
        y = "zurueckgezogen" if a.get("status") == "zurueckgezogen" else (f.get("ergebnis") or "offen")
        rows.append(dict(id=a["id"], firma=a["firma"], A=f["A"], B=f["B"], kanal=f.get("kanal") or "unbekannt",
                         verdikt=f.get("verdikt") or "unbekannt", y=y, ex_ante=bool(f.get("ex_ante")),
                         monat=(a.get("datum_eingereicht") or f.get("datum") or a.get("datum") or "unbekannt")[:7]))
    entschieden = [r for r in rows if r["y"] in Y_WERT]
    for r in entschieden:
        r["Y"] = Y_WERT[r["y"]]
    return rows, entschieden, nicht_kodierbar


def auswertung(D):
    rows, entschieden, nicht_kodierbar = population(D)
    L = []
    p = lambda s="": L.append(s)

    p("# Auswertung Fit-Raster v2 — Anforderungs-Fit und Domänennähe gegen Einladungsergebnis")
    p()
    p("Generiert aus `data/pipeline.json` · `scripts/analyse_fit_v2.py`")
    p()
    p("## Population")
    p()
    p(f"- Kodierte Bewerbungen (v2): **{len(rows)}**, davon ex ante (vor dem Versand) kodiert: {sum(r['ex_ante'] for r in rows)}")
    p(f"- Davon mit arbeitgeberseitig entschiedenem Ergebnis: **{len(entschieden)}**")
    p(f"  - Einladung zum Erstgespräch: **{sum(r['Y'] for r in entschieden)}**")
    p(f"  - Dossier-Absage ohne Kontakt: **{sum(1 - r['Y'] for r in entschieden)}**")
    p(f"- Ausgeschlossen: {sum(1 for r in rows if r['y'] == 'zurueckgezogen')} zurückgezogen (eigener Abbruch, kein "
      f"Arbeitgeber-Urteil), {sum(1 for r in rows if r['y'] not in Y_WERT and r['y'] != 'zurueckgezogen')} offen (zensiert)")
    p(f"- Nicht kodierbar (Anzeige fehlt, A leer): {nicht_kodierbar}")
    p()
    base_k = sum(r["Y"] for r in entschieden); base_n = len(entschieden)
    if base_n < 2 or base_k in (0, base_n):
        p("**Zu wenig entschiedene Fälle oder keine Varianz im Ergebnis — keine Auswertung möglich.**")
        return L
    lo, hi = wilson(base_k, base_n)
    p(f"**Basisrate Einladung: {base_k}/{base_n} = {100*base_k/base_n:.1f}%** (95%-Wilson: {100*lo:.1f}–{100*hi:.1f}%)")
    p()

    # --- H1: B
    p("## H1 — Domänen- und Aktivitätsnähe (B)")
    p()
    p("**Hypothese:** Bei Angebotsüberhang entscheidet, wer die Branche oder die Tätigkeit schon gemacht hat.")
    p()
    p("| B (Domänennähe) | Einlad. | Quote | 95%-KI |")
    p("|---|---|---|---|")
    tB = tab(entschieden, "B")
    for b in (2, 1, 0):
        n0, n1 = tB.get(b, [0, 0]); p(zeile({2: "2 einschlägig", 1: "1 benachbart", 0: "0 keine Nähe"}[b], n1, n0 + n1))
    kb = kontrast(entschieden, lambda r: r["B"] == 2)
    p()
    p(f"**Fisher exakt (B=2 vs. B≤1): p = {kb[4]:.4f}**")

    # --- H2: A
    p()
    p("## H2 — Anforderungs-Fit (A)")
    p()
    p("| A (Anforderungs-Fit) | Einlad. | Quote | 95%-KI |")
    p("|---|---|---|---|")
    tA = tab(entschieden, "A")
    for a_ in (2, 1, 0):
        n0, n1 = tA.get(a_, [0, 0]); p(zeile({2: "2 alle Muss belegt", 1: "1 zwei bis drei Lücken", 0: "0 Kernlücke"}[a_], n1, n0 + n1))
    ka = kontrast(entschieden, lambda r: r["A"] == 2)
    p()
    p(f"**Fisher exakt (A=2 vs. A≤1): p = {ka[4]:.4f}**")
    if ka[1] and ka[3]:
        q1, q0 = ka[0] / ka[1], ka[2] / ka[3]
        p()
        p(f"Risikodifferenz **{100*(q1-q0):+.1f} Prozentpunkte**" + (f" · Risk Ratio **{q1/q0:.2f}**" if q0 else ""))
        nz = fallzahl_je_gruppe(q1, q0)
        if nz:
            p()
            p(f"**Power:** Für die beobachteten Quoten wären bei 80% Power und alpha=0.05 rund **{nz} Fälle pro Gruppe** "
              f"nötig (vorhanden: {ka[1]} vs. {ka[3]})."
              + ("" if min(ka[1], ka[3]) >= nz else
                 " Der Unterschied ist trotz kleiner Gruppe signifikant; die Effektgrösse bleibt aber unsicher "
                 "(Intervalle oben)." if ka[4] < 0.05 else
                 " Die Studie ist zu klein, um diesen Effekt statistisch abzusichern."))

    # --- H3: Zweistufigkeit
    p()
    p("## H3 — Zweistufiges Modell: wirkt B erst bei erfülltem A?")
    p()
    p("| Zelle | Einlad. | Quote | 95%-KI |")
    p("|---|---|---|---|")
    for a_, b_ in product((2, 1, 0), (2, 1, 0)):
        sub = [r for r in entschieden if r["A"] == a_ and r["B"] == b_]
        if sub:
            p(zeile(f"A={a_}, B={b_}", sum(r["Y"] for r in sub), len(sub)))
    p()
    p("**B-Effekt, geschichtet nach A:**")
    p()
    p("| A | B=2 | B≤1 | Differenz | Fisher p |")
    p("|---|---|---|---|---|")
    for a_ in (2, 1, 0):
        sub = [r for r in entschieden if r["A"] == a_]
        k1, n1_, k0, n0_, pv = kontrast(sub, lambda r: r["B"] == 2)
        if n1_ and n0_:
            p(f"| A={a_} | {k1}/{n1_} ({100*k1/n1_:.0f}%) | {k0}/{n0_} ({100*k0/n0_:.0f}%) | {100*k1/n1_-100*k0/n0_:+.0f} pp | {pv:.4f} |")

    # --- H4: Verdikt v2
    p()
    p("## H4 — Trennschärfe des v2-Verdikts")
    p()
    p("| Verdikt v2 | Einlad. | Quote | 95%-KI |")
    p("|---|---|---|---|")
    tV = tab(entschieden, "verdikt")
    for v in ("hoch", "mittel", "tief"):
        n0, n1 = tV.get(v, [0, 0]); p(zeile(v, n1, n0 + n1))
    kv = kontrast(entschieden, lambda r: r["verdikt"] == "hoch")
    p()
    p(f"**Fisher exakt (hoch vs. mittel+tief): p = {kv[4]:.4f}**")

    # --- H5: Kanal
    p()
    p("## H5 — Kanal als Confounder")
    p()
    p("| Kanal | Einlad. | Quote | 95%-KI |")
    p("|---|---|---|---|")
    tK = tab(entschieden, "kanal")
    for k_ in ("+", "0", "-", "unbekannt"):
        n0, n1 = tK.get(k_, [0, 0])
        if n0 + n1:
            p(zeile({"+": "+ Empfehlung/Kontakt", "0": "0 Portal", "-": "− Massenkanal", "unbekannt": "nicht dokumentiert"}[k_], n1, n0 + n1))
    kp = tK.get("+", [0, 0]); km = tK.get("-", [0, 0])
    if sum(kp) and sum(km):
        p()
        p(f"**Fisher exakt (Kanal+ vs. Kanal−): p = {fisher(kp[1], kp[0], km[1], km[0]):.4f}**")
    p()
    p("**Kreuzung A × Kanal** (prüft, ob der A-Effekt nur den Kanal spiegelt):")
    p()
    p("| | Kanal + | Kanal 0 | Kanal − |")
    p("|---|---|---|---|")
    for a_ in (2, 1, 0):
        z = []
        for k_ in ("+", "0", "-"):
            sub = [r for r in entschieden if r["A"] == a_ and r["kanal"] == k_]
            z.append(f"{sum(r['Y'] for r in sub)}/{len(sub)}" if sub else "—")
        p(f"| A={a_} | {z[0]} | {z[1]} | {z[2]} |")

    # --- Einzelfälle
    p()
    p("## Einzelfall-Liste (entschiedene Fälle, sortiert nach Verdikt v2)")
    p()
    p("| Firma | A | B | Kanal | Verdikt v2 | Ergebnis |")
    p("|---|---|---|---|---|---|")
    ordn = {"hoch": 0, "mittel": 1, "tief": 2}
    for r in sorted(entschieden, key=lambda r: (ordn.get(r["verdikt"], 3), -r["Y"], r["firma"], r["id"])):
        p(f"| {r['firma'][:34]} | {r['A']} | {r['B']} | {r['kanal']} | {r['verdikt']} | {'Einladung' if r['Y'] else 'Dossier'} |")

    # --- Sensitivität
    p()
    p("## Sensitivität — wie stabil sind die Befunde gegenüber der Fallauswahl?")
    p()
    p("Jeder entschiedene Fall wird einmal weggelassen (Leave-one-out). Kippt die Richtung oder springt der p-Wert "
      "über die Schwelle, hängt der Befund an einzelnen Fällen.")
    p()
    p("| Kontrast | p (alle) | p min–max ohne je einen Fall | Richtung kippt |")
    p("|---|---|---|---|")
    for name, wahr in (("A=2 vs. A≤1", lambda r: r["A"] == 2), ("B=2 vs. B≤1", lambda r: r["B"] == 2),
                       ("Verdikt hoch vs. Rest", lambda r: r["verdikt"] == "hoch")):
        k1, n1_, k0, n0_, pv = kontrast(entschieden, wahr)
        if not (n1_ and n0_):
            continue
        richtung = (k1 / n1_ > k0 / n0_)
        ps, kippt = [], 0
        for i in range(len(entschieden)):
            rest = entschieden[:i] + entschieden[i + 1:]
            j1, m1, j0, m0, q = kontrast(rest, wahr)
            if m1 and m0:
                ps.append(q)
                kippt += (j1 / m1 > j0 / m0) != richtung
        p(f"| {name} | {pv:.4f} | {min(ps):.4f}–{max(ps):.4f} | {'ja, in ' + str(kippt) + ' Varianten' if kippt else 'nein'} |")
    p()

    # --- Limitationen
    p("## Limitationen — was diese Auswertung nicht kann")
    p()
    offen = sum(1 for r in rows if r["y"] not in Y_WERT and r["y"] != "zurueckgezogen")
    p(f"1. **Zensierte Fälle.** {offen} Bewerbungen sind noch offen. Fallen ihre Ergebnisse anders aus als die der "
      f"entschiedenen (z. B. weil Einladungen schneller kommen als Absagen), verzerrt das die Quoten oben.")
    p()
    ex = sum(r["ex_ante"] for r in entschieden)
    p(f"2. **Kodierzeitpunkt.** {ex} von {len(entschieden)} entschiedenen Fällen sind ex ante kodiert (vor dem Versand, "
      f"ohne Kenntnis des Ausgangs). Nur diese sind ein sauberer Test; nachträglich vergebene Werte kennen den Ausgang.")
    p()
    zellen = [len([r for r in entschieden if r["A"] == a_ and r["B"] == b_]) for a_, b_ in product((2, 1, 0), (2, 1, 0))]
    zellen = [z for z in zellen if z]
    p(f"3. **Fallzahl.** {base_k} Ereignisse auf {base_n} Fälle. Die besetzten Zellen der A×B-Matrix enthalten "
      f"{min(zellen)} bis {max(zellen)} Fälle; ein einzelner Fall verschiebt eine kleine Zelle um viele Prozentpunkte.")
    p()
    leer_a = [a_ for a_ in (0, 1, 2) if not tA.get(a_)]
    leer_b = [b_ for b_ in (0, 1, 2) if not tB.get(b_)]
    if leer_a or leer_b:
        p(f"4. **Keine Varianz auf Teilen der Skala.** Unter den entschiedenen Fällen kommen nicht vor: "
          + ", ".join([f"A={x}" for x in leer_a] + [f"B={x}" for x in leer_b])
          + ". Eine Stufe ohne Fälle kann nichts trennen.")
    else:
        p("4. **Auswahl.** Beworben wird nur, was Schritt 1 bestanden hat und von Alex ein Go bekam. Die Skalen sind "
          "deshalb nach unten ausgedünnt; eine Aussage über Fälle, die nie versandt wurden, ist nicht möglich.")
    p()
    monate = {}
    for r in entschieden:
        monate.setdefault(r["monat"], [0, 0])[r["Y"]] += 1
    p("5. **Zeit als Confounder.** Einladungsquote nach Monat der Einreichung: "
      + " · ".join(f"{m} {v[1]}/{v[0]+v[1]}" for m, v in sorted(monate.items()))
      + ". Frühe und späte Bewerbungen liegen in unterschiedlichen Marktphasen; A, B und Zeit sind nicht entflochten.")
    p()
    return L


def main(argv=None):
    a = sys.argv[1:] if argv is None else argv
    D = json.loads(PIPE.read_text(encoding="utf-8"))
    text = "\n".join(auswertung(D)) + "\n"
    print(text, end="")
    if "--schreiben" in a:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(text, encoding="utf-8")
        print(f"\nGeschrieben: {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
