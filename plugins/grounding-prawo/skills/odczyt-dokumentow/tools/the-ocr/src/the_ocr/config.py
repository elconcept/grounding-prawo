from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from .providers import canonical_provider_name, AzureProvider, DatalabProvider, GoogleVisionProvider, LlamaParseProvider, RapidOCRProvider
from .providers.base import OCRProvider

DEFAULT_CHAIN_ORDER = ["datalab", "llamaparse", "azure", "google_vision"]

#: Every provider the chain can use; ``rapidocr`` is local and opt-in.
PROVIDER_NAMES = [*DEFAULT_CHAIN_ORDER, "rapidocr"]

#: Comma-separated chain order override, e.g. ``azure,google_vision,rapidocr``.
CHAIN_ENV_VAR = "THE_OCR_CHAIN"


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
        "azure": AzureProvider(),
        "google_vision": GoogleVisionProvider(),
        "rapidocr": RapidOCRProvider(),
    }


def chain_order(order: list[str] | None = None) -> list[str]:
    """Explicit order > $THE_OCR_CHAIN > DEFAULT_CHAIN_ORDER; unknown names raise."""
    if order is None:
        configured = os.environ.get(CHAIN_ENV_VAR, "").strip()
        order = [name.strip() for name in configured.split(",") if name.strip()] if configured else DEFAULT_CHAIN_ORDER
    order = [canonical_provider_name(name) for name in order]
    unknown = [name for name in order if name not in PROVIDER_NAMES]
    if unknown:
        raise ValueError(f"unknown provider(s) {', '.join(unknown)}; choices: {', '.join(PROVIDER_NAMES)}")
    return list(order)


def default_providers(order: list[str] | None = None) -> list[OCRProvider]:
    """Provider chain in configured order (default: Datalab, LlamaParse, Azure DI, Google Vision)."""
    by_name = _all_providers_by_name()
    return [by_name[name] for name in chain_order(order)]


def all_providers() -> list[OCRProvider]:
    """Every provider, chain order first, then the rest."""
    by_name = _all_providers_by_name()
    first = chain_order()
    return [by_name[name] for name in first + [name for name in PROVIDER_NAMES if name not in first]]
