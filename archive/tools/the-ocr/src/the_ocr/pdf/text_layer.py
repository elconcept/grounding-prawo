from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import pikepdf

from ..geometry import PageGeometry
from ..models import OCRDocument, OCRWord


MAX_FONTSIZE_PT = 24.0
_MAX_CHARS_PER_FONT = 255


@dataclass(frozen=True)
class _TextLine:
    text: str
    bbox: tuple[float, float, float, float]


def build_searchable_pdf(src: Path, dst: Path, pages: list[PageGeometry]) -> None:
    _write_searchable_pdf(src, dst, [_group_words_into_lines(page.words) for page in pages])


def build_document_searchable_pdf(src: Path, dst: Path, document: OCRDocument) -> None:
    pages: list[list[_TextLine]] = []
    for page in document.pages:
        lines: list[_TextLine] = []
        unpositioned: list[str] = []
        for block in page.blocks:
            if block.words and _word_coverage(block.text, [word.text for word in block.words]) >= 0.95:
                lines.extend(_group_words_into_lines(block.words))
            elif block.bbox is not None and block.text.strip():
                lines.append(_TextLine(" ".join(block.text.split()), block.bbox))
            elif block.text.strip():
                unpositioned.append(" ".join(block.text.split()))
        for index, text in enumerate(unpositioned):
            y0 = min(0.01 + index * 0.002, 0.98)
            lines.append(_TextLine(text, (0.005, y0, 0.995, min(y0 + 0.0015, 0.999))))
        pages.append(lines)
    _write_searchable_pdf(src, dst, pages)


def _write_searchable_pdf(src: Path, dst: Path, pages: list[list[_TextLine]]) -> None:
    with pikepdf.open(src) as pdf:
        if len(pdf.pages) != len(pages):
            raise ValueError(f"page count mismatch: {src} has {len(pdf.pages)} pages, OCR has {len(pages)}")

        characters = sorted({char for page in pages for line in page for char in line.text}) or [" "]
        font_maps, font_objects = _create_nonembedded_fonts(pdf, characters)
        char_map = {
            char: (font_index, code)
            for font_index, mapping in enumerate(font_maps)
            for char, code in mapping.items()
        }

        for page, lines in zip(pdf.pages, pages):
            resources = _copy_resources(page)
            fonts = _copy_dictionary(resources.get("/Font"))
            for index, font_object in enumerate(font_objects, start=1):
                fonts[pikepdf.Name(f"/OCRF{index}")] = font_object
            resources.Font = fonts
            page.obj.Resources = resources

            width, height = _page_dimensions(page)
            operations: list[bytes] = [b"q"]
            for line in lines:
                operations.extend(_line_operations(line, width, height, char_map))
            operations.append(b"Q")
            _append_content_stream(pdf, page, b"\n".join(operations))

        pdf.save(
            dst,
            linearize=True,
            compress_streams=True,
            object_stream_mode=pikepdf.ObjectStreamMode.generate,
        )


def _create_nonembedded_fonts(pdf: pikepdf.Pdf, characters: list[str]):
    font_maps = []
    font_objects = []
    for offset in range(0, len(characters), _MAX_CHARS_PER_FONT):
        chunk = characters[offset:offset + _MAX_CHARS_PER_FONT]
        mapping = {char: index for index, char in enumerate(chunk, start=1)}
        cmap = pdf.make_stream(_to_unicode_cmap(mapping).encode("ascii"))
        font = pdf.make_indirect(
            pikepdf.Dictionary(
                Type=pikepdf.Name.Font,
                Subtype=pikepdf.Name.Type1,
                BaseFont=pikepdf.Name.Helvetica,
                Encoding=pikepdf.Name.WinAnsiEncoding,
                ToUnicode=cmap,
            )
        )
        font_maps.append(mapping)
        font_objects.append(font)
    return font_maps, font_objects


def _to_unicode_cmap(mapping: dict[str, int]) -> str:
    lines = [
        "/CIDInit /ProcSet findresource begin",
        "12 dict begin",
        "begincmap",
        "/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def",
        "/CMapName /TheOCRUnicode def",
        "/CMapType 2 def",
        "1 begincodespacerange",
        "<01> <FF>",
        "endcodespacerange",
    ]
    entries = [(code, char.encode("utf-16-be").hex().upper()) for char, code in mapping.items()]
    for offset in range(0, len(entries), 100):
        chunk = entries[offset:offset + 100]
        lines.append(f"{len(chunk)} beginbfchar")
        lines.extend(f"<{code:02X}> <{unicode_hex}>" for code, unicode_hex in chunk)
        lines.append("endbfchar")
    lines.extend(("endcmap", "CMapName currentdict /CMap defineresource pop", "end", "end"))
    return "\n".join(lines)


