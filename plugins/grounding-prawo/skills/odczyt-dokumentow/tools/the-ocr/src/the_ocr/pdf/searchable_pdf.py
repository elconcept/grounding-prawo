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

# Dotted module name, not a file path: a frozen (PyInstaller) build has no
# .py files on disk, only the bundled modules.
_PLUGIN = "the_ocr.pdf.ocrmypdf_plugin"

LAYER_MODES = ("force", "redo", "skip")


def build_document_searchable_pdf(
    src: Path,
    dst: Path,
    document: OCRDocument,
    *,
    mode: str = "force",
    optimize: int = 1,
    clean_final: bool = False,
    pdfa: bool = False,
) -> None:
    """Graft the provider text layer onto ``src`` pages, writing ``dst``.

    ``optimize`` is OCRmyPDF's ``--optimize`` (0-3), ``clean_final`` its
    ``--clean-final`` (unpaper-cleaned page images in the output; ``force``
    only, since OCRmyPDF refuses it with ``redo`` and ``skip`` keeps text
    pages untouched) and ``pdfa`` selects ``--output-type pdfa``.
    """
    import ocrmypdf
    import pymupdf
    from ocrmypdf.exceptions import ExitCode

    if mode not in LAYER_MODES:
        raise ValueError(f"unknown text-layer mode '{mode}'; expected one of {', '.join(LAYER_MODES)}")
    if optimize not in (0, 1, 2, 3):
        raise ValueError(f"optimize must be 0-3, got {optimize}")
    if clean_final and mode != "force":
        raise ValueError("--clean-final needs the force text-layer mode (--layer force)")
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
            output_type="pdfa" if pdfa else "pdf",
            pdf_renderer="fpdf2",
            optimize=optimize,
            clean_final=clean_final,
            progress_bar=False,
            language=["pol"],
            the_ocr_words=sidecar,
        )
    if code != ExitCode.ok:
        raise RuntimeError(f"OCRmyPDF failed with exit code {code}")
