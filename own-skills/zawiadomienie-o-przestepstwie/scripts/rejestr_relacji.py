#!/usr/bin/env python3
"""Rejestr relacji (autora i innych osób) do HARDGATE skilla zawiadomienie-o-przestepstwie.

Szuka w 01_dowody/ sidecarów .md, które wyglądają na relacje złożone (protokoły przesłuchań,
zeznania, wyjaśnienia, zawiadomienia, oświadczenia) i wiążą się z osobą lub sygnaturą.
Wynik to lista KANDYDATÓW - model sprawdza, które są relacjami autora pisma.

Użycie (z korzenia repo):
  python3 .Codex/skills/zawiadomienie-o-przestepstwie/scripts/rejestr_relacji.py \
      --osoba "Kaczmarczyk" [--osoba "Tomasz"] [--sygnatura II_W_1342_26] [--tresc] [--json]

--tresc   szuka nazwiska także w treści sidecara (wolniej na NFS), nie tylko w ścieżce.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

SLOWA_RELACJI = [
    "przesluch", "zeznan", "wyjasnien", "protokol", "zawiadom", "oswiadcz",
    "wycofan", "odstapien", "wysluchan", "ustne", "uzupelnien",
]
POMIJANE_KATALOGI = {"#snapshot", "#recycle", "@eaDir", ".git"}


def bez_ogonkow(tekst: str) -> str:
    tekst = tekst.replace("ł", "l").replace("Ł", "L")
    return unicodedata.normalize("NFKD", tekst).encode("ascii", "ignore").decode().lower()


def korzen_repo(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / "01_dowody").is_dir():
            return p
    sys.exit("Nie znaleziono 01_dowody/ - uruchom z wnętrza repo abogada.")


def zawiera(tekst: str, fraza: str) -> bool:
    """Dopasowanie całego tokenu: krótkie inicjały (TK, NC) nie łapią się wewnątrz słów."""
    return re.search(rf"(?<![a-z0-9]){re.escape(fraza)}(?![a-z0-9])", tekst) is not None


def data_z_nazwy(nazwa: str) -> str:
    m = re.search(r"(20\d{2})[-_]?(\d{2})[-_]?(\d{2})", nazwa)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else ""


def karta_z_nazwy(nazwa: str) -> str:
    m = re.search(r"_(k\d+(?:-k?\d+)?)_", nazwa)
    return m.group(1) if m else ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--osoba", action="append", default=[], help="nazwisko lub imię (można powtórzyć)")
    ap.add_argument("--sygnatura", action="append", default=[], help="fragment ścieżki z sygnaturą")
    ap.add_argument("--tresc", action="store_true", help="szukaj osoby także w treści sidecara")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = korzen_repo(Path.cwd())
    osoby = [bez_ogonkow(o) for o in args.osoba]
    sygn = [bez_ogonkow(s) for s in args.sygnatura]

    wyniki = []
    for p in sorted((root / "01_dowody").rglob("*.md")):
        if POMIJANE_KATALOGI & set(p.parts) or p.name.startswith("._"):
            continue
        rel = p.relative_to(root).as_posix()
        klucz = bez_ogonkow(rel)
        slowa = [s for s in SLOWA_RELACJI if s in klucz]
        if not slowa:
            continue
        if sygn and not any(s in klucz for s in sygn):
            continue
        trafienie_osoby = [o for o in osoby if zawiera(klucz, o)]
        if osoby and not trafienie_osoby and args.tresc:
            try:
                tekst = bez_ogonkow(p.read_text(encoding="utf-8", errors="ignore"))
            except OSError:
                tekst = ""
            trafienie_osoby = [o for o in osoby if zawiera(tekst, o)]
        if osoby and not trafienie_osoby and not sygn:
            continue
        zrodlo = next((p.with_suffix(e) for e in (".pdf", ".jpg", ".png", ".docx") if p.with_suffix(e).exists()), None)
        wyniki.append({
            "plik": rel,
            "zrodlo": zrodlo.relative_to(root).as_posix() if zrodlo else "",
            "data": data_z_nazwy(p.name),
            "karta": karta_z_nazwy(p.name),
            "slowa": ",".join(slowa),
            "osoba": ",".join(trafienie_osoby),
        })

    wyniki.sort(key=lambda w: (w["data"] or "9999", w["plik"]))
    if args.json:
        print(json.dumps(wyniki, ensure_ascii=False, indent=2))
        return 0
    print(f"Kandydaci na relacje (do sprawdzenia): {len(wyniki)}\n")
    print("| Data | Karta | Plik | Słowa | Osoba |")
    print("|---|---|---|---|---|")
    for w in wyniki:
        print(f"| {w['data']} | {w['karta']} | `{w['plik']}` | {w['slowa']} | {w['osoba']} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
