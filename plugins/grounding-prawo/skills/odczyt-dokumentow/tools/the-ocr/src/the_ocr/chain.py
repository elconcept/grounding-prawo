from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .providers import canonical_provider_name
from .providers.base import ChainAttempt, OCRProvider, OCRResult


@dataclass
class ChainResult:
    result: OCRResult | None
    attempts: list[ChainAttempt] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.result is not None and self.result.ok


def run_chain(path: Path, providers: list[OCRProvider], force: str | None = None) -> ChainResult:
    """Try providers in order; first success wins. `force` (a provider .name)
    skips the chain and runs only that provider, still recorded the same way."""
    attempts: list[ChainAttempt] = []

    candidates = providers
    if force:
        force = canonical_provider_name(force)
        matches = [p for p in providers if p.name == force]
        if not matches:
            names = ", ".join(p.name for p in providers)
            raise ValueError(f"unknown provider '{force}' -- choices: {names}")
        candidates = matches

    for provider in candidates:
        available, reason = provider.is_available()
        if not available:
            attempts.append(ChainAttempt(provider=provider.name, outcome="unavailable", reason=reason))
            continue

        result = provider.recognize(path)

        if result.error:
            attempts.append(ChainAttempt(provider=provider.name, outcome="error", reason=result.error))
            continue

        if not result.text.strip():
            attempts.append(ChainAttempt(provider=provider.name, outcome="empty", reason="no text recognized"))
            continue

        attempts.append(ChainAttempt(provider=provider.name, outcome="success"))
        return ChainResult(result=result, attempts=attempts)

    return ChainResult(result=None, attempts=attempts)
