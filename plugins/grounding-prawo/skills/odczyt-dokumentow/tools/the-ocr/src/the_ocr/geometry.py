from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WordBox:
    """One recognized word, positioned as a fraction (0..1) of the page it
    came from -- not absolute points. Keeping bbox unit-less this way means
    injecting it into a PDF page never has to reconcile the source
    provider's measurement unit
    with the destination page's point space: multiply by the destination
    page's own width/height and the two are automatically in the same
    coordinate space."""

    text: str
    bbox: tuple[float, float, float, float]  # (x0, y0, x1, y1), top-left origin
    confidence: float


@dataclass(frozen=True)
class PageGeometry:
    words: tuple[WordBox, ...]
