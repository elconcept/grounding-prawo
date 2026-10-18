from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import PROVIDER_NAMES, all_providers, default_providers
from .providers import PROVIDER_ALIASES
from .pipeline import process_input


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="the-ocr",
        description=(
            "Create a faithful searchable PDF (Datalab -> LlamaParse -> Azure Document "
            "Intelligence -> Google Vision). Markdown, JSON and an archive copy are optional."
        ),
    )
    parser.add_argument("input", type=Path, help="path to a PDF, JPG, JPEG, or PNG file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="output PDF path (default: PDF in place, image -> <stem>.pdf beside it)",
    )
    parser.add_argument("--markdown", action="store_true", help="also write <output>.md")
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

    providers = [] if args.from_json is not None else all_providers() if args.force_provider else default_providers()
    try:
        result = process_input(
            input_path,
            providers,
            force=args.force_provider,
            output=args.output,
            markdown=args.markdown,
            json_output=args.json_output or args.words,
            archive=args.archive,
            archive_dir=args.archive_dir,
            a4=args.a4,
            layer=args.layer,
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
