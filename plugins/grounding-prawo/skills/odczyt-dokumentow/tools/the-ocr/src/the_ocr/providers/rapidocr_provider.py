from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pymupdf

from ..models import OCRBlock, OCRDocument, OCRPage, doc_id_for, normalize_bbox
from .base import OCRProvider, OCRResult


class RapidOCRProvider(OCRProvider):
    """Lokalny OCR na CPU (RapidOCR, ONNX) - fallback bez chmury.

    Wymaga opcjonalnej zaleznosci ``rapidocr-onnxruntime`` (extra ``local``).
    Strony renderowane w ``THE_OCR_RAPIDOCR_DPI`` (domyslnie 200). RapidOCR
    zwraca linie z ramkami, nie slowa: kazda linia to blok z wlasnym bbox,
    bez wymyslonych wspolrzednych slow.
    """

    name = "rapidocr"

    def __init__(self) -> None:
        self._engine = None

    def is_available(self) -> tuple[bool, str]:
        try:
            import rapidocr_onnxruntime  # noqa: F401
        except ImportError:
            return False, "rapidocr-onnxruntime is not installed (extra 'local')"
        return True, ""

    def recognize(self, path: Path) -> OCRResult:
        available, reason = self.is_available()
        if not available:
            return OCRResult(text="", backend=self.name, error=reason)
        try:
            document = self._recognize(path)
            return OCRResult(text=document.text, backend=self.name, document=document)
        except Exception as exc:
            return OCRResult(text="", backend=self.name, error=f"RapidOCR: {exc}")

    def _recognize(self, path: Path) -> OCRDocument:
        if self._engine is None:
            from rapidocr_onnxruntime import RapidOCR

            self._engine = RapidOCR()
        dpi = int(os.getenv("THE_OCR_RAPIDOCR_DPI", "200"))
        pages: list[OCRPage] = []
        with pymupdf.open(path) as pdf:
            for index, page in enumerate(pdf, start=1):
                pixmap = page.get_pixmap(dpi=dpi, colorspace=pymupdf.csRGB, alpha=False)
                result, _ = self._engine(pixmap.tobytes("png"))
                pages.append(_page(index, page.rect.width, page.rect.height, pixmap.width, pixmap.height, result or []))
        document = OCRDocument(doc_id=doc_id_for(path), provider=self.name, pages=tuple(pages), source_name=path.name)
        document.validate()
        return document


def _page(number: int, width: float, height: float, pixel_width: int, pixel_height: int, lines: list[Any]) -> OCRPage:
    blocks: list[OCRBlock] = []
    for points, text, score in lines:
        text = str(text).strip()
        if not text:
            continue
        xs = [float(point[0]) for point in points]
        ys = [float(point[1]) for point in points]
        try:
            bbox = normalize_bbox([min(xs), min(ys), max(xs), max(ys)], pixel_width, pixel_height)
        except ValueError:
            continue
        blocks.append(
            OCRBlock(
                id=f"p{number:04d}-b{len(blocks) + 1:04d}",
                page=number,
                block_type="paragraph",
                text=text,
                markdown=text,
                bbox=bbox,
                confidence=float(score) if score is not None else None,
            )
        )
    blocks.sort(key=lambda block: (round(block.bbox[1], 2), block.bbox[0]))  # type: ignore[index]
    return OCRPage(number, width, height, tuple(blocks))
