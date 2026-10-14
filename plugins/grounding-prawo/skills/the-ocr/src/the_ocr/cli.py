from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import all_providers, default_providers
from .pipeline import process_input


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="the-ocr",
        description="Create searchable PDF, Markdown, and spatial JSON using Datalab with LlamaParse fallback.",
    )
    parser.add_argument("input", type=Path, help="path to a PDF, JPG, JPEG, or PNG file")
    parser.add_argument(
        "--force-provider",
        choices=("datalab", "llamaparse", "azure-di", "google-vision"),
        help="diagnostic override; normal processing uses Datalab then LlamaParse",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    input_path: Path = args.input
    if not input_path.is_file():
        print(f"error: no such file: {input_path}", file=sys.stderr)
        return 1

    providers = all_providers() if args.force_provider else default_providers()
    try:
        result = process_input(input_path, providers, force=args.force_provider)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for attempt in result.chain_result.attempts:
        detail = f" -- {attempt.reason}" if attempt.reason else ""
        print(f"[{attempt.provider}] {attempt.outcome}{detail}", file=sys.stderr)
    if not result.ok:
        print(f"error: OCR failed; original preserved as {result.archive_path}", file=sys.stderr)
        return 2

    print(f"archive: {result.archive_path}")
    print(f"pdf: {result.pdf_path}")
    print(f"markdown: {result.markdown_path}")
    print(f"json: {result.json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
