#!/usr/bin/env python3
"""Polskie identyfikatory i encje prawne - walidacja i ekstrakcja (stdlib, offline).

Port z Patrona (MateMatic Solutions, AGPL-3.0):
  backend/src/lib/pl-entities/checksums.ts  - sumy kontrolne PESEL/NIP/REGON, format KRS
  backend/src/lib/pl-entities/regex.ts      - sygnatury, CELEX, ELI, firmy, osoby
  backend/src/lib/pseudonim/plDetector.ts   - adresy
Dodatkowo (poza Patronem): odwolania do Dz.U. i dekodowanie PESEL.

Uzycie:
  pl_entities.py extract PLIK|-            JSON z encjami (typ, wartosc, pozycja)
  pl_entities.py extract PLIK --all        takze numery z bledna suma kontrolna
  pl_entities.py validate pesel 44051401458
  pl_entities.py validate nip 526-104-08-28
  pl_entities.py pesel-info 44051401458    data urodzenia i plec
"""
import argparse
import json
import re
import sys
from datetime import date

# --- Sumy kontrolne ---------------------------------------------------------


def is_valid_pesel(s: str) -> bool:
    """11 cyfr, wagi 1-3-7-9-1-3-7-9-1-3, (10 - suma % 10) % 10."""
    if not re.fullmatch(r"\d{11}", s):
        return False
    w = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    total = sum(int(s[i]) * w[i] for i in range(10))
    return (10 - total % 10) % 10 == int(s[10])


def is_valid_nip(s: str) -> bool:
    """10 cyfr (dopuszcza - i spacje), wagi 6-5-7-2-3-4-5-6-7 mod 11; 10 = niepoprawny."""
    d = re.sub(r"[\s-]", "", s)
    if not re.fullmatch(r"\d{10}", d):
        return False
    w = [6, 5, 7, 2, 3, 4, 5, 6, 7]
    c = sum(int(d[i]) * w[i] for i in range(9)) % 11
    return c != 10 and c == int(d[9])


def is_valid_regon9(s: str) -> bool:
    if not re.fullmatch(r"\d{9}", s):
        return False
    w = [8, 9, 2, 3, 4, 5, 6, 7]
    m = sum(int(s[i]) * w[i] for i in range(8)) % 11
    return (0 if m == 10 else m) == int(s[8])


def is_valid_regon14(s: str) -> bool:
    if not re.fullmatch(r"\d{14}", s) or not is_valid_regon9(s[:9]):
        return False
    w = [2, 4, 8, 5, 0, 9, 7, 3, 6, 1, 2, 4, 8]
    m = sum(int(s[i]) * w[i] for i in range(13)) % 11
    return (0 if m == 10 else m) == int(s[13])


def is_valid_regon(s: str) -> bool:
    d = re.sub(r"[\s-]", "", s)
    if len(d) == 9:
        return is_valid_regon9(d)
    if len(d) == 14:
        return is_valid_regon14(d)
    return False


def is_valid_krs_format(s: str) -> bool:
    """KRS nie ma publicznej sumy kontrolnej - tylko format (10 cyfr).
    Istnienie podmiotu sprawdza mcp__krs__get_entity."""
    return bool(re.fullmatch(r"\d{10}", s))


def pesel_info(s: str):
    if not is_valid_pesel(s):
        return None
    yy, mm, dd = int(s[0:2]), int(s[2:4]), int(s[4:6])
    century = {0: 1900, 20: 2000, 40: 2100, 60: 2200, 80: 1800}
    base = mm - mm % 20
    try:
        born = date(century[base] + yy, mm % 20, dd).isoformat()
    except (KeyError, ValueError):
        born = None
    return {"data_urodzenia": born, "plec": "M" if int(s[9]) % 2 else "K"}


VALIDATORS = {
    "pesel": is_valid_pesel,
    "nip": is_valid_nip,
    "regon": is_valid_regon,
    "krs": is_valid_krs_format,
}

# --- Wzorce -----------------------------------------------------------------

UPPER = "A-ZŁŚŻŹĆŃÓĄĘ"
LOWER = "a-ząćęłńóśźż"
ROMAN_1_39 = r"(?:X{1,3}(?:IX|IV|VI{0,3}|I{1,3})?|IX|IV|VI{0,3}|I{1,3})"
NAME_TOKEN = f"[{UPPER}][{LOWER}]+"
NAME_SEQ = f"{NAME_TOKEN}(?:[-\\s]{NAME_TOKEN}){{0,2}}"

