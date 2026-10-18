from __future__ import annotations

import re
from collections import Counter
from dataclasses import replace
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable

import pymupdf

from .models import OCRBlock, OCRDocument, OCRPage, OCRWord, VALID_BLOCK_TYPES, doc_id_for, normalize_bbox


#: Provider labels mapped onto the exact doc-intel-contract-pl taxonomy.
#: Anything visual without its own reference type becomes "figure";
#: handwriting stays a "paragraph" (the reference has no handwriting type).
_DATALAB_TYPES = {
    "sectionheader": "title",
    "title": "title",
    "heading": "title",
    "pageheader": "header",
    "pagefooter": "footer",
    "header": "header",
    "footer": "footer",
    "picture": "figure",
    "figure": "figure",
    "image": "figure",
    "handwriting": "paragraph",
    "handwritten": "paragraph",
    "signature": "signature",
    "stamp": "stamp",
    "listgroup": "list",
    "listitem": "list",
    "list": "list",
    "table": "table",
    "tablegroup": "table",
    "equation": "equation",
    "text": "paragraph",
    "paragraph": "paragraph",
}


class _WordHTMLParser(HTMLParser):
    def __init__(self, width: float, height: float):
        super().__init__(convert_charrefs=True)
        self.width = width
        self.height = height
        self.words: list[OCRWord] = []
        self._span: tuple[list[float], float | None] | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "span" and values.get("data-bbox"):
            try:
                bbox = [float(value) for value in re.split(r"[ ,]+", values["data-bbox"].strip())]
                confidence = float(values["data-confidence"]) if values.get("data-confidence") else None
                self._span = (bbox, confidence)
                self._text = []
            except (TypeError, ValueError):
                self._span = None

    def handle_data(self, data: str) -> None:
        if self._span is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "span" or self._span is None:
            return
        text = "".join(self._text).strip()
        bbox, confidence = self._span
        if text:
            try:
                self.words.append(OCRWord(text, normalize_bbox(bbox, self.width, self.height), confidence))
            except ValueError:
                pass
        self._span = None
        self._text = []


def datalab_document(raw: dict[str, Any], source_path: Path) -> OCRDocument:
    payload = raw.get("json") if isinstance(raw.get("json"), dict) else raw
    roots = payload.get("children") or []
    expected_pages = raw.get("page_count") or _source_page_count(source_path)
    if expected_pages is not None and int(expected_pages) != len(roots):
        raise ValueError(f"Datalab returned {len(roots)} of {expected_pages} pages")
    pages: list[OCRPage] = []
    for page_index, root in enumerate(roots, start=1):
        root_bbox = root.get("bbox") or []
        if len(root_bbox) != 4:
            raise ValueError(f"Datalab page {page_index} has no dimensions")
        width = float(root_bbox[2]) - float(root_bbox[0])
        height = float(root_bbox[3]) - float(root_bbox[1])
        blocks: list[OCRBlock] = []
        for block_index, item in enumerate(_walk_datalab_blocks(root.get("children") or []), start=1):
            if item.get("inference_failed"):
                raise ValueError(f"Datalab inference failed for block {item.get('id', block_index)}")
            markdown = str(item.get("markdown") or "").strip()
            html = str(item.get("html") or "")
            text = _html_text(html) if html else _plain_markdown(markdown)
            if not text and not markdown:
                continue
            block_type = _DATALAB_TYPES.get(str(item.get("block_type", "")).lower(), "unknown")
            if block_type not in VALID_BLOCK_TYPES:
                block_type = "unknown"
            bbox = None
            if item.get("bbox"):
                bbox = normalize_bbox(item["bbox"], width, height)
            parser = _WordHTMLParser(width, height)
            parser.feed(html)
            confidence_values = [word.confidence for word in parser.words if word.confidence is not None]
            blocks.append(
                OCRBlock(
                    id=f"p{page_index:04d}-b{block_index:04d}",
                    page=page_index,
                    block_type=block_type,
                    text=text,
                    markdown=markdown or text,
                    bbox=bbox,
                    confidence=min(confidence_values) if confidence_values else None,
                    words=tuple(parser.words),
                )
            )
        pages.append(OCRPage(page_index, width, height, tuple(blocks)))

    metadata = raw.get("metadata") or payload.get("metadata") or {}
    if metadata.get("failed_pages"):
        raise ValueError(f"Datalab did not process pages: {metadata['failed_pages']}")
    document = OCRDocument(
        doc_id=doc_id_for(source_path),
        provider="datalab",
        pages=tuple(pages),
        source_name=source_path.name,
    )
    document = _normalize_layout(document)
    document.validate()
    return document


