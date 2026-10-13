"""Frontmatter YAML dla ugh-ocr.

Superset schematu wspolnego z markitdown-vision/llamaindex-ocr
(`source_file`/`converted_at`/`converter`/`ocr_backend`/`ocr_used`),
rozszerzony o `pages_count` i `pages_backend` -- lista per-strone, bo ugh-ocr
moze mieszac zrodla w obrebie jednego pliku (markitdown dla stron z prawdziwym
tekstem, OCR dla reszty). `fallback_used` odnotowuje, czy llamaindex-ocr
zawiodl w trakcie i przetwarzanie przelaczylo sie na markitdown-vision.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


def build_frontmatter(
    source_path: Path,
    *,
    pages_backend: list[str] | None,
    fallback_used: bool,
    fallback_reason: str | None,
) -> dict[str, Any]:
    if pages_backend is None:
        # Plik nie-PDF (obraz) -- traktowany jako jedna "strona".
        ocr_used = True
        ocr_backend = "llamaparse" if not fallback_used else "google-cloud-vision"
    else:
        ocr_used = any(b != "text" for b in pages_backend)
        backends_used = {b for b in pages_backend if b != "text"}
        if not backends_used:
            ocr_backend = None
        elif len(backends_used) == 1:
            ocr_backend = next(iter(backends_used))
        else:
            ocr_backend = "mixed"

    frontmatter: dict[str, Any] = {
        "source_file": source_path.name,
        "converted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "converter": "ugh-ocr",
        "ocr_backend": ocr_backend,
        "ocr_used": ocr_used,
    }
    if pages_backend is not None:
        frontmatter["pages_count"] = len(pages_backend)
        frontmatter["pages_backend"] = pages_backend
    frontmatter["fallback_used"] = fallback_used
    if fallback_used:
        frontmatter["fallback_reason"] = fallback_reason
    return frontmatter


def render_with_frontmatter(
    source_path: Path,
    markdown: str,
    *,
    pages_backend: list[str] | None,
    fallback_used: bool,
    fallback_reason: str | None,
) -> str:
    frontmatter = build_frontmatter(
        source_path,
        pages_backend=pages_backend,
        fallback_used=fallback_used,
        fallback_reason=fallback_reason,
    )
    yaml_block = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False).strip()
    body = markdown.strip()
    return f"---\n{yaml_block}\n---\n\n{body}\n"