PERSON_MARKERS = [
    "Pan", "Pani", "Pana", "Panu", "Panią", "Państwo", "Państwa",
    r"adw\.", "adwokat", "adwokata", r"mec\.", "mecenas", "mecenasa",
    r"r\.\s?pr\.", "radca prawny", "radcy prawnego",
    "sędzia", "sędziego", "prokurator", "prokuratora",
    "świadek", "świadka", "oskarżony", "oskarżonego", "oskarżonej", "oskarżona",
    "biegły", "biegłego", "biegła", "powód", "powoda", "pozwany", "pozwanego",
    "pokrzywdzony", "pokrzywdzonego", "obrońca", "obrońcy",
]
# Pierwsza litera markera bez wzgledu na wielkosc ("Świadek X zeznal").
_MARKERS = "|".join(f"[{m[0]}{m[0].upper()}]{m[1:]}" for m in PERSON_MARKERS)

LEGAL_FORMS = [
    "sp. z o.o.", "spółka z ograniczoną odpowiedzialnością",
    "spolka z ograniczona odpowiedzialnoscia", "s.a.", "sp. k.", "sp. j.",
    "sp. p.", "s.k.a.", "p.s.a.", "sp. komandytowa", "spółka komandytowa",
    "spolka komandytowa", "spółka cywilna", "spolka cywilna", "s.c.",
]


def _form_pattern(lit: str) -> str:
    out = ""
    for i, ch in enumerate(lit):
        if ch == ".":
            out += r"\."
        elif ch == " ":
            out += r"\s*" if lit[i - 1] == "." else r"\s+"
        else:
            out += re.escape(ch)
    return out


_FORMS_ALT = "|".join(_form_pattern(f) for f in sorted(LEGAL_FORMS, key=len, reverse=True))

# Nazwa firmy: slowa z wielkiej litery lub cyfry (albo "mBank"), laczone spojnikami.
# Zawezenie wzgledem Patrona: tam nazwa to dowolne 0-80 znakow od pierwszej wielkiej
# litery, wiec "Umowa zawarta pomiedzy ABC sp. z o.o." bylo w calosci nazwa firmy.
_ORG_TOKEN = rf"(?:[{UPPER}0-9\"„][\w.&'\"”-]*|[a-z]+[A-Z][\w.&-]*)"
# Leniwie: nazwa konczy sie na pierwszej formie prawnej ("A S.A. oraz B sp. k." to dwie
# firmy). Spojniki tylko i/and/& - "z", "w", "oraz" wciagaly poczatek zdania.
_ORG_NAME = rf"{_ORG_TOKEN}(?:\s+(?:{_ORG_TOKEN}|i|and|&)){{0,7}}?"

