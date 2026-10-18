from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import PROVIDER_NAMES, all_providers, default_providers
from .providers import PROVIDER_ALIASES
from .pipeline import process_input
from .page_capture import capture_page, make_a4_copy


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="the-ocr",
        description=(
            "PDF-only, model-reviewed OCR. Default: one physical page into Markdown; "
            "Google Vision/Azure first, Datalab/LlamaParse only on explicit review fallback."
        ),
    )
    parser.add_argument("input", type=Path, help="original PDF (never overwritten)")
    parser.add_argument("--page", type=int, help="physical page, 1-based (mandatory for multi-page PDF)")
    parser.add_argument("--legacy-pipeline", action="store_true", help="explicit compatibility for existing Paperless full-document OCR; requires -o <other.pdf>")
    parser.add_argument("--fixme", action="store_true", help="write a separate A4-fitted PDF; preserve original")
    parser.add_argument("--searchable-pdf", action="store_true", help="rebuild OCR layer only from --from-json reviewed contract")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="output Markdown path (default: <stem>.md for single-page, per-page candidates for multi-page); PDF derivative with --from-json",
    )
    parser.add_argument("--markdown", action="store_true", help="legacy flag; Markdown is now the default")
    parser.add_argument("--json", action="store_true", dest="json_output", help="also write <output>.json (doc-intel-contract-pl)")
    parser.add_argument(
        "--words",
        action="store_true",
        help="JSON with editable word geometry (blocks[].words[]) for --from-json; implies --json",
    )
    parser.add_argument(
        "--from-json",
        type=Path,
        default=None,
        metavar="JSON",
        help="no OCR provider: build the text layer from this (corrected) JSON with blocks[].words[]",
    )
    parser.add_argument(
        "--archive",
        action="store_true",
        help="copy the original to the archive before OCR (default dir: $THE_OCR_ARCHIVE_DIR or ~/archive)",
    )
    parser.add_argument(
        "--archive-dir",
        type=Path,
        default=None,
        help="archive directory; implies --archive",
    )
    parser.add_argument(
        "--keep-geometry",
        action="store_false",
        dest="a4",
        help="keep original PDF page sizes (default: fit pages to A4)",
    )
    parser.add_argument(
        "--layer",
        choices=["auto", "redo", "skip", "force"],
        default="auto",
        help="OCRmyPDF text-layer mode (default auto: redo, skip for PDF forms; force rasterizes pages)",
    )
    ocrmypdf = parser.add_argument_group("OCRmyPDF")
    ocrmypdf.add_argument(
        "--optimize",
        type=int,
        choices=[0, 1, 2, 3],
        default=1,
        help="OCRmyPDF --optimize: 0 off, 1 lossless (default), 2-3 lossy (need pngquant, jbig2enc)",
    )
    ocrmypdf.add_argument(
        "--clean-final",
        action="store_true",
        help="OCRmyPDF --clean-final: unpaper-cleaned page images in the output (needs --layer force and unpaper)",
    )
    ocrmypdf.add_argument("--pdfa", action="store_true", help="OCRmyPDF --output-type pdfa (PDF/A-2b)")
    parser.add_argument(
        "--force-provider",
        choices=[*PROVIDER_NAMES, *PROVIDER_ALIASES],
        help="diagnostic override; run only this provider",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    input_path: Path = args.input
    if not input_path.is_file():
        print(f"error: no such file: {input_path}", file=sys.stderr)
        return 1

    if args.from_json is not None and args.force_provider:
        print("error: --from-json and --force-provider exclude each other", file=sys.stderr)
        return 1
    if args.from_json is not None and not args.from_json.is_file():
        print(f"error: no such file: {args.from_json}", file=sys.stderr)
        return 1
    if args.clean_final and args.layer != "force":
        print("error: --clean-final needs --layer force (OCRmyPDF refuses it with redo; skip leaves text pages)", file=sys.stderr)
        return 1

    compat_full_pdf = args.legacy_pipeline or (args.output is not None and args.output.suffix.lower() == ".pdf")
    if args.searchable_pdf and args.from_json is None:
        print("error: --searchable-pdf requires a reviewed --from-json contract", file=sys.stderr)
        return 1
    if not compat_full_pdf and input_path.suffix.lower() != ".pdf":
        print("error: model-reviewed ingest accepts only PDF", file=sys.stderr)
        return 1
    if compat_full_pdf:
        if args.output is None or args.output.resolve() == input_path.resolve() or args.output.suffix.lower() != ".pdf":
            print("error: legacy conversion requires -o <separate.pdf>", file=sys.stderr)
            return 1
    if args.from_json is None and not compat_full_pdf:
        if args.searchable_pdf:
            print("error: --searchable-pdf requires LLM-reviewed --from-json; no automatic full-document OCR", file=sys.stderr)
            return 1
        if args.json_output or args.words or args.archive or args.archive_dir is not None or args.layer != "auto":
            print("error: these legacy PDF flags require explicit --from-json and --searchable-pdf", file=sys.stderr)
            return 1
        try:
            target, provider, page, total = capture_page(
                input_path, page=args.page, provider_name=args.force_provider, output=args.output
            )
            if args.fixme:
                print(f"pdf_a4: {make_a4_copy(input_path)}")
            print(f"candidate_markdown: {target}")
            print(f"page: {page}/{total}; provider: {provider}; review_required: true")
            return 0
        except (OSError, ValueError, RuntimeError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
    if args.page is not None:
        print("error: legacy/full PDF conversion produces a full PDF derivative, not a single-page candidate", file=sys.stderr)
        return 1
    if args.output is not None and args.output.resolve() == input_path.resolve():
        print("error: original PDF must not be overwritten", file=sys.stderr)
        return 1

    providers = [] if args.from_json is not None else all_providers() if args.force_provider else default_providers()
    try:
        result = process_input(
            input_path,
            providers,
            force=args.force_provider,
            output=args.output or input_path.with_name(input_path.stem + "_searchable.pdf"),
            markdown=args.markdown,
            json_output=args.json_output or args.words,
            archive=args.archive,
            archive_dir=args.archive_dir,
            a4=args.fixme if not compat_full_pdf else True,
            layer="redo" if args.layer == "auto" and args.from_json is not None else args.layer,
            from_json=args.from_json,
            words=args.words,
            optimize=args.optimize,
            clean_final=args.clean_final,
            pdfa=args.pdfa,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for attempt in result.chain_result.attempts:
        detail = f" -- {attempt.reason}" if attempt.reason else ""
        print(f"[{attempt.provider}] {attempt.outcome}{detail}", file=sys.stderr)
    if not result.ok:
        kept = f"; original preserved as {result.archive_path}" if result.archive_path else "; input left unchanged"
        print(f"error: OCR failed{kept}", file=sys.stderr)
        return 2

    if result.archive_path:
        print(f"archive: {result.archive_path}")
    print(f"pdf: {result.pdf_path}")
    if result.markdown_path:
        print(f"markdown: {result.markdown_path}")
    if result.json_path:
        print(f"json: {result.json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