def llamaparse_document(raw: Any, source_path: Path) -> OCRDocument:
    payload = raw.model_dump(mode="json") if hasattr(raw, "model_dump") else raw
    pages_raw = ((payload or {}).get("items") or {}).get("pages") or []
    expected_pages = _source_page_count(source_path)
    if len(pages_raw) != expected_pages:
        raise ValueError(f"LlamaParse returned {len(pages_raw)} of {expected_pages} pages")
    page_numbers = [int(page.get("page_number", -1)) for page in pages_raw]
    if page_numbers != list(range(1, len(pages_raw) + 1)):
        raise ValueError(f"LlamaParse returned non-contiguous pages: {page_numbers}")
    pages: list[OCRPage] = []
    for output_number, page in enumerate(pages_raw, start=1):
        if not page.get("success", False):
            raise ValueError(f"LlamaParse failed on page {page.get('page_number', output_number)}: {page.get('error', '')}")
        width = float(page.get("page_width") or 0)
        height = float(page.get("page_height") or 0)
        if width <= 0 or height <= 0:
            raise ValueError(f"LlamaParse page {output_number} has no dimensions")
        blocks: list[OCRBlock] = []
        for block_index, item in enumerate(_walk_llama_items(page.get("items") or []), start=1):
            markdown = str(item.get("md") or item.get("value") or "").strip()
            text = _plain_markdown(markdown)
            if not text:
                continue
            boxes = item.get("bbox") or []
            normalized = [
                normalize_bbox(
                    [box["x"], box["y"], box["x"] + box["w"], box["y"] + box["h"]],
                    width,
                    height,
                )
                for box in boxes
                if all(key in box for key in ("x", "y", "w", "h"))
            ]
            bbox = _union_boxes(normalized) if normalized else None
            confidences = [float(box["confidence"]) for box in boxes if box.get("confidence") is not None]
            blocks.append(
                OCRBlock(
                    id=f"p{output_number:04d}-b{block_index:04d}",
                    page=output_number,
                    block_type=_llama_type(item),
                    text=text,
                    markdown=markdown,
                    bbox=bbox,
                    confidence=min(confidences) if confidences else None,
                )
            )
        pages.append(OCRPage(output_number, width, height, tuple(blocks)))
    document = OCRDocument(
        doc_id=doc_id_for(source_path),
        provider="llamaparse",
        pages=tuple(pages),
        source_name=source_path.name,
    )
    document = _normalize_layout(document)
    document.validate()
    return document


def _walk_datalab_blocks(items: Iterable[dict[str, Any]]) -> Iterable[dict[str, Any]]:
    for item in items:
        if item.get("block_type", "").lower() == "page":
            yield from _walk_datalab_blocks(item.get("children") or [])
        else:
            yield item


def _walk_llama_items(items: Iterable[dict[str, Any]]) -> Iterable[dict[str, Any]]:
    for item in items:
        nested = item.get("items") or []
        if nested and not item.get("bbox"):
            for child in _walk_llama_items(nested):
                child = dict(child)
                if item.get("type") in {"header", "footer"}:
                    child["type"] = item["type"]
                yield child
        else:
            yield item


def _llama_type(item: dict[str, Any]) -> str:
    kind = str(item.get("type") or "unknown").lower()
    markdown = str(item.get("md") or "").lower()
    aliases = {"image": "figure", "text": "paragraph", "list": "list", "heading": "title", "title": "title"}
    for marker, block_type in (
        ("signature:", "signature"), ("podpis:", "signature"),
        ("stamp:", "stamp"), ("pieczęć:", "stamp"), ("pieczec:", "stamp"),
        ("handnote:", "paragraph"), ("odręcz", "paragraph"),
        ("logo:", "figure"), ("photo:", "figure"), ("graphic:", "figure"),
    ):
        if marker in markdown:
            return block_type
    return aliases.get(kind, "unknown")


