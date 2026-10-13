"""Budowanie frontmatteru YAML dla plikow .md wygenerowanych przez markitdown-vision.

Schemat celowo generyczny (source_file/converted_at/converter/ocr_backend/
ocr_used) -- to narzedzie ogolnego przeznaczenia, nie wie nic o konwencjach
konkretnego repozytorium (np. raw/<doc-id>.md w kancelarii). Docelowa nazwa
pliku, doc-id i dodatkowe pola frontmatteru wg konwencji danego projektu
nalezy ustalic osobno przy imporcie wyniku.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

OCR_MARKERS = ("[Google Vision OCR]", "[Image OCR]")


def ocr_was_used(markdown: str) -> bool:
    return any(marker in markdown for marker in OCR_MARKERS)


def build_frontmatter(source_path: Path, markdown: str) -> dict[str, Any]:
    used = ocr_was_used(markdown)
    return {
        "source_file": source_path.name,
        "converted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "converter": "markitdown-vision",
        "ocr_backend": "google-cloud-vision" if used else None,
        "ocr_used": used,
    }


def render_with_frontmatter(source_path: Path, markdown: str) -> str:
    frontmatter = build_frontmatter(source_path, markdown)
    yaml_block = yaml.safe_dump(
        frontmatter, allow_unicode=True, sort_keys=False
    ).strip()
    return f"---\n{yaml_block}\n---\n\n{markdown}\n"
