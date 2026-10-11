from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


BBox = tuple[float, float, float, float]


def normalize_bbox(values: list[float] | tuple[float, ...], width: float, height: float) -> BBox:
    if len(values) != 4 or width <= 0 or height <= 0:
        raise ValueError("bbox requires four coordinates and positive page dimensions")
    x0, y0, x1, y1 = (float(value) for value in values)
    box = (
        max(0.0, min(1.0, x0 / width)),
        max(0.0, min(1.0, y0 / height)),
        max(0.0, min(1.0, x1 / width)),
        max(0.0, min(1.0, y1 / height)),
    )
    if box[0] >= box[2] or box[1] >= box[3]:
        raise ValueError(f"invalid bbox: {values}")
    return tuple(round(value, 6) for value in box)  # type: ignore[return-value]


@dataclass(frozen=True)
class OCRWord:
    text: str
    bbox: BBox
    confidence: float | None = None


@dataclass(frozen=True)
class OCRBlock:
    id: str
    page: int
    block_type: str
    text: str
    markdown: str
    bbox: BBox | None = None
    confidence: float | None = None
    words: tuple[OCRWord, ...] = ()


@dataclass(frozen=True)
class OCRPage:
    number: int
    width: float
    height: float
    blocks: tuple[OCRBlock, ...]


@dataclass(frozen=True)
class OCRDocument:
    source_name: str
    source_sha256: str
    provider: str
    pages: tuple[OCRPage, ...]
    schema_version: str = "1.0"
    provider_metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def text(self) -> str:
        page_texts = []
        for page in self.pages:
            page_texts.append("\n\n".join(block.markdown for block in page.blocks if block.markdown.strip()))
        return "\n\n---\n\n".join(page_texts).strip()

    @property
    def has_geometry(self) -> bool:
        return bool(self.pages) and any(
            block.bbox is not None or block.words
            for page in self.pages
            for block in page.blocks
            if block.text.strip()
        )

    def validate(self) -> None:
        if not self.pages:
            raise ValueError("OCR document has no pages")
        expected = list(range(1, len(self.pages) + 1))
        actual = [page.number for page in self.pages]
        if actual != expected:
            raise ValueError(f"page numbers must be contiguous and 1-based: {actual}")
        ids: set[str] = set()
        for page in self.pages:
            if page.width <= 0 or page.height <= 0:
                raise ValueError(f"page {page.number} has invalid dimensions")
            for block in page.blocks:
                if block.id in ids:
                    raise ValueError(f"duplicate block id: {block.id}")
                ids.add(block.id)
                if block.page != page.number:
                    raise ValueError(f"block {block.id} has mismatched page number")
                if block.bbox is not None:
                    _validate_normalized_bbox(block.bbox, block.id)
                for word in block.words:
                    _validate_normalized_bbox(word.bbox, block.id)
        if not any(block.text.strip() for page in self.pages for block in page.blocks):
            raise ValueError("OCR document has no text")
        if not self.has_geometry:
            raise ValueError("OCR document has no usable geometry")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "source": {"name": self.source_name, "sha256": self.source_sha256},
            "ocr": {"provider": self.provider, **self.provider_metadata},
            "pages": [asdict(page) for page in self.pages],
        }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_normalized_bbox(bbox: BBox, owner: str) -> None:
    x0, y0, x1, y1 = bbox
    if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
        raise ValueError(f"{owner} has invalid normalized bbox: {bbox}")
