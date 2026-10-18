"""Canonical OCR document: doc-intel-contract-pl 1.2.0, no local dialect.

The JSON produced by :meth:`OCRDocument.to_dict` follows the vendored
``contract/contract.schema.json`` (upstream 1.2.0 plus the four real provider
names in ``source.engine`` -- see the ``$comment`` field there). There is no
separate ``the-ocr`` contract, no ``schema_version 1.0``, no ``pages[].blocks[]``
nesting in the output, no SHA-256, no ``words``/``markdown`` grounding in JSON.

``words`` and ``markdown`` stay on the dataclasses as pipeline-internal data
(words position the OCRmyPDF text layer, markdown renders ``.md``); they are
never serialized to ``.json``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONTRACT_VERSION = "1.2.0"

#: Exact block taxonomy of doc-intel-contract-pl. Adapters must map provider
#: labels onto these values, never invent new ones.
VALID_BLOCK_TYPES = frozenset(
    {
        "title",
        "paragraph",
        "table",
        "list",
        "equation",
        "signature",
        "stamp",
        "figure",
        "header",
        "footer",
        "unknown",
    }
)

#: Upstream ``source.engine`` enum plus the four real the-ocr providers
#: (mirrors contract/contract.schema.json).
VALID_ENGINES = frozenset(
    {
        "opendataloader",
        "pdftotext",
        "chandra",
        "gaius",
        "vlm-html",
        "pdf-inspector",
        "liteparse",
        "datalab",
        "llamaparse",
        "azure",
        "google_vision",
        "rapidocr",
    }
)

VALID_VERDICTS = frozenset({"ok", "degraded", "failed"})

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
    """Pipeline-internal word geometry for the PDF text layer (not in JSON)."""

    text: str
    bbox: BBox
    confidence: float | None = None


@dataclass(frozen=True)
class OCRBlock:
    id: str
    page: int
    block_type: str
    text: str
    markdown: str = ""  # pipeline-internal (renders .md); not serialized
    bbox: BBox | None = None
    confidence: float | None = None
    words: tuple[OCRWord, ...] = ()  # pipeline-internal (positions PDF layer)
    flags: tuple[str, ...] = ()


@dataclass(frozen=True)
class OCRPage:
    """Pipeline-internal page (dimensions size the PDF layer); not serialized."""

    number: int
    width: float
    height: float
    blocks: tuple[OCRBlock, ...]


@dataclass(frozen=True)
class OCRDocument:
    doc_id: str  # plain document identifier: input file stem (never a hash)
    provider: str  # one of the four real provider names (-> source.engine)
    pages: tuple[OCRPage, ...]
    source_name: str = ""  # input file name (-> source.path)
    engine_variant: str | None = None  # e.g. provider region (-> source.engine_variant)
    created_at: str = field(default_factory=lambda: _utcnow())
    threshold: float = 0.0  # no confidence scoring; gating is structural only

    @property
    def text(self) -> str:
        page_texts = []
        for page in self.pages:
            page_texts.append("\n\n".join(block.text for block in page.blocks if block.text.strip()))
        return "\n\n---\n\n".join(page_texts).strip()

    @property
    def blocks(self) -> tuple[OCRBlock, ...]:
        """Flat block list in reading order (the contract shape)."""
        return tuple(block for page in self.pages for block in page.blocks)

    @property
    def has_geometry(self) -> bool:
        return bool(self.pages) and any(
            block.bbox is not None or block.words
            for page in self.pages
            for block in page.blocks
            if block.text.strip()
        )

    def validate(self) -> None:
        if self.provider not in VALID_ENGINES:
            raise ValueError(f"unknown provider/engine: {self.provider}")
        if not self.doc_id.strip():
            raise ValueError("OCR document has no doc_id")
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
                if block.block_type not in VALID_BLOCK_TYPES:
                    raise ValueError(f"block {block.id} has invalid block_type: {block.block_type}")
                if block.bbox is not None:
                    _validate_normalized_bbox(block.bbox, block.id)
                for word in block.words:
                    _validate_normalized_bbox(word.bbox, block.id)
        if not any(block.text.strip() for page in self.pages for block in page.blocks):
            raise ValueError("OCR document has no text")
        if not self.has_geometry:
            raise ValueError("OCR document has no usable geometry")

    def gating(self) -> dict[str, Any]:
        """Data-only gating required by the reference schema.

        No queue, no human review runtime: ``review_required`` is always empty.
        ``verdict`` is structural -- ``ok`` when every block is placeable,
        ``degraded`` when some blocks lack geometry, ``failed`` when empty.
        """
        blocks = self.blocks
        ungroundable = [block.id for block in blocks if block.bbox is None]
        auto_approved = [block.id for block in blocks if block.bbox is not None]
        verdict = "failed" if not blocks else ("degraded" if ungroundable else "ok")
        return {
            "threshold": self.threshold,
            "review_required": [],
            "auto_approved": auto_approved,
            "ungroundable": ungroundable,
            "verdict": verdict,
            "note": "structural only: no confidence scoring, no manual review queue",
            "counts": {
                "total": len(blocks),
                "review_required": 0,
                "auto_approved": len(auto_approved),
                "ungroundable": len(ungroundable),
            },
        }

    def to_dict(self, *, include_words: bool = False) -> dict[str, Any]:
        """Reference-contract JSON: flat ``blocks[]``, no hashes.

        ``include_words`` adds an optional ``blocks[].words`` list (text,
        normalized bbox, confidence) -- the editable word geometry that
        :meth:`from_dict` reads back to rebuild the PDF text layer without
        a new OCR run. Off by default, so the plain contract is unchanged.
        """
        payload = {
            "doc_id": self.doc_id,
            "contract_version": CONTRACT_VERSION,
            "source": {
                "path": self.source_name or None,
                "engine": self.provider,
                "engine_variant": self.engine_variant,
                "pages": len(self.pages),
            },
            "blocks": [
                {
                    "id": block.id,
                    "page": block.page,
                    "bbox": list(block.bbox) if block.bbox is not None else None,
                    "block_type": block.block_type,
                    "text": block.text,
                    "confidence": block.confidence,
                    "flags": list(block.flags),
                }
                for block in self.blocks
            ],
            "gating": self.gating(),
            "meta": {"created_at": self.created_at},
        }
        if include_words:
            for entry, block in zip(payload["blocks"], self.blocks):
                entry["words"] = [
                    {"text": word.text, "bbox": list(word.bbox), "confidence": word.confidence}
                    for word in block.words
                ]
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any], page_sizes: list[tuple[float, float]]) -> "OCRDocument":
        """Read a (possibly hand-corrected) contract JSON back into a document.

        ``page_sizes`` are the target PDF pages (points); bboxes stay
        normalized ``0..1``, so they only size the pages. Raises
        ``ValueError`` naming the first defect: page count or numbering,
        missing keys, bbox range/order, a word outside its block.
        """
        validate_contract(payload)
        declared = (payload.get("source") or {}).get("pages")
        if declared is not None and declared != len(page_sizes):
            raise ValueError(f"JSON declares {declared} pages, target PDF has {len(page_sizes)}")
        by_page: dict[int, list[OCRBlock]] = {number: [] for number in range(1, len(page_sizes) + 1)}
        for entry in payload["blocks"]:
            if entry["page"] not in by_page:
                raise ValueError(f"block {entry['id']} is on page {entry['page']}, target PDF has {len(page_sizes)}")
            bbox = tuple(float(value) for value in entry["bbox"]) if entry["bbox"] is not None else None
            words = []
            for word in entry.get("words") or []:
                if not isinstance(word, dict) or not isinstance(word.get("text"), str) or "bbox" not in word:
                    raise ValueError(f"block {entry['id']} has a word without text/bbox")
                box = word["bbox"]
                if not (isinstance(box, list) and len(box) == 4 and all(isinstance(v, (int, float)) for v in box)):
                    raise ValueError(f"block {entry['id']} has an invalid word bbox: {box}")
                box = tuple(float(value) for value in box)
                _validate_normalized_bbox(box, entry["id"])  # type: ignore[arg-type]
                if bbox is not None and not _inside(box, bbox):  # type: ignore[arg-type]
                    raise ValueError(f"block {entry['id']} has word '{word['text']}' outside the block bbox")
                words.append(OCRWord(word["text"], box, word.get("confidence")))  # type: ignore[arg-type]
            by_page[entry["page"]].append(
                OCRBlock(
                    id=entry["id"],
                    page=entry["page"],
                    block_type=entry["block_type"],
                    text=entry["text"],
                    markdown=entry["text"],
                    bbox=bbox,  # type: ignore[arg-type]
                    confidence=entry["confidence"],
                    words=tuple(words),
                    flags=tuple(entry["flags"]),
                )
            )
        source = payload["source"]
        document = cls(
            doc_id=payload["doc_id"],
            provider=source["engine"],
            pages=tuple(
                OCRPage(number, float(width), float(height), tuple(by_page[number]))
                for number, (width, height) in enumerate(page_sizes, start=1)
            ),
            source_name=source.get("path") or "",
            engine_variant=source.get("engine_variant"),
            created_at=payload["meta"]["created_at"],
        )
        document.validate()
        return document


def validate_contract(payload: dict[str, Any]) -> None:
    """Strict check of a ``to_dict()`` payload against the reference shape.

    Mirrors contract/contract.schema.json without adding a validation
    dependency: required keys, enums, bbox range ``0..1`` in ``[x0,y0,x1,y1]``
    order, flat blocks with page numbers.
    """
    for key in ("doc_id", "contract_version", "source", "blocks", "gating", "meta"):
        if key not in payload:
            raise ValueError(f"contract is missing required key: {key}")
    if not isinstance(payload["doc_id"], str) or not payload["doc_id"].strip():
        raise ValueError("contract doc_id must be a non-empty string")
    source = payload["source"]
    if source.get("engine") not in VALID_ENGINES:
        raise ValueError(f"contract source.engine is invalid: {source.get('engine')}")
    if not isinstance(payload["blocks"], list) or not payload["blocks"]:
        raise ValueError("contract blocks must be a non-empty list")
    seen: set[str] = set()
    for block in payload["blocks"]:
        for key in ("id", "page", "bbox", "block_type", "text", "confidence", "flags"):
            if key not in block:
                raise ValueError(f"contract block is missing required key: {key}")
        if block["id"] in seen:
            raise ValueError(f"contract has duplicate block id: {block['id']}")
        seen.add(block["id"])
        if block["block_type"] not in VALID_BLOCK_TYPES:
            raise ValueError(f"contract block has invalid block_type: {block['block_type']}")
        bbox = block["bbox"]
        if bbox is not None:
            if (
                not isinstance(bbox, list)
                or len(bbox) != 4
                or not all(isinstance(value, (int, float)) for value in bbox)
                or not (0 <= bbox[0] < bbox[2] <= 1 and 0 <= bbox[1] < bbox[3] <= 1)
            ):
                raise ValueError(f"contract block {block['id']} has invalid bbox: {bbox}")
        if not isinstance(block["page"], int) or block["page"] < 1:
            raise ValueError(f"contract block {block['id']} has invalid page: {block['page']}")
        if not isinstance(block["flags"], list):
            raise ValueError(f"contract block {block['id']} has invalid flags")
    gating = payload["gating"]
    for key in ("threshold", "review_required", "auto_approved", "ungroundable", "verdict", "counts"):
        if key not in gating:
            raise ValueError(f"contract gating is missing required key: {key}")
    if gating["verdict"] not in VALID_VERDICTS:
        raise ValueError(f"contract gating has invalid verdict: {gating['verdict']}")
    counts = gating["counts"]
    for key in ("total", "review_required", "auto_approved", "ungroundable"):
        if key not in counts:
            raise ValueError(f"contract gating.counts is missing required key: {key}")
    if counts["total"] != len(payload["blocks"]):
        raise ValueError("contract gating.counts.total differs from block count")
    if "created_at" not in payload["meta"]:
        raise ValueError("contract meta is missing created_at")


def doc_id_for(path: Path) -> str:
    """Plain document identifier: file stem, never a hash."""
    return path.stem


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _inside(inner: BBox, outer: BBox, tolerance: float = 0.01) -> bool:
    return (
        inner[0] >= outer[0] - tolerance
        and inner[1] >= outer[1] - tolerance
        and inner[2] <= outer[2] + tolerance
        and inner[3] <= outer[3] + tolerance
    )


def _validate_normalized_bbox(bbox: BBox, owner: str) -> None:
    x0, y0, x1, y1 = bbox
    if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
        raise ValueError(f"{owner} has invalid normalized bbox: {bbox}")
