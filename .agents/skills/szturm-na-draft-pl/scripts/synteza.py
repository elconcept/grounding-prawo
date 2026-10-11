#!/usr/bin/env python3
"""E5+E6 szturmu: synteza ustalen soczewek, bramki napraw i edits.json dla adeu.

Soczewki (E1-E4) oddaja ustalenia w jednym schemacie (references/schemat-ustalenia.json).
Ten skrypt robi to, czego nie wolno zostawic osadowi modelu:

  1. walidacja schematu - ustalenie bez kotwicy, klasy albo wagi nie wchodzi do syntezy;
  2. deduplikacja po (dokument, kotwica, klasa) oraz po (dokument, target_text, klasa):
     zgodnosc soczewek podnosi PEWNOSC (liczba soczewek), nie wage - waga to najciezsza
     ocena skutku zgloszona przez ktorakolwiek soczewke;
  3. bramki naprawy (moga tylko obnizac: AUTO -> REDAKCJA -> DECYZJA_AUTORA; DOWOD = bez edycji):
     - AUTO tylko: 🔴 CYTAT/SYGNATURA/PRZEPIS z dowodem od soczewki deterministycznej E1
       albo 🟡/🟢 STYL/FORMAT;
     - STRATEGIA i KOMPLETNOSC nigdy ponizej DECYZJA_AUTORA;
     - rozne propozycje new_text dla jednego ustalenia -> DECYZJA_AUTORA;
  4. twarde zakazy (edycja wstrzymana albo zablokowana, zamiast tego pytanie do autora):
     - target dotyka fakty_potwierdzone / decyzje_autora, a new_text nie zachowuje ich
       brzmienia -> edycja WSTRZYMANA, ustalenie idzie do autora jako DECYZJA_AUTORA;
     - new_text wprowadza wyjasnienie wykluczone przez rejestr (pole "wyklucza") -> ZABLOKOWANE;
     - new_text dopisuje zwrot "alternatywny" (nie mozna wykluczyc, rownie dobrze...) -> DECYZJA_AUTORA;
     - nowa liczba w new_text bez dowodu (pomiar/zrodlo) -> ZABLOKOWANE;
     - zmiana sygnatury, karty akt albo kwoty poza AUTO -> ZABLOKOWANE;
  5. konflikt kotwic: dwie edycje na nachodzacym tekscie -> zostaje ciezsza, druga KONFLIKT;
  6. edits.<DOKUMENT>.redline.json (wszystkie edycje - wejscie adeu; REDLINE i kopia z accept-all),
     informacyjnie edits.<DOKUMENT>.json (AUTO + REDAKCJA) i edits.<DOKUMENT>.decyzje.json (DECYZJA_AUTORA),
     ustalenia.scalone.json, raport_synteza.md (jedna linia na ustalenie; pytania tylko dla
     DECYZJA_AUTORA i DOWOD). Pliki zawieraja wylacznie pola adeu.

Uzycie:
  python3 synteza.py ustalenia/*.json --rejestry rejestry.json \
      --md PISMO=run/pismo.clean.md --md EKSP=run/ekspertyza.clean.md \
      [--poprzednie run_poprzedni/ustalenia.scalone.json] -o run/

Exit: 0 = synteza gotowa, 1 = sa ustalenia odrzucone przez schemat albo targety do poprawy,
      2 = blad wejscia.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clean_targets import bez_markdownu, plain_doc, sprawdz  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

KLASY = ["CYTAT", "SYGNATURA", "PRZEPIS", "FAKT_BEZ_ZRODLA", "SPRZECZNOSC", "LOGIKA",
         "STRATEGIA", "KOMPLETNOSC", "STYL", "FORMAT"]
WAGI = ["🔴", "🟠", "🟡", "🟢"]  # od najciezszej
NAPRAWY = ["AUTO", "REDAKCJA", "DECYZJA_AUTORA", "DOWOD"]
# soczewki deterministyczne warstwy E1 - tylko ich dowod otwiera AUTO dla 🔴
E1 = {"citation-grounding-pl", "patron-weryfikacja-cytatow", "ekstraktor-cytatow-pl", "iura",
      "saos-orzecznictwo", "lexcache", "patron-identyfikatory-pl", "E1"}
KLASY_AUTO_CZERWONE = {"CYTAT", "SYGNATURA", "PRZEPIS"}
KLASY_AUTO_REDAKCYJNE = {"STYL", "FORMAT"}
KLASY_TYLKO_AUTOR = {"STRATEGIA", "KOMPLETNOSC"}
ZWROTY_ALTERNATYWNE = [
    r"nie (?:można|da się|sposób) wykluczyć", r"alternatywn", r"równie dobrze", r"inne wyjaśnienie",
    r"niewinne wyjaśnienie", r"m[oó]g(?:ł|ło|ła|ły) (?:to )?(?:też |także |również )?wynikać",
    r"może (?:to )?(?:też |także |również )?wynikać", r"przyczyną m[oó]g", r"nie jest wykluczone",
    r"m[oó]g(?:ł|ło|ła|ły) (?:też |także |również )?być", r"być może", r"możliwe (?:jest )?również",
    r"mogło być spowodowane",
]
RE_LICZBA = re.compile(r"\d+(?:[.,:]\d+)*")
RE_SYGNATURA = re.compile(r"\b[IVXL]{1,5}\s+[A-Z][A-Za-z]{0,6}(?:/[A-Za-z]{1,4})?\s+\d+/\d{2,4}(?:/[A-Z])?\b")
RE_KARTA = re.compile(r"\bk\.\s?\d+(?:[-–]\d+)?\b")
RE_KWOTA = re.compile(r"\b\d[\d  ]*(?:,\d{2})?\s?(?:zł|PLN|EUR|złotych)\b")


def norm(t: str) -> str:
    t = unicodedata.normalize("NFC", bez_markdownu(t or ""))
    t = t.replace("„", '"').replace("”", '"').replace("’", "'").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", t).strip().lower()


def norm_kotwica(k: str) -> str:
    return re.sub(r"\s+", "", (k or "")).lower()


def gorsza_naprawa(a: str, b: str) -> str:
    """Bramka moze tylko obnizac automatyzm: AUTO < REDAKCJA < DECYZJA_AUTORA < DOWOD."""
    return a if NAPRAWY.index(a) >= NAPRAWY.index(b) else b


def waliduj(u: dict) -> list[str]:
    bledy = []
    for pole in ("dokument", "kotwica", "klasa", "waga", "naprawa"):
        if not u.get(pole):
            bledy.append(f"brak pola {pole}")
    if u.get("klasa") and u["klasa"] not in KLASY:
        bledy.append(f"klasa spoza listy: {u['klasa']}")
    if u.get("waga") and u["waga"] not in WAGI:
        bledy.append(f"waga spoza listy: {u['waga']}")
    if u.get("naprawa") and u["naprawa"] not in NAPRAWY:
        bledy.append(f"naprawa spoza listy: {u['naprawa']}")
    if not (u.get("soczewki") or u.get("soczewka")):
        bledy.append("brak soczewki")
    return bledy


def wczytaj_ustalenia(sciezki: list[Path]) -> list[dict]:
    out = []
    for p in sciezki:
        pliki = sorted(p.glob("*.json")) if p.is_dir() else [p]
        for f in pliki:
            dane = json.loads(f.read_text(encoding="utf-8"))
            if isinstance(dane, dict):
                dane = dane.get("ustalenia", [dane])
            for u in dane:
                u = dict(u)
                s = u.pop("soczewka", None)
                u["soczewki"] = list(dict.fromkeys((u.get("soczewki") or []) + ([s] if s else [])))
                u["_plik"] = f.name
                # jedno ustalenie naprawiane w kilku miejscach: "edycje": [{target_text, new_text,
                # [kotwica], [dokument]}] - kazda edycja przechodzi bramki osobno, raport ma jedna linie
                edycje = u.pop("edycje", None)
                if not edycje:
                    out.append(u)
                    continue
                grupa = f"{u.get('dokument')}|{u.get('kotwica')}|{u.get('klasa')}"
                for i, e in enumerate(edycje, 1):
                    sub = dict(u)
                    sub.update({k: e[k] for k in ("target_text", "new_text", "kotwica", "dokument") if k in e})
                    if "kotwica" not in e:
                        sub["kotwica"] = f"{u.get('kotwica')}#{i}"
                    sub["grupa"] = grupa
                    sub["_edycja"] = f"{u['_plik']}|{grupa}|{i}"
                    out.append(sub)
    return out


SUROWOSC_STANU = ["ZABLOKOWANE", "WSTRZYMANE", "KONFLIKT", "DO_POPRAWY_TARGET", "PYTANIE",
                  "ZMIANA_DO_DECYZJI", "WPROWADZONE"]


def po_id(grupy: list[dict]) -> list[dict]:
    """Jedna pozycja na ustalenie (ID), takze gdy ustalenie ma kilka edycji."""
    wynik: dict[str, dict] = {}
    for g in grupy:
        w = wynik.get(g["id"])
        if w is None:
            wynik[g["id"]] = {**g, "kotwice": [g["kotwica"]], "stany": [g["stan"]], "powody": list(g["powody"]),
                              "soczewki": list(g["soczewki"])}
            continue
        w["kotwice"].append(g["kotwica"])
        w["stany"].append(g["stan"])
        w["powody"] += [p for p in g["powody"] if p not in w["powody"]]
        w["soczewki"] = list(dict.fromkeys(w["soczewki"] + g["soczewki"]))
        if WAGI.index(g["waga"]) < WAGI.index(w["waga"]):
            w["waga"] = g["waga"]
        w["naprawa"] = gorsza_naprawa(w["naprawa"], g["naprawa"])
    for w in wynik.values():
        w["stan"] = min(w["stany"], key=SUROWOSC_STANU.index)
        w["kotwica"] = w["kotwice"][0] if len(w["kotwice"]) == 1 else \
            w["kotwice"][0].split("#")[0] + f" (+{len(w['kotwice']) - 1})"
        w["pewnosc"] = len(w["soczewki"])
    return sorted(wynik.values(), key=lambda w: w["id"])


def scal(ustalenia: list[dict]) -> tuple[list[dict], list[dict]]:
    grupy: dict[tuple, dict] = {}
    alias: dict[tuple, tuple] = {}
    odrzucone = []
    for u in ustalenia:
        bledy = waliduj(u)
        if bledy:
            odrzucone.append({"ustalenie": {k: v for k, v in u.items() if not k.startswith("_")},
                              "plik": u["_plik"], "bledy": bledy})
            continue
        k1 = (u["dokument"], norm_kotwica(u["kotwica"]), u["klasa"])
        if u.get("_edycja"):
            # edycje jednego ustalenia moga miec wspolna jawna kotwice (ten sam akapit):
            # nie wolno ich scalac ze soba, bo druga edycja by przepadla
            k1 = k1 + (u["_edycja"],)
        k2 = (u["dokument"], norm(u.get("target_text", "")), u["klasa"]) if u.get("target_text") else None
        klucz = alias.get(k1) or (alias.get(k2) if k2 else None) or k1
        alias[k1] = klucz
        if k2:
            alias[k2] = klucz
        g = grupy.get(klucz)
        if g is None:
            g = {**{k: v for k, v in u.items() if not k.startswith("_")},
                 "propozycje": [], "dowody": [], "komentarze": [], "zrodla_plikow": []}
            grupy[klucz] = g
        else:
            g["soczewki"] = list(dict.fromkeys(g["soczewki"] + u["soczewki"]))
            if WAGI.index(u["waga"]) < WAGI.index(g["waga"]):
                g["waga"] = u["waga"]
            # zgodnosc soczewek nie zwieksza automatyzmu: bierzemy ostrozniejsza naprawe
            g["naprawa"] = gorsza_naprawa(g["naprawa"], u["naprawa"])
            for pole in ("target_text", "akapit_docx"):
                if not g.get(pole) and u.get(pole):
                    g[pole] = u[pole]
        if u.get("new_text") is not None and u.get("target_text"):
            g["propozycje"].append({"new_text": u["new_text"], "soczewki": u["soczewki"]})
        if u.get("dowod"):
            g["dowody"].append(u["dowod"])
        if u.get("komentarz"):
            g["komentarze"].append(u["komentarz"])
        g["zrodla_plikow"].append(u["_plik"])
    wynik = []
    for g in grupy.values():
        g["dowody"] = list(dict.fromkeys(g["dowody"]))
        g["komentarze"] = list(dict.fromkeys(g["komentarze"]))
        g["pewnosc"] = len(g["soczewki"])
        wynik.append(g)
    return wynik, odrzucone


def wybierz_propozycje(g: dict) -> None:
    props = g.pop("propozycje")
    rozne = list(dict.fromkeys(norm(p["new_text"]) for p in props))
    g["flagi"] = []
    if not props:
        g["new_text"] = None
        return
    # pierwszenstwo: propozycja od soczewki deterministycznej E1, potem pierwsza zgloszona
    props.sort(key=lambda p: 0 if set(p["soczewki"]) & E1 else 1)
    g["new_text"] = props[0]["new_text"]
    if len(rozne) > 1:
        g["flagi"].append("ROZNE_PROPOZYCJE")
        g["propozycje_alternatywne"] = [p["new_text"] for p in props[1:] if norm(p["new_text"]) != norm(g["new_text"])]


def _zakresy(doc: str, frag: str) -> list[tuple[int, int]]:
    out, i = [], doc.find(frag)
    while frag and i >= 0:
        out.append((i, i + len(frag)))
        i = doc.find(frag, i + 1)
    return out


def nakladka(target: str, chroniony: str, doc: str | None) -> str | None:
    """Tekst wspolny targetu i fragmentu chronionego albo None.

    Z dokumentem: przeciecie zakresow w tekscie (lapie target, ktory zahacza o brzeg faktu).
    Bez dokumentu albo gdy fragment nie wystepuje doslownie: zawieranie oraz wspolny
    brzeg (koniec jednego = poczatek drugiego) dluzszy niz 6 znakow."""
    t, c = bez_markdownu(target).strip(), bez_markdownu(chroniony).strip()
    if not t or not c:
        return None
    if doc:
        zt, zc = _zakresy(doc, t), _zakresy(doc, c)
        if zt and zc:
            for a1, b1 in zt:
                for a2, b2 in zc:
                    if a1 < b2 and a2 < b1:
                        return doc[max(a1, a2):min(b1, b2)]
            return None
    nt, nc = norm(t), norm(c)
    if nc in nt:
        return c
    if nt in nc:
        return t
    for k in range(min(len(nt), len(nc)), 6, -1):
        if nt.endswith(nc[:k]) or nc.endswith(nt[:k]):
            return nc[:k] if nt.endswith(nc[:k]) else nt[:k]
    return None


def rdzenie(fraza: str) -> list[str]:
    """Rdzenie slow >= 4 liter (5 pierwszych znakow) - odmiana i szyk nie ukrywaja wykluczonej tezy."""
    return [w[:5] for w in re.findall(r"[a-ząćęłńóśźż]{4,}", norm(fraza))]


def zawiera_rdzenie(tekst: str, rdz: list[str]) -> bool:
    slowa = re.findall(r"[a-ząćęłńóśźż]+", tekst)
    return bool(rdz) and all(any(s.startswith(r) for s in slowa) for r in rdz)


def bramki(g: dict, rej: dict, doc: str | None = None) -> None:
    g.setdefault("flagi", [])
    g["stan"] = None
    g["powody"] = []
    tgt, new = g.get("target_text") or "", g.get("new_text")
    dowod = " ".join(g["dowody"]).strip()

    if not tgt or new is None:
        if g["naprawa"] != "DOWOD":
            g["powody"].append("brak target_text/new_text - bez edycji")
        g["naprawa"] = "DOWOD"
    if g["naprawa"] == "AUTO":
        czerwone = g["waga"] == "🔴" and g["klasa"] in KLASY_AUTO_CZERWONE and dowod and set(g["soczewki"]) & E1
        redakcyjne = g["waga"] in ("🟡", "🟢") and g["klasa"] in KLASY_AUTO_REDAKCYJNE
        if not (czerwone or redakcyjne):
            g["naprawa"] = "REDAKCJA"
            g["powody"].append("AUTO niedozwolone dla tej klasy/wagi/dowodu -> REDAKCJA")
    if g["klasa"] in KLASY_TYLKO_AUTOR and g["naprawa"] in ("AUTO", "REDAKCJA"):
        g["naprawa"] = "DECYZJA_AUTORA"
        g["powody"].append(f"{g['klasa']} rozstrzyga autor")
    if "ROZNE_PROPOZYCJE" in g["flagi"] and g["naprawa"] in ("AUTO", "REDAKCJA"):
        g["naprawa"] = "DECYZJA_AUTORA"
        g["powody"].append("soczewki proponuja rozne brzmienia")
    if g["naprawa"] == "DOWOD":
        g["stan"] = "PYTANIE"
        return

    n_tgt, n_new = norm(tgt), norm(new)
    # rejestry chronione
    for rodzaj, pole in (("fakty_potwierdzone", "tekst"), ("decyzje_autora", "chroniony_tekst")):
        for poz in rej.get(rodzaj, []):
            wspolne = nakladka(tgt, poz.get(pole) or "", doc)
            if wspolne and norm(wspolne) not in n_new:
                g["naprawa"] = "DECYZJA_AUTORA"
                g["stan"] = "WSTRZYMANE"
                g["powody"].append(f"zmienia {rodzaj} {poz.get('id', '?')} ({wspolne.strip()[:40]!r}) - "
                                   "rejestr chroniony, tylko pytanie do autora")
    for poz in rej.get("fakty_potwierdzone", []):
        for wyk in poz.get("wyklucza", []):
            rdz = rdzenie(wyk)
            if zawiera_rdzenie(n_new, rdz) and not zawiera_rdzenie(n_tgt, rdz):
                g["stan"] = "ZABLOKOWANE"
                g["powody"].append(f"wprowadza wyjasnienie wykluczone przez {poz.get('id', '?')}: {wyk!r}")
    for wz in ZWROTY_ALTERNATYWNE:
        if re.search(wz, n_new) and not re.search(wz, n_tgt):
            g["flagi"].append("ALTERNATYWA")
            if g["naprawa"] in ("AUTO", "REDAKCJA"):
                g["naprawa"] = "DECYZJA_AUTORA"
            g["powody"].append("dopisuje wyjasnienie alternatywne - sprawdz z fakty_potwierdzone")
            break
    nowe_liczby = set(RE_LICZBA.findall(new)) - set(RE_LICZBA.findall(tgt))
    if nowe_liczby and not dowod:
        g["stan"] = "ZABLOKOWANE"
        g["powody"].append(f"nowe liczby bez pomiaru/zrodla: {', '.join(sorted(nowe_liczby))}")
    # "nie zmieniac" = nie usuwac i nie przerabiac istniejacych; dopisanie (np. zrodla "k. 12")
    # wolno, gdy dowod wskazuje dokladnie ten token
    n_dowod = norm(dowod).replace(" ", "")
    for nazwa, rx in (("sygnatura", RE_SYGNATURA), ("karta akt", RE_KARTA), ("kwota", RE_KWOTA)):
        stare, nowe = set(map(norm, rx.findall(tgt))), set(map(norm, rx.findall(new)))
        if stare - nowe and not (g["naprawa"] == "AUTO" and dowod):
            g["stan"] = "ZABLOKOWANE"
            g["powody"].append(f"zmienia/usuwa {nazwa} ({', '.join(sorted(stare - nowe))}) poza AUTO z dowodem")
        brak = [x for x in nowe - stare if x.replace(" ", "") not in n_dowod]
        if brak:
            g["stan"] = "ZABLOKOWANE"
            g["powody"].append(f"dopisuje {nazwa} bez wskazania w dowodzie: {', '.join(brak)}")
    if g["stan"] is None:
        g["stan"] = "ZMIANA_DO_DECYZJI" if g["naprawa"] == "DECYZJA_AUTORA" else "WPROWADZONE"


def komentarz(g: dict) -> str:
    glowa = f"[{g['id']} | {g['klasa']} {g['waga']} | {g['naprawa']} | {', '.join(g['soczewki'])}]"
    tresc = (" ".join(g["komentarze"]) or g["klasa"]).rstrip(". ") + "."
    zr = f" Źródło: {'; '.join(g['dowody'])}." if g["dowody"] else ""
    pref = "DECYZJA AUTORA (przyjmij albo odrzuć): " if g["naprawa"] == "DECYZJA_AUTORA" else ""
    return f"{glowa} {pref}{tresc}{zr}"


def konflikty_kotwic(grupy: list[dict], docs: dict[str, str]) -> None:
    for dok, tekst in docs.items():
        edy = [g for g in grupy if g["dokument"] == dok and g["stan"] in ("WPROWADZONE", "ZMIANA_DO_DECYZJI")]
        zakresy = []
        for g in edy:
            t = bez_markdownu(g["target_text"]).strip()
            i = tekst.find(t)
            if i >= 0:
                zakresy.append((i, i + len(t), g))
        zakresy.sort(key=lambda z: (WAGI.index(z[2]["waga"]), NAPRAWY.index(z[2]["naprawa"])))
        zajete: list[tuple[int, int, str]] = []
        for a, b, g in zakresy:
            kolizja = next((z for z in zajete if a < z[1] and z[0] < b), None)
            if kolizja:
                g["stan"] = "KONFLIKT"
                g["powody"].append(f"nachodzi na {kolizja[2]} - scal recznie w jedna edycje")
            else:
                zajete.append((a, b, g["id"]))


def raport(grupy: list[dict], odrzucone: list[dict], rej: dict) -> str:
    grupy = po_id(grupy)
    kol = ["WPROWADZONE", "ZMIANA_DO_DECYZJI", "WSTRZYMANE", "PYTANIE", "ZABLOKOWANE", "KONFLIKT", "DO_POPRAWY_TARGET"]
    L = ["# Synteza szturmu", ""]
    if rej.get("teza_nadrzedna"):
        L += [f"Teza nadrzędna: {rej['teza_nadrzedna']}", ""]
    L.append("Stan: " + " | ".join(f"{k} {sum(g['stan'] == k for g in grupy)}" for k in kol))
    L += ["", "| ID | Dok | Kotwica | Klasa | Waga | Soczewki (n) | Naprawa | Stan | Ustalenie |",
          "|---|---|---|---|---|---|---|---|---|"]
    for g in sorted(grupy, key=lambda g: (WAGI.index(g["waga"]), g["id"])):
        opis = (" ".join(g["komentarze"]) or g.get("target_text") or "")[:110].replace("|", "/").replace("\n", " ")
        if g["powody"]:
            opis += " — " + "; ".join(g["powody"])[:120].replace("|", "/")
        L.append(f"| {g['id']} | {g['dokument']} | {g['kotwica']} | {g['klasa']} | {g['waga']} | "
                 f"{', '.join(g['soczewki'])} ({g['pewnosc']}) | {g['naprawa']} | {g['stan']} | {opis} |")
    pyt = [g for g in grupy if g["naprawa"] in ("DECYZJA_AUTORA", "DOWOD") or g["stan"] in ("WSTRZYMANE", "ZABLOKOWANE")]
    L += ["", "## Pytania do autora", ""]
    if not pyt:
        L.append("Brak.")
    for i, g in enumerate(pyt, 1):
        co = "Zmiana wprowadzona jako śledzona - przyjąć?" if g["stan"] == "ZMIANA_DO_DECYZJI" else \
             ("Do rozstrzygnięcia przez autora (bez zmiany tekstu)." if not g.get("target_text") else
              "Brak dowodu/źródła - uzupełnić albo usunąć twierdzenie?") if g["naprawa"] == "DOWOD" else \
             "Edycja nie weszła - rozstrzygnąć?"
        powod = "; ".join(p for p in g["powody"] if "->" not in p)
        L.append(f"{i}. **{g['id']}** ({g['dokument']} {g['kotwica']}, {g['klasa']} {g['waga']}): {co} "
                 + (" ".join(g["komentarze"])[:200] or "") + (f" [{powod}]" if powod else ""))
    if odrzucone:
        L += ["", "## Odrzucone przez schemat (popraw i uruchom ponownie)", ""]
        L += [f"- {o['plik']}: {', '.join(o['bledy'])}" for o in odrzucone]
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ustalenia", nargs="+", type=Path, help="pliki JSON soczewek albo katalog")
    ap.add_argument("--rejestry", type=Path, help="rejestry.json: teza, fakty_potwierdzone, decyzje_autora")
    ap.add_argument("--md", action="append", default=[], help="DOKUMENT=plik.clean.md (do sprawdzenia targetow)")
    ap.add_argument("--poprzednie", type=Path, help="ustalenia.scalone.json z poprzedniej rundy (stale ID)")
    ap.add_argument("-o", "--out", type=Path, required=True)
    a = ap.parse_args()
    try:
        rej = json.loads(a.rejestry.read_text(encoding="utf-8")) if a.rejestry else {}
        ustalenia = wczytaj_ustalenia(a.ustalenia)
        docs = {}
        for m in a.md:
            dok, _, sc = m.partition("=")
            docs[dok] = plain_doc(Path(sc).read_text(encoding="utf-8"))
        poprz = json.loads(a.poprzednie.read_text(encoding="utf-8")) if a.poprzednie else []
    except (OSError, json.JSONDecodeError) as e:
        print(f"BLAD wejscia: {e}", file=sys.stderr)
        return 2
    a.out.mkdir(parents=True, exist_ok=True)

    grupy, odrzucone = scal(ustalenia)
    stare_id = {}
    for p in poprz:
        stare_id[(p["dokument"], norm_kotwica(p["kotwica"]), p["klasa"])] = p["id"]
        if p.get("target_text"):
            stare_id[(p["dokument"], "T:" + norm(p["target_text"]), p["klasa"])] = p["id"]
    nr = max([int(p["id"].split("-")[1]) for p in poprz] or [0])
    uzyte: dict[str, str] = {}      # id -> grupa, ktora go uzyla
    id_grupy: dict[str, str] = {}   # grupa edycji -> wspolne id
    for g in grupy:
        grupa = g.get("grupa") or f"_{id(g)}"
        kt = (g["dokument"], "T:" + norm(g.get("target_text") or ""), g["klasa"])
        kk = (g["dokument"], norm_kotwica(g["kotwica"]), g["klasa"])
        stary = stare_id.get(kt) if g.get("target_text") else None
        stary = stary or stare_id.get(kk)
        if grupa in id_grupy:
            g["id"] = id_grupy[grupa]
        elif stary and uzyte.get(stary, grupa) == grupa:
            g["id"] = stary
        else:
            nr += 1
            g["id"] = f"S-{nr:03d}"
        uzyte[g["id"]] = grupa
        id_grupy[grupa] = g["id"]
        wybierz_propozycje(g)
        bramki(g, rej, docs.get(g["dokument"]))
    konflikty_kotwic(grupy, docs)

    do_poprawy = 0
    for dok in sorted({g["dokument"] for g in grupy}):
        edy = [g for g in grupy if g["dokument"] == dok and g["stan"] in ("WPROWADZONE", "ZMIANA_DO_DECYZJI")]
        edits = [{"id": g["id"], "type": "modify", "target_text": g["target_text"], "new_text": g["new_text"],
                  "comment": komentarz(g)} for g in edy]
        if dok in docs:
            for w, g in zip(sprawdz(edits, docs[dok]), edy):
                if not w["ok"]:
                    g["stan"] = "DO_POPRAWY_TARGET"
                    g["powody"] += [p for p in w["problemy"] if p.startswith("BLAD")]
                    do_poprawy += 1
            edy = [g for g in edy if g["stan"] != "DO_POPRAWY_TARGET"]
        # .redline = komplet (REDLINE i kopia z zastosowanymi zmianami); podzial na AUTO+REDAKCJA
        # i DECYZJA_AUTORA sluzy raportowi i kontroli liczby komentarzy
        for sufiks, stany in (("", {"WPROWADZONE"}), (".decyzje", {"ZMIANA_DO_DECYZJI"}),
                              (".redline", {"WPROWADZONE", "ZMIANA_DO_DECYZJI"})):
            adeu = [{"type": "modify", "target_text": bez_markdownu(g["target_text"]).strip(),
                     "new_text": bez_markdownu(g["new_text"]).strip(), "comment": komentarz(g)}
                    for g in edy if g["stan"] in stany]
            (a.out / f"edits.{dok}{sufiks}.json").write_text(json.dumps(adeu, ensure_ascii=False, indent=2),
                                                             encoding="utf-8")

    (a.out / "ustalenia.scalone.json").write_text(
        json.dumps(sorted(grupy, key=lambda g: g["id"]), ensure_ascii=False, indent=2), encoding="utf-8")
    (a.out / "raport_synteza.md").write_text(raport(grupy, odrzucone, rej), encoding="utf-8")
    zbior = po_id(grupy)
    print(f"ustalen wejsciowych {len(ustalenia)} -> po deduplikacji {len(zbior)} ustalen, {len(grupy)} edycji | "
          f"odrzucone przez schemat {len(odrzucone)} | targety do poprawy {do_poprawy}")
    for k in ("WPROWADZONE", "ZMIANA_DO_DECYZJI", "WSTRZYMANE", "PYTANIE", "ZABLOKOWANE", "KONFLIKT", "DO_POPRAWY_TARGET"):
        n = sum(g["stan"] == k for g in zbior)
        if n:
            print(f"  {k}: {n}")
    print(f"wynik: {a.out}/raport_synteza.md, edits.<DOKUMENT>[.decyzje].json, ustalenia.scalone.json")
    return 1 if odrzucone or do_poprawy else 0


if __name__ == "__main__":
    sys.exit(main())
