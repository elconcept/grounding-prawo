#!/usr/bin/env python3
"""Generuje profesjonalny PDF z pliku Markdown (frontmatter YAML -> zmienne
szablonu, nie trafia do PDF; tresc pod naglowkiem YAML -> cialo dokumentu).

Uzycie:
    python generate_pdf.py <plik.md> [--template oswiadczenie] [--engine xelatex] [--out <plik.pdf>]

Szuka xelatex/MiKTeX automatycznie, jesli nie ma go w PATH (typowe na Windows
zaraz po instalacji przez oficjalny instalator, przed restartem powloki).
"""
import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SKILL_DIR / "templates"

MIKTEX_CANDIDATES = [
    Path.home() / "AppData/Local/Programs/MiKTeX/miktex/bin/x64",
    Path("C:/Program Files/MiKTeX/miktex/bin/x64"),
    Path("C:/ProgramData/chocolatey/lib/miktex/tools/miktex/bin/x64"),
]


def ensure_engine_on_path(engine: str) -> None:
    if shutil.which(engine):
        return
    for candidate in MIKTEX_CANDIDATES:
        if (candidate / f"{engine}.exe").exists():
            os.environ["PATH"] = str(candidate) + os.pathsep + os.environ["PATH"]
            return
    raise SystemExit(
        f"Nie znaleziono '{engine}' w PATH ani w typowych lokalizacjach MiKTeX. "
        "Zainstaluj MiKTeX lub podaj --engine innego silnika."
    )


def maybe_preprocess(input_path: Path, template_name: str) -> tuple[Path, Path | None]:
    """Jesli obok szablonu istnieje `<template>_pre.py` z funkcja
    `preprocess(input_path: Path) -> Path`, uruchamia ja przed pandokiem
    (np. do parsowania kluczy frontmatteru, ktorych sam jezyk szablonow
    pandoc nie potrafi obsluzyc -- patrz templates/pismo-procesowe_pre.py).
    Zwraca (sciezka_do_uzycia, sciezka_tymczasowa_do_posprzatania_lub_None).
    Brak `_pre.py` = zachowanie identyczne jak wczesniej (bez zmian)."""
    pre_script = TEMPLATES_DIR / f"{template_name}_pre.py"
    if not pre_script.exists():
        return input_path, None
    spec = importlib.util.spec_from_file_location(f"_pre_{template_name}", pre_script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result_path = module.preprocess(input_path)
    if result_path == input_path:
        return input_path, None
    return result_path, result_path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", type=Path, help="Plik .md do konwersji")
    ap.add_argument("--template", default="oswiadczenie", help="Nazwa szablonu w templates/ (bez .latex)")
    ap.add_argument("--engine", default="xelatex", help="Silnik PDF pandoc (domyslnie xelatex)")
    ap.add_argument("--out", type=Path, default=None, help="Sciezka wyjsciowa PDF (domyslnie ten sam basename)")
    args = ap.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Brak pliku wejsciowego: {args.input}")

    template_path = TEMPLATES_DIR / f"{args.template}.latex"
    if not template_path.exists():
        raise SystemExit(f"Brak szablonu: {template_path}")

    out_path = args.out or args.input.with_suffix(".pdf")

    if not shutil.which("pandoc"):
        raise SystemExit("Brak 'pandoc' w PATH.")

    ensure_engine_on_path(args.engine)

    used_input, tmp_to_clean = maybe_preprocess(args.input, args.template)

    cmd = [
        "pandoc",
        str(used_input),
        "-o", str(out_path),
        f"--pdf-engine={args.engine}",
        f"--template={template_path}",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
    finally:
        if tmp_to_clean is not None:
            tmp_to_clean.unlink(missing_ok=True)
    # MiKTeX drukuje ostrzezenia ("security risk", "major issue") na stderr
    # nawet przy sukcesie -- nie sa bledem, ale pokaz je dla przejrzystosci.
    if result.stderr.strip():
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        raise SystemExit(f"pandoc zakonczyl sie kodem {result.returncode}")

    print(f"OK: {out_path}")


if __name__ == "__main__":
    main()
