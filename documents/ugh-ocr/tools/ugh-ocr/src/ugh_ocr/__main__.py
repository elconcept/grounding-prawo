"""CLI: ugh-ocr <plik>

Mieszany pipeline OCR: markitdown dla stron/plikow z prawdziwa warstwa
tekstu, llamaindex-ocr (LlamaParse) dla reszty, z automatycznym fallbackiem
na markitdown-vision (Google Cloud Vision) gdy llamaindex-ocr zawiedzie.
Wyjscie: <plik_wejsciowy_bez_rozszerzenia>.md -- bez flagi -o.
"""

from __future__ import annotations

import argparse
import sys
import textwrap
from pathlib import Path

from ._core import convert_file
from ._errors import UghOcrError
from llamaindex_ocr import DEFAULT_CUSTOM_PROMPT, TIER_AGENTIC, TIER_AGENTIC_PLUS, TIER_COST_EFFECTIVE


def _print_pretty_error(err: UghOcrError) -> None:
    # Znaki ASCII, nie Unicode box-drawing: konsola Windows w cp1252/cp850
    # (domyslny stdout PowerShell/cmd bez chcp 65001) rzuca UnicodeEncodeError
    # na "┌─│└" -- zweryfikowano empirycznie (crash w tescie z zepsutymi
    # obydwoma backendami OCR). ASCII dziala wszedzie.
    width = 70
    print(file=sys.stdout)
    print("+-- ugh-ocr: blad " + "-" * (width - 18), file=sys.stdout)
    for line in textwrap.wrap(err.title, width - 4) or [err.title]:
        print(f"| {line}", file=sys.stdout)
    if err.detail:
        print("|", file=sys.stdout)
        for raw_line in str(err.detail).splitlines() or [str(err.detail)]:
            for line in textwrap.wrap(raw_line, width - 4) or [""]:
                print(f"| {line}", file=sys.stdout)
    if err.hint:
        print("|", file=sys.stdout)
        for line in textwrap.wrap(f"Podpowiedz: {err.hint}", width - 4):
            print(f"| {line}", file=sys.stdout)
    print("+" + "-" * width, file=sys.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="ugh-ocr",
        description=(
            "Mieszany pipeline OCR dla PDF i obrazow: markitdown dla stron z "
            "prawdziwa warstwa tekstu, llamaindex-ocr (z fallbackiem na "
            "markitdown-vision/Google Cloud Vision) dla reszty. "
            "Wyjscie: <plik_wejsciowy_bez_rozszerzenia>.md"
        ),
    )
    parser.add_argument("input", type=Path, help="Plik wejsciowy (PDF lub obraz)")
    parser.add_argument("--plus", action="store_true", help="Tier LlamaParse agentic_plus zamiast domyslnego agentic")
    parser.add_argument("--eco", action="store_true", help="Tier LlamaParse cost_effective zamiast domyslnego agentic")
    parser.add_argument("--polling-interval", type=float, default=3.0, help="Interwal polling LlamaParse SDK (sekundy)")
    parser.add_argument("--timeout", type=int, default=1800, help="Timeout LlamaParse SDK (sekundy)")
    parser.add_argument("--custom-prompt-file", default=None, help="Plik TXT/MD z wlasnym promptem LlamaParse")
    args = parser.parse_args()

    if args.plus and args.eco:
        parser.error("Nie mozna jednoczesnie uzyc --plus i --eco.")

    tier = TIER_AGENTIC_PLUS if args.plus else TIER_COST_EFFECTIVE if args.eco else TIER_AGENTIC
    custom_prompt = (
        Path(args.custom_prompt_file).read_text(encoding="utf-8")
        if args.custom_prompt_file
        else DEFAULT_CUSTOM_PROMPT
    )

    try:
        output_path = convert_file(
            args.input,
            tier=tier,
            custom_prompt=custom_prompt,
            polling_interval=args.polling_interval,
            timeout=args.timeout,
            warn=print,
        )
    except UghOcrError as e:
        _print_pretty_error(e)
        return 1
    except Exception as e:
        _print_pretty_error(UghOcrError("Niespodziewany blad.", detail=str(e)))
        return 1

    print(f"OK: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
