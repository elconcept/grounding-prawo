"""CLI: llamaindex-ocr <plik>

Parsuje plik przez LlamaCloud i zapisuje wynik jako .md obok niego, pod ta
sama nazwa bazowa -- bez flagi -o, tak samo jak markitdown-vision.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ._core import TIER_AGENTIC, TIER_AGENTIC_PLUS, TIER_COST_EFFECTIVE, parse_file
from ._prompt import DEFAULT_CUSTOM_PROMPT


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="llamaindex-ocr",
        description=(
            "Parsuje plik przez LlamaCloud/LlamaParse. "
            "Wyjscie: <plik_wejsciowy_bez_rozszerzenia>.md"
        ),
    )
    parser.add_argument("input", type=Path, help="Plik wejsciowy (PDF i inne formaty obslugiwane przez LlamaParse)")
    parser.add_argument("--plus", action="store_true", help="Tier agentic_plus zamiast domyslnego agentic")
    parser.add_argument("--eco", action="store_true", help="Tier cost_effective zamiast domyslnego agentic")
    parser.add_argument("--polling-interval", type=float, default=3.0, help="Interwal polling SDK (sekundy)")
    parser.add_argument("--timeout", type=int, default=1800, help="Timeout SDK parse (sekundy)")
    parser.add_argument("--custom-prompt-file", default=None, help="Plik TXT/MD z wlasnym promptem parsera")
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
        output_path = parse_file(
            args.input,
            tier=tier,
            custom_prompt=custom_prompt,
            polling_interval=args.polling_interval,
            timeout=args.timeout,
        )
    except FileNotFoundError as e:
        print(f"Blad: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Blad parsowania: {e}", file=sys.stderr)
        return 1

    print(f"OK: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