def _union_boxes(boxes: list[tuple[float, float, float, float]]) -> tuple[float, float, float, float]:
    return (
        min(box[0] for box in boxes), min(box[1] for box in boxes),
        max(box[2] for box in boxes), max(box[3] for box in boxes),
    )


class _TextParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def _html_text(value: str) -> str:
    parser = _TextParser()
    parser.feed(value)
    return re.sub(r"\s+", " ", " ".join(parser.parts)).strip()


def _plain_markdown(value: str) -> str:
    value = re.sub(r"!\[([^]]*)]\([^)]*\)", r"\1", value)
    value = re.sub(r"\[([^]]+)]\([^)]*\)", r"\1", value)
    value = re.sub(r"[`#*_~>|]", "", value)
    return re.sub(r"\s+", " ", value).strip()


def _source_page_count(path: Path) -> int:
    with pymupdf.open(path) as document:
        return len(document)


def _normalize_layout(document: OCRDocument) -> OCRDocument:
    repeated_candidates = Counter(
        _repetition_key(block.text)
        for page in document.pages
        for block in page.blocks
        if block.bbox is not None and (block.bbox[1] >= 0.82 or block.bbox[3] <= 0.16) and block.text.strip()
    )
    pages = []
    for page in document.pages:
        blocks = []
        for block in page.blocks:
            block_type = block.block_type
            if block.bbox is not None and block_type not in {"signature", "stamp", "figure"}:
                repeated = repeated_candidates[_repetition_key(block.text)] >= 2
                if repeated and block.bbox[1] >= 0.78:
                    block_type = "footer"
                elif repeated and block.bbox[3] <= 0.20:
                    block_type = "header"
            blocks.append(replace(block, block_type=block_type))
        pages.append(replace(page, blocks=tuple(blocks)))
    return replace(document, pages=tuple(pages))


def _repetition_key(text: str) -> str:
    normalized = re.sub(r"\d+", "#", text.casefold())
    return re.sub(r"\W+", " ", normalized).strip()


def azure_document(raw: dict[str, Any], source_path: Path) -> OCRDocument:
    """Azure Document Intelligence (prebuilt-read): linie jako bloki, slowa z ramkami."""
    result = raw.get("analyzeResult") or raw
    pages_raw = result.get("pages") or []
    expected_pages = _source_page_count(source_path)
    if len(pages_raw) != expected_pages:
        raise ValueError(f"Azure returned {len(pages_raw)} of {expected_pages} pages")
    pages: list[OCRPage] = []
    for page_index, page in enumerate(pages_raw, start=1):
        width = float(page.get("width") or 0)
        height = float(page.get("height") or 0)
        if width <= 0 or height <= 0:
            raise ValueError(f"Azure page {page_index} has no dimensions")
        words = [
            (int((word.get("span") or {}).get("offset", -1)), word)
            for word in page.get("words") or []
            if str(word.get("content") or "").strip() and word.get("polygon")
        ]
        blocks: list[OCRBlock] = []
        for line_index, line in enumerate(page.get("lines") or [], start=1):
            text = str(line.get("content") or "").strip()
            if not text or not line.get("polygon"):
                continue
            spans = [(int(span["offset"]), int(span["offset"]) + int(span["length"])) for span in line.get("spans") or []]
            line_words = tuple(
                OCRWord(str(word["content"]).strip(), box, word.get("confidence"))
                for offset, word in words
                if any(start <= offset < end for start, end in spans)
                and (box := _polygon_bbox(word["polygon"], width, height)) is not None
            )
            confidences = [word.confidence for word in line_words if word.confidence is not None]
            blocks.append(
                OCRBlock(
                    id=f"p{page_index:04d}-b{line_index:04d}",
                    page=page_index,
                    block_type="paragraph",
                    text=text,
                    markdown=text,
                    bbox=_polygon_bbox(line["polygon"], width, height),
                    confidence=min(confidences) if confidences else None,
                    words=line_words,
                )
            )
        pages.append(OCRPage(page_index, width, height, tuple(blocks)))
    document = OCRDocument(
        doc_id=doc_id_for(source_path),
        provider="azure",
        pages=tuple(pages),
        source_name=source_path.name,
    )
    document = _normalize_layout(document)
    document.validate()
    return document


