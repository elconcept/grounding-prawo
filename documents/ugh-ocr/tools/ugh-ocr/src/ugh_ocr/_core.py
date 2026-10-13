"""Rdzen ugh-ocr: mieszany pipeline OCR dla PDF-ow i obrazow.

Strategia dla PDF, per strona:
  - strona z prawdziwa (widoczna) warstwa tekstu -> zwykly markitdown
    (bez OCR -- to zbedne, tekst jest juz w PDF).
  - strona bez prawdziwej warstwy tekstu (w tym strona z niewidoczna warstwa
    OCR nalozona wczesniej przez inne narzedzie -- patrz _pdf_analysis.py) ->
    llamaindex-ocr (LlamaParse). Renderowanie do obrazu i ignorowanie
    istniejacego tekstu PDF jest celowe: chcemy swiezego OCR, nie odczytu
    potencjalnie niskiej jakosci istniejacej warstwy.
  - jesli llamaindex-ocr zawiedzie (brak/zly klucz, brak srodkow, blad sieci)
    -> ostrzezenie na stdout + przelaczenie na markitdown-vision (Google
    Cloud Vision) dla tej i wszystkich pozostalych stron OCR w tym pliku.
  - jesli rowniez markitdown-vision zawiedzie -> UghOcrError (CLI formatuje
    czytelnie i konczy dzialanie, bez dalszych prob).

Dla samodzielnych obrazow: ta sama kolejnosc (llamaindex-ocr -> fallback
markitdown-vision), bez etapu klasyfikacji stron.
"""

from __future__ import annotations

import io
import tempfile
from pathlib import Path
from typing import Any, Callable

import pymupdf
from markitdown import MarkItDown
from markitdown_vision import GoogleVisionOCRService
from llamaindex_ocr import DEFAULT_CUSTOM_PROMPT, TIER_AGENTIC
from llamaindex_ocr import parse_markdown as llamaindex_parse_markdown

from ._errors import UghOcrError
from ._frontmatter import render_with_frontmatter
from ._pdf_analysis import classify_pages, extract_single_page_pdf

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp", ".gif"}

WarnFn = Callable[[str], None]


def _default_warn(message: str) -> None:
    print(message)


def _vision_ocr_pdf_page(page_pdf: Path, vision_service: GoogleVisionOCRService) -> str:
    """Renderuje jednostronicowy PDF do obrazu i odpala na nim Google Cloud
    Vision -- niezaleznie od tego, czy PDF ma juz jakas (nawet niewidoczna)
    warstwe tekstu."""
    doc = pymupdf.open(str(page_pdf))
    try:
        pix = doc[0].get_pixmap(dpi=200)
        png_bytes = pix.tobytes("png")
    finally:
        doc.close()

    result = vision_service.extract_text(io.BytesIO(png_bytes))
    if result.error:
        raise RuntimeError(result.error)
    return result.text


def _ocr_one_pdf_page(
    page_pdf: Path,
    *,
    tier: str,
    custom_prompt: str,
    polling_interval: float,
    timeout: int,
    llamaindex_available: bool,
    vision_service: GoogleVisionOCRService,
    warn: WarnFn,
) -> tuple[str, str, bool]:
    """Zwraca (tekst, nazwa_backendu, llamaindex_nadal_dostepny)."""
    if llamaindex_available:
        try:
            text, _raw = llamaindex_parse_markdown(
                page_pdf,
                tier=tier,
                custom_prompt=custom_prompt,
                polling_interval=polling_interval,
                timeout=timeout,
            )
            return text, "llamaparse", True
        except Exception as e:
            warn(
                f"[ugh-ocr] Uwaga: llamaindex-ocr nie zadzialal ({e}). "
                "Przechodze na markitdown-vision (Google Cloud Vision) dla "
                "pozostalych stron OCR w tym pliku."
            )
            llamaindex_available = False

    try:
        text = _vision_ocr_pdf_page(page_pdf, vision_service)
        return text, "google-cloud-vision", False
    except Exception as e:
        raise UghOcrError(
            "Zarowno llamaindex-ocr, jak i markitdown-vision (fallback) zawiodly.",
            detail=str(e),
            hint=(
                "Sprawdz klucz LlamaCloud (~/.claude/secrets/llamacloud_api_key.txt "
                "albo zmienna LLAMA_CLOUD_API_KEY) oraz uwierzytelnienie Google Cloud "
                "Vision (Application Default Credentials albo "
                "GOOGLE_APPLICATION_CREDENTIALS)."
            ),
        ) from e


