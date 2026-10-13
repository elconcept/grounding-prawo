from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv

from .providers import DatalabProvider, LlamaParseProvider
from .providers.base import OCRProvider

DEFAULT_CHAIN_ORDER = ["datalab", "llamaparse"]


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
    }


def default_providers() -> list[OCRProvider]:
    """Production provider chain: Datalab first, LlamaParse on failure."""
    by_name = _all_providers_by_name()
    return [by_name[name] for name in DEFAULT_CHAIN_ORDER]


def all_providers() -> list[OCRProvider]:
    """Every production provider, in fallback order."""
    by_name = _all_providers_by_name()
    return [by_name[name] for name in DEFAULT_CHAIN_ORDER]
