from __future__ import annotations

import os
from dataclasses import replace
from pathlib import Path

from ..adapters import llamaparse_document
from .base import OCRProvider, OCRResult

TIER_AGENTIC = "agentic"
TIER_COST_EFFECTIVE = "cost_effective"

# LlamaCloud has separate US and EU deployments; a key issued in one region
# gets 401 "Invalid API Key. Please check your region" against the other. The
# SDK defaults to US. Override with LLAMA_CLOUD_BASE_URL, or LLAMA_CLOUD_REGION
# = "eu" | "us".
_REGION_BASE_URL = {
    "eu": "https://api.cloud.eu.llamaindex.ai",
    "us": "https://api.cloud.llamaindex.ai",
}


def _resolve_base_url() -> str | None:
    explicit = os.environ.get("LLAMA_CLOUD_BASE_URL", "").strip()
    if explicit:
        return explicit
    region = os.environ.get("LLAMA_CLOUD_REGION", "").strip().lower()
    return _REGION_BASE_URL.get(region)

DEFAULT_CUSTOM_PROMPT = """Transcribe this Polish document faithfully and preserve its reading order, headings, lists, and tables.

Return Markdown without YAML frontmatter and without a document title added by you. Never use HTML, bold, or ordinary italic formatting. Use `-` for unordered lists. Preserve crossed-out source text as `~~text~~`.

Use exactly these annotations for non-printed or visual content:
`*[handnote: text]*`, `*[signature: name or illegible]*`, `*[stamp: text]*`, `*[footer: text]*`, `*[header: text]*`, `*[logo: description]*`, `*[photo: description]*`, `*[graphic: description]*`.

All documents are Polish. Do not translate, silently correct, infer missing text, or omit handwritten notes, signatures, stamps, headers, footers, logos, photos, or graphics. Preserve spelling, dates, names, units, and table relationships exactly as visible.
"""


def _load_api_key() -> str | None:
    candidates = _credential_candidates()
    return candidates[0][1] if candidates else None


def _region_order() -> list[str]:
    configured = os.environ.get("LLAMA_CLOUD_REGION_ORDER", "eu,us")
    regions = [region.strip().lower() for region in configured.split(",")]
    regions = [region for region in regions if region in _REGION_BASE_URL]
    return regions or ["eu", "us"]


def _credential_candidates() -> list[tuple[str, str, str | None]]:
    candidates: list[tuple[str, str, str | None]] = []
    for region in _region_order():
        key = os.environ.get(f"LLAMA_CLOUD_API_KEY_{region.upper()}", "").strip()
        if key:
            url = os.environ.get(f"LLAMA_CLOUD_BASE_URL_{region.upper()}", "").strip() or _REGION_BASE_URL[region]
            candidates.append((region, key, url))
    generic = os.environ.get("LLAMA_CLOUD_API_KEY", "").strip()
    if generic:
        region = os.environ.get("LLAMA_CLOUD_REGION", "us").strip().lower()
        candidates.append((region if region in _REGION_BASE_URL else "custom", generic, _resolve_base_url()))
    return candidates


class LlamaParseProvider(OCRProvider):
    """LlamaCloud / LlamaParse -> Markdown. Paid cloud API, one billed parse
    per document (disable_cache=True, matching the reference impl)."""

    name = "llamaparse"

    def __init__(self, tier: str = TIER_AGENTIC, timeout: int = 1800, base_url: str | None = None):
        self.tier = tier
        self.timeout = timeout
        self.base_url = base_url

    def is_available(self) -> tuple[bool, str]:
        try:
            import llama_cloud  # noqa: F401
        except ImportError:
            return False, "llama-cloud not installed"
        if not _credential_candidates():
            return False, "no LlamaCloud key set (LLAMA_CLOUD_API_KEY_EU/US or LLAMA_CLOUD_API_KEY)"
        return True, ""

    def recognize(self, path: Path) -> OCRResult:
        available, reason = self.is_available()
        if not available:
            return OCRResult(text="", backend=self.name, error=reason)

        try:
            try:
                from llama_cloud import LlamaCloud
            except ImportError:
                from llama_cloud.client import LlamaCloud
        except ImportError as e:
            return OCRResult(text="", backend=self.name, error=f"llama-cloud import failed: {e}")

        errors: list[str] = []
        for region, api_key, regional_url in _credential_candidates():
            try:
                kw = {"api_key": api_key}
                base_url = self.base_url or regional_url
                if base_url:
                    kw["base_url"] = base_url
                client = LlamaCloud(**kw)
                file_obj = client.files.create(file=str(path), purpose="parse")
                result = client.parsing.parse(
                    file_id=file_obj.id,
                    tier=self.tier,
                    version="latest",
                    agentic_options={"custom_prompt": DEFAULT_CUSTOM_PROMPT},
                    disable_cache=True,
                    output_options={"tables_as_spreadsheet": {"guess_sheet_name": True}},
                    expand=["items", "markdown_full", "metadata"],
                    polling_interval=3.0,
                    timeout=self.timeout,
                )
                markdown = getattr(result, "markdown_full", None) or getattr(result, "markdown", None) or ""
                if not str(markdown).strip():
                    raise ValueError("empty markdown")
                document = llamaparse_document(result, path)
                document = replace(document, engine_variant=region)
                return OCRResult(text=document.text, backend=self.name, raw=result, document=document)
            except Exception as exc:
                errors.append(f"{region}: {exc}")
        return OCRResult(text="", backend=self.name, error="LlamaCloud attempts failed: " + "; ".join(errors))
