"""Konwerter dla samodzielnych plikow graficznych (jpg/png/tiff/...).

markitdown-ocr obsluguje tylko obrazy OSADZONE w PDF/DOCX/PPTX/XLSX -- dla
samodzielnego pliku graficznego potrzebny jest osobny, prosty konwerter,
ktory po prostu odpala Google Cloud Vision na calym obrazie.
"""

from __future__ import annotations

from typing import Any, BinaryIO

from markitdown import DocumentConverter, DocumentConverterResult, StreamInfo

from ._ocr_service import GoogleVisionOCRService

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp", ".gif"}


class ImageOCRConverter(DocumentConverter):
    """Konwertuje samodzielny plik graficzny na markdown przez Google Cloud Vision."""

    def __init__(self, ocr_service: GoogleVisionOCRService):
        super().__init__()
        self.ocr_service = ocr_service

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mime = (stream_info.mimetype or "").lower()
        ext = (stream_info.extension or "").lower()
        return mime.startswith("image/") or ext in IMAGE_EXTENSIONS

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        result = self.ocr_service.extract_text(file_stream, stream_info=stream_info)
        if result.error:
            raise RuntimeError(f"Google Cloud Vision OCR nie powiodl sie: {result.error}")

        markdown = f"*[Google Vision OCR]*\n\n{result.text}\n" if result.text else ""
        return DocumentConverterResult(markdown=markdown, title=stream_info.filename)
