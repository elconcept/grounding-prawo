"""Word geometry sidecar for the OCRmyPDF engine plugin.

The sidecar carries provider word boxes (normalized ``0..1``, top-left
origin) to :mod:`the_ocr.pdf.ocrmypdf_plugin`, which serves them page by page
through the official ``OcrEngine.generate_ocr`` API. Only geometry the
provider actually returned is included, plus one entry per textbox block that
has a block bbox but no word boxes (the coarsest real geometry available --
never invented word coordinates). Blocks with no geometry at all are
ungroundable and stay out of the PDF layer (see ``gating`` in the JSON).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image

from ..models import OCRDocument


def write_engine_sidecar(document: OCRDocument, path: Path) -> None:
    """Persist per-page word geometry for the OCRmyPDF plugin engine."""
    payload = {
        "provider": document.provider,
        "pages": [_page_payload(page.blocks) for page in document.pages],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _page_payload(blocks) -> dict[str, Any]:
    words: list[dict[str, Any]] = []
    for block in blocks:
        if block.words:
            for word in block.words:
                if word.text.strip():
                    words.append(
                        {
                            "text": word.text.strip(),
                            "bbox": list(word.bbox),
                            "confidence": word.confidence,
                        }
                    )
        elif block.bbox is not None and block.text.strip():
            # Block-level grounding: the block's own text at the block's own
            # box. Not a word coordinate -- the provider gave nothing finer.
            words.append(
                {
                    "text": " ".join(block.text.split()),
                    "bbox": list(block.bbox),
                    "confidence": block.confidence,
                }
            )
    return {"words": words}


def build_page_tree(page_words: list[dict[str, Any]], image_size: tuple[int, int]):
    """Build an ``OcrElement`` page tree with pixel bboxes for the image."""
    from ocrmypdf import BoundingBox, OcrClass, OcrElement

    width, height = image_size
    lines = _group_into_lines(page_words)
    line_elements = []
    for line_words in lines:
        word_elements = []
        for item in line_words:
            bbox = _to_pixels(item["bbox"], width, height)
            if bbox is None:
                continue
            word_elements.append(
                OcrElement(
                    ocr_class=OcrClass.WORD,
                    bbox=bbox,
                    text=item["text"],
                    confidence=_confidence(item.get("confidence")),
                )
            )
        if not word_elements:
            continue
        line_elements.append(
            OcrElement(
                ocr_class=OcrClass.LINE,
                bbox=_union([element.bbox for element in word_elements]),  # type: ignore[arg-type]
                text=" ".join(element.text for element in word_elements),
                children=word_elements,
            )
        )
    paragraph = OcrElement(
        ocr_class=OcrClass.PARAGRAPH,
        bbox=BoundingBox(0, 0, width, height),
        text=" ".join(element.text for element in line_elements),
        children=line_elements,
    )
    area = OcrElement(
        ocr_class=OcrClass.CAREA,
        bbox=BoundingBox(0, 0, width, height),
        text=paragraph.text,
        children=[paragraph] if line_elements else [],
    )
    return OcrElement(
        ocr_class=OcrClass.PAGE,
        bbox=BoundingBox(0, 0, width, height),
        text=area.text,
        children=[area],
    )


def page_text(page_words: list[dict[str, Any]]) -> str:
    return " ".join(item["text"] for item in page_words if item["text"].strip())


def read_image_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as image:
        return int(image.width), int(image.height)


def _group_into_lines(words: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    ordered = sorted(
        [word for word in words if word["text"].strip()],
        key=lambda word: (word["bbox"][1], word["bbox"][0]),
    )
    grouped: list[list[dict[str, Any]]] = []
    for word in ordered:
        if not grouped:
            grouped.append([word])
            continue
        current = grouped[-1]
        top = min(item["bbox"][1] for item in current)
        bottom = max(item["bbox"][3] for item in current)
        middle = (word["bbox"][1] + word["bbox"][3]) / 2
        if top <= middle <= bottom or abs(word["bbox"][1] - top) < 0.008:
            current.append(word)
        else:
            grouped.append([word])
    for line in grouped:
        line.sort(key=lambda word: word["bbox"][0])
    return grouped


def _to_pixels(bbox: list[float], width: int, height: int):
    from ocrmypdf import BoundingBox

    x0 = max(0, min(width, round(float(bbox[0]) * width)))
    y0 = max(0, min(height, round(float(bbox[1]) * height)))
    x1 = max(0, min(width, round(float(bbox[2]) * width)))
    y1 = max(0, min(height, round(float(bbox[3]) * height)))
    if x1 <= x0 or y1 <= y0:
        return None
    return BoundingBox(x0, y0, x1, y1)


def _union(boxes):
    return type(boxes[0])(
        min(box.left for box in boxes),
        min(box.top for box in boxes),
        max(box.right for box in boxes),
        max(box.bottom for box in boxes),
    )


def _confidence(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if 0.0 <= number <= 1.0:
        return number
    return None
