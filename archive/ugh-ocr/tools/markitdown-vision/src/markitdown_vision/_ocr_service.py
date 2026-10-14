"""Silnik OCR oparty o Google Cloud Vision.

Zgodny z interfejsem markitdown_ocr.LLMVisionOCRService: metoda
`extract_text(image_stream, prompt=None, stream_info=None, **kwargs) -> OCRResult`.
Podlaczany zamiast LLMVisionOCRService do PdfConverterWithOCR/DocxConverterWithOCR/
PptxConverterWithOCR/XlsxConverterWithOCR z pakietu markitdown-ocr -- cala logika
wykrywania "PDF bez warstwy tekstowej" i renderowania stron pozostaje ich,
zmienia sie tylko silnik OCR (Google Cloud Vision zamiast modelu LLM).
"""

from __future__ import annotations

from typing import Any, BinaryIO

from markitdown_ocr import OCRResult

BACKEND_NAME = "google-cloud-vision"


class GoogleVisionOCRService:
    """OCR service backed by Google Cloud Vision `document_text_detection`."""

    def __init__(self, client: Any | None = None) -> None:
        self._client = client

    @property
    def client(self) -> Any:
        if self._client is None:
            from google.cloud import vision

            self._client = vision.ImageAnnotatorClient()
        return self._client

    def extract_text(
        self,
        image_stream: BinaryIO,
        prompt: str | None = None,  # nieuzywane -- Vision document_text_detection nie bierze promptu
        stream_info: Any = None,
        **kwargs: Any,
    ) -> OCRResult:
        from google.cloud import vision

        try:
            image_stream.seek(0)
            content = image_stream.read()
            if not content:
                return OCRResult(
                    text="", backend_used=BACKEND_NAME, error="pusty strumien obrazu"
                )

            image = vision.Image(content=content)
            response = self.client.document_text_detection(image=image)

            if response.error and response.error.message:
                return OCRResult(
                    text="", backend_used=BACKEND_NAME, error=response.error.message
                )

            text = ""
            if response.full_text_annotation and response.full_text_annotation.text:
                text = response.full_text_annotation.text
            elif response.text_annotations:
                text = response.text_annotations[0].description

            return OCRResult(text=text.strip(), backend_used=BACKEND_NAME)
        except Exception as e:
            return OCRResult(text="", backend_used=BACKEND_NAME, error=str(e))
        finally:
            image_stream.seek(0)
