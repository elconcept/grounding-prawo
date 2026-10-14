"""Rdzen: parsowanie pojedynczego pliku przez LlamaCloud i zapis .md obok niego."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

try:
    from llama_cloud import LlamaCloud
except ImportError:
    from llama_cloud.client import LlamaCloud

from ._frontmatter import render_with_frontmatter
from ._prompt import DEFAULT_CUSTOM_PROMPT
from ._secrets import load_api_key

# Konto uzytkownika jest w regionie EU. SDK domyslnie laczy sie z US
# (api.cloud.llamaindex.ai) -> klucz EU dostaje 401. Wymuszamy endpoint EU,
# chyba ze uzytkownik jawnie nadpisze przez LLAMA_CLOUD_BASE_URL.
DEFAULT_BASE_URL = "https://api.cloud.eu.llamaindex.ai"

TIER_AGENTIC = "agentic"
TIER_AGENTIC_PLUS = "agentic_plus"
TIER_COST_EFFECTIVE = "cost_effective"


def parse_markdown(
    input_path: Path,
    *,
    tier: str = TIER_AGENTIC,
    custom_prompt: str = DEFAULT_CUSTOM_PROMPT,
    polling_interval: float = 3.0,
    timeout: int = 1800,
) -> tuple[str, Any]:
    """Parsuje `input_path` przez LlamaCloud. Zwraca (markdown, raw_result)
    bez zapisu do pliku ani budowania frontmatteru -- do uzycia przez inne
    narzedzia (np. ugh-ocr), ktore chca sam tekst i surowy wynik SDK."""
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Brak pliku wejsciowego: {input_path}")

    api_key = load_api_key()
    base_url = os.environ.get("LLAMA_CLOUD_BASE_URL") or DEFAULT_BASE_URL
    client = LlamaCloud(api_key=api_key, base_url=base_url)

    file_obj = client.files.create(file=str(input_path), purpose="parse")

    result: Any = client.parsing.parse(
        file_id=file_obj.id,
        tier=tier,
        version="latest",
        agentic_options={"custom_prompt": custom_prompt},
        disable_cache=True,
        output_options={"tables_as_spreadsheet": {"guess_sheet_name": True}},
        expand=["markdown_full", "metadata"],
        polling_interval=polling_interval,
        timeout=timeout,
    )

    markdown = getattr(result, "markdown_full", None) or getattr(result, "markdown", None) or ""
    return str(markdown), result


def parse_file(
    input_path: Path,
    *,
    tier: str = TIER_AGENTIC,
    custom_prompt: str = DEFAULT_CUSTOM_PROMPT,
    polling_interval: float = 3.0,
    timeout: int = 1800,
) -> Path:
    """Parsuje `input_path` przez LlamaCloud i zapisuje wynik jako
    `<input_path_bez_rozszerzenia>.md` obok niego. Zwraca sciezke wynikowa."""
    input_path = Path(input_path)
    markdown, result = parse_markdown(
        input_path,
        tier=tier,
        custom_prompt=custom_prompt,
        polling_interval=polling_interval,
        timeout=timeout,
    )

    output_path = input_path.with_suffix(".md")
    output_path.write_text(
        render_with_frontmatter(input_path, markdown, tier=tier, raw_result=result),
        encoding="utf-8",
    )
    return output_path
