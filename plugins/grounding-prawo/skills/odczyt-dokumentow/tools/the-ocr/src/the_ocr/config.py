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

#: Explicit path of the .env file; skips the search in :func:`env_file`.
ENV_FILE_VAR = "THE_OCR_ENV_FILE"


def load_env() -> None:
    """Load the first .env found by :func:`env_file`; process variables win."""
    path = env_file()
    if path is not None:
        load_dotenv(dotenv_path=path, override=False)


def env_file() -> Path | None:
    """$THE_OCR_ENV_FILE > .env beside the release executable (source: cwd) > user config .env."""
    configured = os.environ.get(ENV_FILE_VAR, "").strip()
    if configured:
        candidates = [Path(configured).expanduser()]
    else:
        candidates = [runtime_directory() / ".env", user_config_directory() / ".env"]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def config_directory() -> Path:
    """Base for relative paths in .env: the real directory of the loaded .env
    (a symlinked .env resolves to its target), else :func:`runtime_directory`."""
    path = env_file()
    return path.resolve().parent if path is not None else runtime_directory()


def user_config_directory() -> Path:
    """%APPDATA%\\the-ocr on Windows, $XDG_CONFIG_HOME/the-ocr or ~/.config/the-ocr elsewhere."""
    if sys.platform == "win32" and os.environ.get("APPDATA"):
        return Path(os.environ["APPDATA"]) / "the-ocr"
    base = os.environ.get("XDG_CONFIG_HOME", "").strip()
    return (Path(base) if base else Path.home() / ".config") / "the-ocr"


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
