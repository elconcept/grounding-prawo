"""Klasyfikacja stron PDF: prawdziwa (widoczna) warstwa tekstu vs reszta.

Kluczowy problem: `page.get_text()` zwraca tekst takze wtedy, gdy jedyny
tekst na stronie to niewidoczna warstwa dodana przez OCR (np. "sandwich PDF"
z Tesseracta/ocrmypdf) -- sama dlugosc wyekstrahowanego tekstu NIE odroznia
prawdziwej warstwy od nalozonego OCR-u. Zweryfikowano eksperymentalnie: strona
z jednym niewidocznym `insert_text(..., render_mode=3)` ma dlugosc
`get_text("text")` > 0 identycznie jak strona z prawdziwym tekstem.

Rozroznienie: PDF text rendering mode (operator Tr w tresci strony), dostepny
przez `page.get_texttrace()` -> pole "type" kazdego sladu:
  0 = fill (normalny widoczny tekst), 1 = stroke, 2 = fill+stroke,
  3 = invisible (uzywane przez silniki OCR do nalozenia niewidocznej warstwy
      na obraz strony), 4-7 = warianty z clipowaniem.
Strona ma "prawdziwa warstwe tekstu" gdy wiekszosc znakow ma type != 3.
Brak get_texttrace (bardzo stary PyMuPDF) -> fallback na `get_text()`, co jest
gorsza heurystyka (nie odroznia OCR-sandwich), ale lepsza niz nic.
"""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path

import pymupdf

INVISIBLE_RENDER_MODE = 3


@dataclass
class PageClassification:
    index: int  # 0-based
    has_genuine_text: bool
    visible_chars: int
    invisible_chars: int


def classify_pages(pdf_path: Path) -> list[PageClassification]:
    """Klasyfikuje kazda strone `pdf_path` jako majaca prawdziwa (widoczna)
    warstwe tekstu albo nie (brak tekstu lub tylko niewidoczna warstwa OCR)."""
    results: list[PageClassification] = []
    doc = pymupdf.open(str(pdf_path))
    try:
        for i, page in enumerate(doc):
            visible = 0
            invisible = 0
            try:
                traces = page.get_texttrace()
            except Exception:
                traces = None

            if traces is not None:
                for trace in traces:
                    n_chars = len(trace.get("chars", []))
                    if trace.get("type") == INVISIBLE_RENDER_MODE:
                        invisible += n_chars
                    else:
                        visible += n_chars
                has_genuine = visible > 0
            else:
                # Fallback bez get_texttrace: nie odroznia OCR-sandwich,
                # ale przynajmniej lapie strony calkiem bez tekstu.
                plain = page.get_text("text").strip()
                has_genuine = len(plain) > 0
                visible = len(plain)

            results.append(
                PageClassification(
                    index=i,
                    has_genuine_text=has_genuine,
                    visible_chars=visible,
                    invisible_chars=invisible,
                )
            )
    finally:
        doc.close()
    return results


def extract_single_page_pdf(pdf_path: Path, page_index: int, tmp_dir: Path) -> Path:
    """Wycina strone `page_index` (0-based) z `pdf_path` do osobnego pliku PDF
    w `tmp_dir`. Zwraca sciezke nowego pliku."""
    doc = pymupdf.open(str(pdf_path))
    try:
        single = pymupdf.open()
        single.insert_pdf(doc, from_page=page_index, to_page=page_index)
        fd, name = tempfile.mkstemp(
            suffix=".pdf", prefix=f"ugh-ocr-p{page_index + 1}-", dir=str(tmp_dir)
        )
        import os

        os.close(fd)
        out_path = Path(name)
        single.save(str(out_path))
        single.close()
        return out_path
    finally:
        doc.close()
