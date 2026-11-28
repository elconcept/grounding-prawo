#!/usr/bin/env python3
"""Retencja treści między wersjami pisma: nowa wersja zawiadomienia niczego nie gubi (BRAMKA-REDAKCJI.md).

Porównuje poprzednią i nową wersję (DOCX albo Markdown). Każdy cytat „…” (od trzech słów), godzina, data,
odesłanie do karty akt („k. 8–9”), sygnatura i kwota z poprzedniej wersji musi być w nowej. Liczba słów nie maleje.
Świadome usunięcie (decyzja autora, poprawka błędu, np. „k. 43” → „k. 51–55”) wpisuje się do pliku wyjątków,
jeden element w wierszu, z powodem: `- k. 43 | powód: błędne folio, poprawione na k. 51–55`.
Skrócenie pisma tylko na decyzję autora: wiersz `SKRÓCENIE: decyzja autora <data>`.

    python3 retencja_pisma.py <poprzednia> [<starsza> ...] <nowa> [--wyjatki _ZMIANY_vN.md ...] [--json]
Przy kilku wcześniejszych wersjach sprawdza sumę ich elementów (treść utracona dwie wersje temu też jest stratą);
liczbę słów porównuje z bezpośrednio poprzednią wersją. --wyjatki można podać wiele razy.
Kod wyjścia: 0 bez strat, 1 są straty.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pismo_tekst import tekst  # noqa: E402

MIES = "stycznia|lutego|marca|kwietnia|maja|czerwca|lipca|sierpnia|września|października|listopada|grudnia"
WZORY = {
    "cytat": re.compile(r"„([^”]{3,400})”"),
    "godzina": re.compile(r"\b\d{1,2}:\d{2}(?::\d{2})?\b"),
    "data": re.compile(rf"\b\d{{1,2}}\.\d{{2}}\.\d{{4}}\b|\b\d{{1,2}} (?:{MIES}) \d{{4}}\b"),
    "karta": re.compile(r"\bk\.\s?\d+(?:\s?[–-]\s?\d+)?\b"),
    "sygnatura": re.compile(r"\b[IVXL]{1,5}\s[A-Z][A-Za-z]{0,6}(?:\s[A-Z][a-z]{0,3})?\s\d{1,5}/\d{2}\b|"
                            r"\b\d{4}-\d\.Ds\.\d+\.\d{4}\b|\bDs\.?\s?\d+[./]\d{2,4}\b|\bC-\d{1,4}/\d{2}\b|"
                            r"\b[A-ZŚŻ]{2,6}\.\d{3,4}\.\d+\.\d{4}\b"),
    "kwota": re.compile(r"\b\d[\d  ]*(?:,\d{2})?\s?zł\b"),
}


def norm(s):
    return re.sub(r"\s+", " ", s.replace(" ", " ")).strip()


def elementy(t):
    out = {}
    for rodzaj, rx in WZORY.items():
        for m in rx.finditer(t):
            e = norm(m.group(1) if rodzaj == "cytat" else m.group(0))
            if rodzaj == "cytat" and len(e.split()) < 3:
                continue
            out.setdefault(e, rodzaj)
    return out


def porownaj(stary, nowy, wyjatki=""):
    a, b = elementy(stary), elementy(nowy)
    nb, wy = norm(nowy), norm(wyjatki)
    straty = []
    for e, rodzaj in a.items():
        if e in b or e in nb:
            continue
        if e in wy:
            continue
        straty.append((rodzaj, e))
    sa, sb = len(stary.split()), len(nowy.split())
    skrocenie = sb < sa and "SKRÓCENIE: decyzja autora" not in wyjatki
    return straty, sa, sb, skrocenie


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    wyj, pliki, i = "", [], 0
    while i < len(args):
        if args[i] == "--wyjatki":
            p = args[i + 1]
            wyj += open(p, encoding="utf-8").read() + "\n" if os.path.exists(p) else ""
            i += 2
        elif args[i] == "--json":
            i += 1
        else:
            pliki.append(args[i])
            i += 1
    if len(pliki) < 2:
        sys.exit(__doc__)
    *poprzednie, nowa = pliki
    t_nowa = tekst(nowa)
    straty = []
    for p in poprzednie:
        s, _, _, _ = porownaj(tekst(p), t_nowa, wyj)
        straty += [x for x in s if x not in straty]
    _, sa, sb, skr = porownaj(tekst(poprzednie[0]), t_nowa, wyj)
    if "--json" in args:
        print(json.dumps({"straty": straty, "slowa_przed": sa, "slowa_po": sb, "skrocenie": skr}, ensure_ascii=False))
    else:
        for rodzaj, e in straty:
            print(f"STRATA {rodzaj}: {e[:160]}")
        if skr:
            print(f"SKRÓCENIE: {sa} → {sb} słów bez decyzji autora")
        print(f"— strat: {len(straty)}; słowa {sa} → {sb}")
    sys.exit(1 if straty or skr else 0)


if __name__ == "__main__":
    main()
