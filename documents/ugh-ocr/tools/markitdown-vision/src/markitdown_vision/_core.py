"""Rdzen: budowa instancji MarkItDown z podpietym Google Cloud Vision OCR
oraz konwersja pojedynczego pliku wejsciowego do pliku .md obok niego.

Konwertery rejestrowane sa recznie (nie przez mechanizm auto-discovery
pluginow markitdowna) -- kolejnosc prob i silnik OCR sa jawne:
  1. ImageOCRConverter -- samodzielne obrazy (jpg/png/tiff/...), zawsze przez
     Google Cloud Vision.
  2. PdfConverterWithOCR/DocxConverterWithOCR/PptxConverterWithOCR/
     XlsxConverterWithOCR (z pakietu markitdown-ocr) -- normalna ekstrakcja
     tekstu, a Google Cloud Vision tylko gdy strona/plik nie ma warstwy
     tekstowej albo zawiera osadzone obrazy. Logika wykrywania "brak warstwy
     tekstowej" jest markitdown-ocr -- nie jest tu duplikowana.
  3. Wszystko inne (html, xlsx bez obrazow, txt, ...) -- wbudowane konwertery
     markitdowna, bez zmian.
"""

from __future__ import annotations

from pathlib import Path

from markitdown import PRIORITY_SPECIFIC_FILE_FORMAT, MarkItDown
from markitdown_ocr import (
    DocxConverterWithOCR,
    PdfConverterWithOCR,
    PptxConverterWithOCR,
    XlsxConverterWithOCR,
)

from ._frontmatter import render_with_frontmatter
from ._image_converter import ImageOCRConverter
from ._ocr_service import GoogleVisionOCRService

PRIORITY_OCR_ENHANCED = PRIORITY_SPECIFIC_FILE_FORMAT - 1  # przed wbudowanymi konwerterami
PRIORITY_IMAGE = PRIORITY_SPECIFIC_FILE_FORMAT - 10  # jeszcze wczesniej


def build_markitdown(ocr_service: GoogleVisionOCRService | None = None) -> MarkItDown:
    """Tworzy MarkItDown z recznie zarejestrowanymi konwerterami OCR."""
    ocr_service = ocr_service or GoogleVisionOCRService()
    md = MarkItDown()

    md.register_converter(ImageOCRConverter(ocr_service), priority=PRIORITY_IMAGE)
    md.register_converter(
        PdfConverterWithOCR(ocr_service=ocr_service), priority=PRIORITY_OCR_ENHANCED
    )
    md.register_converter(
        DocxConverterWithOCR(ocr_service=ocr_service), priority=PRIORITY_OCR_ENHANCED
    )
    md.register_converter(
        PptxConverterWithOCR(ocr_service=ocr_service), priority=PRIORITY_OCR_ENHANCED
    )
    md.register_converter(
        XlsxConverterWithOCR(ocr_service=ocr_service), priority=PRIORITY_OCR_ENHANCED
    )

    return md


def convert_markdown(input_path: Path, markitdown: MarkItDown | None = None) -> str:
    """Konwertuje `input_path` do tekstu Markdown, bez frontmatteru ani zapisu
    do pliku -- do uzycia przez inne narzedzia (np. ugh-ocr) ktore chca sam
    tekst wyniku."""
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Brak pliku wejsciowego: {input_path}")

    markitdown = markitdown or build_markitdown()
    result = markitdown.convert(str(input_path))
    return result.markdown or ""


def convert_file(input_path: Path, markitdown: MarkItDown | None = None) -> Path:
    """Konwertuje `input_path` do pliku .md o tej samej nazwie/lokalizacji
    (nadpisuje istniejacy .md o tej samej nazwie). Zwraca sciezke wynikowa."""
    input_path = Path(input_path)
    markdown = convert_markdown(input_path, markitdown=markitdown)

    output_path = input_path.with_suffix(".md")
    output_path.write_text(
        render_with_frontmatter(input_path, markdown),
        encoding="utf-8",
    )
    return output_path