def _convert_pdf(
    input_path: Path,
    *,
    tier: str,
    custom_prompt: str,
    polling_interval: float,
    timeout: int,
    warn: WarnFn,
) -> tuple[str, list[str], bool, str | None]:
    classifications = classify_pages(input_path)
    if not classifications:
        raise UghOcrError(f"PDF nie ma zadnych stron: {input_path}")

    parts: list[str] = []
    pages_backend: list[str] = []
    fallback_used = False
    fallback_reason: str | None = None
    llamaindex_available = True
    vision_service = GoogleVisionOCRService()
    markitdown_plain = MarkItDown()

    with tempfile.TemporaryDirectory(prefix="ugh-ocr-") as tmp:
        tmp_dir = Path(tmp)
        for page in classifications:
            page_pdf = extract_single_page_pdf(input_path, page.index, tmp_dir)
            try:
                if page.has_genuine_text:
                    text = markitdown_plain.convert(str(page_pdf)).markdown or ""
                    backend = "text"
                else:
                    was_available = llamaindex_available
                    text, backend, llamaindex_available = _ocr_one_pdf_page(
                        page_pdf,
                        tier=tier,
                        custom_prompt=custom_prompt,
                        polling_interval=polling_interval,
                        timeout=timeout,
                        llamaindex_available=llamaindex_available,
                        vision_service=vision_service,
                        warn=warn,
                    )
                    if was_available and not llamaindex_available:
                        fallback_used = True
                        fallback_reason = (
                            "llamaindex-ocr nie powiodl sie w trakcie przetwarzania "
                            "-- reszta stron OCR poszla przez markitdown-vision "
                            "(Google Cloud Vision)."
                        )
            finally:
                page_pdf.unlink(missing_ok=True)

            marker = f"<!-- ugh-ocr: strona {page.index + 1}/{len(classifications)}, zrodlo: {backend} -->"
            parts.append(f"{marker}\n\n{text.strip()}")
            pages_backend.append(backend)

    return "\n\n".join(parts), pages_backend, fallback_used, fallback_reason


def _convert_image(
    input_path: Path,
    *,
    tier: str,
    custom_prompt: str,
    polling_interval: float,
    timeout: int,
    warn: WarnFn,
) -> tuple[str, bool, str | None]:
    try:
        text, _raw = llamaindex_parse_markdown(
            input_path,
            tier=tier,
            custom_prompt=custom_prompt,
            polling_interval=polling_interval,
            timeout=timeout,
        )
        return text, False, None
    except Exception as e:
        warn(
            f"[ugh-ocr] Uwaga: llamaindex-ocr nie zadzialal ({e}). "
            "Probuje markitdown-vision (Google Cloud Vision)."
        )
        try:
            vision_service = GoogleVisionOCRService()
            with open(input_path, "rb") as f:
                result = vision_service.extract_text(f)
            if result.error:
                raise RuntimeError(result.error)
            return result.text, True, f"llamaindex-ocr: {e}"
        except Exception as e2:
            raise UghOcrError(
                "Zarowno llamaindex-ocr, jak i markitdown-vision (fallback) zawiodly.",
                detail=f"llamaindex-ocr: {e}\nmarkitdown-vision: {e2}",
                hint=(
                    "Sprawdz klucz LlamaCloud (~/.claude/secrets/llamacloud_api_key.txt "
                    "albo zmienna LLAMA_CLOUD_API_KEY) oraz uwierzytelnienie Google Cloud "
                    "Vision (Application Default Credentials albo "
                    "GOOGLE_APPLICATION_CREDENTIALS)."
                ),
            ) from e2


def convert_file(
    input_path: Path,
    *,
    tier: str = TIER_AGENTIC,
    custom_prompt: str = DEFAULT_CUSTOM_PROMPT,
    polling_interval: float = 3.0,
    timeout: int = 1800,
    warn: WarnFn = _default_warn,
) -> Path:
    """Konwertuje `input_path` (PDF albo obraz) do `.md` obok niego, bez
    flagi -o -- tak samo jak markitdown-vision i llamaindex-ocr."""
    input_path = Path(input_path)
    if not input_path.exists():
        raise UghOcrError(f"Brak pliku wejsciowego: {input_path}")

    suffix = input_path.suffix.lower()
    pages_backend: list[str] | None

    if suffix == ".pdf":
        markdown, pages_backend, fallback_used, fallback_reason = _convert_pdf(
            input_path,
            tier=tier,
            custom_prompt=custom_prompt,
            polling_interval=polling_interval,
            timeout=timeout,
            warn=warn,
        )
    elif suffix in IMAGE_EXTENSIONS:
        markdown, fallback_used, fallback_reason = _convert_image(
            input_path,
            tier=tier,
            custom_prompt=custom_prompt,
            polling_interval=polling_interval,
            timeout=timeout,
            warn=warn,
        )
        pages_backend = None
    else:
        raise UghOcrError(
            f"Nieobslugiwany typ pliku: {suffix or '(brak rozszerzenia)'}",
            detail=f"Plik: {input_path}",
            hint="ugh-ocr obsluguje PDF oraz obrazy (.png/.jpg/.jpeg/.tif/.tiff/.bmp/.webp/.gif).",
        )

    output_path = input_path.with_suffix(".md")
    output_path.write_text(
        render_with_frontmatter(
            input_path,
            markdown,
            pages_backend=pages_backend,
            fallback_used=fallback_used,
            fallback_reason=fallback_reason,
        ),
        encoding="utf-8",
    )
    return output_path
