"""markitdown-vision: MarkItDown + Google Cloud Vision OCR.

Konwertuje dowolny plik do .md obok niego, bez potrzeby podawania sciezki
wyjsciowej. Automatycznie uzywa Google Cloud Vision do OCR dla samodzielnych
obrazow oraz dla PDF-ow (i DOCX/PPTX/XLSX z osadzonymi obrazami), gdy brak
warstwy tekstowej.
"""

from ._core import build_markitdown, convert_file, convert_markdown
from ._frontmatter import build_frontmatter, ocr_was_used
from ._ocr_service import GoogleVisionOCRService

__all__ = [
    "build_markitdown",
    "convert_file",
    "convert_markdown",
    "build_frontmatter",
    "ocr_was_used",
    "GoogleVisionOCRService",
]
