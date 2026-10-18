"""OCRmyPDF engine plugin: provider OCR results instead of Tesseract.

Loaded via ``ocrmypdf.ocr(..., plugins=["the_ocr.pdf.ocrmypdf_plugin"])`` with
``the_ocr_words=<sidecar.json>`` (see :mod:`the_ocr.pdf.ocr_words`). The
engine serves precomputed provider word geometry page by page through the
official ``OcrEngine.generate_ocr`` API, so OCRmyPDF's own fpdf2 renderer
places the text layer -- Tesseract never runs and no PDF operators are
hand-written here.

Stateless across worker processes: every call reads the sidecar file and
indexes it with the ``page_number`` OCRmyPDF provides.
"""

from __future__ import annotations

import json
from pathlib import Path

from the_ocr.pdf.ocr_words import build_page_tree, page_text, read_image_size

from ocrmypdf import hookimpl
from ocrmypdf.pluginspec import OcrEngine, OcrOptions, OrientationConfidence


@hookimpl
def add_options(parser) -> None:
    parser.add_argument(
        "--the-ocr-words",
        type=Path,
        default=None,
        help="the-ocr word-geometry sidecar JSON (internal option)",
    )


@hookimpl
def get_ocr_engine(options: OcrOptions | None):
    if options is None:
        return None
    sidecar = getattr(options, "the_ocr_words", None)
    if not sidecar:
        return None
    return TheOcrEngine(Path(sidecar))


class TheOcrEngine(OcrEngine):
    """Serve the-ocr provider geometry as an OCRmyPDF engine."""

    def __init__(self, sidecar: Path):
        self._sidecar = sidecar

    @staticmethod
    def version() -> str:
        return "the-ocr provider geometry 1"

    @staticmethod
    def creator_tag(options: OcrOptions) -> str:
        return "the-ocr"

    def __str__(self) -> str:
        return "the-ocr provider engine"

    @staticmethod
    def languages(options: OcrOptions):
        return {"pol"}

    @staticmethod
    def get_orientation(input_file: Path, options: OcrOptions) -> OrientationConfidence:
        return OrientationConfidence(angle=0, confidence=0.0)

    @staticmethod
    def get_deskew(input_file: Path, options: OcrOptions) -> float:
        return 0.0

    @staticmethod
    def supports_generate_ocr() -> bool:
        return True

    def generate_ocr(self, input_file: Path, options: OcrOptions, page_number: int = 0):
        payload = json.loads(self._sidecar.read_text(encoding="utf-8"))
        pages = payload.get("pages") or []
        words = pages[page_number]["words"] if 0 <= page_number < len(pages) else []
        tree = build_page_tree(words, read_image_size(input_file))
        return tree, page_text(words)

    @staticmethod
    def generate_hocr(input_file: Path, output_hocr: Path, output_text: Path, options: OcrOptions) -> None:
        raise RuntimeError("the-ocr engine serves generate_ocr() (fpdf2 renderer); generate_hocr() is not used")

    @staticmethod
    def generate_pdf(input_file: Path, output_pdf: Path, output_text: Path, options: OcrOptions) -> None:
        raise RuntimeError("the-ocr engine serves generate_ocr() (fpdf2 renderer); generate_pdf() is not used")