# (typ, podtyp, regex, grupa, walidator). Kolejnosc = priorytet przy
# nakladajacych sie dopasowaniach o tym samym poczatku i dlugosci.
RULES = [
    # KRS pierwszy: ma prefiks, wiec jest pewniejszy niz goly ciag 10 cyfr (NIP).
    ("KRS", None, re.compile(r"\bKRS[:\s]*(\d{10})\b", re.I), 1, is_valid_krs_format),
    ("PESEL", None, re.compile(r"\b\d{11}\b"), 0, is_valid_pesel),
    ("NIP", None, re.compile(r"\b\d{3}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}\b"), 0, is_valid_nip),
    ("REGON", None, re.compile(r"\b(\d{14}|\d{9})\b"), 1, is_valid_regon),
    ("EMAIL", None, re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), 0, None),
    ("TELEFON", None, re.compile(r"\+48[\s-]?\d{3}[\s-]?\d{3}[\s-]?\d{3}\b"), 0, None),
    ("SYGNATURA", "NSA",
     re.compile(r"\b(?:I|II|III)\s+(?:FSK|OSK|OPS|GSK|FPS|FSW|FZ)\s+\d{1,5}/\d{2,4}\b"), 0, None),
    ("SYGNATURA", "WSA", re.compile(r"\b(?:I|II|III|IV)\s+SA/[A-Z][a-z]{1,2}\s+\d{1,5}/\d{2,4}\b"), 0, None),
    ("SYGNATURA", "KIO", re.compile(r"\bKIO(?:/UZP)?\s+\d{1,5}/\d{2,4}\b"), 0, None),
    ("SYGNATURA", "SN", re.compile(r"\b(?:I{1,3}|IV|V|VI|VII)\s+[A-Z]{2,4}\s+\d{1,5}/\d{2,4}\b"), 0, None),
    ("SYGNATURA", "TK", re.compile(r"\b(?:K|P|U|SK|Kp|Kpt|Pp)\s+\d{1,4}/\d{2,4}\b"), 0, None),
    ("SYGNATURA", "SAD_POWSZECHNY",
     re.compile(rf"\b{ROMAN_1_39}\s+(?![A-Z]{{2,4}}\s)[A-Z][A-Za-z]{{0,3}}\s+\d{{1,5}}/\d{{2,4}}\b"), 0, None),
    ("CELEX", None, re.compile(r"\b3\d{4}[RLDQ]\d{4}\b"), 0, None),
    ("ELI", None, re.compile(r"eli/(?:sejm|mp|powszechnie|akty-prawne)/[a-z]+/\d{4}/\d+/?\d*", re.I), 0, None),
    ("DZ_U", None,
     re.compile(r"Dz\.\s?U\.\s?(?:z\s)?\d{4}\s?(?:r\.\s?)?(?:Nr\s?\d+,?\s?)?poz\.\s?\d+"), 0, None),
    ("FIRMA", None, re.compile(rf"(?<!\w){_ORG_NAME}\s+(?i:{_FORMS_ALT})(?!\w)"), 0, None),
    ("OSOBA", None, re.compile(rf"(?<!\w)(?:{_MARKERS})\s+({NAME_SEQ})"), 1, None),
    ("ADRES", None,
     re.compile(rf"\b(?:ul\.|ulica|al\.|aleja|alei|pl\.|plac|os\.|osiedle)\s+[{UPPER}0-9][\w.\- ]{{1,50}}?"
                r"\s+\d+[A-Za-z]?(?:\s*/\s*\d+[A-Za-z]?)?\b", re.I), 0, None),
    ("KOD_POCZTOWY", None, re.compile(r"\b\d{2}-\d{3}\b"), 0, None),
]


def extract(text: str, include_invalid: bool = False):
    """Zwraca liste encji bez nakladajacych sie spanow, posortowana po pozycji."""
    found = []
    for prio, (typ, sub, rx, group, validator) in enumerate(RULES):
        for m in rx.finditer(text):
            value = (m.group(group) if group else m.group(0)).strip()
            if not value:
                continue
            start = m.start(group) if group else m.start()
            valid = validator(value) if validator else None
            if valid is False and not include_invalid:
                continue
            item = {"typ": typ, "wartosc": value, "start": start, "end": start + len(value)}
            if sub:
                item["podtyp"] = sub
            if valid is not None:
                item["poprawny"] = valid
            found.append((start, -len(value), prio, item))
    found.sort(key=lambda x: x[:3])
    kept, last_end = [], -1
    for start, _neg_len, _prio, item in found:
        if start >= last_end:
            kept.append(item)
            last_end = item["end"]
    return kept


def _read(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("extract", help="wyciagnij encje z tekstu")
    p.add_argument("path")
    p.add_argument("--all", action="store_true", help="takze numery z bledna suma kontrolna")
    p = sub.add_parser("validate", help="sprawdz sume kontrolna")
    p.add_argument("kind", choices=sorted(VALIDATORS))
    p.add_argument("value")
    p = sub.add_parser("pesel-info", help="data urodzenia i plec z PESEL")
    p.add_argument("value")
    a = ap.parse_args(argv)

    if a.cmd == "extract":
        print(json.dumps(extract(_read(a.path), a.all), ensure_ascii=False, indent=2))
        return 0
    if a.cmd == "validate":
        ok = VALIDATORS[a.kind](a.value)
        print(json.dumps({"typ": a.kind, "wartosc": a.value, "poprawny": ok}, ensure_ascii=False))
        return 0 if ok else 1
    info = pesel_info(a.value)
    print(json.dumps(info if info else {"poprawny": False}, ensure_ascii=False))
    return 0 if info else 1


if __name__ == "__main__":
    sys.exit(main())