def _line_operations(line: _TextLine, page_width: float, page_height: float, char_map) -> list[bytes]:
    text = line.text.strip()
    if not text:
        return []
    x0, y0, x1, y1 = _absolute_bbox(line.bbox, page_width, page_height)
    box_width = max(x1 - x0, 0.1)
    box_height = max(y1 - y0, 0.1)
    font_size = min(box_height, MAX_FONTSIZE_PT, box_width / max(len(text) * 0.5, 0.1))
    font_size = max(font_size, 0.1)
    baseline = max(0.0, min(page_height, page_height - y1))

    runs: list[tuple[int, bytearray]] = []
    for char in text:
        font_index, code = char_map[char]
        if not runs or runs[-1][0] != font_index:
            runs.append((font_index, bytearray()))
        runs[-1][1].append(code)

    operations: list[bytes] = []
    current_x = x0
    for font_index, encoded in runs:
        operations.extend(
            (
                b"BT",
                f"/OCRF{font_index + 1} {font_size:.4f} Tf".encode("ascii"),
                b"3 Tr",
                f"1 0 0 1 {current_x:.4f} {baseline:.4f} Tm".encode("ascii"),
                f"<{encoded.hex().upper()}> Tj".encode("ascii"),
                b"ET",
            )
        )
        current_x += box_width * (len(encoded) / max(len(text), 1))
    return operations


def _group_words_into_lines(words: tuple[OCRWord, ...] | list[OCRWord]) -> list[_TextLine]:
    valid = [word for word in words if word.text.strip()]
    if not valid:
        return []
    ordered = sorted(valid, key=lambda word: (word.bbox[1], word.bbox[0]))
    grouped: list[list[OCRWord]] = []
    for word in ordered:
        if not grouped:
            grouped.append([word])
            continue
        current = grouped[-1]
        line_y0 = min(item.bbox[1] for item in current)
        line_y1 = max(item.bbox[3] for item in current)
        word_mid = (word.bbox[1] + word.bbox[3]) / 2
        if line_y0 <= word_mid <= line_y1 or abs(word.bbox[1] - line_y0) < 0.008:
            current.append(word)
        else:
            grouped.append([word])

    return [
        _TextLine(
            " ".join(word.text.strip() for word in sorted(line, key=lambda word: word.bbox[0])),
            (
                min(word.bbox[0] for word in line),
                min(word.bbox[1] for word in line),
                max(word.bbox[2] for word in line),
                max(word.bbox[3] for word in line),
            ),
        )
        for line in grouped
    ]


def _word_coverage(block_text: str, words: list[str]) -> float:
    expected = re.findall(r"\w+", block_text.casefold(), flags=re.UNICODE)
    actual = " ".join(words).casefold()
    return 1.0 if not expected else sum(token in actual for token in expected) / len(expected)


def _copy_resources(page) -> pikepdf.Dictionary:
    resources = page.obj.get("/Resources")
    current = page.obj.get("/Parent")
    while resources is None and current is not None:
        resources = current.get("/Resources")
        current = current.get("/Parent")
    return _copy_dictionary(resources)


def _copy_dictionary(value) -> pikepdf.Dictionary:
    copied = pikepdf.Dictionary()
    if value is not None:
        for key, item in value.items():
            copied[key] = item
    return copied


def _append_content_stream(pdf: pikepdf.Pdf, page, content: bytes) -> None:
    stream = pdf.make_stream(content)
    existing = page.obj.get("/Contents")
    if existing is None:
        page.obj.Contents = stream
    elif isinstance(existing, pikepdf.Array):
        existing.append(stream)
    else:
        page.obj.Contents = pikepdf.Array([existing, stream])


def _page_dimensions(page) -> tuple[float, float]:
    box = page.mediabox
    return float(box[2]) - float(box[0]), float(box[3]) - float(box[1])


def _absolute_bbox(bbox, page_width: float, page_height: float):
    return (
        max(0.0, min(page_width, bbox[0] * page_width)),
        max(0.0, min(page_height, bbox[1] * page_height)),
        max(0.0, min(page_width, bbox[2] * page_width)),
        max(0.0, min(page_height, bbox[3] * page_height)),
    )
