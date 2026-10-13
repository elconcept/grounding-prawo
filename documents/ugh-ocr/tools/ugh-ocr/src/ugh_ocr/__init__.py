"""ugh-ocr: mieszany pipeline OCR (markitdown + llamaindex-ocr + markitdown-vision).

Per strone PDF: prawdziwa warstwa tekstu -> markitdown, reszta -> llamaindex-ocr
z automatycznym fallbackiem na markitdown-vision (Google Cloud Vision).
"""

from ._core import convert_file
from ._errors import UghOcrError
from ._pdf_analysis import classify_pages

__all__ = ["convert_file", "UghOcrError", "classify_pages"]
