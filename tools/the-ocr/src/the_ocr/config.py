from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv

from .providers import AzureDocumentIntelligenceProvider, DatalabProvider, GoogleVisionProvider, LlamaParseProvider
from .providers.base import OCRProvider

DEFAULT_CHAIN_ORDER = ["datalab", "llamaparse", "azure-di", "google-vision"]
# Override with THE_OCR_CHAIN="azure-di,google-vision,..." (e.g. to spend free tiers first:
# Azure DI F0 500 pages/month + Google Vision 1000 units/month).


def load_env() -> None:
    """Load environment beside the release executable or from source cwd."""
    env_path = runtime_directory() / ".env"
    load_dotenv(dotenv_path=env_path, override=False)


def runtime_directory() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path.cwd()


def _all_providers_by_name() -> dict[str, OCRProvider]:
    load_env()
    return {
        "datalab": DatalabProvider(),
        "llamaparse": LlamaParseProvider(),
        "azure-di": AzureDocumentIntelligenceProvider(),
        "google-vision": GoogleVisionProvider(),
    }


def _chain_order() -> list[str]:
    import os

    configured = [name.strip() for name in os.getenv("THE_OCR_CHAIN", "").split(",") if name.strip()]
    return configured or DEFAULT_CHAIN_ORDER


def default_providers() -> list[OCRProvider]:
    """Production provider chain: Datalab, LlamaParse, Azure DI, Google Vision (THE_OCR_CHAIN overrides)."""
    by_name = _all_providers_by_name()
    return [by_name[name] for name in _chain_order() if name in by_name]


def all_providers() -> list[OCRProvider]:
    """Every production provider, in fallback order."""
    by_name = _all_providers_by_name()
    return [by_name[name] for name in DEFAULT_CHAIN_ORDER]
