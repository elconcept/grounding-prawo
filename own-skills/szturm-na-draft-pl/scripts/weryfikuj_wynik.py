#!/usr/bin/env python3
"""Kontrola struktury wyniku E7 szturmu - niezaleznie od komunikatu adeu.

exit 0 i "applied" przy kazdej pozycji nie dowodza, ze Word pokaze zmiany jako sledzone
(redline-docx-pl, krok 3). Ten skrypt sprawdza plik, nie log:

  REDLINE  w:ins + w:del > 0, usuniety tekst w w:delText, komentarzy >= liczba edycji z edits.json
  CZYSTY   0 w:ins / 0 w:del / 0 komentarzy (sanitize --accept-all zadzialal)
  OBA      skan_placeholder.py z redline-docx-pl (dziury typu [DO UZUPELNIENIA], NN/RR, 0,00 zl)
  KATALOG  brak plikow .pdf w katalogu wyniku (PDF robi prawnik po wlasnej korekcie)

Uzycie:
  python3 weryfikuj_wynik.py --redline X_REDLINE.docx --czysty X.docx \
      [--edits edits.X.json edits.X.decyzje.json] [--katalog DIR]

Exit: 0 = wszystko zgodne, 1 = niezgodnosc (lista), 2 = blad IO.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

SKAN = Path(__file__).resolve().parents[2] / "redline-docx-pl" / "scripts" / "skan_placeholder.py"


def struktura(docx: Path) -> dict:
    z = zipfile.ZipFile(docx)
    x = z.read("word/document.xml").decode("utf-8", "replace")
    # komentarz widoczny = przypiety do tekstu (w:commentReference); comments.xml bywa pelen
    # osieroconych wpisow z wczesniejszej edycji (zmierzone: TK6 z 25.09 mial 31 bez odwolan)
    wpisy = sum(len(re.findall(r"<w:comment ", z.read(n).decode("utf-8", "replace")))
                for n in z.namelist() if re.fullmatch(r"word/comments\d*\.xml", n))
    return {"w:ins": len(re.findall(r"<w:ins ", x)), "w:del": len(re.findall(r"<w:del ", x)),
            "w:delText": len(re.findall(r"<w:delText", x)),
            "komentarze": len(re.findall(r"<w:commentReference", x)), "wpisy_comments_xml": wpisy}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--redline", type=Path, required=True)
    ap.add_argument("--czysty", type=Path)
    ap.add_argument("--edits", type=Path, nargs="+", help="edits.<DOK>.json [edits.<DOK>.decyzje.json] - oczekiwana liczba komentarzy")
    ap.add_argument("--katalog", type=Path, help="katalog wyniku (kontrola braku PDF)")
    a = ap.parse_args()
    bledy = []
    try:
        r = struktura(a.redline)
        print(f"REDLINE {a.redline.name}: " + " | ".join(f"{k} {v}" for k, v in r.items()))
        if r["w:ins"] + r["w:del"] == 0:
            bledy.append("REDLINE bez w:ins/w:del - zmiany poszly poza track changes")
        if r["w:del"] and not r["w:delText"]:
            bledy.append("REDLINE: usuniety tekst nie siedzi w w:delText")
        if a.edits:
            n = sum(len(json.loads(e.read_text(encoding="utf-8"))) for e in a.edits)
            if r["komentarze"] != n:
                bledy.append(f"REDLINE: komentarzy {r['komentarze']} != edycji {n} - kazda zmiana ma miec jeden komentarz z ID")
        if a.czysty:
            c = struktura(a.czysty)
            print(f"CZYSTY  {a.czysty.name}: " + " | ".join(f"{k} {v}" for k, v in c.items()))
            if c["w:ins"] or c["w:del"] or c["komentarze"]:
                bledy.append("CZYSTY: zostaly zmiany sledzone albo komentarze - sanitize --accept-all nie zadzialal")
            if c["wpisy_comments_xml"]:
                bledy.append(f"CZYSTY: {c['wpisy_comments_xml']} osieroconych wpisow w comments.xml (wyciek tresci komentarzy)")
    except (OSError, KeyError, zipfile.BadZipFile, json.JSONDecodeError) as e:
        print(f"BLAD: {e}", file=sys.stderr)
        return 2
    pliki = [p for p in (a.redline, a.czysty) if p]
    if SKAN.exists():
        wynik = subprocess.run([sys.executable, str(SKAN), *map(str, pliki)], capture_output=True, text=True)
        print(wynik.stdout.strip() or "skan_placeholder: czysto")
        if wynik.returncode == 1:
            bledy.append("placeholdery w wyniku - uzupelnij albo odnotuj swiadomie w raporcie")
    else:
        bledy.append(f"brak {SKAN} - skan placeholderow nie wykonany")
    katalog = a.katalog or a.redline.parent
    pdf = sorted(katalog.glob("*.pdf"))
    if pdf:
        bledy.append("PDF w katalogu wyniku: " + ", ".join(p.name for p in pdf))
    for b in bledy:
        print(f"NIEZGODNE: {b}")
    print("WYNIK: " + ("OK" if not bledy else f"{len(bledy)} niezgodnosci"))
    return 1 if bledy else 0


if __name__ == "__main__":
    sys.exit(main())
