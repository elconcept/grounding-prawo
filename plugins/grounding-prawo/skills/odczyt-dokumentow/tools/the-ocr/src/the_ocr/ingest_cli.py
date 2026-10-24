"""Opt-in CLI for LLM-reviewed PDF ingest. Never changes the shared the-ocr CLI."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .page_capture import capture_page, make_a4_copy, number_of_pages


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="the-ocr-ingest-page",
        description="LLM-only workflow: OCR one PDF page into a Markdown candidate.",
    )
    parser.add_argument("input", type=Path, help="PDF source (never overwritten)")
    parser.add_argument("--page", type=int, help="Physical page number (required for multi-page PDFs)")
    parser.add_argument("-o", "--output", type=Path, help="Output Markdown candidate path")
    parser.add_argument("--force-provider", choices=["google_vision", "azure", "datalab", "llamaparse"],
                        help="Explicit OCR provider. Datalab/LlamaParse only after model reviews a failed primary result.")
    parser.add_argument("--fixme", action="store_true",
                        help="Save a separate <stem>_a4.pdf derivative. Original remains unchanged.")
    parser.add_argument("--searchable-pdf", action="store_true",
                        help="Create a separate searchable PDF using approved --from-json, not provider OCR")
    parser.add_argument("--from-json", type=Path,
                        help="Full-document corrected OCR JSON (required by --searchable-pdf)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        number_of_pages(args.input)
        if args.searchable_pdf:
            if args.from_json is None or args.page is not None or args.force_provider or args.fixme:
                raise ValueError("--searchable-pdf requires reviewed --from-json only; no --page/provider/--fixme")
            if not args.from_json.is_file():
                raise ValueError("Reviewed OCR contract JSON not found")
            from .pipeline import process_input
            output = args.output or args.input.with_name(args.input.stem + "_searchable.pdf")
            if output.suffix.lower() != ".pdf" or output.resolve() == args.input.resolve():
                raise ValueError("Searchable PDF must be a separate .pdf derivative")
            if output.exists():
                raise ValueError("Refusing to overwrite an existing derivative PDF")
            result = process_input(args.input, [], from_json=args.from_json,
                                   output=output, a4=False, layer="redo")
            if not result.ok:
                raise RuntimeError("Unable to build derivative PDF from reviewed contract")
            print(f"searchable_pdf: {result.pdf_path}")
            return 0
        if args.from_json is not None:
            raise ValueError("--from-json requires --searchable-pdf")
        if args.output is not None and args.output.suffix.lower() != ".md":
            raise ValueError("Single-page output must be Markdown (.md)")
        target, provider, page, total = capture_page(
            args.input, page=args.page, provider_name=args.force_provider,
            output=args.output,
        )
        if args.fixme:
            print(f"a4_derivative: {make_a4_copy(args.input)}")
        print(f"candidate_markdown: {target}")
        print(f"page: {page}/{total}; engine: {provider}; llm_review_required: true")
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
