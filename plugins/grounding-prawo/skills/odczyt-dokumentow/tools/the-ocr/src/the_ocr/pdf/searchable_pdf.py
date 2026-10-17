"""Searchable PDF via OCRmyPDF (official fpdf2 text renderer).

Provider word geometry flows through the engine plugin
(:mod:`the_ocr.pdf.ocrmypdf_plugin`) fed by a sidecar file
(:mod:`the_ocr.pdf.ocr_words`); the text layer itself is placed by
OCRmyPDF, never by hand-written PDF operators. Tesseract never runs.

``mode`` is OCRmyPDF's own ``--mode`` for pages that already carry text:

- ``force`` (default, CLI behaviour): rasterize every page, then place the layer;
- ``redo``: OCRmyPDF strips the old invisible OCR layer and keeps vector
  content and visible native text;
- ``skip``: pages that already have text are left as they are (mixed PDFs:
  native pages keep their text, scanned pages get the provider layer).
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from ..models import OCRDocument
from .ocr_words import write_engine_sidecar

_PLUGIN = Path(__file__).with_name("ocrmypdf_plugin.py")

LAYER_MODES = ("force", "redo", "skip")


def build_document_searchable_pdf(
    src: Path,
    dst: Path,
    document: OCRDocument,
    *,
    mode: str = "force",
    optimize: int = 1,
) -> None:
    """Graft the provider text layer onto ``src`` pages, writing ``dst``."""
    import ocrmypdf
    import pymupdf
    from ocrmypdf.exceptions import ExitCode

    if mode not in LAYER_MODES:
        raise ValueError(f"unknown text-layer mode '{mode}'; expected one of {', '.join(LAYER_MODES)}")
    with pymupdf.open(src) as pdf:
        if len(pdf) != len(document.pages):
            raise ValueError(
                f"page count mismatch: {src} has {len(pdf)} pages, OCR has {len(document.pages)}"
            )
    with tempfile.TemporaryDirectory(prefix="the-ocr-words-") as work:
        sidecar = Path(work) / "words.json"
        write_engine_sidecar(document, sidecar)
        code = ocrmypdf.ocr(
            src,
            dst,
            plugins=[_PLUGIN],
            mode=mode,
            output_type="pdf",
            pdf_renderer="fpdf2",
            optimize=optimize,
            progress_bar=False,
            language=["pol"],
            the_ocr_words=sidecar,
        )
    if code != ExitCode.ok:
        raise RuntimeError(f"OCRmyPDF failed with exit code {code}")