def google_vision_document(responses: list[dict[str, Any]], source_path: Path) -> OCRDocument:
    """Google Cloud Vision files:annotate (DOCUMENT_TEXT_DETECTION), odpowiedzi stron w kolejnosci."""
    expected_pages = _source_page_count(source_path)
    if len(responses) != expected_pages:
        raise ValueError(f"Google Vision returned {len(responses)} of {expected_pages} pages")
    pages: list[OCRPage] = []
    for page_index, response in enumerate(responses, start=1):
        if response.get("error"):
            raise ValueError(f"Google Vision failed on page {page_index}: {response['error'].get('message', '')}")
        annotation_pages = (response.get("fullTextAnnotation") or {}).get("pages") or []
        page = annotation_pages[0] if annotation_pages else {}
        width = float(page.get("width") or 1)
        height = float(page.get("height") or 1)
        blocks: list[OCRBlock] = []
        for block_index, block in enumerate(page.get("blocks") or [], start=1):
            # Vision tnie interpunkcje na osobne "slowa" bez odstepu (detectedBreak
            # brak) - doklejamy je do poprzedniego slowa razem z ramka.
            words: list[OCRWord] = []
            parts: list[str] = []
            glue = False
            for paragraph in block.get("paragraphs") or []:
                for word in paragraph.get("words") or []:
                    symbols = word.get("symbols") or []
                    value = "".join(str(symbol.get("text") or "") for symbol in symbols).strip()
                    box = _vision_bbox(word.get("boundingBox") or {}, width, height)
                    if not value or box is None:
                        continue
                    if glue and words:
                        previous = words[-1]
                        words[-1] = OCRWord(previous.text + value, _union_boxes([previous.bbox, box]), previous.confidence)
                        parts[-1] += value
                    else:
                        words.append(OCRWord(value, box, word.get("confidence")))
                        parts.append(value)
                    breaks = ((symbols[-1].get("property") or {}).get("detectedBreak") or {}).get("type", "")
                    glue = not breaks
                    if breaks in {"LINE_BREAK", "EOL_SURE_SPACE"}:
                        parts[-1] += "\n"
                    elif breaks:
                        parts[-1] += " "
            text = "".join(parts).strip()
            if not text:
                continue
            blocks.append(
                OCRBlock(
                    id=f"p{page_index:04d}-b{block_index:04d}",
                    page=page_index,
                    block_type="paragraph",
                    text=text,
                    markdown=text,
                    bbox=_vision_bbox(block.get("boundingBox") or {}, width, height),
                    confidence=block.get("confidence"),
                    words=tuple(words),
                )
            )
        pages.append(OCRPage(page_index, width, height, tuple(blocks)))
    document = OCRDocument(
        doc_id=doc_id_for(source_path),
        provider="google_vision",
        pages=tuple(pages),
        source_name=source_path.name,
    )
    document = _normalize_layout(document)
    document.validate()
    return document


def _polygon_bbox(polygon: list[float], width: float, height: float) -> tuple[float, float, float, float] | None:
    """Wielokat Azure [x1, y1, ..., x4, y4] -> ramka; zdegenerowany (zerowe pole) -> None."""
    xs, ys = polygon[0::2], polygon[1::2]
    try:
        return normalize_bbox([min(xs), min(ys), max(xs), max(ys)], width, height)
    except ValueError:
        return None


def _vision_bbox(box: dict[str, Any], width: float, height: float) -> tuple[float, float, float, float] | None:
    """PDF-y daja normalizedVertices (0..1), obrazy vertices w pikselach; brak x/y znaczy 0."""
    if box.get("normalizedVertices"):
        vertices, scale_x, scale_y = box["normalizedVertices"], 1.0, 1.0
    elif box.get("vertices"):
        vertices, scale_x, scale_y = box["vertices"], width, height
    else:
        return None
    xs = [float(vertex.get("x", 0)) for vertex in vertices]
    ys = [float(vertex.get("y", 0)) for vertex in vertices]
    try:
        return normalize_bbox([min(xs), min(ys), max(xs), max(ys)], scale_x, scale_y)
    except ValueError:
        return None
