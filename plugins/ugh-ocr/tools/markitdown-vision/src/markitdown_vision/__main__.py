"""CLI: markitdown-vision <plik>

Konwertuje plik do Markdown, zapisujac wynik obok wejscia pod ta sama nazwa
(tylko rozszerzenie .md) -- bez flagi -o. Automatyczny Google Cloud Vision
OCR dla obrazow i PDF-ow bez warstwy tekstowej.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ._core import convert_file


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="markitdown-vision",
        description=(
            "Konwertuje plik do Markdown (markitdown + Google Cloud Vision OCR "
            "w razie potrzeby). Wyjscie: <plik_wejsciowy_bez_rozszerzenia>.md"
        ),
    )
    parser.add_argument(
        "input", type=Path, help="Plik wejsciowy (PDF, obraz, DOCX, PPTX, XLSX, ...)"
    )
    args = parser.parse_args()

    try:
        output_path = convert_file(args.input)
    except FileNotFoundError as e:
        print(f"Blad: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Blad konwersji: {e}", file=sys.stderr)
        return 1

    print(f"OK: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
