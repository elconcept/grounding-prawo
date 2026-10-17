from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..models import OCRDocument


@dataclass
class OCRResult:
    text: str
    backend: str
    raw: Any = None
    error: str | None = None
    document: OCRDocument | None = None

    @property
    def ok(self) -> bool:
        return self.error is None and bool(self.text.strip()) and self.document is not None


@dataclass
class ChainAttempt:
    provider: str
    outcome: str  # "success" | "error" | "unavailable" | "empty"
    reason: str = ""


class OCRProvider(ABC):
    name: str

    @abstractmethod
    def is_available(self) -> tuple[bool, str]:
        """Cheap local check (credentials/binary present) -- no network call."""

    @abstractmethod
    def recognize(self, path: Path) -> OCRResult:
        """Run OCR on path. Never raises for expected failure modes (missing
        credentials, network error, empty result) -- return an OCRResult with
        .error set instead, so the chain can log and move on."""
