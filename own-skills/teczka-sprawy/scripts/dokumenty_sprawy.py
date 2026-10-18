#!/usr/bin/env python3
"""Odświeża spis dokumentów sprawy (`_dokumenty.md`) względem biblioteki `../dokumentacja` (tylko odczyt).

Spis ma sekcje `## \\`<katalog>\\`` i tabelę `| dokument | tekst |`; kolumna „tekst” = jest sidecar `<nazwa>.md`.
Stare ścieżki `01_dowody/...` (repo abogada) są przepisywane na `../dokumentacja/...`. Plik jest generowany:
nie dopisuj do niego ręcznie, dodaj katalog opcją --dodaj.

  python3 scripts/dokumenty_sprawy.py --sprawa <katalog>                 # podgląd zmian
  python3 scripts/dokumenty_sprawy.py --sprawa <katalog> --wykonaj
  python3 scripts/dokumenty_sprawy.py --sprawa <katalog> --dodaj Dokumentacja/przykladowa-sprawa --wykonaj
  python3 scripts/dokumenty_sprawy.py --wszystkie --wykonaj
"""
from __future__ import annotations

import argparse
import os
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("LEGAL_WORKSPACE", os.getcwd())).resolve()
BIBLIOTEKA = os.environ.get("LEGAL_DOCUMENTS", "Dokumentacja")
POMIN = {".DS_Store", "Thumbs.db"}


def rejestr(sprawa: Path) -> Path:
    for p in (sprawa / "analiza" / "_dokumenty.md", sprawa / "_dokumenty.md"):
        if p.exists():
            return p
    return sprawa / ("analiza" if (sprawa / "analiza").is_dir() else "") / "_dokumenty.md"


def katalogi(tekst: str) -> list[str]:
    out = []
    for m in re.finditer(r"^##\s+`([^`]+)`", tekst, re.M):
        k = re.sub(r"^01_dowody/", BIBLIOTEKA + "/", m.group(1).rstrip("/"))
        if k not in out:
            out.append(k)
    return out


def sidecar(p: Path) -> bool:
    return p.with_suffix(".md").exists() or (p.parent / (p.name + ".md")).exists()


def zbuduj(sprawa: Path, kats: list[str]) -> str:
    w = [f"# Dokumenty sprawy - {sprawa.name}", "",
         f"Wygenerowane {dt.date.today().strftime('%d.%m.%Y')} przez `scripts/dokumenty_sprawy.py`. Dokumenty leżą "
         f"w `{BIBLIOTEKA}/` (tylko odczyt); teczka nie ma kopii. Tekst dokumentu: sidecar `<nazwa>.md` obok pliku "
         "(kolumna „tekst”). Ścieżki względem katalogu `legal`.", ""]
    for k in kats:
        d = (ROOT / k).resolve()
        if not d.is_dir() and d.parent.is_dir():  # stare wpisy różnią się wielkością liter (III_Rns -> III_RNs)
            trafienie = [x for x in d.parent.iterdir() if x.is_dir() and x.name.lower() == d.name.lower()]
            if trafienie:
                d, k = trafienie[0], str(Path(k).parent / trafienie[0].name)
        w += [f"## `{k}`", ""]
        if not d.is_dir():
            w += ["**Katalog nie istnieje** - sprawdź ścieżkę w bibliotece.", ""]
            continue
        pliki = sorted(x for x in d.iterdir()
                       if x.is_file() and x.name not in POMIN and not x.name.startswith((".", "~$"))
                       and not (x.suffix == ".md" and any(x.with_suffix(s).exists() for s in (".pdf", ".jpg", ".png", ".docx", ".m4a", ".mp4", ".eml")))
                       and not x.name.endswith((".contract.json",)))
        w += ["| dokument | tekst |", "|---|---|"]
        w += [f"| `{x.name}` | {'tak' if x.suffix == '.md' or sidecar(x) else ''} |" for x in pliki]
        podk = sorted(x.name for x in d.iterdir() if x.is_dir() and not x.name.startswith(("@", ".", "#")))
        if podk:
            w += ["", "Podkatalogi: " + ", ".join(f"`{x}/`" for x in podk)]
        w.append("")
    return "\n".join(w)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--sprawa")
    g.add_argument("--wszystkie", action="store_true")
    ap.add_argument("--dodaj", action="append", default=[], help="katalog biblioteki do dodania (względem legal/)")
    ap.add_argument("--wykonaj", action="store_true")
    a = ap.parse_args()
    lista = ([ROOT / a.sprawa] if a.sprawa else
             sorted(d for d in ROOT.iterdir() if d.is_dir() and rejestr(d).exists() and not d.name.startswith(("_", ".", "@", "#"))))
    for sprawa in lista:
        if not sprawa.is_dir():
            print(f"brak katalogu sprawy: {sprawa}", file=sys.stderr)
            return 1
        rej = rejestr(sprawa)
        stary = rej.read_text(encoding="utf-8") if rej.exists() else ""
        kats = katalogi(stary) + [k.rstrip("/") for k in a.dodaj if k.rstrip("/") not in katalogi(stary)]
        if not kats:
            print(f"== {sprawa.name}: brak katalogów w spisie - podaj --dodaj")
            continue
        nowy = zbuduj(sprawa, kats)
        brak = nowy.count("**Katalog nie istnieje**")
        print(f"== {sprawa.name}: {len(kats)} katalogów{f', BRAK KATALOGÓW: {brak}' if brak else ''} -> {rej.relative_to(ROOT)}")
        if a.wykonaj:
            rej.parent.mkdir(parents=True, exist_ok=True)
            rej.write_text(nowy, encoding="utf-8")
    if not a.wykonaj:
        print("(podgląd; zapis z --wykonaj)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
