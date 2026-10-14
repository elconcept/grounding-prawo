#!/usr/bin/env python3
"""Metryki stylu pisma (E4 szturmu): dlugosc zdan, rozrzut, tasiemce, pauzy, klamry, podkreslenia.

Te same miary, ktore humanizer-pl liczyl recznie w przebiegu 28.09 (#30 burstiness,
#34 klamry, #14 pauzy), liczone deterministycznie, zeby przebieg N+1 dalo sie porownac
z przebiegiem N liczba do liczby.

Zasady pomiaru (stale - zmiana to nowa wersja skryptu, bo psuje porownywalnosc):
- zdanie konczy sie na . ! ? (takze ze znakiem zamykajacym ) " ” *) przed spacja i wielka litera
  albo cyfra; skroty (art., ust., k.p.k., r., godz., nr, ...) nie tna zdania;
- wiersze tabel markdown (zawierajace |), separatory --- i naglowki # sa pomijane;
- baza 28.09 (humanizer-pl, liczona recznie) nie jest odtwarzalna co do liczby zdan; zgodne sa
  pauzy i podkreslenia. Porownuj przebiegi tym skryptem, nie z tamta tabela;
- znaczniki markdown (#, *, _, <u>) sa usuwane przed liczeniem slow;
- pauza = znak — (U+2014); polpauza – (U+2013) liczona osobno;
- podkreslenia: <u>...</u> w .md albo runy z w:u (poza w:val="none") w .docx.

Uzycie:
  python3 metryki_stylu.py pismo.md [ekspertyza.md ...] [--json] [--prog 40] [--top 10]
  python3 metryki_stylu.py pismo.docx          # tekst z word/document.xml (stdlib)

Exit: 0 = policzone, 2 = blad IO / pusty plik.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
import zipfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

U = "A-ZĄĆĘŁŃÓŚŹŻ"
SKROTY = {
    "art", "ust", "pkt", "lit", "par", "r", "w", "godz", "nr", "tj", "tzn", "np", "ok", "m.in",
    "k", "s", "str", "poz", "sygn", "zob", "por", "tzw", "dr", "prof", "mgr", "inż", "ul", "os",
    "al", "pl", "tel", "wyd", "red", "t", "z", "dz", "u", "zm", "k.p.k", "k.p.w", "k.w", "k.k",
    "k.c", "k.p.c", "k.p", "k.p.a", "p.p.s.a", "min", "sek", "mln", "tys", "zł", "gr", "ww",
    "j", "im", "sp", "o.o", "S.A", "ds", "wz", "vs", "cyt", "ibid", "op", "cit", "itd", "itp",
}
KLAMRY = [
    "Nadto", "Co więcej", "Ponadto", "Dodatkowo", "Warto zauważyć", "Warto podkreślić",
    "Należy podkreślić", "Należy zauważyć", "Podsumowując", "Reasumując", "W konsekwencji",
    "Tym samym", "Jednocześnie", "Wobec powyższego", "Mając na uwadze powyższe",
    "Z powyższego wynika", "Innymi słowy", "Co istotne", "Co ważne", "W tym kontekście",
]
RE_KONIEC = re.compile(r"([.!?…])([)\"”»*_]*)\s+(?=[\"„«(*_]*[" + U + r"0-9])")
RE_MD = re.compile(r"</?u>|\*\*|\*|__|(?<!\w)_|_(?!\w)|^#{1,6}\s+|^>\s?|^\s*[-+]\s+(?=\S)")
RE_SLOWO = re.compile(r"[0-9A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż§]+(?:[-'][0-9A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+)*")
RE_PARAGRAF = re.compile(r"<w:p[ >].*?</w:p>", re.S)
RE_T = re.compile(r"<w:t[^>]*>(.*?)</w:t>", re.S)
RE_U = re.compile(r'<w:u (?:w:val="(?!none)[^"]*")[^>]*/>')


def wiersze(sciezka: Path) -> tuple[list[tuple[int, str]], int]:
    """(nr_linii, tekst) oraz liczba podkreslen."""
    if sciezka.suffix.lower() == ".docx":
        xml = zipfile.ZipFile(sciezka).read("word/document.xml").decode("utf-8", "replace")
        out, podkr = [], 0
        for i, p in enumerate(RE_PARAGRAF.findall(xml), 1):
            if "<w:tbl" in p:
                continue
            podkr += len(RE_U.findall(p))
            t = "".join(RE_T.findall(p))
            out.append((i, re.sub(r"&[a-z]+;", " ", t)))
        return out, podkr
    tekst = sciezka.read_text(encoding="utf-8", errors="replace")
    return list(enumerate(tekst.splitlines(), 1)), len(re.findall(r"<u>", tekst))


def czy_skrot(przed: str) -> bool:
    ost = re.split(r"[\s(„\"]", przed)[-1].rstrip(".")
    return ost in SKROTY or ost.lower() in SKROTY or (len(ost) == 1 and ost.isalpha())


def zdania(linie: list[tuple[int, str]]) -> list[tuple[int, str]]:
    wynik: list[tuple[int, str]] = []
    for nr, linia in linie:
        s = linia.strip()
        if not s or "|" in s or s.startswith("#") or re.fullmatch(r"[-*_ ]{3,}", s) or s.startswith("```"):
            continue
        s = RE_MD.sub("", s).strip()
        if not s:
            continue
        start = 0
        for m in RE_KONIEC.finditer(s):
            if m.group(1) == "." and czy_skrot(s[start:m.start()]):
                continue
            kawalek = s[start:m.end(1) + len(m.group(2))].strip()
            if kawalek:
                wynik.append((nr, kawalek))
            start = m.end()
        reszta = s[start:].strip()
        if reszta:
            wynik.append((nr, reszta))
    return wynik


def metryki(sciezka: Path, prog: int, top: int) -> dict:
    linie, podkr = wiersze(sciezka)
    zd = [(nr, z, len(RE_SLOWO.findall(z))) for nr, z in zdania(linie)]
    zd = [x for x in zd if x[2] > 0]
    if not zd:
        raise ValueError("brak zdan do policzenia")
    dl = [x[2] for x in zd]
    pelny = "\n".join(t for _, t in linie)
    klamry = {k: len(re.findall(r"(?<![\wąćęłńóśźż])" + re.escape(k) + r"(?![\wąćęłńóśźż])", pelny))
              for k in KLAMRY}
    dlugie = sorted((x for x in zd if x[2] > prog), key=lambda x: -x[2])
    return {
        "plik": str(sciezka),
        "zdan": len(dl),
        "srednia_slow": round(statistics.mean(dl), 1),
        "odchylenie_burstiness_30": round(statistics.pstdev(dl), 1),
        f"zdan_powyzej_{prog}": len(dlugie),
        "pauzy_em": pelny.count("—"),
        "polpauzy_en": pelny.count("–"),
        "podkreslenia": podkr,
        "klamry_34": {k: v for k, v in klamry.items() if v},
        "najdluzsze": [{"kotwica": f"{sciezka.name}:{nr}", "slow": n, "poczatek": z[:90]}
                       for nr, z, n in dlugie[:top]],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pliki", nargs="+", type=Path)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--prog", type=int, default=40, help="prog tasiemca w slowach (domyslnie 40)")
    ap.add_argument("--top", type=int, default=10)
    a = ap.parse_args()
    wyniki = []
    for p in a.pliki:
        try:
            wyniki.append(metryki(p, a.prog, a.top))
        except (OSError, KeyError, zipfile.BadZipFile, ValueError) as e:
            print(f"BLAD {p}: {e}", file=sys.stderr)
            return 2
    if a.json:
        print(json.dumps(wyniki, ensure_ascii=False, indent=2))
        return 0
    for w in wyniki:
        print(f"== {w['plik']}")
        print(f"zdan {w['zdan']} | srednia {w['srednia_slow']} | odchylenie #30 {w['odchylenie_burstiness_30']}"
              f" | >{a.prog} slow: {w[f'zdan_powyzej_{a.prog}']} | pauzy — {w['pauzy_em']}"
              f" | polpauzy – {w['polpauzy_en']} | podkreslenia {w['podkreslenia']}")
        print("klamry #34:", ", ".join(f"{k} {v}×" for k, v in w["klamry_34"].items()) or "brak")
        for d in w["najdluzsze"]:
            print(f"  {d['kotwica']} ({d['slow']} slow): {d['poczatek']}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
